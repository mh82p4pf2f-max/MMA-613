---
name: blind-spot-mapper
description: Produce the honest "what this data cannot carry" answer before peers demand it. Use when presenting a ranking to colleagues or the AI Council, or when asked about equity, representativeness, or "are you missing X?". Names who and what is absent from the panel — without quoting any firewalled figure.
---

# Blind-Spot Mapper

## Purpose
A credible analyst names the limits of the data before the room does. This skill produces the
structured **coverage-gap statement** for the triage panel: what it can carry, what it cannot, and
why the gaps matter for the decision. Owning the blind spots is what earns peer trust — the goal is
not to apologise for the data but to state precisely what it does and does not license.

## When to use
- Before a peer briefing, demo, or AI Council review of any ranking.
- When asked: "does this account for race / gender / within-province variation?", "is province-level
  enough?", "what about income and housing?", "are you sure the high-distress group is even in here?".

## Inputs to read
- `Knowledge/processed/policy_triage_panel.csv` — the actual grain (province × month) and which
  columns are populated vs NaN.
- `CLAUDE.md` — scope, automatic-fails, the confidence bands.
- `Knowledge/reference/canadian_social_support_policy_context.md` and its `README.md` — to explain
  *why* a missing layer matters, strictly as firewalled background (never a number).

## The blind spots to map (cover each that applies)
1. **Geographic masking.** The grain is Canada + 10 provinces. Province-level distress can mask
   within-province variation; there is **no city/CMA granularity** — Edmonton/Calgary cannot be a row.
2. **Demographics not built as rows.** The scored panel is province × month with youth carried only
   as a driver column. Gender and age groups exist in the raw LFS but are **not yet scored rows**;
   racialized groups are **not in the panel at all** — e.g. the secondary research discusses a
   markedly higher Black-youth unemployment figure, but it is **absent from the panel**, so the
   dashboard cannot speak to it. State it as a gap, do **not** quote the number.
3. **Income / low-income / housing NaN.** These columns are pending download, so ~25% of the score
   weight is unbacked and confidence sits at medium. Secondary policy research indicates these
   missing layers (the welfare wall, capped indexation) may carry much of the true distress signal —
   so the gap is **substantive, not cosmetic**.
4. **Housing is a proxy.** The housing field is shelter-CPI pressure, **not measured affordability**;
   real rent shocks for low-income households can diverge sharply from the index.
5. **Frequency mismatch.** The LFS spine is monthly; income/low-income/population context is annual
   (repeats across months by join design) — never present annual figures as monthly.

## Output format
```
What this panel CAN carry:  <grain, populated columns, what a score legitimately signals>
What it CANNOT carry:        <each relevant blind spot above, one line each>
Why the gaps matter:         <the decision consequence — what NOT to conclude from this output>
Confidence consequence:      <NaN share → medium; what would lift it>
One-line caveat for slides:  <a governed sentence the analyst can read aloud>
```

## Guardrails
- **No number-as-value.** Never quote a figure from the reference dossier (no Black-youth %, no
  rent $, no caseload, no MBM threshold) — name the gap, not the number.
- **No city/CMA** anywhere, even as illustration of a gap (naming Edmonton as out-of-scope is fine;
  attaching a figure to it is not).
- **Triage language only** — *area to focus on, warrants closer human review*. No eligibility,
  benefit, need, "deep poverty", or "crisis" framing except inside a refusal.
- Attribute any background reasoning as *"secondary policy synthesis, 2026-06-26 — not a StatCan
  source"*; it explains *why* a gap matters, it never fills one.
