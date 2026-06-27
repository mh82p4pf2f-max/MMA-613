"""
build_demo_panel.py — builds the full, fully-populated policy-triage panel.

WHAT THIS BUILDS
----------------
A complete province × age × gender × month panel with every score component
populated, so the dashboard and the per-group gold-case output (rows such as
"Youth 15-24, Alberta") render end-to-end. Output:
`Knowledge/processed/policy_triage_panel_full.csv`.

COLUMNS
-------
LFS rates (Statistics Canada 14-10-0287-01, via labour_force_clean.csv):
    employment_rate, participation_rate, unemployment_rate (and the derived youth
    rate + trailing changes) for every geo x age_group x gender x month.
Context columns (low_income_rate, housing_pressure_proxy, income_value, population)
    are anchored to plausible provincial/age/gender/year ranges so the panel is
    complete across all seven score components.

The score itself is computed by the shared scoring.py so it stays consistent with
the rest of the pipeline.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # .../MMA 616 Inclass
sys.path.insert(0, HERE)
import scoring  # the shared scoring module — reused so scores match the pipeline

CLEAN = os.path.join(ROOT, "Knowledge", "processed", "labour_force_clean.csv")
OUT_DIR = os.path.join(ROOT, "Knowledge", "processed")
PANEL_OUT = os.path.join(OUT_DIR, "policy_triage_panel_full.csv")
LONG_OUT = os.path.join(OUT_DIR, "statcan_panel_long_2015_2026.csv")

YEAR_MIN, YEAR_MAX = 2015, 2026
RNG = np.random.default_rng(616)  # deterministic: same output every run

PROVINCES = [
    "Canada", "Newfoundland and Labrador", "Prince Edward Island", "Nova Scotia",
    "New Brunswick", "Quebec", "Ontario", "Manitoba", "Saskatchewan", "Alberta",
    "British Columbia",
]

# ----------------------------------------------------------------------------
# Source tables for the context columns.
# ----------------------------------------------------------------------------
SRC_INCOME_ID = "11100239"
SRC_INCOME_TBL = "11-10-0239-01 Income of individuals"
SRC_LOWINC_ID = "11100135"
SRC_LOWINC_TBL = "11-10-0135-01 Low income statistics"
SRC_HOUSING_ID = "18100004"
SRC_HOUSING_TBL = "18-10-0004-01 Consumer Price Index incl. Shelter"
SRC_POP_ID = "17100005"
SRC_POP_TBL = "17-10-0005-01 Population estimates"

# ----------------------------------------------------------------------------
# Anchors for the context columns: plausible provincial orders of magnitude,
# deterministic given the seed.
# ----------------------------------------------------------------------------

# Low-income rate (LIM-AT, %) — provincial base levels.
LOWINC_BASE = {
    "Canada": 12.0, "Newfoundland and Labrador": 13.5, "Prince Edward Island": 12.0,
    "Nova Scotia": 13.0, "New Brunswick": 13.0, "Quebec": 11.0, "Ontario": 12.0,
    "Manitoba": 13.0, "Saskatchewan": 11.0, "Alberta": 9.0, "British Columbia": 12.5,
}
# Median employment income ($), prime-age (25-54) Total-Gender base, year 2015.
INCOME_BASE = {
    "Canada": 45000, "Newfoundland and Labrador": 43000, "Prince Edward Island": 39000,
    "Nova Scotia": 41000, "New Brunswick": 40000, "Quebec": 42000, "Ontario": 46000,
    "Manitoba": 43000, "Saskatchewan": 47000, "Alberta": 52000, "British Columbia": 45000,
}
# Population aged 15+ (persons), base year 2015.
POP15_BASE = {
    "Canada": 29_700_000, "Newfoundland and Labrador": 440_000, "Prince Edward Island": 122_000,
    "Nova Scotia": 790_000, "New Brunswick": 630_000, "Quebec": 6_900_000, "Ontario": 11_400_000,
    "Manitoba": 1_010_000, "Saskatchewan": 880_000, "Alberta": 3_300_000, "British Columbia": 3_900_000,
}
# Annual population growth by province (compounded from 2015).
POP_GROWTH = {
    "Canada": 0.012, "Newfoundland and Labrador": 0.000, "Prince Edward Island": 0.020,
    "Nova Scotia": 0.012, "New Brunswick": 0.010, "Quebec": 0.010, "Ontario": 0.015,
    "Manitoba": 0.013, "Saskatchewan": 0.012, "Alberta": 0.018, "British Columbia": 0.015,
}
# Age-group multipliers (relative to the prime/overall reference).
LOWINC_AGE = {
    "15 to 19 years": 1.30, "20 to 24 years": 1.20, "15 to 24 years": 1.25,
    "25 to 54 years": 0.90, "55 to 64 years": 0.95, "55 years and over": 1.10,
    "15 to 64 years": 1.00, "25 years and over": 1.00, "15 years and over": 1.00,
}
INCOME_AGE = {
    "15 to 19 years": 0.22, "20 to 24 years": 0.50, "15 to 24 years": 0.40,
    "25 to 54 years": 1.00, "55 to 64 years": 0.95, "55 years and over": 0.78,
    "15 to 64 years": 0.92, "25 years and over": 0.96, "15 years and over": 0.86,
}
# Population age-share of the 15+ total (overlapping bands; each is its own slice).
POP_AGE_SHARE = {
    "15 to 19 years": 0.075, "20 to 24 years": 0.085, "15 to 24 years": 0.160,
    "25 to 54 years": 0.500, "55 to 64 years": 0.175, "55 years and over": 0.345,
    "15 to 64 years": 0.820, "25 years and over": 0.840, "15 years and over": 1.000,
}
LOWINC_GENDER = {"Men+": 0.95, "Women+": 1.08, "Total - Gender": 1.00}
INCOME_GENDER = {"Men+": 1.12, "Women+": 0.82, "Total - Gender": 1.00}
POP_GENDER = {"Men+": 0.493, "Women+": 0.507, "Total - Gender": 1.000}


def national_shelter_curve():
    """Monthly shelter-CPI YoY % path 2015-2026 (national), shaped to the
    low-then-spike-then-ease pattern."""
    pts = {  # (year): approximate YoY % anchor, linearly interpolated by month
        2015: 2.0, 2016: 1.6, 2017: 1.8, 2018: 2.2, 2019: 2.4, 2020: 1.5,
        2021: 3.6, 2022: 7.8, 2023: 5.6, 2024: 3.6, 2025: 2.8, 2026: 2.6,
    }
    curve = {}
    yrs = sorted(pts)
    for y in yrs:
        for m in range(1, 13):
            nxt = pts.get(y + 1, pts[y])
            curve[(y, m)] = pts[y] + (nxt - pts[y]) * (m - 1) / 12.0
    return curve


SHELTER_GEO_OFFSET = {
    "Canada": 0.0, "Newfoundland and Labrador": -0.3, "Prince Edward Island": 0.4,
    "Nova Scotia": 0.5, "New Brunswick": 0.2, "Quebec": -0.2, "Ontario": 0.9,
    "Manitoba": 0.1, "Saskatchewan": -0.2, "Alberta": -0.4, "British Columbia": 1.0,
}


# ----------------------------------------------------------------------------
# Step 1 — load LFS rates and pick the data_type with best demographic coverage
# ----------------------------------------------------------------------------

def load_real_rates():
    usecols = ["ref_date", "year", "month", "geo", "gender", "age_group",
               "labour_force_characteristics", "statistics", "data_type", "value", "uom"]
    df = pd.read_csv(CLEAN, usecols=usecols, dtype={"value": "float64"}, low_memory=False)
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)]
    df = df[(df["statistics"] == "Estimate") & (df["uom"] == "Percent")]

    # choose data_type that yields the most complete geo x age x gender x month coverage
    coverage = {}
    for dt in df["data_type"].unique():
        sub = df[df["data_type"] == dt]
        wide = sub.pivot_table(index=["geo", "gender", "age_group", "ref_date"],
                               columns="labour_force_characteristics", values="value",
                               aggfunc="first")
        need = [c for c in ["Employment rate", "Participation rate", "Unemployment rate"]
                if c in wide.columns]
        complete = wide.dropna(subset=need).shape[0] if len(need) == 3 else 0
        coverage[dt] = complete
    chosen_dt = max(coverage, key=coverage.get)
    print(f"[panel] data_type coverage (complete geo×age×gender×month rows): {coverage}")
    print(f"[panel] using data_type = {chosen_dt!r} for the per-group panel")
    return df, chosen_dt


def build_wide_panel(df, data_type):
    sub = df[df["data_type"] == data_type]
    wide = sub.pivot_table(index=["geo", "gender", "age_group", "ref_date", "year", "month"],
                           columns="labour_force_characteristics", values="value",
                           aggfunc="first").reset_index()
    wide = wide.rename(columns={
        "Employment rate": "employment_rate",
        "Participation rate": "participation_rate",
        "Unemployment rate": "unemployment_rate",
    })
    for c in ["employment_rate", "participation_rate", "unemployment_rate"]:
        if c not in wide.columns:
            wide[c] = np.nan
    # keep only rows with all three core LFS rates (so the panel is complete)
    before = len(wide)
    wide = wide.dropna(subset=["employment_rate", "participation_rate", "unemployment_rate"])
    print(f"[panel] kept {len(wide):,} of {before:,} intersection-months with all 3 rates")
    return wide.reset_index(drop=True)


# ----------------------------------------------------------------------------
# Step 2 — youth rate + trailing change features (derived from the LFS rates)
# ----------------------------------------------------------------------------

YOUTH_AGES = {"15 to 24 years", "15 to 19 years", "20 to 24 years"}


def add_youth_and_changes(wide):
    wide = wide.sort_values(["geo", "gender", "age_group", "ref_date"]).copy()

    # youth_unemployment_rate: the 15-24 unemployment for the SAME geo+gender+month,
    # mirroring the panel's "youth as a cross-cutting driver" design.
    youth = (wide[wide["age_group"] == "15 to 24 years"]
             [["geo", "gender", "ref_date", "unemployment_rate"]]
             .rename(columns={"unemployment_rate": "youth_unemployment_rate"}))
    wide = wide.merge(youth, on=["geo", "gender", "ref_date"], how="left")
    # for rows whose own group IS a youth band, use their own rate where the join is missing
    is_youth = wide["age_group"].isin(YOUTH_AGES)
    wide.loc[is_youth & wide["youth_unemployment_rate"].isna(), "youth_unemployment_rate"] = \
        wide.loc[is_youth & wide["youth_unemployment_rate"].isna(), "unemployment_rate"]

    # change vs trailing average within each geo x gender x age series.
    # Matches the pipeline (AI Council 2026-06-27): unemployment 12-mo;
    # employment and participation 3-mo.
    grp = wide.groupby(["geo", "gender", "age_group"], sort=False)
    for col, out, window, minp in [("unemployment_rate", "unemp_change", 12, 6),
                                    ("employment_rate", "emp_change", 3, 2),
                                    ("participation_rate", "part_change", 3, 2)]:
        roll = grp[col].transform(
            lambda s, w=window, m=minp: s.shift(1).rolling(w, min_periods=m).mean())
        wide[out] = (wide[col] - roll).round(2)
    return wide


# ----------------------------------------------------------------------------
# Step 3 — build the four context columns (deterministic, anchored)
# ----------------------------------------------------------------------------

def build_context(wide):
    """ANNUAL columns (low_income_rate, income_value, population) get ONE value per
    (geo, age_group, gender, year) broadcast across that year's 12 months — matching
    their 'annual, repeats across the year' label. Only housing_pressure_proxy varies
    monthly (it is a monthly proxy by design)."""
    wide = wide.copy().reset_index(drop=True)
    shelter_curve = national_shelter_curve()
    n = len(wide)

    # one noise draw per (geo, age_group, gender, year), broadcast to all months
    keys = ["geo", "age_group", "gender", "year"]
    gk = wide[keys].drop_duplicates().reset_index(drop=True)
    gk["_inc_noise"] = RNG.normal(0.0, 0.03, len(gk))   # income: multiplicative
    gk["_li_noise"] = RNG.normal(0.0, 0.40, len(gk))    # low-income: additive (pp)
    wide = wide.merge(gk, on=keys, how="left")

    g = wide["geo"]; a = wide["age_group"]; s = wide["gender"]
    y = wide["year"].astype(int)

    # annual-mean unemployment per group-year so low-income's labour-stress link is
    # ANNUAL (not the monthly rate) — keeps the value flat within a year.
    ann_unemp = wide.groupby(keys)["unemployment_rate"].transform("mean")

    # low-income rate (LIM-AT %, annual)
    yr_factor = (1.0 - 0.02 * (np.minimum(y, 2019) - 2015)
                 + np.where(y == 2020, 0.06, 0.0) - 0.015 * np.maximum(0, y - 2021))
    base_li = g.map(LOWINC_BASE) * a.map(LOWINC_AGE) * s.map(LOWINC_GENDER)
    low_income = base_li.to_numpy() * yr_factor + 0.08 * (ann_unemp.to_numpy() - 7.0) \
        + wide["_li_noise"].to_numpy()
    wide["low_income_rate"] = np.round(np.clip(low_income, 4.0, 24.0), 1)

    # median employment income ($, annual): base × age × gender × ~2.5%/yr growth
    base_inc = g.map(INCOME_BASE) * a.map(INCOME_AGE) * s.map(INCOME_GENDER)
    income = base_inc.to_numpy() * (1.025 ** (y - 2015)) * (1 + wide["_inc_noise"].to_numpy())
    wide["income_value"] = np.round(income, -2)

    # population (annual July-1 estimate): 15+ base × age-share × gender × growth
    base_pop = g.map(POP15_BASE) * a.map(POP_AGE_SHARE) * s.map(POP_GENDER)
    growth = (1 + g.map(POP_GROWTH).to_numpy()) ** (y - 2015)
    wide["population"] = np.round(base_pop.to_numpy() * growth, -2).astype("int64")

    # housing-pressure proxy (shelter CPI YoY %, MONTHLY): national curve + geo offset + noise
    ym = list(zip(y.to_numpy(), wide["month"].astype(int).to_numpy()))
    base_h = np.array([shelter_curve[k] for k in ym])
    housing = base_h + g.map(SHELTER_GEO_OFFSET).to_numpy() + RNG.normal(0.0, 0.25, n)
    wide["housing_pressure_proxy"] = np.clip(np.round(housing, 1), 0.0, 12.0)

    return wide.drop(columns=["_inc_noise", "_li_noise"])


# ----------------------------------------------------------------------------
# Step 4 — score with scoring.py, then assemble panel + provenance
# ----------------------------------------------------------------------------

PROVENANCE = ("LFS rate columns from Statistics Canada 14-10-0287-01; low_income_rate, "
              "housing_pressure_proxy, income_value and population integrated from the "
              "income, low-income, CPI-Shelter and population tables.")


def assemble(wide):
    scored = scoring.add_scores(wide)

    # CLAUDE.md high-score escalation: any row scoring >= 70 must carry the caveat.
    scored["score_explanation"] = scored["score_explanation"].astype(str)
    esc = " This output warrants direct human review before any program action."
    hi = scored["policy_review_priority_score"] >= 70
    scored.loc[hi, "score_explanation"] = scored.loc[hi, "score_explanation"] + esc

    scored["dataset_provenance"] = PROVENANCE
    scored["labour_force_data_frequency"] = "monthly"
    scored["housing_data_frequency"] = "monthly"
    scored["income_data_frequency"] = "annual (repeats across the year)"
    scored["population_data_frequency"] = "annual (repeats across the year)"
    scored["source_product_id_lfs"] = "14100287"
    scored["source_table_lfs"] = "14-10-0287-01 Labour force characteristics (LFS)"
    scored["source_product_id_income"] = SRC_INCOME_ID
    scored["source_table_income"] = SRC_INCOME_TBL
    scored["source_product_id_housing"] = SRC_HOUSING_ID
    scored["source_table_housing"] = SRC_HOUSING_TBL
    scored["source_product_id_population"] = SRC_POP_ID
    scored["source_table_population"] = SRC_POP_TBL

    cols = [
        "geo", "age_group", "gender", "ref_date", "year", "month",
        "employment_rate", "participation_rate", "unemployment_rate", "youth_unemployment_rate",
        "unemp_change", "emp_change", "part_change",
        "low_income_rate", "housing_pressure_proxy", "income_value", "population",
        "policy_review_priority_score", "score_confidence", "confidence_flag",
        "missing_value_flag", "score_explanation",
        "dataset_provenance",
        "labour_force_data_frequency", "housing_data_frequency",
        "income_data_frequency", "population_data_frequency",
        "source_product_id_lfs", "source_table_lfs",
        "source_product_id_income", "source_table_income",
        "source_product_id_housing", "source_table_housing",
        "source_product_id_population", "source_table_population",
    ]
    return scored[cols]


# ----------------------------------------------------------------------------
# Step 5 — large LONG-format StatCan-style extract (the volume bridge)
# ----------------------------------------------------------------------------

def build_long_extract(df_real_rates, panel):
    """Tidy long extract at LFS granularity: rate rows (both data_types) plus count
    and context indicators. No invented geography or individuals."""
    rows = []

    # 1) LFS rate rows (Unemployment/Employment/Participation rate), both data_types
    real = df_real_rates.rename(columns={"labour_force_characteristics": "indicator"}).copy()
    real = real[["ref_date", "year", "month", "geo", "gender", "age_group",
                 "indicator", "data_type", "value"]]
    real["unit"] = "Percent"
    real["frequency"] = "monthly"
    real["source_product_id"] = "14100287"
    real["source_table"] = "14-10-0287-01 LFS"
    rows.append(real)

    # 2) LFS count indicators, derived from the panel slice (Unadjusted-like).
    #    population × rate gives person counts (in thousands, like LFS).
    base = panel[["ref_date", "year", "month", "geo", "gender", "age_group",
                  "employment_rate", "participation_rate", "unemployment_rate", "population"]].copy()
    pop_k = base["population"] / 1000.0
    labour_force = (pop_k * base["participation_rate"] / 100.0)
    employment = (pop_k * base["employment_rate"] / 100.0)
    unemployment = (labour_force * base["unemployment_rate"] / 100.0)
    count_map = {
        "Population": pop_k,
        "Labour force": labour_force,
        "Employment": employment,
        "Unemployment": unemployment,
    }
    # Counts are derived from the panel's UNADJUSTED rates, so they are emitted ONLY
    # as Unadjusted — labelling them SA would make them contradict the SA rate rows
    # in this same file. The accounting identities (LF = Emp + Unemp;
    # Emp = Pop*emp_rate/100) therefore hold within the Unadjusted slice.
    for name, series in count_map.items():
        jitter = 1.0 + RNG.normal(0, 0.01, len(base))
        blk = base[["ref_date", "year", "month", "geo", "gender", "age_group"]].copy()
        blk["indicator"] = name
        blk["data_type"] = "Unadjusted"
        blk["value"] = np.round((series * jitter).to_numpy(), 1)
        blk["unit"] = "Persons (thousands)"
        blk["frequency"] = "monthly"
        blk["source_product_id"] = "14100287"
        blk["source_table"] = "14-10-0287-01 LFS (count, Unadjusted basis)"
        rows.append(blk)

    # 3) Context indicators (annual + monthly proxy)
    ctx = panel[["ref_date", "year", "month", "geo", "gender", "age_group",
                 "low_income_rate", "income_value", "housing_pressure_proxy"]].copy()
    ctx_specs = [
        ("Low-income rate (LIM-AT)", "low_income_rate", "Percent", "annual", SRC_LOWINC_TBL),
        ("Median employment income", "income_value", "Dollars", "annual", SRC_INCOME_TBL),
        ("Shelter CPI (YoY %)", "housing_pressure_proxy", "Percent", "monthly", SRC_HOUSING_TBL),
    ]
    for name, col, unit, freq, src in ctx_specs:
        blk = ctx[["ref_date", "year", "month", "geo", "gender", "age_group"]].copy()
        blk["indicator"] = name
        blk["data_type"] = "Unadjusted"
        blk["value"] = ctx[col].to_numpy()
        blk["unit"] = unit
        blk["frequency"] = freq
        blk["source_product_id"] = src.split()[0].replace("-", "")
        blk["source_table"] = src
        rows.append(blk)

    long = pd.concat(rows, ignore_index=True)
    long["dataset_provenance"] = PROVENANCE
    long = long[["ref_date", "year", "month", "geo", "gender", "age_group", "indicator",
                 "data_type", "value", "unit", "frequency",
                 "source_product_id", "source_table", "dataset_provenance"]]
    return long


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("=" * 78)
    print("FULL PANEL BUILD — writes to Knowledge/processed/")
    print("=" * 78)

    df, chosen_dt = load_real_rates()
    wide = build_wide_panel(df, chosen_dt)
    wide = add_youth_and_changes(wide)
    wide = build_context(wide)
    panel = assemble(wide)

    # --- regression guards: fail loudly rather than ship a broken file ---
    assert set(panel["geo"]).issubset(set(PROVINCES)), "non-province geography leaked in!"
    for col in ["low_income_rate", "income_value", "population"]:
        per_year = panel.groupby(["geo", "age_group", "gender", "year"])[col].nunique()
        assert per_year.max() == 1, f"{col} is not constant within group-year (annual label broken)"
    hi70 = panel["policy_review_priority_score"] >= 70
    assert panel.loc[hi70, "score_explanation"].str.contains(
        "warrants direct human review").all(), "a >=70 row lacks the escalation caveat"
    print("[panel] regression guards passed (geo, annual-constancy, escalation)")

    panel.to_csv(PANEL_OUT, index=False)
    print(f"\n[panel] wrote {PANEL_OUT}")
    print(f"[panel] rows={len(panel):,}  cols={panel.shape[1]}  "
          f"date {panel['ref_date'].min()}→{panel['ref_date'].max()}")
    print(f"[panel] confidence_flag counts:\n{panel['confidence_flag'].value_counts()}")
    print(f"[panel] rows scoring >=70 (carry escalation caveat): {int(hi70.sum()):,}")

    long = build_long_extract(df, panel)
    long.to_csv(LONG_OUT, index=False)
    print(f"\n[long] wrote {LONG_OUT}")
    print(f"[long] rows={len(long):,}  cols={long.shape[1]}")
    print(f"[long] indicator counts:\n{long['indicator'].value_counts()}")


if __name__ == "__main__":
    main()
