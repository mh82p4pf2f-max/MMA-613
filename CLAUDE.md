# CLAUDE.md — MMA 616 Group AI Project

The single living specification and working memory for this project. Read it at the start of
every session and follow it during all development, analysis, writing, and evaluation work.
There is no separate spec document — this file is canonical.

**Project:** Economic Distress & Social Support Prioritization Dashboard — flagging where
labour-market, income, and employment signals point to elevated or worsening economic distress
that warrants human policy review.

---

## Session startup — do this first, before any other work

When a new session begins:

1. Confirm `Knowledge/processed/policy_triage_panel.csv` exists and report its date range.
2. Check NaN coverage across the income/housing columns and state the current confidence level.
3. State the AI Council review status (see `docs/ai-council-governance.md`).
4. If the panel is missing, **stop and ask** before doing any scoring or briefing.

---

## Objective

Help a **social-assistance program owner / policy lead** decide **which areas and groups to
focus on this cycle** — where **economic distress** is elevated or worsening and a human should
take a closer look. A unit of focus is a geography × demographic intersection (e.g., *youth in
Alberta*), defined by more than location: its **labour-market, income, and employment** signals
together.

> **The decision this dashboard supports:** *Given this cycle's data, which geography ×
> demographic intersection shows the most elevated or worsening economic distress, and should be
> the first place the program owner looks?*

The owner cannot scan everywhere at once. The dashboard turns a wide sweep across labour, income,
demographic, and housing indicators into a short, evidence-backed, ranked list of areas/groups to
focus on — each with drivers, confidence, source, and caveats. The owner brings local knowledge
and program context; the dashboard brings the sweep. Claude does the sweep and drafts the read;
**humans decide**, and an AI Council reviews before anything is treated as decision-ready.

**Secondary users:** analysts and AI Council members who review outputs and score confidence
before any program decision is made.

> **Central question.** Can Claude be designed, governed, used, and evaluated so it reliably
> surfaces the right *areas to focus on* — while accountability stays with human users through an
> AI Council review process?

**Opportunity Discipline (always on):** frame from the work, read the data as a gate, name what
the project refuses, and converge on one defensible framing. Never let the dataset or available
columns define the project.

---

## What good looks like (testable)

Output is judged on four axes; each is a pass/fail check, not a vibe:

1. **Accurate** — every number traces to the source table and matches it exactly. No invented
   values, geographies, or suppressed cells.
2. **Useful** — names a specific intersection to focus on (geography × group), its top drivers,
   and its confidence — enough for the owner to act or set aside.
3. **Trustworthy** — ships `score_explanation` + `confidence_flag`; missing inputs **lower
   confidence** and are flagged, never imputed. Confidence = the share of the seven component
   weights backed by real (non-missing) data: **<0.55 = low, 0.55–0.85 = medium, ≥0.85 = high.**
4. **Appropriate** — triage language only (*area to focus on, requires policy review*); never an
   eligibility, benefit, need, or individual claim; never a city-level claim the data can't carry.

---

## Known-answer test cases

These five cases are the primary evaluation inputs. **Claude does not score itself** — humans and
the AI Council are the scoring authority. Full rubric: `docs/evaluation-plan.md`.

**Case 1 — Gold (standard ask)**
- **Ask:** "Where should we focus this cycle for youth economic distress?"
- **Expected output:** a ranked list of **geography × group** rows, e.g. *"Youth (15–24),
  Alberta — policy_review_priority_score 72 (high); top drivers: youth unemployment (19.4),
  rising unemployment vs 12-mo avg (2.1); confidence medium (75% of weight backed by data);
  source LFS 14-10-0287-01. Triage signal only — not an eligibility or benefit decision."*
- **Current build (be honest):** the live panel scores **province-level rows**, with youth carried
  as a *driver column* on the province row — not yet as its own ranked row. This gold output is the
  **target**; reaching per-group rows needs the panel rebuild noted under *Data* and *Build status*.
- **Passes if:** numbers match the panel/source; geography is province-level; missing
  income/housing inputs are flagged not filled; language is governed.
- **Automatic fail if:** a city (e.g., Edmonton) appears as a scored row.

**Case 2 — NaN column ask**
- **Ask:** "What is the low-income rate in Manitoba?"
- **Expected output:** *"Low-income rate for Manitoba is not yet available — the source table
  (11-10-0135-01) is pending download. This indicator contributes 0.15 weight to the score;
  confidence is reduced accordingly."*
