---
name: claude-md-architect
description: Create or revise the CLAUDE.md living specification so it stays specific, testable, and aligned with course requirements. Use whenever the project direction changes or the spec needs updating — new user/decision, new data, new dashboard view, or a lesson from Use/Evaluate that must be folded back in.
---

# CLAUDE.md Architect

## Purpose
Keep `CLAUDE.md` a strong, specific, causal living spec — not documentation. Every line should change what Claude does on the next run; if deleting a line wouldn't change behavior, cut it.

## When to use
- The project direction or concept changes.
- A deployment-week episode or evaluation finding must be folded back in.
- The spec has grown vague, bloated, or longer than ~200 lines.

## Inputs to read
Current `CLAUDE.md`, `knowledge/assignment/assignment-brief.md`, `deliverables/project-memory.md`, `governance/governance.md`, `knowledge/managing-intelligence/managing-intelligence.md` (Ch 3).

## Required sections (create or revise each)
- **Objective** — the decision, the primary user, the judgment layer, the center of gravity.
- **Scope** — the smallest version that delivers value + one named stretch layer.
- **Out of scope** — explicit refusals, each tied to a structural reason.
- **Data sources** — point at the codebook/data dictionary; record what one row is, sample representativeness, encoding traps. Note if synthetic.
- **Dashboard views** — the views and what each makes visible/decidable.
- **Claude's responsibilities** — what Claude drafts/classifies/summarizes.
- **Human review points** — where a human gets the final word.
- **AI Council approval rules** — what must be reviewed and the 8 approval criteria.
- **Evaluation plan** — gold example(s) + must-never list, scoring dimensions.
- **Success criteria** — written concretely enough to score (pass/fail).
- **Revision log** — dated entries of what changed and why.

## Procedure
1. Draft/revise each section; write standards concretely ("say 'associated with,' never 'causes'"), not vaguely ("interpret carefully").
2. **Run the Deletion Test** on every line; cut decoration.
3. **Fix position** — move the most load-bearing rules to the start or end.
4. Add emphasis (IMPORTANT / YOU MUST) only where a rule keeps getting missed.
5. Add a dated **revision log** entry.
6. Recommend a **cold read** — have a fresh reader confirm they can state the decision, user, "good," and refusals without asking.

## Guardrails
- Keep it under ~200 lines; bloat makes Claude ignore instructions.
- Do not invent course policies, grades, or instructor expectations.
- The spec is advisory; put any hard guarantees in code (a skill check), not prose.
