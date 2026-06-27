# Knowledge Inventory — Knowledge stock

*MMA 616 · Stage: KNOWLEDGE (curate the source)*

The "Knowledge stock" is the curated source material the project is grounded in. **Connect
the source; do not paste fragments.**

| Knowledge asset | Where it lives | Role |
|---|---|---|
| Statistics Canada source tables (8) | `Knowledge/raw/<domain>/` (LFS present; rest pending download) | Primary data |
| Cleaned LFS | `Knowledge/processed/labour_force_clean.csv` | Analysis-ready labour data |
| Dashboard panel | `Knowledge/processed/policy_triage_panel.csv` | The scored dataset the dashboard reads |
| Data sources table | `Knowledge/metadata/data_sources.md` | Product IDs, URLs, frequency, limitations |
| Data dictionary | `Knowledge/metadata/data_dictionary.md` | Every panel field defined |
| Integration notes | `Knowledge/metadata/integration_notes.md` | Joins, frequency, missing-value rules |
| Panel audit | `Knowledge/metadata/policy_triage_panel_audit.md` | Independent QA + readiness verdict |
| Pull/clean/score code | `Knowledge/src/` | Reproducible pipeline |
| Notebooks 00–05 | `Knowledge/notebooks/` | Readable workflow |

See `data_source_summary.md`, `statcan_table_notes.md`, and `data_limitations.md` in this
folder for the curated detail.

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
