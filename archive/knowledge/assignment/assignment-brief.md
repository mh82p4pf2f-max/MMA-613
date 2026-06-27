# ASSIGNMENT.md — MMA 616 Group AI Project (Official Brief + Compliance Checklist)

> **Why this file exists.** This is the faithful, organized capture of the **official assignment brief** (source: `MMA 616 - Group AI Project vF.pdf`), paired with a **requirements compliance checklist** that maps every graded item to our *Governed Claude in the Classroom* project. Claude reads this alongside `CLAUDE.md` at the start of every session to make sure the build stays inside what is actually graded — not just what our concept describes.
>
> **Rule of priority:** Where our concept and the brief seem to diverge, the **brief wins on what must exist** (a working, deployed dashboard on a connected data source). Our AI Council governance layer is *how we satisfy and exceed* the "human review and override" expectation — it does not replace the dashboard requirement.

---

## Part 1 — The Official Assignment (faithful capture)

### Overview

The group project runs across the four course days plus the gap week between Days 2 and 3, ending on **Day 4 (July 4)** with a capstone presentation. In teams of **four or five**, you build a working dashboard on a data source you choose, put it to use for a week, evaluate how it performed, and present the result. You work in **Claude Code throughout**, with a **`CLAUDE.md` file as the project's specification**.

The project applies the four-step method taught in the course — **Plan, Build, Use, Evaluate** — end to end on a problem your team chooses.

- **Weight:** 40% of the course grade
- **Format:** one shared deliverable per team
- **Presentation:** ~20 minutes plus Q&A on Day 4 (July 4)

### What you build

A **dashboard built on a data source** — real or synthetic — that turns it into the views, metrics, and comparisons a specific user needs to make a decision. The data is the raw material; the value is in what the dashboard **makes visible and decidable**. A good project is one where someone would actually open the dashboard to make a decision or get work done.

You build it in an **agentic workspace**: a Claude Code project governed by a `CLAUDE.md`, with the data connected as a real source and Claude Skills, subagents, and workflows used where they help. The workspace is *how* you build the dashboard, not a layer inside it, and you walk us through it in the presentation.

The project is graded on **judgment rather than capability**: whether the dashboard is worth building, whether it shows what you said it would, and whether you can show that it does. **A working, deployed dashboard is required.** Going further with the agentic workspace (Claude Skills, subagents, APIs, MCP connectors, custom workflows) is rewarded where it serves the project.

### Choosing the opportunity

Decide what is worth building **before** settling on a dataset. Ask who the user is, what decision the dashboard supports, and why a dashboard is the right tool. Settle on one dashboard concept, then check whether the data it needs is available and workable. Starting from a menu dataset is fine, as long as the **user and decision drive the choice** rather than the features the data happens to support. The most common failure is a clever build with no clear user and no clear decision.

### Deliverables and timeline

| Stage | When | Deliverable |
|---|---|---|
| **Plan** | Day 1 (Fri Jun 26) | Project `CLAUDE.md`: objective, scope, the shape of your data, and success criteria specific enough to test later. |
| **Build** | Day 2 (Sat Jun 27) | A **deployed dashboard prototype** and an **evaluation baseline** — a small set of known-answer test cases and a way to check the dashboard's output against them. |
| **Use** | Gap week | A **deployment log**: what you ran, what worked, what fell short, what you corrected, and how others reacted. |
| **Evaluate** | Day 3 (Fri Jul 3) | A **deployment assessment** with before-and-after evaluation results, and a **revised `CLAUDE.md`**. |
| **Present** | Day 4 (Sat Jul 4) | The capstone presentation and the final submission. |

The **final graded submission** is the version handed in at the end of Day 4, after acting on the feedback received that afternoon.

### The deployment week

The week between Day 2 and Day 3 is for **real use, not a rehearsal**. Use the dashboard to do the work you built it for, and keep a short log: where output was useful, where it fell short, what you overrode and why, and how anyone you showed it to responded. One week will not produce statistics, and the project is **not graded on how much you used it** — record the episodes that taught you something and what each revealed about the dashboard's output.

