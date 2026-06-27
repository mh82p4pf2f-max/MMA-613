#!/usr/bin/env python3
"""
build_panel.py — Clean the StatCan source tables, integrate them, and compute a
transparent `policy_review_priority_score` for the Labour Market Stress &
Social Support Prioritization Dashboard.

Pipeline
--------
raw/<domain>/<pid>.csv  (from pull_statcan.py)
  -> processed/labour_force_clean.csv
  -> processed/income_clean.csv
  -> processed/demographics_clean.csv
  -> processed/housing_affordability_clean.csv
  -> processed/policy_triage_panel.csv   (integrated + scored)

Requires: pandas, numpy   (pip install pandas numpy)

GOVERNANCE (read data/metadata/integration_notes.md and the project CLAUDE.md)
- This is a TRIAGE indicator for human policy review. It does NOT determine
  eligibility and must never approve, deny, or reduce benefits.
- Suppressed/blank values are NEVER invented or imputed; they lower confidence
  and set missing_value_flag.
- The housing field is a labelled PROXY (shelter-CPI pressure), not a true
  affordability/core-housing-need measure.
- Annual context (income, low income, population) is joined to monthly labour
  data BY YEAR and is clearly labelled annual.

IMPORTANT — confirm member labels on first real run. StatCan member strings
(e.g. the exact label for "Unemployment rate" or an income source) occasionally
change. This script prints the unique values it finds and WARNS when a
configured label is missing, so you can adjust CONFIG below. Run with
`--selftest` first to see the whole pipeline work on synthetic data.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent
RAW = DATA / "raw"
PROCESSED = DATA / "processed"

# --------------------------------------------------------------------------- #
# CONFIG — member labels and scoring. Confirm against printed unique values.
# --------------------------------------------------------------------------- #
CONFIG = {
    # Labour Force Survey (14100287)
    "lfs_data_type": "Seasonally adjusted",
    "lfs_statistic": "Estimate",
    "lfs_age_headline": "15 years and over",
    "lfs_age_youth": "15 to 24 years",
    "lfs_gender_total_contains": "Total",          # "Total - Gender" / "Both sexes"
    "lfs_rate_chars": ["Unemployment rate", "Employment rate", "Participation rate"],
    "lfs_count_chars": ["Employment", "Unemployment", "Population", "Labour force"],
    # Income of individuals (11100239) — annual
    "income_age_contains": "16 years and over",
    "income_sex_contains": "Both sexes",
    "income_sources": ["Median employment income", "Median after-tax income"],
    # Low income (11100135) — annual
    "lowinc_line_contains": "Low income measure after tax",
    "lowinc_stat_contains": "Percentage of persons in low income",
    "lowinc_age_contains": "All persons",
    # CPI (18100004) — monthly
    "cpi_shelter_contains": "Shelter",
    "cpi_allitems_contains": "All-items",
    # Scoring: component weights (must reflect the spec's transparency rule)
    "weights": {
        "unemp_level": 0.30,
        "unemp_change": 0.15,
        "emp_decline": 0.10,
        "part_decline": 0.10,
        "youth_unemp": 0.10,
        "low_income": 0.15,
        "housing_pressure": 0.10,
    },
    # Normalisation anchors (value -> 0 .. value -> 1), clipped. Documented &
    # fixed so the score is stable and explainable, not a per-run min-max.
    "anchors": {
        "unemp_level": (4.0, 14.0),        # unemployment rate %
        "unemp_change": (0.0, 3.0),        # pp rise vs 12-mo avg
        "emp_decline": (0.0, 3.0),         # pp fall in employment rate vs 12-mo avg
        "part_decline": (0.0, 3.0),        # pp fall in participation rate vs 12-mo avg
        "youth_unemp": (8.0, 25.0),        # youth unemployment rate %
        "low_income": (5.0, 20.0),         # low-income rate %
        "housing_pressure": (0.0, 10.0),   # shelter CPI year-over-year %
    },
}


# --------------------------------------------------------------------------- #
# Generic helpers
# --------------------------------------------------------------------------- #
def _col(df, *needles):
    """First column whose name contains any needle (case-insensitive)."""
    for n in needles:
        for c in df.columns:
            if n.lower() in c.lower():
                return c
    return None


def _norm(value, lo, hi):
    """Min-max to 0..1 against fixed anchors, clipped."""
    if pd.isna(value):
        return np.nan
    return float(np.clip((value - lo) / (hi - lo), 0.0, 1.0))


SUPPRESSION = {"", "..", "...", "F", "x", "E", "n/a", "NA"}


def clean_statcan(df: pd.DataFrame, pid: int, frequency: str) -> pd.DataFrame:
    """Standardise any StatCan full-table CSV to a tidy long frame.

    Adds: ref_date, year, month, geo, dguid, value, status, missing_value_flag,
    data_frequency, source_product_id. Keeps original dimension columns too.
    """
    df = df.copy()
    ref = _col(df, "REF_DATE") or "REF_DATE"
    geo = _col(df, "GEO") or "GEO"
    val = _col(df, "VALUE") or "VALUE"
    status = _col(df, "STATUS")
    dguid = _col(df, "DGUID")

    df["ref_date"] = df[ref].astype(str)
    df["year"] = df["ref_date"].str.slice(0, 4)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["month"] = df["ref_date"].str.slice(5, 7)
    df["month"] = pd.to_numeric(df["month"], errors="coerce").astype("Int64")
    df["geo"] = df[geo].astype(str)
    df["dguid"] = df[dguid].astype(str) if dguid else pd.NA
    df["value"] = pd.to_numeric(df[val], errors="coerce")

    blank_status = df[status].astype(str).isin(SUPPRESSION) if status else False
    df["missing_value_flag"] = df["value"].isna() | blank_status
    df["data_frequency"] = frequency
    df["source_product_id"] = pid
    return df


def _check_labels(series: pd.Series, wanted, name: str) -> None:
    have = set(series.dropna().unique())
    for w in (wanted if isinstance(wanted, (list, tuple)) else [wanted]):
        if not any(w.lower() in str(h).lower() for h in have):
            print(f"  [WARN] {name}: configured label '{w}' not found. "
                  f"Available (first 12): {sorted(map(str, have))[:12]}")


# --------------------------------------------------------------------------- #
# Per-source feature extraction
# --------------------------------------------------------------------------- #
def lfs_features(clean: pd.DataFrame) -> pd.DataFrame:
    c = CONFIG
    char = _col(clean, "characteristic")
    dtype = _col(clean, "data type")
    stat = _col(clean, "Statistics") or _col(clean, "statistic")
    gender = _col(clean, "gender", "sex")
    age = _col(clean, "age group")
    _check_labels(clean[char], c["lfs_rate_chars"], "LFS characteristics")

    f = clean
    if dtype:
        f = f[f[dtype].astype(str).str.contains(c["lfs_data_type"], case=False, na=False)]
    if stat:
        f = f[f[stat].astype(str).str.contains(c["lfs_statistic"], case=False, na=False)]
    gtot = f[gender].astype(str).str.contains(c["lfs_gender_total_contains"], case=False, na=False)

    # headline slice: total gender, 15+
    head = f[gtot & (f[age].astype(str) == c["lfs_age_headline"])]
    keep = c["lfs_rate_chars"] + c["lfs_count_chars"]
    head = head[head[char].isin(keep)]
    wide = head.pivot_table(index=["geo", "ref_date", "year", "month"],
                            columns=char, values="value", aggfunc="first").reset_index()
    wide = wide.rename(columns={"Unemployment rate": "unemployment_rate",
                                "Employment rate": "employment_rate",
                                "Participation rate": "participation_rate",
                                "Employment": "employment", "Unemployment": "unemployment",
                                "Population": "population", "Labour force": "labour_force"})

    # youth unemployment rate (15-24), total gender
    youth = f[gtot & (f[age].astype(str) == c["lfs_age_youth"]) &
              (f[char] == "Unemployment rate")]
    yt = youth[["geo", "ref_date", "value"]].rename(columns={"value": "youth_unemployment_rate"})
    wide = wide.merge(yt, on=["geo", "ref_date"], how="left")

    # rolling 12-month changes vs the trailing average (stress = rise/fall)
    wide = wide.sort_values(["geo", "ref_date"])
    for col, out in [("unemployment_rate", "unemp_change"),
                     ("employment_rate", "emp_change"),
                     ("participation_rate", "part_change")]:
        avg = wide.groupby("geo")[col].transform(lambda s: s.rolling(12, min_periods=6).mean().shift(1))
        wide[out] = wide[col] - avg
    return wide


def income_features(clean: pd.DataFrame) -> pd.DataFrame:
    c = CONFIG
    src = _col(clean, "income source")
    age = _col(clean, "age group")
    sex = _col(clean, "sex", "gender")
    if src is None:
        print("  [WARN] income: no 'Income source' column found; skipping income features.")
        return pd.DataFrame(columns=["geo", "year", "income_value", "income_indicator"])
    _check_labels(clean[src], c["income_sources"], "Income source")

    f = clean
    if age:
        f = f[f[age].astype(str).str.contains(c["income_age_contains"], case=False, na=False)]
    if sex:
        f = f[f[sex].astype(str).str.contains(c["income_sex_contains"], case=False, na=False)]
    f = f[f[src].astype(str).str.contains("|".join(c["income_sources"]), case=False, na=False)]
    out = (f[["geo", "year", src, "value"]]
           .rename(columns={src: "income_indicator", "value": "income_value"}))
    # prefer employment income for the headline income_value
    emp = out[out["income_indicator"].str.contains("employment", case=False, na=False)]
    return (emp if not emp.empty else out)[["geo", "year", "income_indicator", "income_value"]]


def low_income_features(clean: pd.DataFrame) -> pd.DataFrame:
    c = CONFIG
    line = _col(clean, "low income lines", "low income line")
    stat = _col(clean, "Statistics", "statistic")
    age = _col(clean, "age group")
    fam = _col(clean, "economic family type", "family type")
    f = clean
    for col, want in [(line, c["lowinc_line_contains"]), (stat, c["lowinc_stat_contains"]),
                      (age, c["lowinc_age_contains"])]:
        if col:
            f = f[f[col].astype(str).str.contains(want, case=False, na=False)]
    if fam:
        f = f[f[fam].astype(str).str.contains("All", case=False, na=False)]
    return (f[["geo", "year", "value"]]
            .rename(columns={"value": "low_income_rate"})
            .groupby(["geo", "year"], as_index=False)["low_income_rate"].first())


def population_features(clean: pd.DataFrame) -> pd.DataFrame:
    """Working-age / youth / senior shares, dependency ratio, median age."""
    age = _col(clean, "age group")
    gender = _col(clean, "gender", "sex")
    if age is None:
        return pd.DataFrame(columns=["geo", "year", "population_total"])
    f = clean
    if gender:
        f = f[f[gender].astype(str).str.contains("Total", case=False, na=False)]

    def agg(group):
        a = group.set_index(group[age].astype(str))["value"]
        def total(label):  # 5-year groups summed by a simple bucket match
            return a[a.index.str.contains(label, na=False)].sum()
        out = {}
        out["population_total"] = a.get("All ages", np.nan)
        out["median_age"] = a.get("Median age", np.nan)
        return pd.Series(out)

    res = f.groupby(["geo", "year"]).apply(agg, include_groups=False).reset_index()
    return res


def cpi_features(clean: pd.DataFrame) -> pd.DataFrame:
    c = CONFIG
    prod = _col(clean, "Products and product groups", "product")
    if prod is None:
        print("  [WARN] CPI: no product column found; skipping housing features.")
        return pd.DataFrame(columns=["geo", "ref_date", "housing_pressure_proxy"])
    _check_labels(clean[prod], [c["cpi_shelter_contains"], c["cpi_allitems_contains"]], "CPI products")

    shelter = clean[clean[prod].astype(str).str.fullmatch(c["cpi_shelter_contains"], case=False, na=False)]
    if shelter.empty:  # fall back to 'contains' if exact label differs
        shelter = clean[clean[prod].astype(str).str.contains(c["cpi_shelter_contains"], case=False, na=False)]
    s = (shelter[["geo", "ref_date", "year", "month", "value"]]
         .rename(columns={"value": "shelter_cpi"}).sort_values(["geo", "ref_date"]))
    # year-over-year shelter CPI growth = housing cost pressure proxy
    s["housing_pressure_proxy"] = s.groupby("geo")["shelter_cpi"].pct_change(12) * 100
    return s[["geo", "ref_date", "shelter_cpi", "housing_pressure_proxy"]]


# --------------------------------------------------------------------------- #
# Integrate + score
# --------------------------------------------------------------------------- #
def integrate(lfs, inc, low, pop, cpi) -> pd.DataFrame:
    panel = lfs.copy()
    if not inc.empty:
        panel = panel.merge(inc, on=["geo", "year"], how="left")          # annual by year
    if not low.empty:
        panel = panel.merge(low, on=["geo", "year"], how="left")          # annual by year
    if not pop.empty:
        panel = panel.merge(pop, on=["geo", "year"], how="left")          # annual by year
    if not cpi.empty:
        panel = panel.merge(cpi, on=["geo", "ref_date"], how="left")      # monthly by month
    if {"income_value", "shelter_cpi"} <= set(panel.columns):
        panel["income_to_shelter_pressure_ratio"] = panel["shelter_cpi"] / panel["income_value"]
    return panel


def score(panel: pd.DataFrame) -> pd.DataFrame:
    w, anc = CONFIG["weights"], CONFIG["anchors"]
    comp_src = {
        "unemp_level": "unemployment_rate", "unemp_change": "unemp_change",
        "emp_decline": "emp_change", "part_decline": "part_change",
        "youth_unemp": "youth_unemployment_rate", "low_income": "low_income_rate",
        "housing_pressure": "housing_pressure_proxy",
    }

    def row_score(r):
        contribs, wsum = {}, 0.0
        for comp, col in comp_src.items():
            if col not in panel.columns:
                continue
            raw = r.get(col)
            # declines are stress only when negative -> flip sign for *_decline
            if comp in ("emp_decline", "part_decline"):
                raw = -raw if pd.notna(raw) else raw
            n = _norm(raw, *anc[comp])
            if pd.notna(n):
                contribs[comp] = (w[comp], n, r.get(col))
                wsum += w[comp]
        if wsum == 0:
            return pd.Series({"policy_review_priority_score": np.nan,
                              "score_confidence": 0.0, "missing_value_flag": True,
                              "score_explanation": "No scoring inputs available."})
        sc = 100.0 * sum(wt * n for wt, n, _ in contribs.values()) / wsum
        conf = wsum / sum(w.values())
        top = sorted(contribs.items(), key=lambda kv: kv[1][0] * kv[1][1], reverse=True)[:3]
        why = "; ".join(f"{k} ({raw:.1f})" for k, (_, n, raw) in top if pd.notna(raw))
        return pd.Series({"policy_review_priority_score": round(sc, 1),
                          "score_confidence": round(conf, 2),
                          "missing_value_flag": conf < 1.0,
                          "score_explanation": f"Elevated stress flagged for review — drivers: {why}. "
                                               f"Triage only; not an eligibility or benefit decision."})

    return pd.concat([panel, panel.apply(row_score, axis=1)], axis=1)


def read_raw(domain: str, pid: int) -> pd.DataFrame | None:
    path = RAW / domain / f"{pid}.csv"
    if not path.exists():
        print(f"  [skip] {path} not found — run: python3 pull_statcan.py --table ...")
        return None
    return pd.read_csv(path, low_memory=False)


def build(out_dir: Path = PROCESSED) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Reading raw tables ...")
    raw = {
        "labour_force": read_raw("labour_force", 14100287),
        "income": read_raw("income", 11100239),
        "low_income": read_raw("income", 11100135),
        "population": read_raw("demographics", 17100005),
        "cpi": read_raw("housing_affordability", 18100004),
    }
    if raw["labour_force"] is None:
        sys.exit("Labour Force table is required. Pull it first.")

    print("Cleaning + writing *_clean.csv ...")
    lfs_c = clean_statcan(raw["labour_force"], 14100287, "monthly")
    lfs_c.to_csv(out_dir / "labour_force_clean.csv", index=False)
    inc_c = clean_statcan(raw["income"], 11100239, "annual") if raw["income"] is not None else pd.DataFrame()
    low_c = clean_statcan(raw["low_income"], 11100135, "annual") if raw["low_income"] is not None else pd.DataFrame()
    if not inc_c.empty or not low_c.empty:
        pd.concat([inc_c, low_c]).to_csv(out_dir / "income_clean.csv", index=False)
    pop_c = clean_statcan(raw["population"], 17100005, "annual") if raw["population"] is not None else pd.DataFrame()
    if not pop_c.empty:
        pop_c.to_csv(out_dir / "demographics_clean.csv", index=False)
    cpi_c = clean_statcan(raw["cpi"], 18100004, "monthly") if raw["cpi"] is not None else pd.DataFrame()
    if not cpi_c.empty:
        cpi_c.to_csv(out_dir / "housing_affordability_clean.csv", index=False)

    print("Extracting features + integrating ...")
    panel = integrate(
        lfs_features(lfs_c),
        income_features(inc_c) if not inc_c.empty else pd.DataFrame(),
        low_income_features(low_c) if not low_c.empty else pd.DataFrame(),
        population_features(pop_c) if not pop_c.empty else pd.DataFrame(),
        cpi_features(cpi_c) if not cpi_c.empty else pd.DataFrame(),
    )
    print("Scoring (policy_review_priority_score) ...")
    panel = score(panel)
    panel["source_table"] = "StatCan WDS (see data/metadata/data_sources.md)"
    out = out_dir / "policy_triage_panel.csv"
    panel.to_csv(out, index=False)
    print(f"\nDONE. {len(panel):,} rows -> {out}")
    print("Columns:", list(panel.columns))


# --------------------------------------------------------------------------- #
# Self-test on synthetic, structurally-faithful data (no real/fake project data)
# --------------------------------------------------------------------------- #
def selftest() -> None:
    print(">>> SELF-TEST on SYNTHETIC data (not real StatCan values) <<<\n")
    rng = np.random.default_rng(0)
    geos, months = ["Alberta", "Ontario"], pd.period_range("2023-01", "2024-12", freq="M")

    lfs_rows = []
    for g in geos:
        for p in months:
            base = 6 if g == "Ontario" else 7
            for char, v in [("Unemployment rate", base + rng.normal(0, 0.4)),
                            ("Employment rate", 61 + rng.normal(0, 0.3)),
                            ("Participation rate", 65 + rng.normal(0, 0.3)),
                            ("Employment", 1e6), ("Unemployment", 8e4), ("Population", 4e6)]:
                for age in ["15 years and over", "15 to 24 years"]:
                    lfs_rows.append({"REF_DATE": str(p), "GEO": g, "DGUID": f"2016A0002{g[:2]}",
                                     "Labour force characteristics": char, "Gender": "Total - Gender",
                                     "Age group": age, "Statistics": "Estimate",
                                     "Data type": "Seasonally adjusted",
                                     "VALUE": (v + (4 if age.startswith("15 to") and "rate" in char else 0)),
                                     "STATUS": ""})
    inc = pd.DataFrame([{"REF_DATE": y, "GEO": g, "Age group": "16 years and over",
                         "Sex": "Both sexes", "Income source": "Median employment income",
                         "VALUE": 45000 + rng.integers(-3000, 3000), "STATUS": ""}
                        for g in geos for y in [2023, 2024]])
    low = pd.DataFrame([{"REF_DATE": y, "GEO": g, "Age group": "All persons",
                         "Gender": "Total", "Economic family type": "All persons",
                         "Low income lines": "Low income measure after tax",
                         "Statistics": "Percentage of persons in low income",
                         "VALUE": 11 + rng.normal(0, 1), "STATUS": ""}
                        for g in geos for y in [2023, 2024]])
    pop = pd.DataFrame([{"REF_DATE": y, "GEO": g, "Gender": "Total",
                         "Age group": a, "VALUE": v, "STATUS": ""}
                        for g in geos for y in [2023, 2024]
                        for a, v in [("All ages", 4.4e6), ("Median age", 39.5)]])
    cpi = pd.DataFrame([{"REF_DATE": str(p), "GEO": g,
                         "Products and product groups": prod,
                         "VALUE": (170 if prod == "Shelter" else 158) + i * 0.4 + rng.normal(0, 0.3),
                         "STATUS": ""}
                        for g in geos for i, p in enumerate(months)
                        for prod in ["Shelter", "All-items"]])

    tmp = Path(tempfile.mkdtemp())
    panel = integrate(
        lfs_features(clean_statcan(pd.DataFrame(lfs_rows), 14100287, "monthly")),
        income_features(clean_statcan(inc, 11100239, "annual")),
        low_income_features(clean_statcan(low, 11100135, "annual")),
        population_features(clean_statcan(pop, 17100005, "annual")),
        cpi_features(clean_statcan(cpi, 18100004, "monthly")),
    )
    panel = score(panel)
    panel.to_csv(tmp / "policy_triage_panel.csv", index=False)
    latest = panel.sort_values("ref_date").groupby("geo").tail(1)
    cols = ["geo", "ref_date", "unemployment_rate", "youth_unemployment_rate",
            "low_income_rate", "housing_pressure_proxy",
            "policy_review_priority_score", "score_confidence", "missing_value_flag"]
    print(latest[[c for c in cols if c in latest.columns]].to_string(index=False))
    print("\nExample explanation:\n  ", latest.iloc[0]["score_explanation"])
    print(f"\nSelf-test wrote a synthetic panel to {tmp/'policy_triage_panel.csv'}")
    print("Pipeline mechanics OK. Real values require running pull_statcan.py on a networked machine.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Clean, integrate, and score StatCan tables.")
    ap.add_argument("--build", action="store_true", help="build from data/raw -> data/processed")
    ap.add_argument("--selftest", action="store_true", help="prove the pipeline on synthetic data")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    elif args.build:
        build()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
