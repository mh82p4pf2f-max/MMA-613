---
name: peer-briefing-builder
description: Build the recurring cycle-briefing an analyst presents to peers and decision-makers — the short, defensible "here's where to focus this cycle" story. Use each cycle when turning the dashboard's ranking into a briefing for colleagues. This is the repeatable working-meeting counterpart to the one-time capstone presentation-story-builder.
---

# Peer Briefing Builder

## Purpose
Turn a cycle's ranking into a tight, defensible briefing a program owner can act on or set aside —
not a pile of charts and not a one-off capstone talk. Where `presentation-story-builder` scripts the
~20-minute project showcase, this builds the **recurring** briefing arc an analyst runs every cycle
in front of peers: shortlist → drivers → confidence → robustness → blind spots → what needs human
review. The briefing leads with the decision and carries its own caveats.

## When to use
- Each cycle, when presenting the dashboard's areas-to-focus-on to colleagues, a program owner, or
  the AI Council.

## Inputs to read
- `Knowledge/processed/policy_triage_panel.csv` (the authority for every number).
- `weight-sensitivity-analyst` output (robustness) and `red-team-ranking` output (the counter-case).
- `blind-spot-mapper` output (coverage limits) and any `reconciliation-logger` entries from last cycle.
- `CLAUDE.md` (governed language, confidence bands, high-score escalation rule).

## Briefing arc (organize the briefing around this)
1. **The call.** The single top area to focus on this cycle: geography × group, score, confidence —
   stated first, in one sentence.
2. **The drivers.** The 2–3 components carrying the score, with their panel values and source table.
3. **Confidence.** What share of weight is backed, what's missing (income/housing NaN → medium), and
   what that means for acting now.
4. **Robustness.** Whether the ranking holds under weight changes; the nearest flip threshold — so
   the room knows how solid the #1 is. *(from sensitivity)*
5. **The counter-case.** The strongest reason it might be the runner-up instead, and what would
   change the call. *(from red-team)*
6. **Blind spots.** What this output does NOT cover — masking, un-built demographics, the proxy.
7. **What needs human review.** Escalation if score ≥ 70 or a trend reversal; the decision the owner
   actually makes; what is explicitly out of scope (eligibility, intervention choice).

## Output format
```
Cycle: <ref_date>
The call:        <one-sentence top area to focus on + score + confidence>
Drivers:         <2–3 drivers with values + source>
Confidence:      <backed share, what's missing, act-now implication>
Robustness:      <holds / fragile + nearest flip threshold>
Counter-case:    <runner-up's case + what would change it>
Blind spots:     <coverage limits in one or two lines>
Needs human review: <escalation + the owner's decision + out-of-scope boundary>
```

## Guardrails
- Lead with the decision; keep it short enough to act on. Depth lives in the evidence panel, not the
  briefing.
- Every number traces to the panel/source; never invent, and never import a figure from the reference
  dossier as a value.
- Triage language only — *area to focus on, requires policy review, triage signal only, warrants
  closer human review*. Never eligibility, benefit, need, "recommendation", or "crisis".
- Province-level only; no city/CMA row. The briefing is a claim for human/AI Council review, carrying
  *"prototype — not reviewed"* until the Council approves.
- Always include the high-score escalation line when the top score is ≥ 70 or a trend reversal is cited.
