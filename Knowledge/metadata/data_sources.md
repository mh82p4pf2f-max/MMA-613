# Data Sources

All sources are **official Statistics Canada tables**, public and aggregate, pulled via the
Web Data Service (WDS) API (no key) by `Knowledge/src/statcan_api.py`. No values are manually pasted.
Product IDs, titles, dimensions, geography, frequency, and date ranges were verified on
statcan.gc.ca in June 2026; `python3 Knowledge/src/statcan_api.py --metadata <pid>` prints the
authoritative `cubeTitleEn`, dimensions, and date range at pull time — confirm and update
this file if a label changed.

| Dataset | Product ID | Source URL | Frequency | Geography | Date Range | Key Dimensions | Why Used | Limitations |
|---|---:|---|---|---|---|---|---|---|
| Labour force characteristics (LFS) — **spine** | 14-10-0287-01 | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028701 | **Monthly** (SA + trend-cycle) | Canada, provinces | 1976-01 → ~2026-05 | Geography, Labour force characteristics, Gender, Age group, Statistics, Data type | Core labour-market stress: unemployment / participation / employment rates by province, gender, age | Measures labour-market stress only — not eligibility, poverty, or need; sub-provincial detail limited |
| **Employment income by industry, education, immigrant status, work activity, age, gender (2021 Census)** | **98-10-0597-01** *(NEW)* | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810059701 | **One-time** (2021 Census, income year 2020) | Canada, provinces/territories, CMAs/CAs | 2020 income (2021 Census) | Geography, Industry (NAICS), Education, Immigrant status & period, Work activity, Age, Gender, Statistics | Rich **income context** by industry and demographic group to distinguish labour stress from structural income vulnerability | Single reference year (2020, pandemic-affected); 25% sample estimates with rounding; not a time series — structural context only |
| **Employee wages by occupation, annual** | **14-10-0417-01** *(NEW)* | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410041701 | **Annual** | Canada, provinces | ~1997 → 2025 | Geography, Occupation (NOC), Type of work, Gender, Age group, Wage statistics (avg/median hourly & weekly) | Wage-level **income context** by occupation/age/gender; shows *quality* of work, not just quantity | Annual (join by year); occupation-level (not household); survey-based; confirm member labels on first pull |
| **Employee wages by occupation, monthly** | **14-10-0426-01** *(NEW)* | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410042601 | **Monthly** (confirm via `--metadata`) | Canada, provinces | confirm on pull | Geography, Occupation (NOC), Type of work, Gender, Age group, Wage statistics | Higher-frequency wage **context** alongside the monthly LFS | Title/frequency to confirm via `getCubeMetadata`; occupation-level; survey-based |
| Income of individuals by age group, sex and income source | 11-10-0239-01 | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1110023901 | **Annual** | Canada, region, provinces, CMA | 1976 → 2023 | Geography, Age group, Sex, Income source | Median employment / after-tax / market income & transfers — income vulnerability context | Annual (join by year); latest year lags the LFS by ~2 years |
| Low income statistics by age, gender and economic family type | 11-10-0135-01 | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1110013501 | **Annual** | Canada, region, provinces, CMA | 1976 → 2024 | Geography, Age, Gender, Family type, Low income lines (LIM/LICO/MBM), Statistics | Low-income **rate** (LIM-AT default) — direct economic-vulnerability layer | Annual; line choice changes levels; not individual eligibility |
| Population estimates on July 1, by age and gender | 17-10-0005-01 | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000501 | **Annual** | Canada, provinces | 1971 → 2025 | Geography, Gender, Age group (5-yr + median age) | Population structure to normalise signals & show how many people a signal affects | Annual July-1 estimates; used for normalisation/context |
| Consumer Price Index, monthly (incl. Shelter) | 18-10-0004-01 | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810000401 | **Monthly** | Canada, provinces (+ CMAs) | 1914 → current | Geography, Products & product groups (incl. **Shelter**); base 2002=100 | Housing **cost-pressure PROXY**: YoY growth in Shelter CPI by province | A PROXY, not a true affordability / core-housing-need measure; index level, not dollar rent; province-level |

> **NEW this iteration (June 2026):** 98-10-0597-01, 14-10-0417-01, 14-10-0426-01 were added
> to deepen the income/wage context layer. All three map to the **income** domain
> (`Knowledge/raw/income/`). They are downloaded by `Knowledge/src/statcan_api.py`; titles/dimensions are
> confirmed at pull time.

## How to (re)pull

```bash
python3 Knowledge/src/statcan_api.py --list                 # configured tables (NEW flagged)
python3 Knowledge/src/statcan_api.py --check                # which tables changed today?
python3 Knowledge/src/statcan_api.py --metadata 9810059701  # confirm a table's dimensions
python3 Knowledge/src/statcan_api.py --table census_income  # pull one by key
python3 Knowledge/src/statcan_api.py --all                  # pull everything
```

Each pull writes the data CSV, the StatCan metadata CSV, and a `<pid>.source.json`
(zip URL, table page, retrieval date, UTC pull time) into `Knowledge/raw/<domain>/`. **The WDS
endpoints must be reached from a networked machine** — they are not reachable from the
sandboxed analysis environment used to build the cleaned LFS data.

## Retrieval status (this build)

- **14-10-0287-01 (LFS):** retrieved → `Knowledge/raw/labour_force/lfs_14100287_tidy.csv`
  (rate indicators, 1976-01 → 2026-05). Cleaned and scored.
- **98-10-0597-01, 14-10-0417-01, 14-10-0426-01, 11-10-0239-01, 11-10-0135-01,
  17-10-0005-01, 18-10-0004-01:** configured in `Knowledge/src/statcan_api.py`, **pending download**
  on a networked machine. Until then the panel's income/demographics/affordability fields
  are present but **NaN and flagged**, never invented.

## Considered but not used (for the AI Council)

- **CMHC average rent / vacancy** and **Census core housing need / shelter-cost-to-income
  ≥30%** would be truer affordability measures but are not StatCan WDS monthly series. The
  CPI-Shelter **proxy** is the practical API-connected stand-in and is labelled a proxy
  everywhere. Recorded as a future upgrade.

## Secondary / contextual sources — NOT StatCan WDS, NOT used for scoring

These are **background reading only**, not connected data. **No figure in them may be cited as a
value, used as a scoring input, or treated as panel data.** They are quarantined outside every
pipeline-read path under `Knowledge/reference/` (which the pipeline never reads).

| Item | What it is | Status |
|---|---|---|
| `Knowledge/reference/canadian_social_support_policy_context.md` | Two Gemini deep-research syntheses (federal + Alberta; then national / cross-province) on social-assistance funding, welfare incomes, indexation, clawbacks, and the welfare wall | **Context only** — secondary/advocacy synthesis (Maytree, PBO, OAG Alberta, HelpSeeker, U Calgary SPP, Alberta budget docs, Canada.ca); **NOT a StatCan WDS source**; saturated with **city-level** (Edmonton/Calgary) and **eligibility/benefit** content that are automatic fails if they reach a scored output. See [`Knowledge/reference/README.md`](../reference/README.md) for the full firewall. |

> **Why it is fenced off, not merged here:** it overlaps the connected panel essentially nil (the
> panel holds only LFS rate indicators + the score — no dollars, caseloads, or poverty rates). Its
> CPI/rent figures are **not** our 18-10-0004 Shelter *proxy*, and its MBM/poverty-adequacy ratios
> are **not** our 11-10-0135 low-income *rate* — both panel fields stay NaN/flagged until downloaded.
> Use it for caveats, province-level briefing context, and AI-Council weight rationale only.