### Building your own evaluation

Because a single week is thin evidence, you build your own test of the **output, not the code**: are the views and answers useful and accurate for the decision the dashboard supports? Assemble a small set of test cases paired with the output a good answer would give, plus a way to check against them — **recomputing the numbers independently, and reviewing any narrative output yourself rather than having a model score it.** Measure a **baseline on Day 2**, make improvements, and **measure again after the Day 3 revision** to show the difference. The score matters less than what it tells you about where output is weak and what to change.

### The capstone presentation

~20 minutes to present, ~10 minutes of questions. Two anchors:
1. **Walk through the agentic workspace** and the reasoning behind it — the `CLAUDE.md` spec, how you connected and curated the data, and the Skills, subagents, and workflows you built and why each earns its place.
2. **Live demonstration of the dashboard.**

Around those anchors, cover the opportunity (who it serves, what decision it supports), the deployment week, evaluation results before and after, and what you would do next. **Every team member presents part of the talk, and any member may be asked any question.** Time is enforced — rehearse. Bring a recording/screenshots as backup, but the **live demo is the point**.

### Assessment (six components, 40% of course grade)

| Component | Weight | What it covers |
|---|---|---|
| **Opportunity and creativity** | 20% | A clear user and decision, and judgment about what decision the dashboard serves — rather than a project built around whatever data was at hand. |
| **Specification (the `CLAUDE.md`)** | 15% | A usable spec: objective, scope, what is out of scope, the data, and **testable success criteria, revised as the project develops**. |
| **Data and context** | 10% | Data **connected directly** (file, tool, API, or connector) rather than pasted in, kept relevant and current, with the dashboard's output grounded in it. |
| **The build** | 30% | A **working, deployed dashboard**, and how well you used the agentic workspace to build it: skills, subagents, workflows, and connectors used where they help. |
| **Evaluation and governance** | 15% | A real test of the output with before-and-after results, a deployment log read for what it reveals, and **sensible human review and override points**. |
| **Presentation and defense** | 10% | A clear, well-paced presentation, a reasoned walkthrough of the agentic workspace, a working dashboard demonstration, and accurate Q&A answers from every member. |

Grading notes: assessed on **what the dashboard does and whether you can stand behind it, not code elegance**. Limited use in one week is not penalized; what you learned is. A deployed dashboard is the baseline; building beyond it is rewarded where it serves the project. **All team members receive the same project grade**; individual accountability comes through Q&A and **confidential peer-contribution ratings**.

### Choosing your data

Use any source, real or synthetic. A good dataset gives a dashboard **something worth showing for a real user**. Look for:
- A real user and a decision the dashboard supports.
- Enough substance for an insightful dashboard, not a single chart — multiple dimensions, categories, time, or several related tables.
- Data you can **connect** and that is documented, so the workspace reads the **live source** rather than a pasted fragment.
- A scale workable in a week, without a heavy sign-up process.

**Government of Alberta open data is allowed** and is good practice for the individual final's portal. **Your individual final must use a *different* GoA dataset and a *different* problem than your group's.** If no public dataset fits, you may generate **synthetic data** matching the structure you need — but **say in `CLAUDE.md` what is synthetic and what that means for the claims the dashboard can make.**

### Dataset menu

Most strong dashboards take one of four forms — **choose the kind of dashboard first, then find data**:
- **Operational / monitoring** — tracks a live feed, shows current status, flags what's off.
- **Exploratory / analytical** — lets a user slice and compare across dimensions to find patterns.
- **KPI / briefing** — headline metrics and trends for a decision-maker, numbers that matter up top.
- **Comparison / benchmarking** — ranks or compares units, periods, or categories against each other or a norm.

