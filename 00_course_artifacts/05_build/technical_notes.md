# Technical Notes — Build

*MMA 616 · Stage: BUILD.*

## Run the dashboard
```bash
pip install streamlit pandas
streamlit run dashboard/app.py
```
Reads `Knowledge/processed/policy_triage_panel.csv`. Path is resolved as
`Path(__file__).resolve().parents[1] / "Knowledge" / "processed" / "policy_triage_panel.csv"`,
so the app works regardless of the working directory **as long as `dashboard/app.py` stays in
`dashboard/`** (it does). The data pipeline lives under `Knowledge/`; the dashboard sits at the
repo root and reaches into `Knowledge/` for the panel.

## Pipeline
`Knowledge/src/statcan_api.py` (pull) → `Knowledge/notebooks/01` → `Knowledge/src/data_cleaning.py`
+ `Knowledge/notebooks/02` (clean → `Knowledge/processed/*_clean.csv`) → `Knowledge/src/scoring.py`
+ `Knowledge/notebooks/04` (score → `policy_triage_panel.csv`) → `Knowledge/notebooks/05` (exports).
The `Knowledge/src` modules resolve their root via `parents[1]` (= `Knowledge/`); notebooks import
`src/` via `Path.cwd().parent / "src"`; the dashboard (at the repo root) reaches the panel via
`parents[1] / "Knowledge" / "processed"`.

## Paths after the reorg
The `00_course_artifacts/` course layer is **additive** (no technical folder moved for it). The
data pipeline lives under `Knowledge/`, and the dashboard at the repo root resolves the panel at
`ROOT/Knowledge/processed/policy_triage_panel.csv`. Verified: the `Knowledge/src` modules import;
the dashboard's data path resolves; the panel loads.

## Known technical issues
- Four context columns are empty until the StatCan downloads run (sandbox has no network).
- `missing_value_flag` is True for all rows (two components always missing) → non-discriminating
  until context data lands.
- Large raw CSV (~337 MB) lives in `Knowledge/raw/labour_force/`; `.gitignore` covers `__pycache__`.

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
