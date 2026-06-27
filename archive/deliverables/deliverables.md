# Deliverables — index and status

This is the index of every artifact the project must produce, mapped to the **Plan → Build → Use → Evaluate** method and to the six graded components of the assignment. Use it to see at a glance what exists, what is in progress, and what is outstanding. The detailed requirements live in [../knowledge/assignment/assignment-brief.md](../knowledge/assignment/assignment-brief.md).

Status key: ✅ done · 🟡 in progress / drafted · ⬜ not started.

---

## Deliverables by stage

| Stage | Deliverable | Where it lives | Status |
|---|---|---|---|
| **Plan** (Day 1) | `CLAUDE.md` living spec — objective, scope, data shape, testable success criteria | [../CLAUDE.md](../CLAUDE.md) | 🟡 |
| **Plan** | Project concept (user, decision, why-worth-building) | [project-memory.md](project-memory.md) | 🟡 |
| **Plan** | Curated Knowledge stock (course material, assignment, dataset + codebook) | [../knowledge/](../knowledge) | 🟡 |
| **Build** (Day 2) | **Deployed dashboard prototype** on a connected data source | *(to build)* | ⬜ |
| **Build** | Evaluation baseline — 5–10 known-answer test cases + a way to check output | [evaluation-plan.md](evaluation-plan.md) | 🟡 |
| **Build** | Initial known risks + deployment-readiness criteria | [ai-council-governance.md](ai-council-governance.md), [../governance/governance.md](../governance/governance.md) | 🟡 |
| **Use** (gap week) | Deployment log — episodes, overrides, failures, predicted-vs-observed, outside reactions | *(to produce in Use)* | ⬜ |
| **Evaluate** (Day 3) | Deployment Assessment — before/after results, revised `CLAUDE.md`, improvement plan, spec diff | *(to produce in Evaluate)* | ⬜ |
| **Evaluate** | AI Council Review Packet + Decision Log | [ai-council-governance.md](ai-council-governance.md) | 🟡 |
| **Present** (Day 4) | Capstone presentation + final submission | *(to produce)* | ⬜ |

---

## Mapping to the six graded components

| Component (weight) | Primary evidence | Status |
|---|---|---|
| **Opportunity & creativity (20%)** | Locked single user + single decision in `CLAUDE.md` / project-memory | 🟡 — converge on one |
| **Specification — `CLAUDE.md` (15%)** | Living spec with testable success criteria, revised over time | 🟡 |
| **Data & context (10%)** | A real or synthetic dataset connected live (file/API/connector), grounded output | ⬜ — choose & connect |
| **The build (30%)** | A working, deployed dashboard + agentic workspace (skills, subagents, workflows, connectors where they help) | ⬜ — highest weight |
| **Evaluation & governance (15%)** | Before/after output test, deployment log, human review & override points (our AI Council) | 🟡 |
| **Presentation & defense (10%)** | Clear talk, workspace walkthrough, live demo, every member answers Q&A | ⬜ |

---

## Supporting deliverable documents in this folder

- **[project-memory.md](project-memory.md)** — full project memory: purpose, users, dashboard requirements, agentic workspace design, quality bar, presentation story, style rules.
- **[ai-council-governance.md](ai-council-governance.md)** — AI Council purpose, review scope, approval criteria, deployment rule, Review Packet checklist, Decision Log template.
- **[evaluation-plan.md](evaluation-plan.md)** — known-answer test case structure, scoring (accuracy, usefulness, trustworthiness, appropriateness), before-and-after comparison, reusable test-case table.

> **Reminder from the assignment:** a working, deployed dashboard on a connected data source is **mandatory**. Governance and documentation strengthen the build's evaluation component — they do not substitute for the dashboard.
