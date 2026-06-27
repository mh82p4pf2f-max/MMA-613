# Dashboard Requirements — Build

*MMA 616 · Stage: BUILD.* For each view: what it shows, why it matters, the decision it
supports, the data behind it, what Claude contributes, what a human must review.

| View | Shows | Decision it supports | Data | Claude contributes | Human reviews |
|---|---|---|---|---|---|
| 1 Executive summary | Top areas by triage score + caveat | Where to start | panel | optional briefing draft | verifies before use |
| 2 Regional stress | Score + unemployment trend by geo | Which regions to review | LFS | — | reads trend |
| 3 Demographic vulnerability | Youth vs overall; gender/age | Which groups to review | LFS (pending granularity) | — | scope caveat |
| 4 Income context | Income/wages (annual) | Distinguish stress from income vulnerability | income tables (pending) | — | annual-context label |
| 5 Affordability pressure | Shelter-CPI YoY (**proxy**) | Cost-pressure context | CPI (pending) | — | proxy label |
| 6 Priority score | Score + explanation + confidence | Rank review priority | derived | explanation text | checks drivers |
| 7 Evidence panel | Values + source per flag | Defend a flag | panel + sources | — | confirms source |
| 8 AI Council status | approve / revisions / do not deploy | Deployment gate | governance | — | Council decides |
| 9 Caveats | Limitations | Avoid misuse | metadata | — | sign-off |

## Non-functional requirements
- Caveat banner visible on the summary; "triage, not eligibility" stated.
- Missing data shown as "data pending", never zero-filled.
- Proxies labelled on every affordability view.
- Source traceable from the dashboard (panel now carries `source_*` fields).

> **Governance.** This is a *triage* tool: it flags where to prioritise human policy review. It does **not** determine social-assistance need, eligibility, or benefits, and never operates on individuals. Claude outputs are claims, not facts; missing data is flagged, never invented; the AI Council reviews interpretations before deployment.
