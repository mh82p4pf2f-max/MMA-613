# Data Limitations — Knowledge stock

*MMA 616 · Stage: KNOWLEDGE.* What the data **can** and **cannot** support. Mirrors the
governance boundary in `Knowledge/metadata/integration_notes.md` and the audit.

## Missing / suppressed data
- StatCan blank / `F` / `x` / `..` cells are treated as **missing**: value = NaN and
  `missing_value_flag` set. **Never invented or imputed.**
- In the current panel, the income / low-income / housing / population columns are **100%
  empty** (sources not yet downloaded) → score confidence capped at **medium**. This is
  honest missingness, flagged, not faked.

## Frequency mismatches (documented, not hidden)
- Monthly LFS spine vs **annual** income / wages / population (joined by `year`, repeating
  one annual value across 12 months and labelled annual context).
- Monthly CPI/Shelter and monthly wages join directly on `ref_date`.
- 2021 Census income is **one-time** (2020) structural context, never a current value.
- Per-field frequency is recorded in the panel's `*_data_frequency` columns.

## Geographic & demographic limits
- **Territories absent** (LFS 14-10-0287 is provinces only).
- The panel currently collapses to Total-Gender, 15+ (plus youth); gender and detailed-age
  breakdowns exist in `labour_force_clean.csv` but are not yet carried into the panel.

## What the data CAN support
Identifying areas and groups with elevated economic distress (labour-market signals plus
income/affordability **context**) across provinces, groups, and time; a transparent triage
score flagging where to focus, with evidence + confidence.

## What the data CANNOT support
Determining social-assistance need, eligibility, poverty, household need, or any individual
decision; approving/denying/reducing benefits; representativeness for suppressed cells; a
true affordability measure (the housing field is a **proxy**).

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
