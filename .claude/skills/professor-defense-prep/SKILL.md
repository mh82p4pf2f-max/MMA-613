---
name: professor-defense-prep
description: Prepare the team for capstone Q&A by generating tough professor-style questions and drafting strong, concise answers. Use before the presentation and the defense. Pressure-tests whether the project was worth building, whether the user/decision/evaluation hold up, and whether governance is meaningful rather than performative.
---

# Professor Defense Prep

## Purpose
Anticipate the hardest questions a rigorous examiner would ask, and draft a strong, concise, evidence-backed answer to each — so any member can field any question.

## When to use
- Before the capstone presentation and during defense prep.

## Inputs to read
All `deliverables/`, `governance/governance.md`, the deployment log, evaluation results, `CLAUDE.md`, `knowledge/assignment/assignment-brief.md`.

## Question bank (generate tough versions of each, then answer)
- Why was this worth building? What decision does it actually change?
- Is the user specific enough, or is this "students/instructors" in general?
- Does the dashboard support a real decision, or is it a pile of charts?
- Is the AI Council process meaningful, or performative theater?
- Does the evaluation actually prove anything? How do you know the output is right?
- Is Claude overstepping instructor judgment anywhere?
- What failed during deployment, and what did you learn?
- What would you improve next, and why didn't you do it now?

## Procedure
1. For each question, write the sharpest version an examiner would ask.
2. Draft a concise answer (3-5 sentences) grounded in specific evidence (a number, an episode, a Decision Log entry, a spec line).
3. Flag any question the team currently cannot answer well — that's a gap to close before the talk.
4. Note which member owns which answer, but ensure every member can speak to the whole.

## Output format
```
Q: <tough question>
A: <concise, evidence-backed answer>
Evidence cited:
Owner / who can answer:
Gap to close (if any):
```

## Guardrails
- Answers must cite real evidence, not assertions; if there's no evidence, say so and treat it as a gap.
- Be honest about weaknesses and remaining risks — a defensible "here's the limit and why" beats overclaiming.