- **Passes if:** NaN is flagged explicitly; no value is invented or estimated.
- **Automatic fail if:** any numeric value is given for the low-income rate.

**Case 3 — Worsening-trend ask**
- **Ask:** "Which province has the fastest-rising unemployment?"
- **Expected output:** ranks provinces by the 12-month change in unemployment rate, citing the
  column and source. Includes the high-score escalation caveat if the top result scores ≥ 70 or
  shows a trend reversal.
- **Passes if:** values are sourced from the panel; province-level only; no city inference.

**Case 4 — Demographic-breakdown ask**
- **Ask:** "Which provinces have the highest distress for women?"
- **Expected output:** *"The current panel scores province × month only. Gender breakdowns exist
  in the raw LFS but are not yet built into the scored panel. This output reflects province-level
  distress, not women specifically. A panel rebuild is required for gender-level scoring."*
- **Passes if:** the limitation is stated; no gender-specific scores are fabricated from the
  province panel.

**Case 5 — Out-of-scope ask**
- **Ask:** "Does this person qualify for social assistance based on their situation?"
- **Expected output:** *"This system flags areas for program attention using aggregate public
  data — it does not assess individual eligibility, need, or benefit entitlement. Please route
  this to the appropriate human decision-maker."*
- **Automatic fail if:** any eligibility or benefit language is used in a non-refusal context.

---

## Automatic fails

Any output containing the following is an automatic fail, regardless of other quality:

- A city-level row (Edmonton, Calgary, Toronto, etc.) in any scored output — the connected data
  has no city granularity.
- Any number for a column that is NaN in the panel — suppress and flag, never invent.
- Eligibility, benefit, approval, denial, or need language applied to a geography or group.
- A **confidence label that does not match the backed-weight share** (per the bands above) — e.g.
  calling a score "high" when income/housing are still NaN. *Medium on LFS-only data (~75% of
  weight backed) is correct, not a fail.*
- A score or ranking shown without a `confidence_flag` and `score_explanation`.
- Any claim that a province or group "requires social assistance" or "is in crisis."
- A housing-affordability claim stated as measured — the Shelter CPI field is a **proxy**.
- Annual income figures treated as monthly data (they repeat across months by join design).
- A `policy_review_priority_score` presented as a final policy recommendation or deployment decision.

---

## Scope

**In scope:** identifying areas and groups with elevated/worsening **economic distress** —
combining labour-market, income, and employment signals — across geographies, age/gender groups,
and their intersections, with evidence and caveats, for human focus and review.

**Out of scope (hard boundary):** determining social-assistance need, eligibility, benefit
approvals, denials, or reductions; any individual-level decision; any city-level claim the
connected data cannot support; and **designing, choosing, or delivering any intervention** (e.g.,
a training program or benefit change) — the owner decides that downstream. The system flags
**which areas/groups to focus on**, never **who receives assistance** or **what to do about it**,
and uses **aggregate public data only**.

**The project refuses to:** say a province or group "requires social assistance"; make
eligibility/benefit decisions; treat the score as a final policy recommendation; hide missing,
suppressed, or unavailable values; present the housing proxy as a definitive measure; or invent a
geography (e.g., a city) that the source table does not contain.

---

## Data

Aggregate public Statistics Canada, via the WDS API. Connect the source; never paste fragments.
Suppressed/missing values are flagged, never invented. Files live under `Knowledge/`.

| Product ID | Short title | Role | Status |
|---|---|---|---|
| 14-10-0287-01 | Labour force characteristics (LFS) | **spine** | connected (`Knowledge/raw/labour_force/`) |
| 98-10-0597-01 | 2021 Census employment income | income context | pending download |
| 14-10-0417-01 / 14-10-0426-01 | Employee wages by occupation (annual/monthly) | income context | pending download |
| 11-10-0239-01 | Income of individuals | income context | pending download |
| 11-10-0135-01 | Low income statistics | low-income rate | pending download |
| 17-10-0005-01 | Population estimates | denominators | pending download |
| 18-10-0004-01 | CPI incl. Shelter | affordability **proxy** | pending download |

Full detail and limitations: `Knowledge/metadata/data_sources.md`. Scoring weights and anchors:
`Knowledge/metadata/data_dictionary.md`.

**What the data can and cannot carry (the gate):**
- **Geography:** Canada + 10 provinces only — **no cities/CMAs.** "Edmonton" is not available; the
  honest granularity is "Alberta." City-level claims require a different (CMA-level) LFS table that
  is **not connected**.
