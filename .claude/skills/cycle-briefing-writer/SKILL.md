---
name: cycle-briefing-writer
description: Turn the scored panel into the cycle briefing the program owner opens to decide where to focus — the ranked top area(s), drivers, confidence, source, and caveats in the governed gold-case format. Use each cycle for the everyday "where should we focus this cycle?" output. This is the base briefing that peer-briefing-builder extends for a peer audience.
---

# Cycle Briefing Writer

## Purpose
Produce the dashboard's primary output: a short, governed briefing that names the top **area to
focus on** this cycle and gives the owner enough to act on it or set it aside. This is the front
door — the everyday read, before any peer-presentation framing. It states the decision first and
carries its own evidence and caveats.

## When to use
- Each cycle, when the program owner / policy lead asks "where should we focus this cycle?".
- As the input that `peer-briefing-builder` wraps for a skeptical audience.

## Inputs to read
- `Knowledge/processed/policy_triage_panel.csv` — the authority for every number and the ranking.
- `Knowledge/metadata/data_dictionary.md` — driver labels, anchors, source tables.
- `CLAUDE.md` — governed language, confidence bands, automatic-fails, high-score escalation rule.

## Procedure
1. **Rank the cycle.** Take the latest `ref_date`, province-level rows only (Canada is a baseline,
   not a focus area), sorted by `policy_review_priority_score`.
2. **Name the call.** The top intersection — at the current build that is a **province**, with
   age/gender carried as *driver columns* (not yet their own rows). State this honestly; do not
   present a demographic as a scored row until the panel rebuild lands.
3. **Give the drivers.** The 2–3 top components from `score_explanation`, each with its panel value.
4. **State confidence.** The `confidence_flag` and the backed-weight share (income/housing NaN →
   medium ~75%); say what would lift it.
5. **Cite the source.** The LFS product id (14-10-0287-01) for labour drivers; mark any annual field.
6. **Attach caveats.** Province-level only; housing is a proxy; triage signal, not eligibility.
7. **Escalate if needed.** If the top score is ≥ 70 or the explanation cites a trend reversal
   (unemployment rising after 6+ months of decline), append the escalation line.
8. **Verify before relying.** Run the `calculation-verifier` skill on the briefing's numbers; do not
   circulate figures that have not been recomputed against the panel.

## Output format (gold-case)
```
[Group/area], [Province] — policy_review_priority_score [N] ([flag]);
  top drivers: [driver1 (value)], [driver2 (value)];
  confidence [flag] ([X]% of weight backed by data); source LFS 14-10-0287-01.
Triage signal only — not an eligibility or benefit decision.
[If ≥70 or reversal:] This output warrants direct human review before any program action.
```

## Guardrails
- Every number comes from the panel — never invent, never fill a NaN column, never round-trip a
  figure from the reference dossier.
- Governed language only — *area to focus on, requires policy review, triage signal only, warrants
  closer human review*. Never eligibility, benefit, need, "recommendation", or "crisis".
- Province-level only; **no city/CMA row** (automatic fail). If asked for a demographic-specific
  row, state: "the current panel scores province × month only; [group] breakdowns require a panel
  rebuild — this reflects province-level distress."
- The briefing is a claim for human / AI Council review and carries *"prototype — not reviewed"*
  until the Council approves.
