---
name: reconciliation-logger
description: Capture and resolve a peer's disagreement with the dashboard's ranking in a governed way. Use when a colleague, program owner, or AI Council member says "that doesn't match what I see on the ground" — to record the model's read, the human's local knowledge, what the data can and can't confirm, and the disposition (accept / override / route to review).
---

# Reconciliation Logger

## Purpose
The dashboard does the sweep; humans bring local knowledge and decide. When the two disagree, that
disagreement is **signal, not noise** — and it must be recorded honestly rather than smoothed over.
This skill turns "your algorithm ranks Manitoba high, but I know that economy is improving" into a
structured entry that states what the data supports, what it cannot, and what was decided — feeding
the deployment log and the next cycle's comparison.

## When to use
- Live in a briefing or review when a human contests a ranking, a driver, or a confidence flag.
- Afterward, to consolidate contested episodes for evaluation and the AI Council.

## Inputs to read
- `Knowledge/processed/policy_triage_panel.csv` — to confirm exactly what the panel does/doesn't say.
- The output under dispute (the ranking / briefing line).
- `CLAUDE.md` confidence bands and automatic-fails.

## Per-entry fields
```
Date:
Cycle (ref_date):
Output under dispute:        <the ranked row / driver / confidence flag being contested>
What the model said:         <the panel-grounded claim, with its number + source>
What the human says:         <the local knowledge / contextual objection, attributed to the person>
What the data CAN confirm:   <the part of the dispute the panel actually settles>
What the data CANNOT confirm:<the part outside the panel's grain/coverage — link to blind-spot-mapper>
Confidence impact:           <does this raise/lower confidence, or expose an unbacked weight?>
Disposition:                 accept model | override (human judgment) | route to human/AI Council review
Reason for disposition:
Follow-up / what would settle it: <data to download, panel rebuild, next-cycle check>
```

## Procedure
1. Restate the model's claim grounded in the panel (number + source) — no paraphrase drift.
2. Capture the human's objection in their words, attributed.
3. Split the dispute into what the panel can settle vs what is outside its coverage (province-level
   masking, NaN income/housing, un-built demographics) — do not resolve the uncertain part by
   inventing data.
4. Record the disposition and the value it protected; if overridden, the model output stays on
   record alongside the override.
5. Note what would settle it next cycle, and whether confidence should change.

## Guardrails
- **Never resolve a disagreement by inventing or imputing a value.** If the panel can't settle it,
  say so and route it.
- An override is a logged human decision, not an error to hide — keep both reads.
- Triage language only; no eligibility/benefit/need/"crisis" framing; province-level only; no city.
- Minimise/anonymise any personal information; record what taught you something, not every exchange.