Five public datasets to start from:
1. **Calgary 311 Service Requests** (municipal operations) — 2.6M requests since 2012, API-updated. City ops lead watches volumes by ward/category, sees backlogs, spikes flagged vs. recent norm.
2. **Edmonton Building Permits** (municipal development) — ~236K permits since 2009, with construction value and location. Developer/econ-dev analyst sees where activity is picking up by area and quarter.
3. **Alberta Historical Wildfire Data, 2006–2025** (provincial risk) — every recorded fire with cause, size, location, weather, suppression; published data dictionary. Risk/emergency analyst compares this season vs. 10-year norm by cause and region.
4. **Calgary Restaurant Inspections** (municipal public health) — facilities, inspection dates, violations. Inspector sees violations by severity and a re-inspection priority view; consumer checks a venue's history.
5. **Statistics Canada Labour Force Survey** (federal economics) — monthly labour-market data by industry, occupation, demographics; CSV, API, microdata. Economist/policy analyst tracks latest release vs. prior months.

Other sources: **Canadian** — Open Alberta, Open Edmonton, Open Calgary, Statistics Canada, Open Government Canada. **International** — CFPB Consumer Complaints, SEC EDGAR, World Bank, OECD, Our World in Data, data.gov, NYC Open Data. **Text/ratings** — Yelp Open Dataset, Olist e-commerce, MovieLens, Amazon Reviews. **Catalogues** — Kaggle, Hugging Face, Google Dataset Search. (Links current as of June 2026; confirm a source before relying on it. Instructor can help scope a dataset on Day 1.)

### Teams and logistics

- **Teams:** four or five students; one shared dashboard and submission.
- **Schedule:** Days 1–2 — **Fri Jun 26 & Sat Jun 27**; deployment week; Days 3–4 — **Fri Jul 3 & Sat Jul 4**. 9:00 a.m.–5:00 p.m., room **ESB-236**.
- **Tools:** Claude Code throughout. `CLAUDE.md` is the specification and the way you direct the build.
- The instructor builds a parallel project on the **STEP family business survey** to demonstrate the method live.

---

## Part 2 — Requirements Compliance Checklist

Status key: ✅ done · 🟡 in progress / drafted · ⬜ not started · ⚠️ risk or gap to resolve.

### A. Required deliverables by stage

| # | Requirement | Maps to | Status | Notes |
|---|---|---|---|---|
| A1 | `CLAUDE.md` with objective, scope, shape of data, testable success criteria (Plan / Day 1) | Spec (15%) | 🟡 | `CLAUDE.md` exists as living spec. **Confirm it names a concrete dataset, its shape, and success criteria specific enough to test.** |
| A2 | **Deployed dashboard prototype** (Build / Day 2) | The build (30%) | ⬜ | Core requirement. Nothing built yet — only specs/docs exist. This is the single biggest open item. |
| A3 | **Evaluation baseline**: known-answer test cases + a way to check output (Build / Day 2) | Eval & gov (15%) | 🟡 | `docs/evaluation-plan.md` defines structure; **baseline must be measured against a built dashboard on Day 2.** |
| A4 | **Deployment log** from real use (Use / gap week) | Eval & gov (15%) | ⬜ | Cannot start until the dashboard is deployed and used for real. |
| A5 | **Deployment assessment** + before/after results + **revised `CLAUDE.md`** (Evaluate / Day 3) | Eval & gov (15%) | ⬜ | Day 3 deliverable; depends on A3 baseline + A4 log. |
| A6 | Capstone presentation + final submission (Present / Day 4) | Presentation (10%) | ⬜ | Build around the 16-beat story in `docs/project-memory.md`. Every member presents. |

### B. Graded components — coverage check

