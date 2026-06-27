# Audit — `Knowledge/processed/policy_triage_panel.csv`

*MMA 616 — Labour Market Stress & Social Support Prioritization Dashboard.*
Audit run 2026-06-26 against the live file the dashboard reads. Every number below was
computed directly from the file, not assumed. **Governance note:** this is a *policy review
priority* dataset — a triage signal for human review. It is **not** a social-assistance need,
eligibility, or benefit dataset, and nothing here should be presented as such.

---

## 1. Dataset summary (structure)

| Property | Finding |
|---|---|
| Rows | **6,655** |
| Columns | **20** |
| Date range | **1976-01 → 2026-05** (monthly) |
| Geographies | **11** — Canada + 10 provinces |
| Territories | **Absent** (Yukon, NWT, Nunavut not in LFS 14-10-0287; scope limit, not an error) |
| Duplicate rows (full) | **0** |
| Duplicate `geo + ref_date` | **0** |
| `geo + ref_date` unique key? | **Yes** — uniquely identifies every row |
| Data types | Correct: `geo/ref_date/confidence_flag/score_explanation` = object/text; `year/month` = int; all rates/score/confidence = float; `missing_value_flag` = bool |

### Missing values by column

| Column | Missing | Note |
|---|---:|---|
| geo, ref_date, year, month | 0 | complete |
| employment_rate, participation_rate, unemployment_rate, youth_unemployment_rate | 0 | complete monthly LFS |
| unemp_change, emp_change, part_change | **66** | each geo's first 6 months (1976-01→1976-06); expected artifact of the trailing-12-month window — **not** corrupt |
| **low_income_rate** | **6,655 (100%)** | column entirely empty |
| **housing_pressure_proxy** | **6,655 (100%)** | column entirely empty |
| **income_value** | **6,655 (100%)** | column entirely empty |
| **population** | **6,655 (100%)** | column entirely empty |
| policy_review_priority_score, score_confidence, confidence_flag, missing_value_flag, score_explanation | 0 | complete |

### Demographic detail lost during integration (material finding)

The panel was collapsed to the **Total-Gender, 15+ headline** slice, plus youth (15–24)
unemployment as a single derived column. The cleaned source (`labour_force_clean.csv`) still
contains granularity that **did not survive into the panel**:

- **Gender:** `Men+`, `Women+`, `Total - Gender` → panel keeps only the total.
- **Age groups:** `15–19, 20–24, 25–54, 55–64, 55+, 15–64, 25+, 15+` → panel keeps only `15+`
  and `15–24` (the latter only as `youth_unemployment_rate`).

Consequence: the dashboard's "Demographic vulnerability" view can currently show only youth
vs overall. Gender and detailed-age breakdowns are recoverable from the cleaned LFS but are
not in this panel.

---

## 2. Time alignment

| Field | Native frequency | In this file |
|---|---|---|
| employment_rate, participation_rate, unemployment_rate, youth_unemployment_rate | **Monthly** (LFS) | populated |
| unemp_change, emp_change, part_change | **Monthly** (derived: vs trailing-12-mo avg) | populated (first 6 mo/geo NaN) |
| low_income_rate | **Annual** (CIS 11-10-0135) | empty |
| income_value | **Annual** (income 11-10-0239 / wages 14-10-0417 / Census 98-10-0597) | empty |
| population | **Annual** (17-10-0005, July-1 estimate) | empty |
| housing_pressure_proxy | **Monthly** (CPI/Shelter 18-10-0004 YoY) | empty |
| policy_review_priority_score, score_confidence, confidence_flag, missing_value_flag, score_explanation | **Monthly** (derived) | populated |

**Frequency-mismatch status:** there is currently **no hidden mismatch in the data**, because
every annual field is empty — no annual values have been joined to the monthly spine yet. The
*intended* integration (documented in `integration_notes.md`) joins annual sources to the
monthly spine **by `year`**, repeating one annual value across that year's 12 months and
labelling it annual context. That mismatch must be surfaced on the dashboard the moment those
columns are populated — it is not present today only because the columns are blank.

**Recommended fields (not yet present):** add `labour_force_data_frequency`,
`income_data_frequency`, `housing_data_frequency`, `population_data_frequency` so each row
self-documents the frequency of its inputs. *(Added in this iteration — see §"Fixes applied".)*

---

## 3. Source traceability

**The panel contains no source fields.** Source metadata is **not lost**, however — it
survives upstream in three places:

- `Knowledge/processed/labour_force_clean.csv` — carries `source_product_id`,
  `source_table_title`, `source_category`, `retrieval_date`.
- `Knowledge/metadata/data_sources.md` — full product IDs, URLs, frequencies, limitations.
- `Knowledge/src/statcan_api.py` — the configured table list with PIDs and titles.

