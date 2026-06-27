"""
sensitivity.py — Weight-robustness checks for the `policy_review_priority_score`.

WHY THIS EXISTS
---------------
The score's component weights (0.30 unemployment, 0.15 low-income, ...) are
TEAM-SET ANCHORS, not validated standards — a known project risk and the first
thing a reviewer or peer will challenge: *"your weights are arbitrary."* This
module answers that challenge with evidence instead of assertion. It re-scores
the live panel under perturbed weight vectors and reports whether the ranking —
the top area to focus on — actually CHANGES.

It is a defence/diagnostic tool, NOT a scoring change. It never edits
`scoring.py`, never writes the panel, and never invents a value: every number it
reports is re-computed from `Knowledge/processed/policy_triage_panel.csv` using
the same `add_scores()` the dashboard uses.

HONEST LIMIT IT SURFACES
------------------------
`low_income` and `housing_pressure` are NaN in the current panel. Because
`score_row()` divides by the weight actually backed by data, those two weights
have ZERO effect on today's ranking — sensitivity to them is moot until the
tables download. So the meaningful robustness question is among the 5
LFS-backed components, and this tool reports the inert weights explicitly rather
than pretending they matter.

USAGE
-----
    python3 Knowledge/src/sensitivity.py                 # latest cycle, ±33%
    python3 Knowledge/src/sensitivity.py --date 2026-05 --delta 0.33 --top-n 5
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

# Reuse the production scoring logic — do not re-implement it here.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scoring import (  # noqa: E402
    ANCHORS,
    COMPONENT_SOURCE,
    LABELS,
    WEIGHTS,
    add_scores,
)

# Columns produced by scoring; dropped before re-scoring so we don't duplicate.
_SCORE_COLS = [
    "policy_review_priority_score", "score_confidence", "confidence_flag",
    "missing_value_flag", "score_explanation", "score_missing_value_flag",
]

_DEFAULT_PANEL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "processed", "policy_triage_panel.csv",
)

# The national aggregate is a reference baseline, not an "area to focus on".
_DEFAULT_EXCLUDE = ("Canada",)


# --------------------------------------------------------------------------- #
# Core: re-rank the panel under a given weight vector
# --------------------------------------------------------------------------- #
def rank_slice(panel: pd.DataFrame, weights=WEIGHTS, anchors=ANCHORS,
               ref_date: str | None = None,
               exclude_geos=_DEFAULT_EXCLUDE) -> pd.DataFrame:
    """Re-score one cycle and return geos ranked by score (desc)."""
    df = panel
    if ref_date is not None:
        df = df[df["ref_date"] == ref_date]
    if exclude_geos:
        df = df[~df["geo"].isin(exclude_geos)]
    base = df.drop(columns=[c for c in _SCORE_COLS if c in df.columns])
    scored = add_scores(base.copy(), weights=weights, anchors=anchors)
    ranked = scored.sort_values(
        "policy_review_priority_score", ascending=False, na_position="last")
    return ranked.reset_index(drop=True)


def backed_components(panel: pd.DataFrame, weights=WEIGHTS,
                      ref_date: str | None = None,
                      exclude_geos=_DEFAULT_EXCLUDE):
    """Split components into those backed by real data in this slice vs inert (NaN)."""
    df = panel
    if ref_date is not None:
        df = df[df["ref_date"] == ref_date]
    if exclude_geos:
        df = df[~df["geo"].isin(exclude_geos)]
    backed, inert = [], []
    for comp, col in COMPONENT_SOURCE.items():
        if comp not in weights:
            continue
        (backed if (col in df.columns and df[col].notna().any()) else inert).append(comp)
    return backed, inert


# --------------------------------------------------------------------------- #
# Weight perturbation helpers
# --------------------------------------------------------------------------- #
def set_weight(base_weights: dict, comp: str, value: float) -> dict:
    """Set comp's weight to `value`, scaling the others to keep the total at 1.0."""
    others = {k: v for k, v in base_weights.items() if k != comp}
    s = sum(others.values())
    scale = (1.0 - value) / s if s > 0 else 0.0
    w = {k: v * scale for k, v in others.items()}
    w[comp] = value
    return w