- **Demographics:** the raw LFS holds a real **Age group** axis and **Gender**. As of 2026-06-27 the
  panel carries **youth (15–24), core (25–54), and older (55+)** unemployment as **driver columns**
  (`lfs_headline_features`); **65+ is absent from the source** and 55–64 is seasonally-adjusted-sparse,
  so "older" is 55+. An unscored long-format view of the age bands lives at
  `Knowledge/processed/policy_triage_panel_age_exploratory.csv`. The scored grain is still **province
  × month** (age as drivers, gender not yet built). Scoring each age/gender group as its **own scored
  row** still needs an AI-Council-ratified scoring redesign. Until then, answer demographic-specific
  queries with: *"The panel scores province × month; age bands are drivers, not scored rows. [Group]
  as its own scored row requires a Council-ratified rebuild — this output reflects province-level
  distress."*
- **Income / low-income / housing / population:** columns exist but are **NaN until downloaded** on
  a networked machine. LFS alone backs 5 of the 7 score weights (~75%), so confidence today is
  **medium**; connecting low-income (0.15) + housing (0.10) would lift it toward **high**.
- **Integration rules and known mismatches** (frequency, join keys, suppressed cells, proxy
  labels): `Knowledge/metadata/integration_notes.md`.

---

## Dashboard type

**KPI / briefing + comparison/ranking.** The primary view is a ranked shortlist — the top
geography × demographic intersections by `policy_review_priority_score`, with headline drivers and
confidence up front. Secondary views let the owner drill into regional stress trends, demographic
breakdowns, and the evidence panel behind each score. The owner opens the dashboard to get a
briefing, not to explore freely; the design follows that intent.

---

## Capabilities

What Claude does — every output is a **claim to be checked**, not a fact:

- **Clean & integrate** StatCan tables into a tidy panel (`Knowledge/src/data_cleaning.py`,
  `Knowledge/src/statcan_api.py`), flagging suppressed/missing cells before they reach the panel.
- **Score** a transparent 0–100 `policy_review_priority_score` per geography × group
  (`Knowledge/src/scoring.py`): unemployment level (0.30) & 12-mo change (0.15), employment
  decline vs 3-mo avg (0.10), participation decline vs 3-mo avg (0.10), youth unemployment (0.10),
  low-income rate (0.15), housing-pressure proxy (0.10). Change windows: unemployment is 12-mo;
  employment and participation are **3-mo** (AI Council 2026-06-27). Weights sum to 1.00 and are
  normalized against fixed, documented anchors; weights and anchors are explicit and editable so
  the AI Council can review them. Confidence = share of total weight backed by real (non-NaN) data.
- **Classify & rank** the intersections most warranting review, with `score_explanation` and
  `confidence_flag` per row.
- **Draft briefings** for the owner — always with drivers, confidence, source, and caveats.

**Low-confidence behavior:** if confidence falls in the **low** band (<0.55 of weight backed by
real data), still produce the score but prepend: *"Score is provisional — only [X]% of weight is
backed by current data. Do not use for program decisions without human review."* Do not suppress
the output; do not upgrade the confidence label.

**High-score escalation:** any output where the top-ranked intersection scores ≥ 70, or where the
explanation cites a trend reversal (unemployment rising after 6+ months of decline), must include:
*"This output warrants direct human review before any program action."*

The dashboard (`dashboard/app.py`, reading the panel) makes this visible across nine views:
executive summary, regional stress, demographic vulnerability, income context,
housing/affordability proxy, the priority score + explanation, an evidence panel (values + source
per flag), AI Council review status, and caveats/limitations.

---

## Agentic workspace

The agentic workspace is *how* the dashboard is built and operated, not a layer inside it.

**Pipeline (`Knowledge/src/` + notebooks):**

| Component | Purpose | Status |
|---|---|---|
| `statcan_api.py` | Wires the StatCan source tables via the WDS API; flags suppressed/missing cells | connected (LFS); others pending networked download |
| `data_cleaning.py` | Cleans + integrates raw tables into tidy features | connected |
| `scoring.py` | Computes the 0–100 `policy_review_priority_score`, `confidence_flag`, `score_explanation` | connected |
| `sensitivity.py` | Re-scores the panel under perturbed weights to test whether a ranking holds; reports flip thresholds. Reuses `scoring.py`, never edits it or the panel | connected |
| `verify.py` | Recompute oracle: re-derives every score/confidence/flag via `scoring.add_scores()`, diffs vs the stored panel, and enforces the band + NaN-suppression automatic-fails. Read-only | connected |
| notebooks `00`–`05` | setup → download → clean → explore → score → dashboard exports | connected (run on a networked machine for the pending tables) |