| Component (weight) | What graders want | Status | Gap to close |
|---|---|---|---|
| **Opportunity & creativity (20%)** | One clear primary user + one clear decision the dashboard serves; user/decision drove the dataset, not vice versa. | ⚠️ | **Lock exactly one primary user and one decision.** `project-memory.md` still lists candidate problems — pick one and commit. |
| **Specification — `CLAUDE.md` (15%)** | Objective, scope, out-of-scope, data, **testable** success criteria, revised as project develops. | 🟡 | Add/confirm: named data source + its shape; success criteria phrased as pass/fail tests; keep a revision log. |
| **Data & context (10%)** | Data **connected directly** (file/tool/API/connector), current, output grounded in it. | ⚠️ | **Choose and connect a real or synthetic dataset.** Pasted fragments lose marks. If synthetic, state so in `CLAUDE.md` and what it limits. |
| **The build (30%)** | A **working, deployed dashboard**; agentic workspace (skills, subagents, workflows, connectors) used where it helps. | ⬜ | Highest weight. Must produce a multi-view dashboard a user would actually open. |
| **Evaluation & governance (15%)** | Real output test, before/after results, deployment log read for insight, sensible **human review & override** points. | 🟡 | Our **AI Council** is a strong fit for the "human review & override" expectation — make sure it gates a real, evaluated dashboard, not just docs. |
| **Presentation & defense (10%)** | Clear talk, workspace walkthrough, **live demo**, every member answers Q&A. | ⬜ | Rehearse to time; live demo is the point; bring screenshot/recording backup. |

### C. Constraints and rules to honor

- ⬜ **Team of 4–5 students**, one shared deliverable.
- ⚠️ **A working, deployed dashboard is mandatory** — governance docs do not substitute for it.
- ⚠️ **Connect the data live** (file/tool/API/connector), do not paste fragments. Keep it current.
- ⚠️ **If using synthetic data, declare it in `CLAUDE.md`** and state what it means for the dashboard's claims.
- ⬜ **Evaluation is output-quality, not code.** Recompute numbers independently; review narrative output by hand — **do not have a model score itself** (consistent with our governance rule that Claude does not judge itself).
- ⬜ **Baseline on Day 2, re-measure after Day 3 revision**; show the before/after delta.
- ⬜ **Built in Claude Code throughout**, directed via `CLAUDE.md`.
- ⬜ **Every member presents**; any member may field any Q&A question; **confidential peer ratings** apply.
- ℹ️ **Individual final note:** must use a *different* GoA dataset and a *different* problem than this group project — avoid burning your preferred GoA dataset/problem here.

### D. Alignment flags — our concept vs. the brief

These are the points where *Governed Claude in the Classroom* must be checked against what is actually graded:

1. **"Dashboard on a data source" is the deliverable.** ⚠️ The brief grades a working dashboard built on a connected dataset. Our concept must resolve to a concrete dashboard with a real/synthetic data source feeding multiple views — not only a governance and review apparatus. **Action: name the dataset and the views it powers.**
2. **The AI Council is our governance edge, not a substitute.** It maps cleanly to "sensible human review and override points" in Evaluation & governance (15%) and strengthens the story — but it sits *on top of* the dashboard requirement.
3. **Pick one user + one decision now.** ⚠️ Opportunity & creativity (20%) penalizes a clever build with no clear user/decision. Our docs still list candidate problems; converge on one.
4. **Success criteria must be testable.** The Spec component rewards criteria "specific enough to test later" — phrase them so a known-answer test case can pass or fail them.
5. **Data must be live-connected.** ⚠️ A classroom-intelligence concept can drift toward hand-curated example content; the brief explicitly rewards a documented, connected, current source.

---

## Part 3 — Key dates (this cohort)

| Date | Day | Milestone |
|---|---|---|
| **Fri Jun 26** | Day 1 | **Plan** — `CLAUDE.md`: objective, scope, data shape, testable success criteria. *(Today)* |
| **Sat Jun 27** | Day 2 | **Build** — deployed dashboard prototype + evaluation baseline. |
| Jun 28 – Jul 2 | Gap week | **Use** — real deployment + deployment log. |
| **Fri Jul 3** | Day 3 | **Evaluate** — deployment assessment, before/after results, revised `CLAUDE.md`. |
| **Sat Jul 4** | Day 4 | **Present** — capstone (~20 min + ~10 min Q&A); act on feedback; **final submission by end of day**. |

Location: ESB-236, 9:00 a.m.–5:00 p.m.

---

*Source: `MMA 616 - Group AI Project vF.pdf` (instructor brief). This file captures the official requirements; `CLAUDE.md` and `docs/` capture our team's concept and how we satisfy them.*
