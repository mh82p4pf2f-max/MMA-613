# AI Council Review — 2026-06-27

*MMA 616 · Stage: GOVERNANCE.* Structured review prepared by Claude (`ai-council-reviewer` skill),
applying the `governance-risk-auditor` and `source-grounding-checker` lenses and the `verify.py`
recompute oracle. **Claude does not self-approve** — this is a recommendation for the human AI
Council to ratify. Status stays *prototype* until a human records the decision in
`ai_council_decision_log.md`.

---

## 1. Review packet

- **Project summary.** Governed decision-support dashboard that flags geography × group showing
  elevated/worsening labour-market distress for human policy review. Triage only — never eligibility,
  benefit, need, or individual claims.
- **User & decision.** Social-assistance program owner / policy lead deciding *which areas to focus
  on this cycle*. Choosing/delivering interventions is out of scope.
- **Data sources.** LFS spine 14-10-0287-01 (connected). Income (11-10-0239-01, 98-10-0597-01),
  low-income (11-10-0135-01), wages (14-10-0417/0426-01), population (17-10-0005-01), CPI-Shelter
  (18-10-0004-01) — **wired but pending networked download**.
- **Panel under review.** `Knowledge/processed/policy_triage_panel.csv` — Canada + 10 provinces ×
  month, 1976-01 → 2026-05 (6,655 rows).
- **Score methodology.** 7-component 0–100 `policy_review_priority_score` with explicit weights +
  fixed anchors (`scoring.py`); confidence = share of weight backed by real data.
- **New tooling reviewed (built 2026-06-27).** `verify.py` (recompute oracle) + `calculation-verifier`
  skill; `sensitivity.py` + `weight-sensitivity-analyst`; `cycle-briefing-writer`,
  `peer-briefing-builder`, `blind-spot-mapper`, `reconciliation-logger`, `peer-challenge-prep`;
  `red-team-ranking`.

---

## 2. Data-coverage audit — "do we have every indicator needed?"

Audited against the indicator list requested for this review. **Authority = the connected LFS table
+ the panel; verified against the raw file `lfs_14100287_tidy.csv` and `verify.py`.**

| Indicator (requested) | Weight | In panel? | Backed now? | Finding |
|---|---|---|---|---|
| Unemployment rate | 0.30 | ✅ `unemployment_rate` | ✅ | Seasonally adjusted, 15+. Sound. |
| Unemployment, **12-mo** change | 0.15 | ✅ `unemp_change` | ✅ | Trailing-12-mo. Matches request. |
| Employment, **3-mo** change | 0.10 | ⚠️ `emp_change` | ✅ data, ⚠️ window | **Computed as 12-mo, not 3-mo** (`data_cleaning.py:117-125`). Discrepancy vs request. |
| Participation, **3-mo** change | 0.10 | ⚠️ `part_change` | ✅ data, ⚠️ window | **Computed as 12-mo, not 3-mo.** Same discrepancy. |
| Youth (15–24) unemployment | 0.10 | ✅ `youth_unemployment_rate` | ✅ | SA, full coverage (16,643 obs). Sound. |
| Core (25–54) unemployment | — | ❌ not built | ⚠️ available | In raw LFS, SA full coverage. **Buildable** via panel rebuild; not yet a column/row. |
| Mature (55–64) unemployment | — | ❌ not built | ⚠️ sparse SA | Only 1,513 seasonally-adjusted obs vs 16k+ for major bands. Viable only inside **55+**. |
| Seniors (65+) unemployment | — | ❌ **not in source** | ❌ | **Not published in 14-10-0287-01 at all.** Cannot be built from connected data. |
| Low-income rate | 0.15 | ✅ column, **NaN** | ❌ pending | Table 11-10-0135-01 wired, awaiting networked download. |
| Housing pressure (Shelter-CPI **proxy**) | 0.10 | ✅ column, **NaN** | ❌ pending | Table 18-10-0004-01 wired, awaiting download. Proxy, not measured affordability. |

**Backed weight today = 0.75 (medium).** The two NaN components (0.15 + 0.10) are exactly the 25%
gap; `sensitivity.py` confirms they currently have **zero effect** on any ranking.

**Age-band verdict (the requested broadening is correct *and* forced by the data):** seasonally-
adjusted coverage exists for **15–24, 25–54, and 55+** but is sparse for 55–64 and absent for 65+.
The defensible banding is **Youth (15–24) / Core (25–54) / Older workers (55+)** — three SA-clean
bands — not the four requested. Building 55–64 or 65+ as their own rows would either mix
adjusted/unadjusted data (an automatic-fail-adjacent integration risk) or invent a series the source
does not contain.

---

## 3. Criteria scorecard