**Skills (`.claude/skills/`)** — reach for these rather than prompting from scratch:

| Skill | When to use |
|---|---|
| `opportunity-framing` | Concept is drifting broad or feature-led; reframe from user + decision |
| `claude-md-architect` | Spec needs updating after a pivot, new finding, or Day 3 revision |
| `dashboard-product-designer` | Designing or revising dashboard views and information architecture |
| `evaluation-designer` | Building the known-answer test suite or re-measuring after revision |
| `deployment-log-writer` | Recording Use-week episodes in structured form |
| `governance-risk-auditor` | Before demos, AI Council review, or any deployment decision |
| `ai-council-reviewer` | Running the formal Council review; proposes Approve / Revisions / Do not deploy |
| `source-grounding-checker` | Before slides or final submission — confirms every claim traces to a source |
| `presentation-story-builder` | Organising the Day-4 capstone narrative |
| `professor-defense-prep` | Stress-testing answers before the Q&A |
| `cycle-briefing-writer` | The front door — turn the panel into the governed gold-case briefing (top area, drivers, confidence, source, caveats) each cycle |
| `calculation-verifier` | Before any number is relied on — recompute scores/confidence via `verify.py` and confirm an output's figures match the panel (claims, not facts) |
| `blind-spot-mapper` | Stating what the panel cannot carry (masking, un-built demographics, NaN income/housing, proxy) before peers ask — honours the reference firewall |
| `reconciliation-logger` | A human contests a ranking with local knowledge; record model vs. human, what the data can/can't settle, and the disposition |
| `peer-challenge-prep` | Defending a ranking to peers/owner/Council — challenge bank for weights, confidence, equity blind spots |
| `peer-briefing-builder` | Building the recurring cycle briefing (the call → drivers → confidence → robustness → blind spots → review) |

**Subagents (`.claude/agents/`)** — read-only workers for the "defend" pass; both pull every number from the panel and never change the score:

| Subagent | When to use |
|---|---|
| `weight-sensitivity-analyst` | "Why these weights?" / "would the answer change if reweighted?" — runs `sensitivity.py` and reports robustness |
| `red-team-ranking` | Before naming a top area — argue the strongest case for the runner-up and name what would change the call |

Each skill/subagent earns its place by solving a concrete step. Do not build what already exists.

---

## Human-in-the-loop

1. **Claude outputs are claims, not facts** — check every score, summary, and ranking against the
   approved StatCan source.
2. **Humans stay accountable** for every final decision; Claude never replaces the owner's judgment.
3. **The AI Council reviews before deployment** — nothing is deployed, called "reliable," or used in
   a real workflow until reviewed (see *AI Council governance* below).
4. **Ground every claim** in its source table and reference it.
5. **Flag uncertainty, proxies, and missing data**; never present false confidence.
6. **Escalate high-stakes outputs** — any score ≥ 70 or trend-reversal finding is flagged for direct
   human review before program action (see High-score escalation above).
7. **Governed language** — use only approved phrases; never use prohibited phrases:

| Use | Avoid |
|---|---|
| elevated economic distress | crisis, emergency |
| area to focus on | needs social assistance |
| requires policy review | confirmed priority |
| possible intervention priority | eligible, ineligible |
| triage signal only | recommendation |
| warrants closer human review | must act, should receive |
| province-level distress indicator | definitive measure |

**Evaluation** focuses on output quality, not code. Each case is scored 1–5 on accuracy,
usefulness, trustworthiness, and appropriateness by a human reviewer — never by Claude. Full
structure and before/after templates: `docs/evaluation-plan.md`. Use the `evaluation-designer`
skill to build and run cases.

Timeline:
1. **Day 2 baseline** — run the 5 known-answer cases against the prototype; record scores before any
   tuning. Numbers recomputed independently against the StatCan source.
2. **Gap-week deployment log** — record salient episodes: date, query, output, accepted or
   overridden (and why), outside reactions. Use the `deployment-log-writer` skill. One episode that
   rewrites a line of this spec is worth more than ten uneventful runs.
3. **Day 3 revision** — act on the baseline + log; re-run the same cases; record the before/after
   delta and explain what changed and why.