def compare_rankings(baseline: pd.DataFrame, perturbed: pd.DataFrame,
                     top_n: int = 3) -> dict:
    """How much did a re-rank move? Top change, top-N overlap, Spearman, margin."""
    b_top = baseline["geo"].iloc[0]
    p_top = perturbed["geo"].iloc[0]
    b_set = set(baseline["geo"].head(top_n))
    p_set = set(perturbed["geo"].head(top_n))
    merged = baseline[["geo", "policy_review_priority_score"]].merge(
        perturbed[["geo", "policy_review_priority_score"]],
        on="geo", suffixes=("_base", "_pert"))
    spearman = (merged["policy_review_priority_score_base"]
                .corr(merged["policy_review_priority_score_pert"], method="spearman"))
    margin = float(baseline["policy_review_priority_score"].iloc[0]
                   - baseline["policy_review_priority_score"].iloc[1])
    return {
        "top_changed": b_top != p_top,
        "baseline_top": b_top,
        "perturbed_top": p_top,
        "topn_overlap": len(b_set & p_set),
        "topn": top_n,
        "spearman": None if pd.isna(spearman) else round(float(spearman), 3),
        "baseline_margin": round(margin, 1),
    }


def flip_threshold(panel: pd.DataFrame, comp: str, ref_date: str,
                   base_weights=WEIGHTS, anchors=ANCHORS,
                   grid=None, exclude_geos=_DEFAULT_EXCLUDE) -> dict:
    """Sweep comp's weight across [0, 0.95]; find the nearest weight ABOVE and BELOW
    its current value at which the top-ranked geo changes (directional thresholds)."""
    current = base_weights[comp]
    base_top = rank_slice(panel, base_weights, anchors, ref_date,
                          exclude_geos)["geo"].iloc[0]
    if grid is None:
        grid = [round(float(x), 3) for x in np.linspace(0.0, 0.95, 40)]
    tops = [(w, rank_slice(panel, set_weight(base_weights, comp, w), anchors,
                           ref_date, exclude_geos)["geo"].iloc[0]) for w in grid]
    below = [(w, t) for w, t in tops if w < current and t != base_top]
    above = [(w, t) for w, t in tops if w > current and t != base_top]
    # nearest boundary to the current weight on each side
    lower = max(below, key=lambda x: x[0]) if below else None
    raise_ = min(above, key=lambda x: x[0]) if above else None
    return {
        "component": comp, "current_weight": current, "base_top": base_top,
        "lower_below": None if lower is None else {"weight": lower[0], "new_top": lower[1]},
        "raise_above": None if raise_ is None else {"weight": raise_[0], "new_top": raise_[1]},
        "stable_full_range": not below and not above,
    }


def one_at_a_time(panel: pd.DataFrame, ref_date: str, backed: list,
                  base_weights=WEIGHTS, anchors=ANCHORS, delta: float = 0.33,
                  exclude_geos=_DEFAULT_EXCLUDE) -> dict:
    """Nudge each backed weight ±delta (relative); does the top-ranked geo hold?"""
    base_top = rank_slice(panel, base_weights, anchors, ref_date,
                          exclude_geos)["geo"].iloc[0]
    results, any_flip = [], False
    for comp in backed:
        for sign in (1, -1):
            val = float(np.clip(base_weights[comp] * (1 + sign * delta), 0.0, 0.95))
            top = rank_slice(panel, set_weight(base_weights, comp, val), anchors,
                             ref_date, exclude_geos)["geo"].iloc[0]
            flipped = top != base_top
            any_flip = any_flip or flipped
            results.append({"component": comp, "direction": "+" if sign > 0 else "-",
                            "weight": round(val, 3), "top": top, "flipped": flipped})
    return {"base_top": base_top, "delta": delta, "any_flip": any_flip,
            "results": results}


