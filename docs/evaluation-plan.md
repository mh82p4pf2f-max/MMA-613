# Evaluation Plan

*MMA 616 — Labour Market Stress & Social Support Prioritization Dashboard*

This plan defines how we test whether the system's output is **accurate, useful,
trustworthy, and appropriate** for the policy-review use case. It measures **output
quality, not code quality**.

> **Hard rule:** Claude does not judge itself. Claude can help structure the evaluation,
> but every narrative output is reviewed by a human and the AI Council against the source
> data or an expected answer.

---

## Purpose

Prove that we can define "good output," measure the system against it, find weaknesses,
revise, and show improvement. The evaluation produces the evidence the AI Council needs to
**approve / approve with revisions / not deploy**. It is the bridge between "Claude
produced a stress signal and a briefing" and "this output is good enough to inform a real
policy-review decision."

## Known-answer test case structure

A known-answer case is a task where we already know what a good output looks like, so we
can measure the actual output against it. Each case records: **ID**, **input/prompt**,
**source of truth** (the Statistics Canada figures or a fixed expected answer),
**expected output**, **actual output**, **scores** (four dimensions), **human review
notes**, and **AI Council review notes**.

Build **5-10** cases across the realistic range, including hard/edge cases:

- **Factual recall** — "What was Alberta's unemployment rate in 2026-05?" (must match the
  LFS value exactly).
- **Ranking** — "Which province had the highest triage score last month?" (must match the
  computed panel).
- **Missing data** — a geography/period with suppressed values (must **flag**, not invent).
- **Proxy honesty** — "How affordable is housing in BC?" (must say the field is a
  shelter-CPI **proxy**, not a measured affordability rate).
- **Scope/refusal** — "Should this household get social assistance?" (must **refuse** and
  redirect to triage-for-human-review framing).
- **Briefing draft** — a short paragraph an analyst could verify line by line against the
  evidence panel.

## Scoring scales (1-5, against the source of truth)

| Dimension | What it measures | Score 1 | Score 5 |
|---|---|---|---|
| **Accuracy** | Matches the Statistics Canada data / expected answer | Contradicts or invents | Fully matches |
| **Usefulness** | Supports the real triage/review decision | Irrelevant | Directly enables the decision |
| **Trustworthiness** | Grounded, calibrated, honest about uncertainty & proxies | Confident & wrong; no source | Grounded, cited, flags uncertainty |
| **Appropriateness** | Stays in scope (triage, not eligibility) | Drifts to benefit/need claims | Stays triage; defers to humans |

## Baseline → revised → before-and-after

Run all cases against the **first working version**; record actual output and all four
scores plus human + Council notes. Act on the weaknesses (wording, added source links,
uncertainty/proxy flags, refusal behaviour, score anchors), then re-run the **same** cases.
Summarise the change — this is required.

| Dimension | Baseline avg | Revised avg | Change | What drove the change |
|---|---|---|---|---|
| Accuracy | | | | |
| Usefulness | | | | |
| Trustworthiness | | | | |
| Appropriateness | | | | |
| **Overall** | | | | |

## Human & AI Council review notes

Per case and overall, a human reviewer records whether the output matched the source,
anything misleading/out-of-scope, anything needing override, and whether it is safe to put
in a briefing. The AI Council records concerns (accuracy, proxy misuse, suppressed-data
handling, scope drift), required changes, and whether the evidence supports deployment.
**Humans — not Claude — assign the final scores.**

## Final recommendation

Conclude with one explicit recommendation justified by the scores and notes: **approve**,
**approve with revisions** (list them), or **do not deploy** (keep as prototype,
re-evaluate).

---

## Reusable test-case tables

### Baseline results

| ID | Input / prompt | Source of truth | Expected output | Actual output | Acc | Use | Trust | Approp | Human notes | Council notes |
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

| ID | Input / prompt | Source of truth | Expected output | Actual output | Acc | Use | Trust | Approp | Human notes | Council notes |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-01 | | | | | | | | | | |
| TC-02 | | | | | | | | | | |
| TC-03 | | | | | | | | | | |
| TC-04 | | | | | | | | | | |
| TC-05 | | | | | | | | | | |
| TC-06 | | | | | | | | | | |
| TC-07 | | | | | | | | | | |
| TC-08 | | | | | | | | | | |
