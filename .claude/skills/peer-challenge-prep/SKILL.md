---
name: peer-challenge-prep
description: Prepare an analyst to defend a dashboard-derived ranking in front of peers and decision-makers. Use before presenting a cycle's areas-to-focus-on to colleagues or the AI Council. Generates the hardest working-analyst challenges — weights, confidence, equity blind spots, province masking — each with a grounded, governed answer.
---

# Peer Challenge Prep

## Purpose
Anticipate the sharpest questions a room of fellow analysts and program owners will ask about a
ranking, and draft a strong, concise, evidence-backed answer to each — so the analyst is never
caught flat. This is the **working-briefing** counterpart to `professor-defense-prep`: the audience
is peers acting on the output, not an examiner grading the project, so it adds the challenges that
version omits (weight defensibility, confidence math, equity/coverage blind spots).

## When to use
- Before presenting a cycle's shortlist to peers, a program owner, or the AI Council.

## Inputs to read
- `Knowledge/processed/policy_triage_panel.csv` and the proposed shortlist/briefing.
- Output of the `weight-sensitivity-analyst` and `red-team-ranking` subagents (run them first).
- The `blind-spot-mapper` skill output.
- `CLAUDE.md` (scope, confidence bands, automatic-fails); `Knowledge/metadata/data_dictionary.md`.

## Question bank (generate the sharp version of each, then answer)
**Weights & method**
- Why these weights (0.30 unemployment, 0.15 ...)? They look arbitrary.
- Would the top of the list change if you weighted differently? *(answer from sensitivity output)*
- One driver is carrying this rank — isn't the ranking really just unemployment level?

**Confidence & data**
- You say "medium confidence" — what exactly is missing, and why act on it?
- Income and housing are NaN — isn't a quarter of your score made up?
- Annual vs monthly data — are you comparing like with like?

**Equity & coverage**
- Does this account for race, gender, or within-province variation? *(answer from blind-spot-mapper)*
- Could the most distressed group be invisible to this panel entirely?
- Province-level only — why is "Alberta" an honest answer when the need is local?

**Decision & accountability**
- Why this province and not the runner-up? *(answer from red-team-ranking)*
- What happens if a program owner's local knowledge contradicts this? *(reconciliation-logger)*
- Is this a recommendation? What are you actually asking us to do with it?

## Output format
```
Q: <sharp peer question>
A: <concise 3–5 sentence answer, grounded in a panel number / sensitivity result / spec line>
Evidence cited:
Gap to close (if any):
```

## Guardrails
- Answers cite real evidence (a panel value, a sensitivity threshold, a spec line) — never assertion.
- Be honest about limits: "here's the boundary and why" beats overclaiming. A question you can't
  answer is a gap to close before the briefing, not something to bluff.
- Triage language only — *area to focus on, warrants closer human review*; never eligibility,
  benefit, need, "recommendation", or "crisis". Province-level only; no city/CMA.
- Frame every answer as a claim for human/AI Council review, not a settled fact.
