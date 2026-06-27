# `Knowledge/reference/` — Background context (NOT data, NOT a source)

> **READ THIS BEFORE USING ANYTHING IN THIS FOLDER.**
>
> Files here are **secondary / advocacy / policy synthesis** gathered to give the team
> *qualitative* understanding of the social-assistance landscape behind the labour-market
> signals the dashboard scores. **Nothing in this folder is a Statistics Canada WDS connected
> source, and nothing in it may be cited as a value, used as a scoring input, or treated as
> panel data.** The connected, scored data lives only in `Knowledge/raw/`, `Knowledge/processed/`,
> and is documented in `Knowledge/metadata/`.

## Hard firewall (why this folder is fenced off)

This material is **high-value reading but a high-risk data artifact**. It is saturated with two
categories of content that are **automatic fails** under `CLAUDE.md` if they reach a scored output
or briefing:

1. **City / CMA-level figures** — Edmonton's ~$7.5B social-support ecosystem, Calgary's $14M
   transit-pass shortfall, Edmonton/Calgary CMA MBM thresholds, Civida social-housing rent math,
   Edmonton's 6.9% property-tax increase. The panel is **Canada + 10 provinces only**. A city row
   in any scored output is an automatic fail (Case 1 / Automatic fails).
2. **Eligibility / benefit / need / clawback language** — AISH, Income Support, ADAP, CDB, DTC
   eligibility, benefit dollar amounts, caseloads, "deep poverty," welfare-income adequacy.
   The dashboard speaks **triage language only** and never makes eligibility, benefit, or need
   claims (Case 5 / Human-in-the-loop language table).

It also **explicitly proposes injecting its figures into `policy_review_priority_score` and
re-weighting components.** Those proposals are **rejected as scoring instructions.** Any change to
weights or anchors goes through **AI Council review** — this folder does not authorize it.

## Rules for anyone (human or Claude) using this folder

- **Pipeline isolation.** This path is never read by `statcan_api.py`, `data_cleaning.py`, or
  `scoring.py`, and must never be joined into `policy_triage_panel.csv` or any `*_clean.csv`.
- **No numbers as values.** No dollar amount, caseload, poverty rate, MBM threshold, budget
  figure, indexation rate, or program parameter from these files may be shown as a dashboard value
  or used to fill a NaN panel column. The income / low-income / housing / population columns stay
  **NaN and flagged** until the real StatCan tables are downloaded (Case 2 rule).
- **No city/CMA leakage.** Edmonton, Calgary, Civida, and any CMA-keyed figure may inform
  narrative understanding only — never a scored row, driver, or sub-provincial claim.
- **Triage language only.** When this context is referenced in an output, use governed phrases
  (*area to focus on, requires policy review, triage signal only, warrants closer human review*).
  Never echo benefit/eligibility/"crisis"/"deep poverty" framing except inside a refusal.
- **Proxy integrity.** The panel's housing field is the **CPI-Shelter proxy**; the report's
  measured rent-inflation percentages must never be presented as affordability measures or merged
  into the proxy.
- **Annual / forward-looking labelling.** Welfare incomes, transfers, deficits, OAS/EI/CDB amounts,
  and 2025–28 projections are annual or projected context — never compared to the monthly LFS panel
  or shown as current.
- **Attribution.** Cite as *"Gemini secondary synthesis, 2026-06-26"* plus the specific underlying
  source (Maytree, PBO, OAG Alberta, HelpSeeker, U Calgary SPP, Alberta budget docs, Canada.ca) —
  **never** as Statistics Canada, even where the report repeats StatCan-derived items, because they
  were not pulled through the project's WDS pipeline or verified against the source tables.
- **Prototype status unchanged.** Outputs informed by this folder remain *"prototype — not
  reviewed."* This material does not constitute AI Council review.

## What it *is* good for (governance-compliant uses)

- Explaining, in the **caveats panel**, why an LFS-only labour score *understates* true distress
  (the welfare wall + capped indexation), making the income/housing NaN gap a substantive
  analytical limitation rather than a cosmetic footnote.
- Strengthening the **housing-proxy caveat** (real rent dynamics diverge from the index).
- Adding **province-level narrative context** to a row's score rationale (e.g., Alberta's
  2025–2026 policy shifts) — tagged as policy context, never changing the score.
- Giving the **AI Council** external grounding when it reviews the low-income (0.15) and
  housing-proxy (0.10) weights and anchors.
- Cataloguing **deliberately-out-of-scope sources** (mirrors `data_sources.md` "Considered but not
  used").

## Contents

| File | What it is |
|---|---|
| `canadian_social_support_policy_context.md` | Two Gemini deep-research syntheses (federal + Alberta, then national/cross-province), merged and faithfully preserved, behind a provenance banner and a "how to use" governance firewall. |

Full per-finding audit (governance / source-grounding / utility) that produced these rules was run
2026-06-26; its conclusions are folded into the dossier's "How to use" section.
