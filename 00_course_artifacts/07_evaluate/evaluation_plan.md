# Evaluation Plan — Evaluate

*MMA 616 · Stage: EVALUATE.* Measures **output quality, not code quality**. Full long-form
version: [`../../docs/evaluation-plan.md`](../../docs/evaluation-plan.md).

## Purpose
Prove we can define "good output", measure against it, find weaknesses, revise, and show
improvement — producing the evidence the AI Council needs to approve / approve with revisions /
not deploy. **Claude does not judge itself.**

## Dimensions (scored 1–5 by humans, against the source of truth)
- **Accuracy** — matches the Statistics Canada data / expected answer.
- **Usefulness** — supports the real triage decision.
- **Trustworthiness** — grounded, calibrated, honest about uncertainty & proxies.
- **Appropriateness** — stays triage, not eligibility.

## Process
Run 5–10 known-answer cases at **baseline**, record actual outputs + scores + human/Council
notes, act on weaknesses, re-run the **same** cases (**revised**), and summarise the
before-and-after. See `known_answer_tests.md`, `baseline_results.md`, `revised_results.md`,
`evaluation_summary.md`.

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