# --------------------------------------------------------------------------- #
# Top-level report + governed prose
# --------------------------------------------------------------------------- #
def robustness_report(panel: pd.DataFrame, ref_date: str,
                      base_weights=WEIGHTS, anchors=ANCHORS,
                      delta: float = 0.33, top_n: int = 5,
                      exclude_geos=_DEFAULT_EXCLUDE) -> dict:
    ranked = rank_slice(panel, base_weights, anchors, ref_date, exclude_geos)
    backed, inert = backed_components(panel, base_weights, ref_date, exclude_geos)
    oaat = one_at_a_time(panel, ref_date, backed, base_weights, anchors, delta,
                         exclude_geos)
    thresholds = {c: flip_threshold(panel, c, ref_date, base_weights, anchors,
                                    exclude_geos=exclude_geos) for c in backed}
    top = ranked.iloc[0]
    runner = ranked.iloc[1]
    return {
        "ref_date": ref_date,
        "top": {"geo": top["geo"],
                "score": float(top["policy_review_priority_score"]),
                "confidence_flag": top["confidence_flag"]},
        "runner_up": {"geo": runner["geo"],
                      "score": float(runner["policy_review_priority_score"])},
        "margin": round(float(top["policy_review_priority_score"]
                              - runner["policy_review_priority_score"]), 1),
        "backed_components": backed,
        "inert_components": inert,
        "one_at_a_time": oaat,
        "flip_thresholds": thresholds,
        "ranking": ranked[["geo", "policy_review_priority_score",
                           "confidence_flag"]].head(top_n).to_dict("records"),
    }


def summarize(report: dict) -> str:
    """Governed, triage-language prose summary for an analyst defending the ranking."""
    t = report["top"]
    lines = []
    lines.append(
        f"Cycle {report['ref_date']}: the top area to focus on is {t['geo']} "
        f"(policy_review_priority_score {t['score']:.1f}, confidence {t['confidence_flag']}), "
        f"ahead of {report['runner_up']['geo']} by {report['margin']:.1f} points.")

    if not report["one_at_a_time"]["any_flip"]:
        lines.append(
            f"Robustness: {t['geo']} stays the top-ranked area under "
            f"±{report['one_at_a_time']['delta']:.0%} on every data-backed weight.")
    else:
        flips = [r for r in report["one_at_a_time"]["results"] if r["flipped"]]
        detail = "; ".join(
            f"{LABELS.get(r['component'], r['component'])} {r['direction']}→ {r['top']}"
            for r in flips)
        lines.append(
            f"Robustness: the top rank CHANGES under ±"
            f"{report['one_at_a_time']['delta']:.0%} for: {detail}. Treat as fragile.")

    for comp, th in report["flip_thresholds"].items():
        label = LABELS.get(comp, comp)
        cur = th["current_weight"]
        if th["stable_full_range"]:
            lines.append(
                f"  • {label} (currently {cur:.2f}): top rank holds across the full "
                f"0–0.95 weight range.")
        else:
            parts = []
            if th["raise_above"] is not None:
                r = th["raise_above"]
                parts.append(f"raising it above ~{r['weight']:.2f} → {r['new_top']}")
            if th["lower_below"] is not None:
                lo = th["lower_below"]
                parts.append(f"lowering it below ~{lo['weight']:.2f} → {lo['new_top']}")
            lines.append(
                f"  • {label} (currently {cur:.2f}): top rank changes by "
                + " or ".join(parts) + ".")

    if report["inert_components"]:
        inert = ", ".join(LABELS.get(c, c) for c in report["inert_components"])
        lines.append(
            f"Note: the {inert} weights have NO effect on today's ranking because "
            f"those columns are NaN (income/housing pending download). Sensitivity to "
            f"them is moot until the tables connect — which is also why confidence is "
            f"capped at medium.")

    lines.append(
        "All values re-computed from policy_triage_panel.csv via scoring.add_scores(). "
        "Triage signal only — not an eligibility or benefit decision; province-level only.")
    return "\n".join(lines)


def _latest_date(panel: pd.DataFrame) -> str:
    return str(panel["ref_date"].max())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Weight-robustness check for the triage score.")
    ap.add_argument("--panel", default=_DEFAULT_PANEL, help="path to policy_triage_panel.csv")
    ap.add_argument("--date", default=None, help="ref_date (YYYY-MM); default = latest")
    ap.add_argument("--delta", type=float, default=0.33, help="relative ± weight nudge")
    ap.add_argument("--top-n", type=int, default=5, help="rows to show in the ranking")
    args = ap.parse_args(argv)

    panel = pd.read_csv(args.panel)
    ref_date = args.date or _latest_date(panel)
    report = robustness_report(panel, ref_date, delta=args.delta, top_n=args.top_n)

    print(summarize(report))
    print("\nTop ranking this cycle:")
    for i, r in enumerate(report["ranking"], 1):
        print(f"  {i}. {r['geo']:<22} "
              f"{r['policy_review_priority_score']:>5.1f}  ({r['confidence_flag']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
