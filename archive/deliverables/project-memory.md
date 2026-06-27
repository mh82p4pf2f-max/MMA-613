# Project Memory — Governed Claude in the Classroom

*MMA 616: Managing Intelligence — Group AI Project*

This document is the readable project memory. Any teammate should be able to read it and understand exactly what we are building, for whom, and to what standard — without needing a meeting.

---

## Project title

**Governed Claude in the Classroom** — a governed classroom intelligence system.

## Project purpose

Design, build, use, and evaluate a practical classroom intelligence system in which Claude supports learning, decision-making, and classroom workflows — but **all information, outputs, risks, and evaluation results are reviewed by a human AI Council before anything is deployed.**

The project exists to demonstrate graduate-level judgment in applied AI: scope, human accountability, testable success criteria, and governance. It is **not** a demonstration that "Claude can answer questions." It is a demonstration that we can define good output, test it, find its weaknesses, revise the system, and govern its release.

## Central project question

> **Can Claude be designed, governed, used, and evaluated as a practical classroom intelligence system that improves learning, decision-making, and student support while keeping accountability with human users through an AI Council review process?**

The project must show we understand the difference between **AI capability** and **human judgment**. Claude can generate summaries, recommendations, classifications, and feedback — but we must prove we can define what good output means, test it, identify weaknesses, revise, and have a human governance body approve or reject deployment.

## What we are building

A focused, working **dashboard or classroom-support application** that uses Claude as part of an agentic workspace (Claude Code with a `CLAUDE.md` living specification), built and run through the **Plan → Build → Use → Evaluate** method.

The concept must be **specific** — not a vague "AI classroom assistant." It must have a clear user, a clear decision, a clear dashboard/app structure, and a clear reason it is worth building. Candidate problems the tool may focus on:

- Helping students understand assignment expectations.
- Helping students identify learning gaps before submission.
- Helping instructors see where students are confused.
- Helping teaching teams analyze student questions or feedback patterns.
- Helping students improve prompt quality and study planning.
- Helping students compare their work against a rubric before submitting.
- Helping instructors summarize common themes from class activity or course materials.
- Helping the AI Council review whether classroom AI outputs are accurate, appropriate, and ready for use.

## Target users

Before building anything, the team must lock these down:

- **Primary user** — exactly one of: student, professor, teaching assistant, project team, or AI Council.
- **Secondary users** — anyone else who benefits from or reviews the tool.
- **Decision or workflow supported** — the specific decision the primary user makes, and the task that becomes easier, faster, or better because of the tool.
- **Why it matters** — the classroom pain point solved, and the reason someone would actually open the tool.

## Classroom decision or workflow supported

Define explicitly: *What decision does the primary user need to make, and how does the tool make that decision faster, easier, or better?* This is the spine of the whole project — every dashboard view, evaluation case, and governance check should trace back to it.

## What the dashboard / app should make visible

The dashboard is not a single chart. It should surface the items relevant to the chosen use case, drawn from:

- Confusion patterns
- Assignment readiness
- Learning gaps
- Rubric alignment
- Prompt quality
- Course resource usage
- Feedback themes
- Student progress
- AI Council review status
- Risks or items requiring human review

## Required deliverables

1. **Project Concept** — title; primary and secondary users; classroom problem; decision/workflow supported; why it is worth building; data/course material used; what the dashboard shows; what Claude does in the workflow; what humans still review or decide; how the AI Council reviews outputs before deployment; what deployment means in this classroom context.
2. **CLAUDE.md Specification** — the living spec (see requirements below).
3. **Dashboard / App Requirements** — multiple useful views, each documented (see below).
4. **Agentic Workspace Design** — how Claude Code is used as a workspace, not a chatbot (see below).
5. **Deployment Log** — realistic use, post-Council review (the "Use" stage).
6. **Evaluation** — baseline and revised results with before-and-after comparison (see [evaluation-plan.md](evaluation-plan.md)).
7. **AI Council Review Packet** and **AI Council Decision Log** (see [ai-council-governance.md](ai-council-governance.md)).
8. **Final Presentation** — built around the presentation story below.

## CLAUDE.md specification requirements

The `CLAUDE.md` must be specific enough that another person could open the project and understand exactly what we are building. It should contain: objective; primary user; secondary users; classroom use case; scope; out of scope; data sources; dashboard views; Claude's responsibilities; human review points; AI Council responsibilities; AI Council approval criteria; success criteria; evaluation plan; governance rules; known risks; deployment rules; revision log; AI Council decision log.