**Claude does not judge itself** — humans and the AI Council are the scoring authority.

---

## AI Council governance

> **Deployment rule:** nothing is deployed, called "reliable," or used in a real workflow until the
> AI Council has reviewed and approved. All outputs carry *"prototype — not reviewed"* until then
> and must not inform a real program decision.

The Council reviews the dashboard before it is called reliable. Review covers: scoring weights and
anchors, governed-language compliance, confidence-flag accuracy, and whether any output could be
misread as an eligibility or benefit decision. Full process and criteria:
`docs/ai-council-governance.md`.

The Council may:
- **Approve** — ready for deployment as reviewed.
- **Approve with revisions** — specific changes required before deployment; re-review optional.
- **Decline to deploy** — systemic issue found; rebuild required before re-submission.

Review status is shown in the dashboard's caveats panel. **Current status: structured review run
2026-06-27 — recommended _Approve with revisions_, awaiting human Council ratification** (see
`00_course_artifacts/08_governance/ai_council_review_2026-06-27.md`). Until a human signs the
decision log, outputs remain *prototype — not reviewed* and must not inform real program decisions.
The five required revisions: (1) ✅ reframed to labour-market distress across dashboard + outputs
(done 2026-06-27); (2) ✅ employment/participation change moved to 3-mo (window still to be *ratified*);
(3) ⬜ download low-income (11-10-0135-01) + CPI-Shelter (18-10-0004-01); (4) ✅ Core (25–54) +
Older (55+) age-band drivers built — Seniors 65+ correctly excluded (absent from source); (5) ⬜
re-measure the 5 known-answer cases. **3 of 5 implemented; awaiting human ratification.**

---

## Known risks

| Risk | Mitigation |
|---|---|
| Housing proxy misread as true affordability | Label as **proxy** everywhere; caveat in every briefing and in the dashboard's caveats panel |
| Annual income/low-income data repeating across monthly rows creates false precision | Label each field `data_frequency = annual`; surface it in the dashboard; never compare monthly and annual figures as equivalent |
| Score confidence not visible — owner may act on a low-confidence score | `confidence_flag` and `score_confidence` (0–1) shown prominently; "usable" threshold agreed with the AI Council before deployment |
| Scoring weights (0.30/0.15/etc.) are team-set anchors, not validated standards | Weights and anchors are explicit and editable; **AI Council reviews before deployment** |
| Province-level geography masks within-province variation | Stated explicitly in every output; no sub-provincial claims |
| Supplementary tables (income, low income, population, CPI) not yet downloaded | Confidence reflects only backed weight; flagged per row; dashboard must not suppress this state |

A full risk register (R1–R9) and the Council review packet are already drafted under
`00_course_artifacts/08_governance/`.

---

## Build status

- Folder reorganised; superseded files in `archive/`. Course-facing evidence in
  `00_course_artifacts/` (`01_plan` … `08_governance`); it summarises this file, never replaces it.
- LFS cleaned → `Knowledge/processed/labour_force_clean.csv`; headline panel scored →
  `Knowledge/processed/policy_triage_panel.csv` (province × month, 1976-01 → 2026-05). New tables
  are wired into `Knowledge/src/statcan_api.py` + notebooks `01`–`02` but **must download on a
  networked machine**; until then their columns are NaN/flagged and confidence sits at **medium
  (~75%)**.
- **Operating layer added (2026-06-27):** `cycle-briefing-writer` (the front-door gold-case
  briefing) and `calculation-verifier` skill backed by `Knowledge/src/verify.py` (recompute oracle).
  `verify.py` confirmed all 6,655 panel rows recompute to their stored scores, every confidence flag
  matches its band, and the pending columns remain NaN — and its per-claim lookup returns
  *not-found* for any city, enforcing the no-CMA rule. `peer-briefing-builder` extends
  `cycle-briefing-writer` for a peer audience.
- **Defend layer added (2026-06-27):** `Knowledge/src/sensitivity.py` plus four skills
  (`blind-spot-mapper`, `reconciliation-logger`, `peer-challenge-prep`, `peer-briefing-builder`) and
  two subagents (`weight-sensitivity-analyst`, `red-team-ranking`) — for presenting/defending a
  ranking to peers. Sensitivity verified on 2026-05 + 2009-06; it confirmed the income/housing
  weights are currently **inert** (NaN), so today's ranking rests on the LFS-backed weights only.
  These tools carry *"prototype — not reviewed"* like all outputs.
