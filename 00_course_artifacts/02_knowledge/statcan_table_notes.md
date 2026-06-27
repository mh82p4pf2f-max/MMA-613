# Statistics Canada Table Notes — Knowledge stock

*MMA 616 · Stage: KNOWLEDGE.* Per-table notes. Titles/dimensions are confirmed at pull time
via `python3 Knowledge/src/statcan_api.py --metadata <pid>`.

## 14-10-0287-01 — Labour force characteristics (LFS) — the spine
Monthly, Canada + 10 provinces (no territories), 1976→2026. Dimensions: geography, labour
force characteristics, gender (Men+/Women+/Total), age group, statistics, data type
(seasonally adjusted / unadjusted). The dashboard uses the SA, Total-Gender, 15+ slice plus
youth (15–24). ~0.2% of estimate cells suppressed/missing → flagged, never imputed.

## 98-10-0597-01 — Employment income (2021 Census) *(new)*
One-time, income year **2020**, 25% sample. Income by industry (NAICS), education, immigrant
status & period, work activity, age, gender. Rich structural income context — **not a time
series**; the reference year is pandemic-affected.

## 14-10-0417-01 — Employee wages by occupation, annual *(new)*
Annual, ~1997→2025. Average/median hourly & weekly wages by NOC, type of work, gender, age.
Wage-level income context; join by year. Confirm member labels on first pull.

## 14-10-0426-01 — Employee wages by occupation, monthly *(new)*
Monthly (confirm via `--metadata`). Higher-frequency wage context alongside the LFS.

## 11-10-0239-01 / 11-10-0135-01 — Income of individuals / Low income
Annual. Median income & income source; low-income rate (LIM-AT default). Economic-vulnerability
context; latest year lags the LFS by ~2 years; line choice (LIM/LICO/MBM) changes levels.

## 17-10-0005-01 — Population estimates
Annual July-1 estimates by age & gender. Used for normalisation/context.

## 18-10-0004-01 — CPI incl. Shelter
Monthly, base 2002=100. Shelter-CPI YoY growth is the **housing-pressure proxy** — index
level, not dollar rent; province-level, not household.

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
