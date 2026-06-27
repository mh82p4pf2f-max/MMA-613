# Data Dictionary — `policy_triage_panel.csv`

The integrated panel produced by the `src/` pipeline (`data_cleaning.py` +
`scoring.py`, driven by `notebooks/02`, `04`, `05`). Grain: **one row per geography ×
month** for the headline labour-force slice (Total - Gender, 15+, seasonally adjusted),
with annual context joined by year and monthly affordability joined by month. A field is
only populated if its source table was downloaded and the member labels matched; otherwise
it is present but **NaN and flagged**.

| Field | Description | Source Dataset | Unit | Frequency | Notes |
|---|---|---|---|---|---|
| `ref_date` | Reference period | LFS (spine) | YYYY-MM | Monthly | Spine key |
| `year` | Year of `ref_date` | derived | year | — | Join key for annual sources |
| `month` | Month of `ref_date` | derived | 1–12 | — | — |
| `geo` | Geography (Canada / province) | LFS (spine) | name | — | Join key |
| `gender` | Gender slice of the headline row | LFS | label | — | "Total - Gender" in this build |
| `age_group` | Age slice of the headline row | LFS | label | — | "15 years and over" |
| `labour_force_characteristic` | Indicator family for the row | LFS | label | — | "headline rates (LFS)" |
| `unemployment_rate` | Unemployment rate (SA, 15+) | LFS 14-10-0287 | % | Monthly | Primary stress signal |
| `employment_rate` | Employment rate (SA, 15+) | LFS | % | Monthly | — |
| `participation_rate` | Participation rate (SA, 15+) | LFS | % | Monthly | — |
| `youth_unemployment_rate` | Unemployment rate, 15–24, Total - Gender (SA) | LFS | % | Monthly | Youth-stress view; feeds the score |
| `core_unemployment_rate` | Unemployment rate, 25–54, Total - Gender (SA) | LFS | % | Monthly | Demographic driver (not yet scored) |
| `older_unemployment_rate` | Unemployment rate, 55+, Total - Gender (SA) | LFS | % | Monthly | Demographic driver; 55+ because 65+ is absent and 55–64 SA-sparse in the source |
| `unemp_change` | Unemployment rate minus its trailing **12-mo** average | derived (LFS) | pp | Monthly | Positive = worsening |
| `emp_change` | Employment rate minus its trailing **3-mo** average (AI Council 2026-06-27) | derived (LFS) | pp | Monthly | Negative = worsening |
| `part_change` | Participation rate minus its trailing **3-mo** average (AI Council 2026-06-27) | derived (LFS) | pp | Monthly | Negative = people leaving the labour force |
| `income_indicator` | Income/wage measure used | Income 11-10-0239 / wages 14-10-0417 / Census 98-10-0597 | label | **Annual / one-time** | Context; NaN until those tables are downloaded |
| `income_value` | Income / wage amount | as above | dollars | **Annual** | Context; joined by year; NaN until downloaded |
| `low_income_rate` | Low-income rate (LIM-AT, all persons) | Low income 11-10-0135 | % | **Annual** | Context; NaN until downloaded |
| `demographic_indicator` | Demographic measure used | Population 17-10-0005 | label | **Annual** | Context; NaN until downloaded |
| `demographic_value` | Demographic value | Population 17-10-0005 | varies | **Annual** | Context; NaN until downloaded |
| `population` | Population (context) | Population 17-10-0005 | persons | **Annual** | Normalisation/context; NaN until downloaded |
| `affordability_indicator` | Affordability proxy label | CPI 18-10-0004 | label | Monthly | "shelter CPI YoY" when present |
| `affordability_value` / `housing_pressure_proxy` | YoY % change in Shelter CPI | derived (CPI) | % | Monthly | **PROXY** for housing cost pressure — not true affordability; NaN until downloaded |
| `policy_review_priority_score` | Triage score 0–100 (higher = more elevated stress) | derived | score | Monthly | **Triage for human review only — NOT eligibility/benefits** |
| `score_confidence` | Share of score weight backed by available data (0–1) | derived | ratio | Monthly | < 1 = some inputs missing |
| `confidence_flag` | `high` / `medium` / `low` / `no inputs` | derived | label | Monthly | ≥0.85 high · ≥0.55 medium · else low |
| `missing_value_flag` | True if any scoring input was missing/suppressed | derived | bool | Monthly | Missing data lowers confidence; never silently filled |
| `score_explanation` | Plain-language drivers + triage disclaimer | derived | text | Monthly | Evidence behind every flag |
| `data_frequency` | Native frequency of the row's spine | derived | monthly | — | — |
| `source_product_id` | StatCan product ID of the spine | derived | code | — | 14100287 (LFS) |

## Scoring components & weights (`policy_review_priority_score`)

Each component is normalised to 0–1 against fixed, documented anchors (see `WEIGHTS` /
`ANCHORS` in `src/scoring.py`), then combined:
`score = 100 × Σ(weight·component) / Σ(weight of available components)`.

| Component | Field | Default weight | Anchors (0 → 1) |
|---|---|---:|---|
| Unemployment level | `unemployment_rate` | 0.30 | 4% → 14% |
| Unemployment rise vs 12-mo avg | `unemp_change` | 0.15 | 0 → +3 pp |
| Employment-rate decline (vs 3-mo avg) | `emp_change` (flipped) | 0.10 | 0 → 3 pp fall |
| Participation-rate decline (vs 3-mo avg) | `part_change` (flipped) | 0.10 | 0 → 3 pp fall |
| Youth unemployment | `youth_unemployment_rate` | 0.10 | 8% → 25% |
| Low-income rate | `low_income_rate` | 0.15 | 5% → 20% |
| Housing cost pressure (proxy) | `housing_pressure_proxy` | 0.10 | 0 → 10% YoY |

Weights and anchors are explicit and editable so the AI Council can review and adjust them.
**The score identifies areas for review; it does not decide who receives assistance.**

> **Current build:** only the LFS is downloaded, so `low_income_rate` and
> `housing_pressure_proxy` are missing → `confidence_flag` is capped at **medium (75%)**.
> Downloading the income / demographics / affordability tables raises confidence.
