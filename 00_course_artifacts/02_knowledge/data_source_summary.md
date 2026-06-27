# Data Source Summary — Knowledge stock

*MMA 616 · Stage: KNOWLEDGE.* Aggregate public Statistics Canada tables, pulled via the WDS
API by `Knowledge/src/statcan_api.py`. Full detail & limitations: `Knowledge/metadata/data_sources.md`.

| Product ID | Title (short) | Category | Frequency | Status |
|---|---|---|---|---|
| 14-10-0287-01 | Labour force characteristics (LFS) — **spine** | labour force | monthly | **downloaded** |
| 98-10-0597-01 *(new)* | Employment income (2021 Census) | income | one-time | pending download |
| 14-10-0417-01 *(new)* | Employee wages by occupation, annual | income/wages | annual | pending download |
| 14-10-0426-01 *(new)* | Employee wages by occupation, monthly | income/wages | monthly | pending download |
| 11-10-0239-01 | Income of individuals | income | annual | pending download |
| 11-10-0135-01 | Low income statistics | income | annual | pending download |
| 17-10-0005-01 | Population estimates | demographics | annual | pending download |
| 18-10-0004-01 | CPI incl. Shelter (affordability **proxy**) | affordability | monthly | pending download |

## Indicator coverage
- **Labour force:** unemployment / employment / participation rates (15+ and youth 15–24),
  by province, monthly, 1976→2026 — and trailing-12-month changes (the stress signal).
- **Income:** median employment / after-tax income; wages by occupation; 2021 Census income
  by industry/education/immigration — annual/structural **context**.
- **Demographics:** population estimates by age & gender — normalisation/context.
- **Affordability:** shelter-CPI year-over-year growth — a labelled **proxy**, not a measured
  affordability or core-housing-need rate.

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
