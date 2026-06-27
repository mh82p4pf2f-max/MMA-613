---
name: ai-council-reviewer
description: Run the AI Council governance review and return Approve / Approve with revisions / Do not deploy, with reasons. Use before anything is treated as deployment-ready — before the Use week, before demos presented as reliable, and before final submission. Structures the review for human Council sign-off; it does not replace human judgment.
---

# AI Council Reviewer

## Purpose
Enforce the governance membrane: nothing is deployed, called reliable, or used in a classroom workflow until reviewed. This skill structures the review and proposes a decision; **the human AI Council makes the final call.**

## When to use
- Before the Use-week deployment.
- Before any demo or claim presented as reliable.
- Before final submission.

## Inputs to read
`governance/governance.md`, `deliverables/ai-council-governance.md`, `CLAUDE.md`, the evaluation results (`deliverables/evaluation-plan.md`), the deployment log, and the dashboard outputs under review. Run the `governance-risk-auditor` and `source-grounding-checker` skills first.

## What to review
Objective & classroom use case · primary user & decision · data sources · `CLAUDE.md` · dashboard views & outputs · Claude-generated summaries/recommendations/classifications · known-answer test cases & results · known risks · human review points · deployment readiness.

## Approval criteria (score each; all must hold to approve)
Accurate · Useful · Clear · Appropriate · Governed · Safe to use · Aligned with scope · Evidence-based.

## Procedure
1. Assemble the **AI Council Review Packet** (project summary; user & decision; data sources; dashboard/feature summary or screenshots; key Claude outputs; known-answer test cases; baseline + revised evaluation results; known risks; human review points; recommended status).
2. Score the system against the 8 criteria, citing the evidence for each.
3. List concerns and the specific changes each requires.
4. Render a recommended decision and explain why.
5. Write a **Decision Log** entry for human sign-off.

## Output format
```
Decision: Approve | Approve with revisions | Do not deploy
Why: <reasons tied to the 8 criteria>
Criteria scorecard: Accurate _ Useful _ Clear _ Appropriate _ Governed _ Safe _ In-scope _ Evidence-based _
Required changes (if any):
Decision Log entry — Date / What was reviewed / Main concerns / Required changes / Final decision / Who approved / Status:
```

## Guardrails
- Claude **does not self-approve**; this output is a recommendation for the human Council to ratify.
- If any criterion fails, the default is "Approve with revisions" or "Do not deploy," never silent approval.
- Record who on the Council signed off; the decision is not final until a human records it.
