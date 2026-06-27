---
name: dashboard-product-designer
description: Turn the project concept into a dashboard someone would actually open to make a classroom decision. Use when designing or revising the dashboard's views, information architecture, metrics, and flows. Prevents the dashboard from collapsing into a single chart or a generic interface.
---

# Dashboard Product Designer

## Purpose
Design a multi-view dashboard that makes a classroom decision clearer — not a single chart, not a generic interface. Every view must trace back to the primary user's decision.

## When to use
- After the opportunity is framed and before/while building.
- When the dashboard feels like a pile of charts rather than a decision tool.
- When adding or revising a view.

## Inputs to read
`CLAUDE.md` (objective, data), `data/` (dataset + codebook), `deliverables/project-memory.md` (dashboard view menu), `knowledge/managing-intelligence/managing-intelligence.md` (Ch 4).

## Procedure
1. Restate the primary user, their decision, and the center of gravity.
2. Define the **information architecture**: the small set of views and how they relate (summary then detail; filters that cross-link).
3. For **each view**, document the block below.
4. Define the **user flow** (how a user moves through views) and the **decision flow** (how the views lead to the decision/action).
5. Draw a **scope ladder**: rank views from the one the app cannot ship without, up through nice-to-haves; draw the one-week line low.
6. Note which views need a human-review or evidence/source panel built into the surface.

## Per-view documentation
For each view, specify:
```
View name:
What it shows:
Why it matters:
What decision it supports:
What data powers it (approved source):
What Claude contributes (summary/classification/recommendation):
What humans must review:
What counts as a good output (the standard to score against):
```

Candidate views (use only those that serve the decision): Summary, Student Readiness, Rubric Alignment, Learning Gap, Prompt Quality, Common Confusion Themes, Recommended Next Actions, Evidence/Source, Human Review/Override, AI Council Review Status, Deployment Readiness, Risk & Governance.

## Guardrails
- A view that answers a question nobody asked is cut, however pretty.
- Show sample sizes; flag/suppress small cells; surface caveats where readers encounter them, not in a footnote.
- Output is a design proposal to review with the team, then write into `CLAUDE.md` via the `claude-md-architect` skill.
