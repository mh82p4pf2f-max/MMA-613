# AI Council Governance

*MMA 616 — Labour Market Stress & Social Support Prioritization Dashboard*

> **Rule of the project:** Nothing is deployed, presented as reliable, or used in a real
> policy workflow until the AI Council has reviewed it.

The AI Council is the **human governance layer**. This document defines what it is, what
it reviews, how it decides, and how its work is documented.

---

## Purpose

The Council reviews all information, outputs, assumptions, risks, and evaluation results
before the dashboard or any Claude-supported workflow is used to inform real policy
review. Its job is to confirm the system is accurate, appropriate, ethical, and aligned
with scope **before** any output is treated as decision-ready — and to keep accountability
with humans, not the model.

## Why governance is required here

A wrong or overconfident labour-market reading is not harmless: it could misdirect scarce
analyst attention, or — if misused — be wrongly cited to justify a benefit decision the
data cannot support. Governance separates **AI capability** from **human judgment**:
Claude computes signals and drafts briefings; the Council decides whether those claims are
good enough, and in-scope, to act on. The single most important boundary: **this is a
triage signal for review, never a determination of who needs assistance.**

## What the Council reviews

- The project objective and the policy use case (triage, not eligibility).
- The primary user and the decision being supported.
- The data sources used and their limitations (incl. the housing **proxy**).
- The `CLAUDE.md` specification.
- The dashboard views and outputs.
- The `policy_review_priority_score` — its **weights, anchors, and explanations**.
- Claude-generated briefing summaries and classifications.
- Known-answer test cases and evaluation results.
- Risks: accuracy, bias, suppressed-data handling, proxy misuse, over-interpretation,
  overreliance, and any drift toward eligibility/benefit language.
- Whether the system is ready to inform review, needs revision, or stays a prototype.

## Approval criteria (all eight must hold)

1. **Accurate** — output matches the Statistics Canada source data.
2. **Useful** — output supports a real policy-review/triage decision.
3. **Clear** — users understand what each view shows and what the score means.
4. **Appropriate** — it stays a triage signal; it does not drift into eligibility, need,
   or benefit determinations, and never operates on individuals.
5. **Governed** — human review points are clearly defined.
6. **Safe to use** — no misleading conclusions; proxies and missing data are labelled.
7. **Aligned with scope** — it only does what the project says.
8. **Evidence-based** — every claim is grounded in an approved source and referenced.

## Deployment rule

> Deployment is not allowed until the AI Council **approves** the system, or **approves it
> with revisions**.

A review ends in exactly one of three outcomes:

- **Approve** — ready to inform the defined policy-review workflow.
- **Approve with revisions** — usable once named changes are made; changes recorded.
- **Do not deploy** — stays a prototype until re-reviewed.

"Deployment" here means: an analyst uses the dashboard/briefing to inform a real
policy-review triage decision — only after Council approval.

## AI Council Review Packet — checklist

- [ ] **Project summary** — governed triage dashboard; user; decision.
- [ ] **Data sources used** — product IDs, frequencies, geography, limitations, proxies.
- [ ] **Dashboard / view summary** — each of the nine views.
- [ ] **Score methodology** — components, weights, anchors, confidence and missing-data
      handling.
- [ ] **Key Claude outputs** — representative briefing drafts / summaries.
- [ ] **Known-answer test cases** — the 5-10 evaluation cases.
- [ ] **Baseline evaluation results** — scores + notes before revision.
- [ ] **Revised evaluation results** — scores + notes after improvement.
- [ ] **Known risks** — accuracy, proxy misuse, suppressed-data handling, scope drift.
- [ ] **Human review points** — where a human must check or override.
- [ ] **Recommended deployment status** + **final recommendation**.

## AI Council Decision Log — template

| Date | What was reviewed | Main concerns raised | Required changes | Final decision | Approved by | Status |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | e.g., baseline dashboard + score | e.g., housing proxy read as affordability | label proxy on every view; cap confidence | Approve / w-revisions / Do not deploy | Name(s) | — |
| | | | | | | |

## Human accountability rules

- **Claude outputs are claims, not facts.**
- **Human users remain accountable** for every final decision.
- **The AI Council must review outputs before deployment.**
- Claude must **cite/reference** the Statistics Canada source behind any output.
- Claude must **not invent** values, suppressed cells, or policy conclusions.
- Claude must **flag uncertainty** and missing/proxy data explicitly.
- Claude must **route to a human analyst** anything that could affect a real decision.
- The system must **never** approve, deny, or reduce benefits, or operate on individuals.
- Use governed language: *elevated stress, requires policy review, possible intervention
  priority, should be reviewed by human analysts* — never *needs social assistance*.

## How to present the governance story

Tell governance as a strength: why a wrong labour-market read has real consequences; how
the Council review works and its eight criteria; what the Council flagged at baseline;
what changed; and the final decision — supported by the Decision Log and a completed
Review Packet as appendix evidence that the process actually ran.