| Criterion | Verdict | Evidence |
|---|---|---|
| **Accurate** | ✅ Pass | `verify.py`: all 6,655 rows recompute to stored scores; every `confidence_flag` matches its band; NaN columns unfilled. *Caveat: the "change" window labelling (§2) must be corrected.* |
| **Useful** | ✅ Pass | Produces a ranked, driver-explained, confidence-flagged shortlist for the focus decision. |
| **Clear** | ✅ Pass | `score_explanation` + `confidence_flag` on every row; governed language. |
| **Appropriate** | ✅ Pass | Triage language only; no eligibility/benefit/need framing; out-of-scope asks refused. |
| **Governed** | ✅ Pass | Reference firewall intact; Use/Avoid table; high-score escalation; prototype labelling. |
| **Safe to use** | ⚠️ Conditional | Safe **only** as a human-reviewed triage prototype. 25% of weight unbacked — not safe as a standalone decision tool. |
| **Aligned with scope** | ⚠️ Conditional | The **"economic distress"** framing overclaims while income/housing are NaN; today it is a **labour-market** distress signal. |
| **Evidence-based** | ✅ Pass | `verify.py` recompute + `sensitivity.py` robustness + source grounding to the LFS. |

---

## 4. Recommended decision

**Approve with revisions.** The architecture is sound, the calculations are independently verified,
governance is genuine (not performative), and the new verification/robustness tooling materially
strengthens trust. It is **not** approvable as a full "economic-distress" measure or for real program
decisions until the revisions below land. It continues as a **governed prototype**; outputs keep the
*"prototype — not reviewed → reviewed-with-revisions"* label and must not inform a real decision.

### Required changes
1. ✅ **DONE (2026-06-27) — pending ratification.** Reframed to labour-market distress across the
   dashboard header, `app.py`, the design mockup, and outputs; the bundled HTML export's header/status/
   title were reframed too. "Economic distress" is retained only as the project's stated *aim* once
   income/housing connect. *(Note: the bundled export's embedded data is pre-rebuild — regenerate or
   archive it.)* *(scope, governed language)*
2. ✅ **DONE (2026-06-27) — pending ratification.** Change-window discrepancy resolved: `emp_change`
   and `part_change` re-implemented as **3-mo** (unemployment stays 12-mo); documented in
   `data_cleaning.py`, `data_dictionary.md`, `CLAUDE.md`. Panel regenerated; `verify.py` re-PASSED.
   The Council still ratifies the window choice. *Open sub-item:* the emp/part **anchors** (0→3 pp)
   were calibrated for a 12-mo window and may warrant recalibration for the shorter horizon.
3. ⬜ **Download the two pending tables** (11-10-0135-01 low-income; 18-10-0004-01 CPI-Shelter) on a
   networked machine to lift backed weight 0.75 → 1.0 and confidence toward high. Until then, keep
   confidence capped and the gap flagged — never imputed. *(data sufficiency)*
4. ✅ **DONE (2026-06-27) — pending ratification.** **Core (25–54)** and **Older (55+)** unemployment
   added as seasonally-adjusted **driver columns**; **Seniors (65+) correctly NOT built** (absent from
   the source); 55–64 folded into 55+. Unscored long view at
   `policy_triage_panel_age_exploratory.csv`. Scoring age bands as their **own rows** remains a
   Council-gated scoring redesign (not done). *(coverage)*
5. ⬜ **Re-measure after revisions:** re-run the 5 known-answer cases and `verify.py`; record the
   before/after delta. (`verify.py` re-PASSED; the 5 known-answer cases not yet re-run.)

### Post-review implementation note (2026-06-27)
Revisions #2 and #4 were implemented after this review at the project owner's direction. Impact: the
top area to focus on (Newfoundland and Labrador, 2026-05) was **unchanged**, its lead widened
11.1 → 16.5 points, and the ranking became **more** robust to weight changes — evidence the
methodology change did not destabilise the call. The recommended decision is unchanged:
**Approve with revisions**, now with 2 of 5 revisions implemented and **awaiting human ratification**.

---

## 5. Decision Log entry (for human sign-off)

```
Date:            2026-06-27
What was reviewed: Scored panel + scoring methodology + new verification/robustness/briefing tooling;
                   data-coverage audit against the requested indicator list.
Main concerns:   25% of score weight unbacked (income/housing NaN); employment & participation
                 "change" computed 12-mo not the requested 3-mo; requested age bands not built and
                 65+ not available in the source; "economic distress" framing overclaims vs LFS-only data.
Required changes: (1) reframe to labour-market distress; (2) ratify/fix the change window;
                 (3) download low-income + CPI-Shelter; (4) build Core/Older(55+) bands, not 65+;
                 (5) re-measure.
Final decision:  Approve with revisions  [RECOMMENDED — awaiting human Council ratification]
Approved by:     __________ (human Council member) — NOT YET SIGNED
Status:          Prototype — reviewed, revisions required; not for real program decisions.
```
