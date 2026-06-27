# data/ — the project's data sources

This folder is where the project's datasets live. It is the **Knowledge stock's** raw material: the data the dashboard turns into the views, metrics, and comparisons our user needs to make a decision.

## Layout & pipeline (Labour Market Stress & Social Support Prioritization)

```
data/
  pull_statcan.py            # pull all source tables via the StatCan WDS API
  build_panel.py             # clean + integrate + score -> processed/
  pull_lfs.py                # (single-table LFS puller, superseded by pull_statcan.py)
  lfs_validation.ipynb       # interactive LFS pull + validation notebook
  raw/{labour_force,income,demographics,housing_affordability}/   # downloaded source CSVs
  processed/                 # *_clean.csv + policy_triage_panel.csv (the dashboard input)
  metadata/                  # data_sources.md, data_dictionary.md, integration_notes.md
```

**To (re)build the data on a networked machine:**

```
python3 pull_statcan.py --check     # which tables changed?
python3 pull_statcan.py --all       # download every source -> raw/
python3 build_panel.py --build      # clean, integrate, score -> processed/
python3 build_panel.py --selftest   # prove the pipeline on synthetic data (no network)
```

Five verified StatCan sources feed it: LFS (14-10-0287-01), income (11-10-0239-01), low income (11-10-0135-01), population (17-10-0005-01), and CPI/Shelter (18-10-0004-01). Full details, frequencies, and limitations are in **[metadata/data_sources.md](metadata/data_sources.md)**; the integrated columns are documented in **[metadata/data_dictionary.md](metadata/data_dictionary.md)**; join/missing-value/governance rules are in **[metadata/integration_notes.md](metadata/integration_notes.md)**.

> **Governance:** the integrated panel produces a `policy_review_priority_score` that is a **triage signal for human review only** — it does not establish eligibility or need, and the housing field is a labelled **proxy**. See integration_notes.md.

## Rules for what goes here

- **Connect the source; do not paste fragments.** The workspace should read the live source (file, API, or connector), not a screenshot or thirty pasted rows. *(Managing Intelligence, Ch 2 & 6.)*
- **Pair data with its meaning.** A raw data file is paired with the document that explains it (a codebook, data dictionary, or schema note). Numbers without their meaning get read confidently and wrongly.
- **Curate, don't dump.** Keep only what the task needs, and keep it current. Record the encoding traps and non-obvious facts the column names cannot carry.
- **If the data is synthetic, say so.** State in `CLAUDE.md` what is synthetic and what that means for the claims the dashboard can make.
- **Minimize/anonymize sensitive information**, especially anything student-related.

## What to put here once chosen

1. The dataset file(s) — or a documented connection to the live source.
2. The codebook / data dictionary / schema note.
3. A short `data-notes.md` capturing: what one row is, sample representativeness, what blanks mean, and the encoding traps (the "five traps" style list from Ch 2).

## Candidate sources (from the assignment dataset menu)

Choose the **kind of dashboard first** (operational/monitoring, exploratory/analytical, KPI/briefing, or comparison/benchmarking), then find data that supports it. Public starters include:

- Calgary 311 Service Requests (municipal operations, API)
- Edmonton Building Permits (municipal development)
- Alberta Historical Wildfire Data 2006–2025 (provincial risk, with data dictionary)
- Calgary Restaurant Inspections (municipal public health)
- Statistics Canada Labour Force Survey (federal economics, CSV/API/microdata)

> **Notes.** Government of Alberta open data is allowed for the group project. **The individual final must use a *different* GoA dataset and a *different* problem** than the group's — don't burn your preferred GoA dataset/problem here. The dataset should have enough substance for an insightful dashboard (multiple dimensions, categories, time, or related tables), be documented and connectable, and be workable within a week.

*Currently empty — add the dataset and its codebook once the team commits to one user, one decision, and one concept.*
