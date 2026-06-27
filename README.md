# Labour Market Stress & Social Support Prioritization Dashboard

*MMA 616 — Managing Intelligence. A governed decision-support project.*

## Problem statement

A social-assistance program owner / policy lead must triage limited attention across many
provinces, regions, age groups, and demographic groups. **Which areas and groups should we
focus on this cycle?** This project turns aggregate Statistics Canada data into a transparent,
comparable **economic-distress signal** — combining labour-market, income, and employment
indicators — that flags areas and groups warranting a closer human look, with the evidence and
caveats attached to every flag.

## What this is — and is not

- It **is** a governed decision-support dashboard that **flags areas for human policy
  review and triage**.
- It is **not** a tool that determines who needs social assistance, eligibility, or
  benefits. It never operates on individuals.
- **Claude outputs are claims, not facts.** Missing/suppressed data is flagged, not invented.
- **The AI Council reviews any policy interpretation before it is treated as decision-ready.**

## User and decision

- **Primary user:** a social-assistance program owner / policy lead.
- **Decision supported:** which areas and groups (geography × demographic, e.g. *youth in
  Alberta*) to focus on for policy review this cycle. Choosing or delivering any intervention is
  the owner's downstream call — out of scope here.

## Data sources (aggregate public Statistics Canada, via the WDS API)

| Product ID | Title (short) | Category | Frequency |
|---|---|---|---|
| 14-10-0287-01 | Labour force characteristics (LFS) — spine | labour force | monthly |
| 98-10-0597-01 *(new)* | Employment income (2021 Census) | income | one-time |
| 14-10-0417-01 *(new)* | Employee wages by occupation, annual | income/wages | annual |
| 14-10-0426-01 *(new)* | Employee wages by occupation, monthly | income/wages | monthly |
| 11-10-0239-01 | Income of individuals | income | annual |
| 11-10-0135-01 | Low income statistics | income | annual |
| 17-10-0005-01 | Population estimates | demographics | annual |
| 18-10-0004-01 | CPI incl. Shelter (affordability **proxy**) | affordability | monthly |

Detail and limitations: [`Knowledge/metadata/data_sources.md`](Knowledge/metadata/data_sources.md).

## Folder structure

This project is aligned with the **MMA 616 Day-1 method (Agentic Project Design)** and reads
two ways: a **course-facing** layer that makes the method visible, and a **technical** layer
that implements it. The living spec is the root `CLAUDE.md`.

### Course-facing structure — `00_course_artifacts/`

Organised around **Plan → Build → Use → Evaluate** and the Day-1 artifacts
**Knowledge → Living Spec → Mock Deliverable → Governance**:

```
00_course_artifacts/
  01_plan/             opportunity brief · user & decision · success criteria        (PLAN)
  02_knowledge/        inventory · data-source summary · table notes · limitations   (KNOWLEDGE)
  04_deliverable_mockup/  mockup notes · html_mockup/index.html                      (MOCK DELIVERABLE)
  05_build/            build log · dashboard requirements · technical notes           (BUILD)
  06_use/              deployment log · user feedback log (templates)                 (USE)
  07_evaluate/         plan · known-answer tests · baseline/revised · summary         (EVALUATE)
  08_governance/       AI Council governance · review packet · decision log · risks   (GOVERNANCE)
```

Start at [`00_course_artifacts/README.md`](00_course_artifacts/README.md). The HTML mockup of
the nine intended dashboard views is
[`00_course_artifacts/04_deliverable_mockup/html_mockup/index.html`](00_course_artifacts/04_deliverable_mockup/html_mockup/index.html)
(open in any browser).

### Technical structure — implementation

```
CLAUDE.md   README.md   .gitignore   .claude/
Knowledge/   raw/ (StatCan CSVs) · processed/ (clean + policy_triage_panel.csv) · metadata/
             notebooks/ (00 setup · 01 download · 02 clean · 03 explore · 04 score · 05 export)
             src/ (statcan_api.py · data_cleaning.py · scoring.py · utils.py) · outputs/
dashboard/   app.py (Streamlit, 9 views) · assets/
docs/        ai-council-governance.md · evaluation-plan.md
00_course_artifacts/   MMA 616 course-facing evidence (01_plan … 08_governance)
archive/     superseded files (moved, not deleted)
```

The `Knowledge/` and `dashboard/` folders are for implementation; `00_course_artifacts/` is for
the MMA 616 method and presentation. The living spec is the root `CLAUDE.md` — there is no
separate spec document.

## How to run

### 1. Download the data (networked machine)

```bash
python3 Knowledge/src/statcan_api.py --list                 # configured tables
python3 Knowledge/src/statcan_api.py --check                # which tables changed?
python3 Knowledge/src/statcan_api.py --metadata 9810059701  # confirm a new table's dimensions
python3 Knowledge/src/statcan_api.py --all                  # download every table → Knowledge/raw/<domain>/
```

> The WDS endpoints must be reached from a networked machine. The LFS table is already
> present at `Knowledge/raw/labour_force/lfs_14100287_tidy.csv`.

### 2. Run the notebooks (in order)

```bash
pip install pandas numpy matplotlib jupyter
jupyter lab    # then run Knowledge/notebooks/00 → 05
```

`02` cleans → `Knowledge/processed/*_clean.csv`; `04` scores → `policy_triage_panel.csv`;
`05` exports the dashboard tables.

### 3. Launch the dashboard

```bash
pip install streamlit pandas
streamlit run dashboard/app.py
```

It reads [`Knowledge/processed/policy_triage_panel.csv`](Knowledge/processed) and shows nine views:
executive summary, regional stress, demographic vulnerability, income context, affordability
pressure, the priority score, an evidence panel, AI Council review status, and caveats.

## The policy review priority score

A transparent 0–100 **triage** signal combining unemployment level & 12-month change,
employment/participation decline, youth unemployment, low-income rate, and shelter-cost
pressure — each normalised against fixed, documented anchors and weighted with explicit,
editable weights. Every score carries its drivers (`score_explanation`) and a
`confidence_flag`; missing inputs lower confidence and are never imputed. It is a triage
signal for human review — **not** an eligibility or benefit decision. See `Knowledge/src/scoring.py`
and [`Knowledge/metadata/data_dictionary.md`](Knowledge/metadata/data_dictionary.md).

## Current status

- ✅ Folder reorganised to the target tree; superseded files archived.
- ✅ LFS cleaned and scored → `policy_triage_panel.csv` (6,655 rows, 1976-01 → 2026-05).
- ✅ `Knowledge/` notebooks + `src/` modules, dashboard, docs, and metadata in place.
- 🟡 The 7 context tables (incl. the 3 new ones) are wired up but **pending download** on a
  networked machine; until then their fields are flagged missing and confidence is capped at
  medium.
- ⬜ AI Council review not yet run (prototype). Evaluation cases to be completed.

## Known limitations

Triage, not need. The housing field is a **proxy** (shelter-CPI growth), not measured
affordability. Monthly LFS spine vs annual income/wages/population context (joined by year).
Province-level (sub-provincial gaps). Suppressed cells flagged, never imputed. Claude-drafted
summaries require analyst + AI Council review. Full detail:
[`Knowledge/metadata/integration_notes.md`](Knowledge/metadata/integration_notes.md).
