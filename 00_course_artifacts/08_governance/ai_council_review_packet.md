# AI Council Review Packet — Governance

*MMA 616 · Stage: GOVERNANCE.* Prepared before any deployment decision. Check each item.

- [ ] **Project summary** — governed triage dashboard; user; decision.
- [ ] **Data sources** — product IDs, frequencies, geography, limitations, proxies
      (`02_knowledge/`, `Knowledge/metadata/data_sources.md`).
- [ ] **Dashboard view summary** — the nine views (`05_build/dashboard_requirements.md`).
- [ ] **Score methodology** — components, weights, anchors, confidence, missing-data handling
      (`Knowledge/src/scoring.py`, audit §4).
- [ ] **Key Claude outputs** — representative briefing drafts / explanations.
- [ ] **Known-answer test cases** — `07_evaluate/known_answer_tests.md`.
- [ ] **Baseline results** — `07_evaluate/baseline_results.md`.
- [ ] **Revised results** — `07_evaluate/revised_results.md`.
- [ ] **Known risks** — `risk_register.md`.
- [ ] **Human review points** — where a human must check/override.
- [ ] **Data audit** — `Knowledge/metadata/policy_triage_panel_audit.md` (verdict + fixes).
- [ ] **Recommended deployment status** + **final recommendation**.

## Current packet status
Prototype. Data audit complete (READY WITH MINOR FIXES). Evaluation cases drafted, not yet
run. **No deployment decision has been made.**

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