## Dashboard / app requirements

The dashboard should include multiple useful views — for example: Summary, Student Readiness, Rubric Alignment, Learning Gap, Prompt Quality, Common Confusion Themes, Recommended Next Actions, Evidence/Source, Human Review/Override, AI Council Review Status, Deployment Readiness, and Risk & Governance.

For **each view**, document the following:

| Field | What to specify |
|---|---|
| What the view shows | The information displayed |
| Why it matters | The reason it earns space in the dashboard |
| What decision it supports | The user action it informs |
| What data powers it | The approved source(s) behind it |
| What Claude contributes | The summary, classification, or recommendation Claude produces |
| What humans must review | The human checkpoint before the output is trusted |
| What counts as a good output | The standard the output is measured against |

## Agentic workspace design

Explain how Claude Code is used as a **workspace**, not just a chatbot. Define:

- **What Claude reads** — the files and data it has access to.
- **What files/data it uses** — the approved sources.
- **What workflows it follows** — the fixed steps for each task.
- **What skills or subagents are useful** — only where they clearly improve the project; do not overbuild.
- **Where Claude can reason** — the open-ended parts.
- **Where the process is fixed** — the steps that must not vary.
- **Where human approval is required.**
- **Where AI Council approval is required.**
- **What Claude is not allowed to decide on its own.**

## Plan → Build → Use → Evaluate

- **Plan** — Define the classroom opportunity, user, decision, data, scope, success criteria, and AI Council governance model. Answer: who is the user; what decision/workflow we support; what problem we solve; what data/course material we use; what good output looks like; what the Council must review before deployment; what is out of scope.
- **Build** — Build the dashboard/app, connect the data, write the `CLAUDE.md`, and establish a baseline evaluation. Define: dashboard structure; data inputs; Claude-supported workflows; review checkpoints; the AI Council review packet; baseline test cases; initial known risks; deployment-readiness criteria.
- **Use** — Deploy in a realistic classroom scenario **only after AI Council review**. Keep a deployment log documenting what was tested, who used it, what worked, what failed, what users found helpful, what required human override, what the Council flagged, what revisions were needed, and whether the tool was approved, approved with revisions, or not approved.
- **Evaluate** — Test whether output was accurate, useful, trustworthy, and appropriate. Include baseline results, revised results after improvement, human review notes, AI Council review notes, a before-and-after comparison, a final deploy recommendation, and updates to `CLAUDE.md` based on what was learned.

## Evaluation requirements

The evaluation focuses on **output quality, not code quality**. It must include: 5–10 known-answer test cases; expected output per case; actual output; accuracy, usefulness, trustworthiness, and appropriateness scores; human review notes; AI Council review notes; and a before-and-after comparison after revisions. **Claude does not judge itself** — humans and the Council review every narrative output against a rubric, source material, or expected answer. Details and templates: [evaluation-plan.md](evaluation-plan.md).

## Quality bar

The strongest version of this project shows: a specific classroom user; a real classroom decision or workflow; a dashboard someone would actually use; a well-written `CLAUDE.md`; connected or clearly structured data; a realistic deployment log; a before-and-after evaluation; clear human review points; a defined AI Council review process; a completed AI Council Review Packet; a clear AI Council Decision Log; a strong presentation story; and a defensible answer to **"Why was this worth building?"** It must feel polished, graduate-level, and practical — never like generic AI hype.

## Presentation story

Prepare the final presentation around this 16-beat arc:

1. The classroom problem we identified.
2. Who the tool serves.
3. The decision or workflow it supports.
4. Why Claude is useful here.
5. Why governance is necessary.
6. How the AI Council review process works.
7. How the agentic workspace was designed.
8. What the dashboard/app does.
9. How we used it in a realistic classroom scenario.
10. What the baseline evaluation showed.
11. What the AI Council flagged.
12. What we changed after testing and review.
13. What improved.
14. What risks remain.
15. Whether the system was approved, approved with revisions, or not approved.
16. What we would build next.

## Style rules

Be direct, specific, and rigorous. Avoid generic AI language and buzzwords unless tied directly to the project. Never say "AI will revolutionize education." Instead, state exactly what Claude helps the classroom user **see, decide, or do**. Always push the project toward a clear user, clear decision, clear classroom workflow, clear dashboard output, clear evaluation, clear governance, clear AI Council review process, and clear deployment criteria. Never let the project collapse into a vague AI assistant, and never describe it as simply "Claude in the classroom."
