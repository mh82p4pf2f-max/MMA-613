# Risk Register — Governance

*MMA 616 · Stage: GOVERNANCE.* Risks, likelihood/impact, and mitigations. Review before any
demo or deployment.

| # | Risk | Likelihood | Impact | Mitigation | Status |
|---|---|---|---|---|---|
| R1 | Triage score misread as a "who needs assistance" / eligibility decision | Med | **High** | Caveat banner; governed language; refusal tests (TC-05/07); explanation disclaimer | mitigated, monitor |
| R2 | Shelter-CPI **proxy** read as measured affordability | Med | High | Label "proxy" on every affordability view & in metadata | mitigated |
| R3 | Empty context columns shown as zero / treated as real | Med | High | Show "data pending"; missing_value_flag; never zero-fill | mitigated |
| R4 | Overconfidence — score trusted beyond the data | Med | Med | confidence_flag; confidence capped at medium until context lands | mitigated |
| R5 | Suppressed/missing cells silently filled | Low | High | Never imputed; flagged in cleaning & scoring | mitigated |
| R6 | Demographic claims beyond what the panel holds (gender/age collapsed) | Med | Med | State youth-only limitation; restore granularity before the demographic view | open |
| R7 | Territories absent read as "no stress" | Low | Med | State province-only scope explicitly | mitigated |
| R8 | Claude briefing treated as fact without review | Med | High | Claims-not-facts rule; analyst + AI Council review gate | mitigated |
| R9 | Stale data (source tables not re-pulled) | Med | Med | `statcan_api.py --check` freshness gate; retrieval_date recorded | open |

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
