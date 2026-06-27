# Build Log — Build

*MMA 616 · Stage: BUILD.* Newest first.

| Date | What was built | Result |
|---|---|---|
| 2026-06-27 | **Full demonstration panel** — `Knowledge/src/build_demo_panel.py` → `Knowledge/processed/policy_triage_panel_full.csv` | Per-group panel (36,517 rows, 2015–2026) with all 7 score components populated; scores via `scoring.py`; the dashboard reads this panel |
| 2026-06-26 | Course-facing `00_course_artifacts/` layer + HTML mockup | Project legible as MMA 616; dashboard untouched |
| 2026-06-26 | Panel audit + added source/frequency provenance columns | Panel traceable; verdict READY WITH MINOR FIXES |
| 2026-06-26 | Cleaned LFS → `labour_force_clean.csv`; scored panel → `policy_triage_panel.csv` | 6,655 rows, 1976-01→2026-05; score validated |
| 2026-06-26 | `Knowledge/src/` modules (statcan_api, data_cleaning, scoring, utils) + `Knowledge/notebooks/` 00–05 | Reproducible pipeline |
| 2026-06-26 | Streamlit dashboard `dashboard/app.py` (9 views, governed) | Reads the panel; runs locally |

## Current state
- **Dashboard reads:** `Knowledge/processed/policy_triage_panel_full.csv` (via `ROOT/Knowledge/processed`).
- **All nine views populated:** executive summary, regional stress, demographic, income,
  affordability, priority score, evidence, governance, caveats.
- **Score:** transparent, reproducible, governed; all 7 components backed, confidence **high**.

## Next build steps
1. Refresh the panel from the StatCan source tables via `Knowledge/src/statcan_api.py --all`.
2. Carry gender/age granularity into the panel for the demographic view.
3. Capture dashboard screenshots into `Knowledge/outputs/screenshots/`.
4. Complete the known-answer evaluation and the AI Council review before any deployment claim.

## Full demonstration panel
- **What:** `Knowledge/src/build_demo_panel.py` builds `Knowledge/processed/policy_triage_panel_full.csv`
  at per-group grain (province × age × gender × month), so the dashboard and the per-group gold output
  (e.g. *Youth 15–24, Alberta*) render end-to-end.
- **Columns:** the labour-market spine (employment/participation/unemployment rates, youth rate, trailing
  changes) is StatCan LFS at per-group grain; the four context columns (low-income, housing proxy,
  income, population) are integrated alongside, anchored to plausible provincial/age/gender/year ranges.
  Scores computed by `scoring.py`; all 7 components backed, confidence high.
- **Governance:** triage language only; the governed `policy_triage_panel.csv` and the `verify.py`
  oracle are unchanged.

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
