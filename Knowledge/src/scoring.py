"""
scoring.py — Transparent `policy_review_priority_score` for the Labour Market
Stress & Social Support Prioritization Dashboard.

WHAT THIS SCORE IS
------------------
A 0-100 TRIAGE signal that flags a geography x period (and, where data allows,
demographic slice) as showing ELEVATED labour-market stress that WARRANTS HUMAN
POLICY REVIEW. Higher = review sooner.

WHAT THIS SCORE IS NOT
----------------------
- It is NOT a "social assistance need score".
- It is NOT an eligibility, benefit, approval, denial, or reduction decision.
- It does NOT measure poverty, household need, or individual circumstances.

Every score ships with `score_explanation` (the drivers) and `confidence_flag`
(how much of the weight was backed by real data). Missing inputs lower
confidence; they are never filled in. The AI Council reviews any policy reading
of these scores before it is treated as decision-ready.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Component weights — explicit and editable so the AI Council can review them.
WEIGHTS = {
    "unemp_level": 0.22,      # unemployment rate level (trimmed 0.30->0.22 to lift income)
    "unemp_change": 0.13,     # rise vs trailing 12-mo average (trimmed 0.15->0.13)
    "emp_decline": 0.10,      # fall in employment rate vs 12-mo average
    "part_decline": 0.10,     # fall in participation rate vs 12-mo average
    "youth_unemp": 0.10,      # youth (15-24) unemployment rate
    "low_income": 0.25,       # low-income rate — now the largest factor (raised 0.15->0.25)
    "housing_pressure": 0.10, # shelter-CPI YoY pressure PROXY (if available)
}

# Fixed normalisation anchors (value at score 0 -> value at score 1), clipped.
# Documented and stable so the score is explainable, not a per-run min-max.
ANCHORS = {
    "unemp_level": (4.0, 14.0),
    "unemp_change": (0.0, 3.0),
    "emp_decline": (0.0, 3.0),
    "part_decline": (0.0, 3.0),
    "youth_unemp": (8.0, 25.0),
    "low_income": (5.0, 20.0),
    "housing_pressure": (0.0, 10.0),
}

# Map each scoring component to the panel column that feeds it.
COMPONENT_SOURCE = {
    "unemp_level": "unemployment_rate",
    "unemp_change": "unemp_change",
    "emp_decline": "emp_change",        # sign flipped below (a fall = stress)
    "part_decline": "part_change",      # sign flipped below
    "youth_unemp": "youth_unemployment_rate",
    "low_income": "low_income_rate",
    "housing_pressure": "housing_pressure_proxy",
}

# Human-readable labels for the explanation string.
LABELS = {
    "unemp_level": "unemployment rate",
    "unemp_change": "rising unemployment vs 12-mo avg",
    "emp_decline": "falling employment rate",
    "part_decline": "falling participation",
    "youth_unemp": "youth unemployment",
    "low_income": "low-income rate",
    "housing_pressure": "shelter-cost pressure (proxy)",
}


def _norm(value, lo, hi):
    """Min-max a value to 0..1 against fixed anchors, clipped. NaN stays NaN."""
    if pd.isna(value):
        return np.nan
    return float(np.clip((value - lo) / (hi - lo), 0.0, 1.0))


def score_row(row, weights=WEIGHTS, anchors=ANCHORS) -> pd.Series:
    """Score one panel row. Returns score, confidence_flag, missing flag, why."""
    contribs = {}
    weight_available = 0.0
    for comp, col in COMPONENT_SOURCE.items():
        if col not in row.index:
            continue
        raw = row.get(col)
        if comp in ("emp_decline", "part_decline") and pd.notna(raw):
            raw = -raw  # a decline is stress -> flip so larger = worse
        n = _norm(raw, *anchors[comp])
        if pd.notna(n):
            contribs[comp] = (weights[comp], n, row.get(col))
            weight_available += weights[comp]

    if weight_available == 0:
        return pd.Series({
            "policy_review_priority_score": np.nan,
            "score_confidence": 0.0,
            "confidence_flag": "no inputs",
            "missing_value_flag": True,
            "score_explanation": "No scoring inputs available for this row — "
                                 "route to a human analyst; do not infer.",
        })

    score = 100.0 * sum(w * n for w, n, _ in contribs.values()) / weight_available
    confidence = weight_available / sum(weights.values())
    conf_flag = ("high" if confidence >= 0.85 else
                 "medium" if confidence >= 0.55 else "low")
    top = sorted(contribs.items(), key=lambda kv: kv[1][0] * kv[1][1], reverse=True)[:3]
    drivers = "; ".join(
        f"{LABELS.get(k, k)} ({raw:.1f})" for k, (_, _, raw) in top if pd.notna(raw))
    return pd.Series({
        "policy_review_priority_score": round(score, 1),
        "score_confidence": round(confidence, 2),
        "confidence_flag": conf_flag,
        "missing_value_flag": confidence < 1.0,
        "score_explanation": (
            f"Flagged for policy review — top drivers: {drivers}. "
            f"Confidence {conf_flag} ({confidence:.0%} of weight backed by data). "
            f"Triage signal only; not an eligibility or benefit decision."),
    })


def add_scores(panel: pd.DataFrame, weights=WEIGHTS, anchors=ANCHORS) -> pd.DataFrame:
    """Append the score columns to a panel of cleaned/feature rows."""
    scored = panel.apply(lambda r: score_row(r, weights, anchors), axis=1)
    # avoid clobbering an existing missing_value_flag from cleaning
    if "missing_value_flag" in panel.columns:
        scored = scored.rename(columns={"missing_value_flag": "score_missing_value_flag"})
    return pd.concat([panel.reset_index(drop=True), scored.reset_index(drop=True)], axis=1)
