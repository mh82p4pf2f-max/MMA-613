# Governance — Governed Claude in the Classroom

This is the single home for the project's governance model: the rules always in force, the AI Council review process, the human review points, and the deployment gates. It is the **governance membrane** from the Agentic Project Design loop — the boundary every input and output crosses under human review. Detailed Council procedure, the Review Packet checklist, and the Decision Log template live in [../deliverables/ai-council-governance.md](../deliverables/ai-council-governance.md).

> **Core principle:** Claude does the work; humans own the outcome. Nothing is deployed, presented as reliable, or used in a classroom workflow until the AI Council has reviewed it.

---

## 1. Governance rules (always in force)

These rules govern how Claude operates inside this project at all times. They are also enforced operationally by the project skills (see [`.claude/skills/`](../.claude/skills)).

1. **Claude outputs are claims, not facts.** Every summary, recommendation, or classification is a claim to check against an approved source.
2. **Humans remain accountable** for every final decision. Claude does not replace instructor judgment.
3. **The AI Council must review outputs before deployment.** No deployment, "reliable" labeling, or live classroom use happens before Council review.
4. **Ground every claim** in the course material, rubric, dataset, or other approved source — and reference that source.
5. **Do not invent** course policies, grades, or instructor expectations.
6. **Flag uncertainty** explicitly rather than presenting it as confidence.
7. **Route to a human** (student, instructor, TA, or Council member) anything that needs manual review.
8. **Minimize or anonymize** sensitive student information.
9. **Any student-facing output must be reviewed** before use.
10. **Anything that could affect grades, assessment, or student perception requires human approval.**

---

## 2. The AI Council review process

The AI Council is the **human governance layer**. Its purpose is to review all information, outputs, assumptions, risks, and evaluation results before the dashboard or any Claude-supported workflow is used with real users. It is not there to slow the project down — it is there to confirm the system is accurate, appropriate, ethical, and aligned with the classroom use case before anything is released.

### What the Council reviews

- The project objective and classroom use case
- The primary user and the decision being supported
- The data sources / course materials used
- The `CLAUDE.md` specification
- The dashboard views and outputs
- Claude-generated summaries, recommendations, or classifications
- Known-answer test cases and evaluation results
- Risks: accuracy, bias, privacy, student interpretation, overreliance
- Whether the system is ready to deploy, needs revision, or should stay a prototype

### Approval criteria (all eight must hold)

A system is approved only when it is judged:

1. **Accurate** — output matches the source material, rubric, or data.
2. **Useful** — output supports a real classroom decision or workflow.
3. **Clear** — users understand what the dashboard shows and why.
4. **Appropriate** — it does not overstep the role of instructor, student, or teaching team.
5. **Governed** — human review points are clearly defined.
6. **Safe to use** — it does not expose sensitive information or create misleading conclusions.
7. **Aligned with scope** — it only does what the project says it should.
8. **Evidence-based** — claims are grounded in an approved source.

### The three possible decisions

- **Approve** — ready for the intended classroom use.
- **Approve with revisions** — deployable once specified changes are made; the changes are listed and verified.
- **Do not deploy** — keep to prototype use; reasons and required changes are recorded.

> Use the [`ai-council-reviewer`](../.claude/skills/ai-council-reviewer) skill to run a structured review and the [`governance-risk-auditor`](../.claude/skills/governance-risk-auditor) skill to surface risks before any review or demo.

---

## 3. Human review points

Every place a human gets the final word, written down in advance:

| Review point | Who reviews | Trigger |
|---|---|---|
| Student-facing output | Instructor or TA | Before any output is shown to a student |
| Grade/assessment-adjacent output | Instructor | Before any output that could affect grades or perception |
| Claude summaries / classifications | Designated team member, then Council | Before being treated as reliable |
| Dashboard deployment | AI Council | Before the dashboard is used with real users |
| Evaluation verdicts | Human + Council | Claude structures the evaluation; it never grades itself as final authority |
| Override of a Claude output | Whoever overrides | Logged with the value the override protected |

---

## 4. Deployment gates

Deployment is staged. A gate is passed only when its condition is met:

1. **Baseline measured** — known-answer test cases run before any classroom use (see [../deliverables/evaluation-plan.md](../deliverables/evaluation-plan.md)).
2. **Risk audit clean (or risks accepted in writing)** — the governance-risk-auditor checklist has been run.
3. **AI Council Review Packet complete** — see [../deliverables/ai-council-governance.md](../deliverables/ai-council-governance.md).
4. **AI Council decision recorded** — approve / approve with revisions / do not deploy, with reasons, in the Decision Log.
5. **Revisions verified** — if "approve with revisions," the changes are made and re-checked before use.

> **No gate may be skipped.** "Deployment" in this classroom context means: the dashboard/workflow is used by its intended user (student, instructor, TA, or team) for a real classroom decision during the Use week — only after the Council approves or approves with revisions.

---

## 5. Where governance evidence lives

- **AI Council Review Packet & Decision Log** — [../deliverables/ai-council-governance.md](../deliverables/ai-council-governance.md)
- **Evaluation results (baseline + revised)** — [../deliverables/evaluation-plan.md](../deliverables/evaluation-plan.md)
- **Deployment log (Use week)** — to be produced in the Use phase; see the [`deployment-log-writer`](../.claude/skills/deployment-log-writer) skill
- **Governance rules in the living spec** — [../CLAUDE.md](../CLAUDE.md)
