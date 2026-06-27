---
name: governance-risk-auditor
description: Identify governance and safety risks before deployment. Use before demos, presentation prep, AI Council review, and deployment decisions. Checks for hallucinated policies, unsupported recommendations, privacy and bias risks, overreliance, student-facing risk, grade sensitivity, and missing human-review or Council-approval points.
---

# Governance Risk Auditor

## Purpose
Surface risks before anything is shown or shipped, so the AI Council reviews a known risk profile rather than discovering problems live.

## When to use
- Before demos and presentation prep.
- Before an AI Council review.
- Before any deployment decision.

## Inputs to read
`governance/governance.md`, `CLAUDE.md`, the dashboard outputs and Claude-generated summaries, the dataset, the evaluation results.

## Checklist (flag each as OK / Risk / Blocker, with evidence)
- **Hallucinated course policies** — any claim about course rules, deadlines, or expectations not grounded in an approved source.
- **Unsupported recommendations** — advice not backed by data, rubric, or source.
- **Privacy concerns** — sensitive or identifying student information not minimized/anonymized.
- **Bias risks** — outputs that could systematically disadvantage a group; unrepresentative sample read as representative.
- **Overreliance risks** — places a user might treat a claim as fact without checking.
- **Student-facing risk** — any output reaching a student without prior human review.
- **Instructor judgment risk** — anywhere the tool oversteps or substitutes for instructor judgment.
- **Grade / assessment sensitivity** — anything that could affect grades, assessment, or student perception without human approval.
- **Missing human review points** — steps that should route to a human but don't.
- **Missing AI Council approval** — anything heading toward use without Council sign-off.

## Output format
```
Risk register:
  [Area] — OK | Risk | Blocker — evidence — required mitigation — owner
Blockers (must fix before deploy):
Risks accepted in writing (with rationale + who accepted):
Recommended gate status: pass to Council | fix blockers first
```

## Guardrails
- A **Blocker** stops deployment until fixed or explicitly accepted in writing by a human.
- This audit feeds the `ai-council-reviewer`; it does not itself approve deployment.
- When uncertain whether something is a risk, flag it and route to a human.
