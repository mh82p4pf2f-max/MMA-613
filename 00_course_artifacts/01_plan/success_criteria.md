# Success Criteria — Plan

*MMA 616 · Stage: PLAN*

The project succeeds when the system is judged **accurate, useful, trustworthy, and
appropriate** for the policy-review use case — by humans and the AI Council, not by Claude.

| # | Success criterion | How we test it |
|---|---|---|
| 1 | **Accurate** — figures match the Statistics Canada source | Known-answer tests vs the source table |
| 2 | **Useful** — supports the real triage decision | Analyst can rank and justify where to review first |
| 3 | **Trustworthy** — grounded, calibrated, honest about uncertainty & proxies | Missing data lowers confidence; proxies labelled |
| 4 | **Appropriate** — stays triage, never eligibility/benefits | Refusal + safe-language tests pass |
| 5 | **Transparent** — the score is explainable to a professor in plain language | Weights, anchors, and drivers documented & reproducible |
| 6 | **Governed** — human review points defined; AI Council gate before deployment | Review Packet + Decision Log completed |
| 7 | **Evidence-based** — every claim references its source | Source fields + data_sources.md |

## Quantitative bar (current build)
- Triage score reproducible to the decimal (independently re-computed: ✓).
- `geo + ref_date` a unique key, zero duplicates (✓).
- Missing inputs reduce `score_confidence`, never silently filled (✓).
- ≥ 5 known-answer evaluation cases passing before any deployment-ready claim (pending).

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
