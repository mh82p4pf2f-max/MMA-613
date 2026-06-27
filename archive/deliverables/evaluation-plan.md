# Evaluation Plan

*MMA 616 — Governed Claude in the Classroom*

This plan defines how we test whether the system's output is **accurate, useful, trustworthy, and appropriate** for the classroom use case. The evaluation measures **output quality, not code quality**.

> **Hard rule:** Claude does not judge itself. Claude can help structure the evaluation, but every narrative output is reviewed by a human and the AI Council against a rubric, the source material, or an expected answer.

---

## Evaluation purpose

Prove that we can define what "good output" means, measure the system against it, find weaknesses, revise, and demonstrate improvement. The evaluation produces the evidence the AI Council needs to decide whether to **approve**, **approve with revisions**, or **not deploy**. It is the bridge between "Claude can produce something" and "this output is good enough to use in a classroom."

## Known-answer test case structure

A known-answer test case is a question or task where we already know what a good output looks like, so we can measure the actual output against it. Each case records:

- **ID** — short identifier (e.g., TC-01).
- **Input / prompt** — exactly what is given to the system.
- **Source of truth** — the rubric, course material, or dataset the answer must match.
- **Expected output** — what a good answer looks like.
- **Actual output** — what the system actually produced.
- **Scores** — accuracy, usefulness, trustworthiness, appropriateness (see scales below).
- **Human review notes** — what a human reviewer observed.
- **AI Council review notes** — what the Council flagged.

Build **5–10** cases spanning the realistic range of the use case, including a few hard or edge cases (ambiguous input, missing information, out-of-scope requests) so the evaluation surfaces real weaknesses rather than only easy wins.

## Scoring scales

Use a consistent 1–5 scale for each dimension (1 = unacceptable, 3 = borderline, 5 = excellent). Score against the source of truth, not against impressions.

| Dimension | What it measures | Score 1 (low) | Score 5 (high) |
|---|---|---|---|
| **Accuracy** | Does the output match the source material, rubric, or data? | Contradicts or invents content | Fully matches the source of truth |
| **Usefulness** | Does it support the real classroom decision or workflow? | Irrelevant or unusable | Directly enables the user's decision |
| **Trustworthiness** | Is it grounded, calibrated, and honest about uncertainty? | Confident and wrong; no sources | Grounded, cited, flags uncertainty |
| **Appropriateness** | Does it stay within the proper role and scope? | Oversteps instructor/student role | Stays in scope; defers to humans correctly |

## Baseline evaluation

Run all test cases against the **first working version** of the system, before any tuning. Record the actual output and all four scores per case, plus human and AI Council review notes. The baseline is the "before" snapshot — do not fix issues yet; capture them.

## Revised evaluation

After acting on the weaknesses found in the baseline (revised prompts, workflows, dashboard wording, added source links, uncertainty flags, human review points), re-run the **same** test cases. Record the new actual outputs and scores. Keep the cases identical so the comparison is fair.

## Before-and-after comparison

Summarize the change from baseline to revised, per dimension and overall. This is required.

| Dimension | Baseline avg | Revised avg | Change | What drove the change |
|---|---|---|---|---|
| Accuracy | | | | |
| Usefulness | | | | |
| Trustworthiness | | | | |
| Appropriateness | | | | |
| **Overall** | | | | |

Narrate the comparison plainly: what was weak at baseline, what we changed, what improved, and what still needs human review. This is the heart of the presentation's "what we changed / what improved" beats.

## Human review notes

For each case (and overall), a human reviewer records: whether the output matched the source of truth, anything misleading or out of scope, anything that needed a human override, and whether the output is safe to put in front of a student or instructor. Human reviewers — not Claude — assign the final scores.

## AI Council review notes

The AI Council records, per review: main concerns about accuracy, bias, privacy, student interpretation, or overreliance; required changes; and whether the evaluation evidence supports deployment. These notes feed the [AI Council Review Packet and Decision Log](ai-council-governance.md).

## Final recommendation

Conclude the evaluation with one explicit recommendation, justified by the scores and review notes:

- **Approve** — output quality meets the bar across all four dimensions for the defined use case.
- **Approve with revisions** — usable once named changes are made; list them.
- **Do not deploy** — output quality is insufficient; keep as prototype and re-evaluate.

---

## Reusable test-case table template

Copy this block for the test suite. Fill 5–10 rows. Use one table for **baseline** and a second identical table for **revised**, so the before-and-after is auditable.

### Baseline results

| ID | Input / prompt | Source of truth | Expected output | Actual output | Accuracy (1–5) | Usefulness (1–5) | Trust (1–5) | Appropriateness (1–5) | Human review notes | AI Council notes |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-01 | | | | | | | | | | |
| TC-02 | | | | | | | | | | |
| TC-03 | | | | | | | | | | |
| TC-04 | | | | | | | | | | |
| TC-05 | | | | | | | | | | |
| TC-06 | | | | | | | | | | |
| TC-07 | | | | | | | | | | |
| TC-08 | | | | | | | | | | |

### Revised results (after improvement)

| ID | Input / prompt | Source of truth | Expected output | Actual output | Accuracy (1–5) | Usefulness (1–5) | Trust (1–5) | Appropriateness (1–5) | Human review notes | AI Council notes |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-01 | | | | | | | | | | |
| TC-02 | | | | | | | | | | |
| TC-03 | | | | | | | | | | |
| TC-04 | | | | | | | | | | |
| TC-05 | | | | | | | | | | |
| TC-06 | | | | | | | | | | |
| TC-07 | | | | | | | | | | |
| TC-08 | | | | | | | | | | |
