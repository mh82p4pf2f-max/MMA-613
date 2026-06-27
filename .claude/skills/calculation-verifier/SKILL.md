---
name: calculation-verifier
description: Independently re-compute the scores, confidence, and derived values and confirm an output's numbers match the authoritative panel exactly. Use before any briefing, ranking, or score is presented, circulated, or submitted, and whenever an output cites a number. This is the "Claude outputs are claims, not facts" rule made operational — distinct from source-grounding-checker, which checks that claims trace to a source, not that a number is correctly calculated.
---

# Calculation Verifier

## Purpose
Catch a wrong number before anyone acts on it. Claude's scores and rankings are **claims**, not
facts; this skill re-derives the calculated data from the raw component columns and confirms every
figure in an output matches the panel exactly. It is the numeric counterpart to
`source-grounding-checker`: that skill asks "does this claim trace to a source?"; this one asks
"is this number actually what the data computes?".

## When to use
- Before any briefing, ranking, or score is circulated, presented, or submitted.
- Whenever an output states a `policy_review_priority_score`, a driver value, a confidence figure,
  or a rate.
- After any change to `scoring.py`, the weights/anchors, or the panel.

## Inputs to read
- `Knowledge/src/verify.py` — the recompute oracle (run it; do not eyeball the math).
- `Knowledge/processed/policy_triage_panel.csv` — the authority.
- The output under check (briefing, ranking, slide, answer).

## Procedure
1. **Panel integrity first.** Run the oracle:
   ```bash
   python3 Knowledge/src/verify.py            # full panel, or --date YYYY-MM
   ```
   It recomputes every score/confidence/flag via `scoring.add_scores()` and checks: stored ==
   recomputed, `confidence_flag` matches its band, and the pending columns are still NaN. A non-zero
   exit / any FAIL means the panel itself is untrustworthy — stop and resolve before checking outputs.
2. **Per-claim check.** For each number in the output, look up the authoritative value:
   ```python
   import sys; sys.path.insert(0, "Knowledge/src"); import verify, pandas as pd
   p = pd.read_csv("Knowledge/processed/policy_triage_panel.csv")
   verify.lookup(p, "<geo>", "<ref_date>")    # returns the row's verified fields
   ```
   Confirm each asserted value equals the looked-up value exactly (allow only the panel's own
   rounding). A `found: False` means the geography is **not in the panel** — if the output cited it
   (e.g. a city), that is an automatic fail.
3. **Guard the automatic-fails.** Flag any of: a number given for a NaN column (low-income, housing);
   a `confidence_flag` that does not match the backed-weight band; a city/CMA value; an annual field
   presented as monthly; a score shown without `confidence_flag` + `score_explanation`.
4. **Verdict.** Mark each claim verified / mismatch / unverifiable, and give an overall PASS/FAIL.

## Output format
```
Panel integrity:  PASS/FAIL  (verify.py result)
Per-claim:
  <claim> → stored <value> | asserted <value> → VERIFIED / MISMATCH / UNVERIFIABLE (not in panel)
Automatic-fail guards: <none | list>
Overall: PASS — safe to rely / FAIL — do not circulate until corrected
```

## Guardrails
- **Recompute; never trust.** A number is verified only when the oracle reproduces it — not because
  it looks plausible.
- Never "fix" a mismatch by adopting the output's value; the panel (recomputed) is the authority.
- An unverifiable number (not in the panel, or in a NaN column) fails — it is never passed with a
  caveat.
- Verification is a calculation check, not a policy judgment; a PASS means the numbers are right, not
  that the ranking is approved — that still goes to human / AI Council review.
