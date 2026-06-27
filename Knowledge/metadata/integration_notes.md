# Integration Notes

How the Statistics Canada tables are downloaded, cleaned, joined, and scored into
`Knowledge/processed/policy_triage_panel.csv` by the `Knowledge/src/` pipeline — and, just as importantly,
what the result can and cannot support.

## Pipeline

```
Knowledge/src/statcan_api.py  → Knowledge/raw/<domain>/<pid>.csv      (download via WDS API)
        │  data_cleaning.clean_statcan(): standardise REF_DATE→ref_date/year/month/quarter,
        │  GEO→geo, DGUID→dguid, VALUE→value; snake_case columns; flag suppressed/blank
        │  cells; attach source_product_id / source_table_title / source_category /
        │  retrieval_date
        ▼
Knowledge/processed/*_clean.csv
        │  data_cleaning.lfs_headline_features(): headline slice (Total-Gender, 15+, SA),
        │  pivot to wide, add youth (15-24) unemployment + trailing-12-month changes
        ▼
scoring.add_scores() → Knowledge/processed/policy_triage_panel.csv   (the dashboard input)
```

How it was run in this build: `Knowledge/notebooks/02` cleaned the LFS into
`labour_force_clean.csv`; `Knowledge/notebooks/04` built and scored the headline panel; `Knowledge/notebooks/05`
exported the dashboard tables. Downloads (`Knowledge/notebooks/01`) must run on a networked machine —
the WDS endpoints are not reachable from the sandboxed analysis environment, so this build
cleaned and scored the **already-present** LFS file and left the other sources flagged as
pending.

## Spine and join keys

- **Spine:** the LFS monthly series (14-10-0287-01), headline slice = seasonally adjusted,
  Total - Gender, 15+. Grain = `geo × ref_date`.
- **Join keys:**
  - `geo` + `ref_date` (YYYY-MM) → monthly affordability proxy (CPI/Shelter 18-10-0004) and
    monthly wages (14-10-0426).
  - `geo` + `year` → annual income (11-10-0239), low income (11-10-0135), annual wages
    (14-10-0417), population (17-10-0005).
  - The 2021 Census income table (98-10-0597) is a **structural, one-time** layer joined by
    `geo` (and, where used, demographic slice) — not a time series.
- `dguid` is carried for stable geography matching, but `geo` (name) is the practical key
  because every table exposes it.

## Frequency handling (a core rule)

- **Monthly × monthly:** LFS ↔ CPI/Shelter and ↔ monthly wages join directly on `ref_date`.
- **Monthly × annual:** income, low income, annual wages, and population are **annual** and
  are joined to every month of their `year`, **clearly labelled annual context**
  (`data_frequency` + the dictionary marks each field). We do **not** fabricate monthly
  values; the same annual figure repeats across the year's months by design, which the
  dashboard surfaces (e.g., "income is an annual context indicator").
- **One-time Census:** 98-10-0597 reflects income year **2020** only — used as structural
  context, never as a current-period value.

## Missing, suppressed, and unavailable values

- StatCan blank `VALUE` cells and any `F` / `x` / `..` status are treated as **missing**:
  `value` is `NaN` and `missing_value_flag` is set. In the cleaned LFS estimates, ~0.2% of
  cells are suppressed/missing.
- **Never invented or imputed.** No silent fills. Any future imputation would be a separate,
  labelled column — not a backfill.
- In scoring, a missing component is **dropped from that row's weighted average and lowers
  `score_confidence`/`confidence_flag`**; it never defaults to zero (which would understate
  stress).

## What could not be joined / cleanly merged (this build)

- **Income / demographics / affordability:** not yet downloaded here, so those panel columns
  are present but NaN and flagged. Run `Knowledge/notebooks/01`-`02` on a networked machine to
  populate them, then re-run `04`-`05`.
- **Sub-provincial geography:** income/low-income/CPI/Census offer CMA detail, but the LFS
  spine is province-level, so CMA rows are not merged in this build. A future version can add
  LFS economic-region tables.
- **Age/gender alignment across sources:** age-group definitions differ (LFS 15+/15-24 vs
  income 16+ vs Census/wage NOC bands), so cross-source demographic joins default to total
  slices and are documented as a known mismatch.
- **True housing affordability** (core housing need, shelter-cost-to-income ≥30%, average
  rent) is **not** in these WDS tables — the CPI-Shelter proxy stands in and is labelled a
  proxy everywhere.

## Member-label confirmation

StatCan member strings occasionally change. `Knowledge/src/statcan_api.py --metadata <pid>` prints the
authoritative title, dimensions, and member codes; confirm them on the first real pull and
update `data_sources.md` if a label changed. The two wage tables (14-10-0417, 14-10-0426)
and the Census table (98-10-0597) especially warrant a label check on first download.

## What the integrated data CAN support

- Identifying **areas and groups with elevated economic distress** by combining
  **labour-market** signals (unemployment, participation, employment, youth) with **income and
  employment context** — across provinces, age/gender groups, and over time.
- Adding **income / wage context** (levels by occupation, industry, demographic group) and
  **cost-pressure context** (shelter-CPI growth) to distinguish labour stress from broader
  hardship.
- A transparent, explainable **triage score** that flags geography × group areas for the
  **program owner's review**, with the evidence and confidence behind each flag — so the owner
  can decide where to focus (choosing or delivering any intervention is their downstream call,
  out of scope here).

## What the integrated data CANNOT support (governance boundary)

- It **cannot** establish that a region or group **requires** social assistance, nor
  determine individual **eligibility, poverty, household need, disability, food insecurity,
  or housing insecurity**.
- It **cannot** approve, deny, or reduce benefits, and must never be used to.
- It **cannot** claim representativeness for small/suppressed cells.
- The housing field is a **proxy**, not a measured affordability rate.
- Use language like *"elevated economic distress," "area to focus on," "requires policy
  review," "possible intervention priority," "should be reviewed by a human."* Claude outputs
  are **claims, not facts**, and the **AI Council must review** any policy interpretation
  before it is treated as decision-ready.
