"""
verify.py — Independent recomputation check for the triage panel.

WHY THIS EXISTS
---------------
The project's first rule is "Claude outputs are claims, not facts." This module
is the calculation oracle behind that rule: it re-derives every
`policy_review_priority_score`, `score_confidence`, and `confidence_flag` from the
raw component columns using the SAME `scoring.add_scores()` the dashboard uses,
then diffs the result against what is stored in the panel. If a stored number
was hand-edited, drifted, or never matched the scoring logic, this surfaces it.

It also enforces two of CLAUDE.md's automatic-fail guards directly in code:
  * the `confidence_flag` must match the backed-weight band
    (<0.55 low, 0.55–0.85 medium, ≥0.85 high), and
  * the pending columns (`low_income_rate`, `housing_pressure_proxy`) must stay
    NaN — never silently filled.

It is read-only: it never writes the panel and never invents a value. A briefing
number is verified by looking it up here, not by trusting the briefing.

USAGE
-----
    python3 Knowledge/src/verify.py                 # full panel integrity check
    python3 Knowledge/src/verify.py --date 2026-05  # restrict to one cycle
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scoring import WEIGHTS, add_scores  # noqa: E402

_SCORE_COLS = [
    "policy_review_priority_score", "score_confidence", "confidence_flag",
    "missing_value_flag", "score_explanation", "score_missing_value_flag",
]

# Columns that must stay NaN until the real StatCan tables download.
_PENDING_COLS = ["low_income_rate", "housing_pressure_proxy"]

_DEFAULT_PANEL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "processed", "policy_triage_panel.csv",
)


def _band(conf: float) -> str:
    """Confidence band per CLAUDE.md — must match scoring.py exactly."""
    return "high" if conf >= 0.85 else "medium" if conf >= 0.55 else "low"


# --------------------------------------------------------------------------- #
# Check 1 — recompute every score and diff against what's stored
# --------------------------------------------------------------------------- #
def recompute_check(panel: pd.DataFrame, score_tol: float = 0.05,
                    conf_tol: float = 0.01) -> dict:
    base = panel.drop(columns=[c for c in _SCORE_COLS if c in panel.columns])
    re = add_scores(base.copy())

    def _mismatch_rows(col, tol):
        old = panel[col].to_numpy(dtype=float)
        new = re[col].to_numpy(dtype=float)
        bad = ~np.isclose(old, new, atol=tol, equal_nan=True)
        idx = np.where(bad)[0]
        return [{"geo": panel["geo"].iloc[i], "ref_date": panel["ref_date"].iloc[i],
                 "stored": old[i], "recomputed": new[i]} for i in idx]

    flag_bad = panel["confidence_flag"].ne(re["confidence_flag"]) & ~(
        panel["confidence_flag"].isna() & re["confidence_flag"].isna())
    flag_rows = [{"geo": panel["geo"].iloc[i], "ref_date": panel["ref_date"].iloc[i],
                  "stored": panel["confidence_flag"].iloc[i],
                  "recomputed": re["confidence_flag"].iloc[i]}
                 for i in np.where(flag_bad.to_numpy())[0]]

    return {
        "rows_checked": len(panel),
        "score_mismatches": _mismatch_rows("policy_review_priority_score", score_tol),
        "confidence_mismatches": _mismatch_rows("score_confidence", conf_tol),
        "flag_mismatches": flag_rows,
    }


# --------------------------------------------------------------------------- #
# Check 2 — confidence_flag must match the backed-weight band (automatic fail)
# --------------------------------------------------------------------------- #
def band_check(panel: pd.DataFrame) -> list:
    bad = []
    for i in range(len(panel)):
        score = panel["policy_review_priority_score"].iloc[i]
        conf = panel["score_confidence"].iloc[i]
        flag = panel["confidence_flag"].iloc[i]
        if pd.isna(score):
            expected = "no inputs"
        else:
            expected = _band(float(conf))
        if flag != expected:
            bad.append({"geo": panel["geo"].iloc[i],
                        "ref_date": panel["ref_date"].iloc[i],
                        "score_confidence": conf, "flag": flag, "expected": expected})
    return bad


# --------------------------------------------------------------------------- #
# Check 3 — pending columns must stay NaN (no invented values)
# --------------------------------------------------------------------------- #
def suppression_check(panel: pd.DataFrame, cols=_PENDING_COLS) -> dict:
    return {c: int(panel[c].notna().sum()) for c in cols if c in panel.columns}


# --------------------------------------------------------------------------- #
# Per-claim lookup — verify a single briefing number against the panel
# --------------------------------------------------------------------------- #
def lookup(panel: pd.DataFrame, geo: str, ref_date: str) -> dict:
    """Return the authoritative values for one geo × cycle, for claim-checking."""
    row = panel[(panel["geo"] == geo) & (panel["ref_date"] == ref_date)]
    if row.empty:
        return {"found": False, "geo": geo, "ref_date": ref_date}
    r = row.iloc[0]
    fields = ["unemployment_rate", "youth_unemployment_rate", "unemp_change",
              "emp_change", "part_change", "low_income_rate", "housing_pressure_proxy",
              "policy_review_priority_score", "score_confidence", "confidence_flag"]
    return {"found": True, "geo": geo, "ref_date": ref_date,
            **{f: r[f] for f in fields if f in row.columns}}


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #
def summarize(recompute: dict, bands: list, suppression: dict) -> tuple[str, bool]:
    lines, ok = [], True
    s, c, f = (recompute["score_mismatches"], recompute["confidence_mismatches"],
               recompute["flag_mismatches"])
    lines.append(f"Recompute check — {recompute['rows_checked']} rows re-scored "
                 f"via scoring.add_scores():")
    for label, rows in (("score", s), ("confidence", c), ("flag", f)):
        if rows:
            ok = False
            lines.append(f"  FAIL {label}: {len(rows)} row(s) differ from stored, e.g. "
                         f"{rows[0]['geo']} {rows[0]['ref_date']} "
                         f"stored={rows[0]['stored']} recomputed={rows[0]['recomputed']}")
        else:
            lines.append(f"  PASS {label}: every stored value matches recomputation.")

    if bands:
        ok = False
        lines.append(f"  FAIL confidence band: {len(bands)} flag(s) do not match the "
                     f"backed-weight band, e.g. {bands[0]['geo']} {bands[0]['ref_date']} "
                     f"flag={bands[0]['flag']} expected={bands[0]['expected']}")
    else:
        lines.append("  PASS confidence band: every confidence_flag matches its band.")

    filled = {k: v for k, v in suppression.items() if v > 0}
    if filled:
        ok = False
        lines.append(f"  FAIL suppression: pending NaN column(s) carry values: {filled} "
                     f"— a value in a pending column is an automatic fail.")
    else:
        cols = ", ".join(suppression.keys())
        lines.append(f"  PASS suppression: pending columns ({cols}) remain NaN.")

    lines.append(f"\nResult: {'PASS — calculations verified.' if ok else 'FAIL — do not rely on the panel until resolved.'}")
    lines.append("Recomputed from component columns via scoring.add_scores(); no value invented. "
                 "Triage signal only — verification of calculated data, not a policy decision.")
    return "\n".join(lines), ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Recompute and verify the triage panel.")
    ap.add_argument("--panel", default=_DEFAULT_PANEL)
    ap.add_argument("--date", default=None, help="restrict to one ref_date (YYYY-MM)")
    args = ap.parse_args(argv)

    panel = pd.read_csv(args.panel)
    if args.date:
        panel = panel[panel["ref_date"] == args.date].reset_index(drop=True)

    recompute = recompute_check(panel)
    bands = band_check(panel)
    suppression = suppression_check(panel)
    text, ok = summarize(recompute, bands, suppression)
    print(text)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
