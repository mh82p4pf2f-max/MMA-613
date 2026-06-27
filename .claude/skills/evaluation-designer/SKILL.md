---
name: evaluation-designer
description: Build the before-and-after evaluation plan — 5 to 10 known-answer test cases with expected outputs, actual outputs, and accuracy/usefulness/trustworthiness/appropriateness scores. Use when establishing the Day-2 baseline, after revisions to re-measure, or whenever building/maintaining the evaluation. Claude structures the evaluation; humans and the AI Council are the final scoring authority.
---

# Evaluation Designer

## Purpose
Build an evaluation focused on **output quality, not code quality**: a small set of known-answer test cases, run before and after revision, scored by humans against a rubric or source.

## When to use
- Establishing the baseline (before deployment).
- Re-measuring after a revision (the after).
- Designing or maintaining the test set.

## Inputs to read
`CLAUDE.md` (gold example + must-never list), `deliverables/evaluation-plan.md`, the dataset and rubric/source material, the dashboard outputs.

## Procedure
1. Derive **5-10 known-answer test cases** from the gold example and must-never list. Each case has an input and the **expected output a good answer gives**, computed/verified independently.
2. Capture the **actual output** the dashboard/Claude produced for each case.
3. Score each on four dimensions (define the scale, e.g. 1-5, and what each level means): **accuracy, usefulness, trustworthiness, appropriateness**.
4. Add **human review notes** and **AI Council review notes** per case.
5. Run the set **before** revision (baseline) and **after** revision, and produce a **before-and-after comparison**.
6. Recompute numbers independently; review any narrative output by hand. Read the scores for *where output is weak and what to change*, not just the total.

## Output format (per case)
```
Case #:  Input:
Expected output:           Source/how verified:
Actual output (baseline):  Actual output (revised):
Accuracy _  Usefulness _  Trustworthiness _  Appropriateness _
Human review notes:        AI Council notes:
```
Plus a baseline-vs-revised summary table and a deploy recommendation for the Council.

## Guardrails
- **Claude does not grade itself as the final authority.** It structures the evaluation and proposes scores; humans and the AI Council confirm them against the rubric, source, or expected answer.
- Do not use a model to score narrative output — recompute numbers and read narratives by hand.
- Keep the same test set across baseline and revised runs so the before-and-after means something.
