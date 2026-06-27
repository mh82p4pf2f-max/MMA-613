# Build Log — Build

*MMA 616 · Stage: BUILD.* Newest first.

| Date | What was built | Result |
|---|---|---|
| 2026-06-26 | **Synthetic demo bridge** — `Knowledge/synthetic/` (generator `Knowledge/src/generate_synthetic_demo.py`) | Per-group scored panel (36,517 rows, 2015–2026) + long extract (596,501 rows); real panel left untouched; clearly labelled, never for decisions |
| 2026-06-26 | Course-facing `00_course_artifacts/` layer + HTML mockup | Project legible as MMA 616; dashboard untouched |
| 2026-06-26 | Panel audit + added source/frequency provenance columns | Panel traceable; verdict READY WITH MINOR FIXES |
| 2026-06-26 | Cleaned LFS → `labour_force_clean.csv`; scored panel → `policy_triage_panel.csv` | 6,655 rows, 1976-01→2026-05; score validated |
| 2026-06-26 | `Knowledge/src/` modules (statcan_api, data_cleaning, scoring, utils) + `Knowledge/notebooks/` 00–05 | Reproducible pipeline |
| 2026-06-26 | Streamlit dashboard `dashboard/app.py` (9 views, governed) | Reads the panel; runs locally |

## Current state
- **Dashboard reads:** `Knowledge/processed/policy_triage_panel.csv` (via `ROOT/Knowledge/processed`).
- **Working views:** executive summary, regional stress, priority score, evidence, governance,
  caveats. **Pending data:** income, demographic, affordability views (source tables not yet
  downloaded).
- **Score:** transparent, reproducible, governed; confidence capped at medium until context
  data lands.

## Next build steps
1. Run `Knowledge/src/statcan_api.py --all` on a networked machine to populate the 4 empty columns.
2. Carry gender/age granularity into the panel for the demographic view.
3. Capture dashboard screenshots into `Knowledge/outputs/screenshots/`.
4. Complete the known-answer evaluation and the AI Council review before any deployment claim.

## Synthetic demonstration data (prototype bridge)
- **Why:** the 4 context columns (low-income, housing proxy, income, population) are NaN in the real
  panel until their StatCan tables download, capping confidence at medium and blocking the per-group
  gold output. To demo the dashboard end-to-end now, a **clearly-labelled synthetic** dataset was
  built in `Knowledge/synthetic/` — see `README_SYNTHETIC.md`.
- **What's real vs fake:** the labour-market spine (employment/participation/unemployment rates, youth
  rate, 12-mo changes) is **real** StatCan LFS at per-group grain; only the 4 context columns are
  **simulated** (seeded, anchored). Scores computed by the real `scoring.py`.
- **Governance guardrails:** writes only to `Knowledge/synthetic/`; the real
  `Knowledge/processed/policy_triage_panel.csv` is untouched (still 6,655 rows, context columns still
  100% NaN); every row carries `is_synthetic=True` + a provenance string; every `score_explanation`
  is suffixed `[SYNTHETIC DEMO DATA …]`. **Must not** be merged into the real panel, presented as
  StatCan-sourced, or used for any decision / AI Council sign-off.

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
