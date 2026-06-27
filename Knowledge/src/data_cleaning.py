"""
data_cleaning.py — Standardise and clean StatCan source tables for the
Labour Market Stress dashboard.

Core rules (see Knowledge/metadata/integration_notes.md):
- Column names -> lowercase snake_case.
- REF_DATE -> ref_date + derived year / month / quarter + data_frequency.
- GEO -> geo, DGUID -> dguid, VALUE -> value.
- Suppressed / blank / "F" / ".." cells become NaN and set missing_value_flag.
  We NEVER invent or impute missing values.
- Source provenance columns are attached: source_product_id, source_table_title,
  source_category, retrieval_date.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

try:  # importable both as a package and as a loose module (e.g. in a notebook)
    from .utils import SUPPRESSION, find_col, snake
except ImportError:  # pragma: no cover
    from utils import SUPPRESSION, find_col, snake


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase snake_case every column label."""
    return df.rename(columns={c: snake(c) for c in df.columns})


def clean_statcan(
    df: pd.DataFrame,
    *,
    product_id: int,
    frequency: str,
    table_title: str = "",
    category: str = "",
    retrieval_date: str = "",
) -> pd.DataFrame:
    """Standardise any StatCan full-table CSV into a tidy long frame.

    Adds: ref_date, year, month, quarter, data_frequency, geo, dguid, value,
    status, missing_value_flag, and source_* provenance columns. Original
    dimension columns are kept (snake_cased) so feature extraction can slice.
    """
    df = df.copy()
    ref = find_col(df, "REF_DATE") or "REF_DATE"
    geo = find_col(df, "GEO") or "GEO"
    val = find_col(df, "VALUE") or "VALUE"
    status = find_col(df, "STATUS")
    dguid = find_col(df, "DGUID")

    ref_date = df[ref].astype(str)
    year = pd.to_numeric(ref_date.str.slice(0, 4), errors="coerce").astype("Int64")
    month = pd.to_numeric(ref_date.str.slice(5, 7), errors="coerce").astype("Int64")

    value = pd.to_numeric(df[val], errors="coerce")
    status_series = df[status].astype(str) if status else pd.Series([""] * len(df))
    suppressed = status_series.isin({str(s) for s in SUPPRESSION if s is not None})

    out = standardize_columns(df)
    out["ref_date"] = ref_date
    out["year"] = year
    out["month"] = month
    out["quarter"] = ((month - 1) // 3 + 1).astype("Int64")
    out["data_frequency"] = frequency
    out["geo"] = df[geo].astype(str)
    out["dguid"] = df[dguid].astype(str) if dguid else pd.NA
    out["value"] = value
    out["missing_value_flag"] = value.isna() | suppressed
    out["source_product_id"] = product_id
    out["source_table_title"] = table_title
    out["source_category"] = category
    out["retrieval_date"] = retrieval_date
    return out


# --------------------------------------------------------------------------- #
# Labour Force Survey: the dashboard spine
# --------------------------------------------------------------------------- #
RATE_CHARS = ("unemployment rate", "participation rate", "employment rate")


def lfs_headline_features(clean: pd.DataFrame) -> pd.DataFrame:
    """From a cleaned LFS frame, build the headline geo x month panel.

    Headline slice = Total - Gender, 15 years and over, Seasonally adjusted
    (falls back to whatever data type is present). Adds age-band unemployment
    (youth 15-24, core 25-54, older 55+) and the change features used by the
    triage score: unemployment change is 12-month, employment and participation
    change are 3-month (AI Council 2026-06-27).
    """
    char = find_col(clean, "labour_force_characteristics", "characteristic")
    dtype = find_col(clean, "data_type")
    gender = find_col(clean, "gender", "sex")
    age = find_col(clean, "age_group")

    f = clean
    if dtype and f[dtype].astype(str).str.contains("Seasonally adjusted", case=False, na=False).any():
        f = f[f[dtype].astype(str).str.contains("Seasonally adjusted", case=False, na=False)]
    gtot = f[gender].astype(str).str.contains("Total", case=False, na=False) if gender else True

    head = f[gtot & (f[age].astype(str).str.contains("15 years and over", case=False, na=False))]
    head = head[head[char].astype(str).str.lower().isin([c for c in RATE_CHARS])]
    wide = (head.pivot_table(index=["geo", "ref_date", "year", "month"],
                             columns=char, values="value", aggfunc="first")
                .reset_index())
    wide.columns = [snake(c) if c not in ("geo", "ref_date", "year", "month") else c
                    for c in wide.columns]

    # Age-band unemployment rates (Total - Gender, seasonally-adjusted slice).
    # Youth feeds the score (youth_unemp component); core/older are descriptive
    # drivers for the demographic view. The connected LFS table publishes
    # 15-24, 25-54, and 55+ with full seasonally-adjusted coverage; it does NOT
    # publish 65+, and 55-64 alone is seasonally-adjusted-sparse — so "older
    # workers" is deliberately 55+. Scoring these bands as their own rows needs an
    # AI-Council-ratified scoring redesign and is not done here.
    AGE_BANDS = (("15 to 24", "youth_unemployment_rate"),
                 ("25 to 54", "core_unemployment_rate"),
                 ("55 years and over", "older_unemployment_rate"))
    for pattern, outcol in AGE_BANDS:
        band = f[gtot
                 & f[age].astype(str).str.contains(pattern, case=False, na=False)
                 & f[char].astype(str).str.contains("unemployment rate", case=False, na=False)]
        if not band.empty:
            b = (band[["geo", "ref_date", "value"]]
                 .rename(columns={"value": outcol})
                 .drop_duplicates(["geo", "ref_date"]))
            wide = wide.merge(b, on=["geo", "ref_date"], how="left")

    # Change vs trailing average (stress = rise in unemp / fall in emp & part).
    # Unemployment uses a 12-month window; employment and participation use a
    # 3-month window (AI Council 2026-06-27). Each shifted by 1 so the current
    # month is compared to the months before it.
    CHANGE_SPECS = (("unemployment_rate", "unemp_change", 12, 6),
                    ("employment_rate", "emp_change", 3, 2),
                    ("participation_rate", "part_change", 3, 2))
    wide = wide.sort_values(["geo", "ref_date"])
    for col, out, window, minp in CHANGE_SPECS:
        if col in wide.columns:
            avg = wide.groupby("geo")[col].transform(
                lambda s, w=window, m=minp: s.rolling(w, min_periods=m).mean().shift(1))
            wide[out] = wide[col] - avg
    return wide
