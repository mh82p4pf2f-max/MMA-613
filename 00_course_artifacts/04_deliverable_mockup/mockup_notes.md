# Deliverable Mockup Notes

*MMA 616 · Stage: MOCK DELIVERABLE (make the spec visible before the full build).*

## What the mockup is
A single-file static HTML mockup of the dashboard, in
[`html_mockup/index.html`](html_mockup/index.html). Open it in any browser — no server needed.
It shows the **intended nine views** with representative (clearly-labelled illustrative)
numbers so the professor and team can see the target before the full Streamlit build is
complete.

## The nine intended views
1. Executive summary (top areas by triage score + caveat banner)
2. Regional labour-market stress (score + unemployment trend)
3. Demographic vulnerability (youth vs overall; gender/age when available)
4. Income context (annual)
5. Housing / affordability pressure (**proxy**)
6. Policy review priority score (transparent, with explanation)
7. Evidence panel (values + source behind each flag)
8. AI Council review status (approve / approve with revisions / do not deploy)
9. Caveats & limitations

## Relationship to the working build
The **live, working** dashboard is the Streamlit app at `dashboard/app.py`, which reads
`Knowledge/processed/policy_triage_panel.csv`. The mockup is the *design intent*; the Streamlit app
is the *implementation*. Views 3–5 in the live app currently show "data pending" because the
income/demographic/affordability source tables are not yet downloaded (see the audit).

## Honesty note
The mockup numbers are illustrative placeholders for layout only — they are **not** real
StatCan values and are labelled as such in the page. Real figures come only from the panel.

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
