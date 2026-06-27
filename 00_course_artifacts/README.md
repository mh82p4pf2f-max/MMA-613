# 00_course_artifacts — MMA 616 Course-Facing Evidence

This folder makes the project legible as an **MMA 616 Agentic Project Design** project,
following the course loop **Plan → Build → Use → Evaluate** and the Day-1 artifacts
(**Knowledge → Living Spec → Mock Deliverable → Governance**). It is the *course-facing* layer;
the *technical* implementation lives in `../Knowledge/` (data, `notebooks/`, `src/`, `outputs/`,
`metadata/`) and `../dashboard`. The living spec itself is the root [`../CLAUDE.md`](../CLAUDE.md);
there is no separate living-spec document.

| Folder | Stage / Artifact | Contents |
|---|---|---|
| `01_plan/` | **Plan** | opportunity brief, user & decision, success criteria |
| `02_knowledge/` | **Knowledge** | inventory, data-source summary, table notes, limitations |
| `04_deliverable_mockup/` | **Mock Deliverable** | mockup notes + `html_mockup/index.html` |
| `05_build/` | **Build** | build log, dashboard requirements, technical notes |
| `06_use/` | **Use** | deployment log, user feedback log (templates) |
| `07_evaluate/` | **Evaluate** | plan, known-answer tests, baseline/revised results, summary |
| `08_governance/` | **Governance** | AI Council governance, review packet, decision log, risk register |

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