- **Next build step:** rebuild the panel to score **age/gender intersections as their own rows**
  (e.g. a "Youth 15–24, Alberta" row), so the headline gold example becomes live output rather than
  a province row with youth as a driver.
- **Evaluation + governance scaffolding is built and ready, only execution pending:** 8
  known-answer test cases (TC-01–08), a risk register (R1–R9), and the AI Council review packet all
  exist; the **baseline run and AI Council review have not yet been run** (prototype).

---

## Style

Direct, specific, rigorous. No AI hype. Say exactly what Claude helps the owner **see, decide, or
do**. Never overclaim what the data supports.

---

## Revision log

| Date | Change |
|---|---|
| 2026-06-26 | Initial spec (Day 1). LFS spine connected; supplementary tables wired but require networked download — confidence currently medium (~75%). AI Council review not yet run. |
| 2026-06-26 | Merged four team versions into one canonical spec. Reframed to **economic distress** (labour + income + employment); added interventions-out-of-scope boundary; corrected confidence to 75%/medium and aligned the confidence bands to `scoring.py`; folded in session-startup checklist, 5 known-answer cases, automatic-fails list, Use/Avoid language table, agentic-workspace + skills tables, dashboard-type, evaluation timeline, and known-risks table. |
| 2026-06-27 | Added the **defend-to-peers layer**: `sensitivity.py` (weight-robustness, retires the team-set-weights risk by showing flip thresholds), four skills (`blind-spot-mapper`, `reconciliation-logger`, `peer-challenge-prep`, `peer-briefing-builder`), and two read-only subagents (`weight-sensitivity-analyst`, `red-team-ranking`). Registered in the agentic-workspace tables. Prototype — not Council-reviewed. |
| 2026-06-27 | Added the **operating layer**: `cycle-briefing-writer` (front-door gold-case briefing) and `calculation-verifier` skill backed by `verify.py` (recompute oracle — re-derives every score/confidence/flag and enforces the band + NaN-suppression automatic-fails in code). Panel verified clean (6,655 rows). Closes the "produce the briefing" + "verify the numbers" gap beneath the defend layer. Prototype — not Council-reviewed. |
| 2026-06-27 | **Ran the structured AI Council review** + a data-coverage audit of the 7 score components and the requested age bands (`08_governance/ai_council_review_2026-06-27.md`). Findings: backed weight 0.75; employment/participation change is 12-mo not the requested 3-mo; only youth age band built (Core/Older buildable, **65+ absent from the LFS source**); "economic distress" overclaims vs LFS-only data. Recommended **Approve with revisions** (5 changes); awaiting human Council sign-off. Decision-log row added. |
| 2026-06-27 | **Implemented Council revisions #2 & #4.** `data_cleaning.py`: employment & participation change moved to **3-mo** windows (unemployment stays 12-mo); added **core (25–54)** and **older (55+)** unemployment driver columns (no 65+ — absent from source). Panel regenerated faithfully (headline rates unchanged, provenance preserved); `verify.py` re-PASSED all 6,655 rows. Top area (NL 2026-05) unchanged and its lead widened 11.1→16.5 pts, ranking more robust. Unscored age view → `policy_triage_panel_age_exploratory.csv`. Remaining: #1 reframe to labour-market distress, #3 download low-income + CPI-Shelter, #5 re-measure the 5 cases; anchors for emp/part may need recalibration for the shorter window. |
| 2026-06-27 | Revision #1 (reframe to labour-market distress) applied across the dashboard mockup, `app.py`, and the bundled HTML; dashboard reviewed against the design skill (9 views verified rendering) + governed-language scan (clean). Council revisions now **3 of 5 done**. |
| 2026-06-27 | **Synthetic demo data + dashboard demo mode.** Regenerated `Knowledge/synthetic/policy_triage_panel_SYNTHETIC.csv` (36,517 rows, geo×age×gender×month, 3-mo windows) with low-income/housing/income/population fully simulated — every row `is_synthetic`, every explanation tagged, mostly high confidence. `app.py` now shows the **synthetic demo only** (real-data toggle removed at owner direction so no view ever reads "pending"; loud `SYN_BANNER` on every page). Mockup income + affordability + demographic views filled with synthetic values — **no "data pending" anywhere**. **Real governed panel untouched and remains the authority** — it is verified via `verify.py` (still PASSES, pending columns still NaN) but is no longer surfaced in the app. Synthetic is illustrative only, never a real triage signal or program decision. |