For in-class defensibility the panel itself should carry source pointers. **Recommended
fields:** `source_product_id_lfs`, `source_product_id_income`, `source_product_id_housing`,
`source_product_id_population`, `source_table_lfs`, `source_table_income`,
`source_table_housing`, `source_table_population`. *(Added in this iteration — see §"Fixes
applied".)* Note the raw provenance `*.source.json` files do **not** exist yet because the WDS
downloads have not been run on a networked machine.

---

## 4. Policy review score validation

**This is a `policy_review_priority_score` — a triage signal only. It is NOT a social
assistance need score and never an eligibility or benefit decision.**

- **Variables used (currently active):** unemployment rate, unemployment change vs 12-mo
  average, employment-rate decline, participation-rate decline, youth unemployment. **Not
  active (columns empty):** low-income rate, housing-pressure proxy.
- **Weights** (`Knowledge/src/scoring.py`, explicit and editable for AI Council review):
  unemployment level 0.30 · unemployment change 0.15 · employment decline 0.10 ·
  participation decline 0.10 · youth unemployment 0.10 · low-income rate 0.15 ·
  housing pressure 0.10.
- **Normalised?** Yes — each component is min-max scaled to 0–1 against **fixed, documented
  anchors** (e.g., unemployment 4%→14%) and clipped, then combined as
  `100 × Σ(weight·component) / Σ(weight of available components)`.
- **Higher = higher priority?** Yes. Correlation with unemployment rate **0.92**, with youth
  unemployment **0.89**.
- **Missing reduces confidence (not silently filled)?** **Confirmed.** With low-income and
  housing always missing, available weight is 0.75 → `score_confidence = 0.75` / `medium`
  for 6,589 rows; the first 6 months/geo also lack `unemp_change` → 0.40 / `low` for 66 rows.
  No component is ever defaulted to zero or imputed.
- **Independent recompute:** Newfoundland & Labrador, 2026-05 → recomputed score **38.2**,
  file score **38.2**; recomputed confidence **0.75**, file **0.75**. The score is fully
  reproducible and explainable in plain language.

**Caveat to flag:** because two components are empty for every row, `missing_value_flag` is
`True` for **100%** of rows and `score_confidence` takes only two values (0.75, 0.40). The
flag is therefore correct but **non-discriminating** right now — it cannot distinguish "good"
from "weak" rows until the context columns are populated.

---

## 5. Score explanation validation

Sampled and scanned all unique `score_explanation` strings.

| Check | Result |
|---|---|
| References actual indicators | **Yes** — names the top drivers with their values (e.g., "unemployment rate (9.6); youth unemployment (18.7)") |
| Avoids overclaiming | **Yes** — "Flagged for policy review", "Triage signal only" |
| Says "not eligibility/benefit" | **Yes** — "not an eligibility or benefit decision" appears in every row |
| Mentions "social assistance" / "need" | **No** (correct — neither phrase appears) |
| Flags weak/missing evidence | **Yes** — states "Confidence low/medium (X% of weight backed by data)" |
| Uses exact phrase "elevated labour-market stress" | **No** — uses "Flagged for policy review" instead. Acceptable, but adding the governed phrase would align wording with the spec. *(Minor.)* |

---

## 6. Key strengths

1. Clean, unique monthly spine — `geo + ref_date` is a true key; zero duplicates; correct types.
2. Long, complete time series (1976–2026) with no gaps in the core LFS rate fields.
3. Transparent, reproducible, normalised score with explicit weights and fixed anchors.
4. Governance behaves correctly: missing data lowers confidence; nothing is imputed; every
   explanation carries the triage disclaimer.
5. Honest missingness — empty context columns are blank and flagged, not faked.

## 7. Data quality issues (ranked)

1. **Four context columns are 100% empty** (`low_income_rate`, `housing_pressure_proxy`,
   `income_value`, `population`) → the income, affordability, and demographic dashboard views
   have no data, and score confidence is capped at medium.
2. **Demographic granularity collapsed** in integration → gender and detailed-age views not
   available from the panel (recoverable from `labour_force_clean.csv`).
3. **No source fields in the panel** → traceability requires opening other files.
4. **No per-field frequency fields** → annual-vs-monthly mismatch isn't self-documented.
5. `missing_value_flag` is non-discriminating (True for all rows) until context data lands.
6. Territories absent (scope limitation to state explicitly).

---

## Fixes applied in this iteration (additive, no invented values)

To improve traceability without fabricating any data, the panel was extended with
**metadata-only** columns (frequencies and source pointers — these describe provenance, not
measurements; the empty value columns remain empty and flagged):

- `labour_force_data_frequency = monthly`, `housing_data_frequency = monthly`,
  `income_data_frequency = annual`, `population_data_frequency = annual`.
- `source_product_id_lfs / _income / _housing / _population` and
  `source_table_lfs / _income / _housing / _population` (StatCan product IDs + table codes).

These make every row defensible in class. They do **not** populate the empty measurement
columns — that still requires running `Knowledge/src/statcan_api.py` on a networked machine.

## Required fixes before presentation

- [ ] **Decide dashboard scope:** either (a) launch on the labour-market-stress core now and
      clearly grey out / hide the income, affordability, and demographic views with a "data
      pending" note, or (b) run the StatCan downloads (`Knowledge/src/statcan_api.py --all`) so the four
      empty columns populate before enabling those views.
- [ ] If annual data is joined, **surface the annual-by-year repeat** on the dashboard (label
      income/low-income/population as annual context).
- [ ] **Restore demographic granularity** for the demographic view (carry gender + age slices
      from `labour_force_clean.csv`), or state the youth-only limitation explicitly.
- [ ] Optionally align explanation wording with the governed phrase "elevated labour-market
      stress."
- [ ] Route the dashboard interpretation through the **AI Council** before any deployment-ready
      claim.

---

## Dashboard readiness decision

> ## ⚠️ READY WITH MINOR FIXES

**Reasoning.** The **labour-market-stress core is dashboard-ready**: a clean, uniquely-keyed,
50-year monthly series with a transparent, independently-reproduced, governed triage score and
safe explanations. None of the issues are data *corruption* — the spine is sound and all
missingness is honestly flagged. The fixes are mechanical, not data-repair: handle the four
empty context columns in the UI (or download their sources), add the source/frequency fields
(done additively here), and document the demographic and territory scope. **The dataset is not
ready to power the income, affordability, or demographic views** — those depend on the four
empty columns — so the dashboard must either scope to the stress core for now or wait for the
StatCan context downloads. Treat every score and explanation as a **claim for human/AI-Council
review**, not a fact.
