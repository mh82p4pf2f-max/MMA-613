# Canadian Social Support & Economic Distress — Policy Context Dossier

> ## ⚠ BACKGROUND CONTEXT ONLY — NOT A SOURCE, NOT DATA
>
> This file is a **secondary research synthesis** (two Gemini deep-research outputs provided by
> the user on **2026-06-26**). **It is NOT a Statistics Canada WDS connected source.** No figure in
> it may be cited as a value, used as a scoring input or driver, or treated as panel data. It is
> **province-only, triage-only** background reading. See [`README.md`](README.md) for the full
> firewall. The connected, scored data lives only in `Knowledge/processed/policy_triage_panel.csv`
> (Canada + 10 provinces, LFS rate indicators + the 0–100 score).

---

## How to use this in the dashboard (the governance firewall)

A three-lens audit (governance-risk, source-grounding, utility) was run over this material on
2026-06-26. Its conclusions:

### Permitted uses (governance-compliant)
1. **Caveats panel — "context layer."** Explain that labour-market signals *alone* understate true
   economic distress, because distress must be read against the welfare wall and the real-dollar
   erosion from capped indexation. This reframes the income/housing **NaN** gap as a *substantive*
   analytical limitation, not just "download pending." Cite as secondary synthesis; never produces a number.
2. **Housing-proxy caveat (reinforce).** Real Alberta rent dynamics and the SHAR rent restructuring
   justify *why* the Shelter-CPI field must stay labelled a **proxy** — an index can diverge sharply
   from the rent shock low-income households actually face. Use to explain the proxy; **do not** import
   any rent percentage or `$220` shock as a dashboard value.
3. **Province-level briefing context.** When a province surfaces in a ranking, a narrative sidebar
   (not the numeric score) may note relevant policy context — e.g. Alberta is mid-transition across
   Bill 32 (2.0% indexation cap), SHAR (rent restructuring), and the CDB clawback. Tag as policy
   context, province-level only, never Edmonton/Calgary, never altering the score.
4. **AI Council scoring rationale.** The emphasis on capped indexation and welfare-wall METRs is
   external grounding *for* keeping the `low_income_rate` (0.15) and `housing_pressure_proxy` (0.10)
   weights and for treating their NaN state as a real confidence reduction. Informs Council
   deliberation; does not pre-decide weights.
5. **"Considered but not used" catalogue.** Maytree welfare incomes, MBM thresholds, the HelpSeeker
   municipal ecosystem, and PBO GBI modelling are richer-but-out-of-scope sources — cataloguing them
   strengthens the project's scope honesty (mirrors `data_sources.md`).

### Ready-to-use caveat lines (governance-safe)
- *"This dashboard scores labour-market signals (unemployment, participation, employment, youth) for
  Canada and the 10 provinces. It does not capture benefit adequacy, clawback mechanics, or the
  real-dollar erosion of social-assistance incomes — factors that secondary policy research indicates
  can substantially deepen distress beyond what labour data shows. Treat the score as a labour-market
  triage signal, not a full distress measure."*
- *"Alberta context (reference, not measured): Alberta is mid-transition across several 2025–2026
  social-policy changes — a statutory 2.0% cap on default benefit indexation (Bill 32), a
  30%-of-gross-income social-housing rent restructuring (SHAR), and a 100% provincial clawback of the
  federal Canada Disability Benefit. These may amplify distress in ways the labour-market score does
  not register. Source: secondary policy synthesis, not a connected StatCan table — for human /
  AI-Council context only."*
- *"The low-income (0.15) and housing-proxy (0.10) components are currently NaN/pending, holding
  confidence at medium (~75%). Policy research suggests these missing layers carry much of the true
  distress signal, so the gap is substantive, not cosmetic."*

### The report's 4 proposed "dashboard integration variables" — verdicts (DO NOT IMPLEMENT as scoring)
The dossier ends by proposing that these be wired into `policy_review_priority_score`. **All are
rejected as scoring logic** — they are recorded here only as *ideas the AI Council could weigh*, and
each fails on current data:

| Proposed variable | Feasible as scoring now? | Why not |
|---|---|---|
| **1. Indexation-deprivation trigger** (auto-escalate score for unattached singles when CPI outpaces the 2.0% cap) | **No** | Needs non-StatCan policy facts (Bill 32 cap, "40% of MBM" baseline), food CPI (not a panel field), a benefit-recipient demographic axis the panel lacks, and would escalate a score off a NaN proxy. *Salvageable only as a non-scoring narrative flag.* |
| **2. Housing-subsidy clawback** (flag working-age disabled in subsidised municipal housing; weight proxy from rent-shock data) | **No** | Requires disability status, housing tenure, and **municipal-level rent** — none in the connected data; municipal = automatic fail. Clearest scope breach of the four. |
| **3. CDB offset** (make logic "neutralize" CDB poverty-reduction; keep disabled distress elevated) | **Partial** | Cannot be score logic (no disability axis, advocacy-sourced facts). Legitimate only as a one-line **caveat** on a future Alberta `low_income_rate` reading: a federal benefit injection may not improve AB low-income figures because the province claws the CDB back. |
| **4. BFE blind-spot proxy** (cross-reference the $7.5B HelpSeeker Edmonton ecosystem / shelter / charity data) | **No** | HelpSeeker data is **Edmonton (city) + non-StatCan** — direct automatic-fail geography, plus a benefit-recipient cohort the panel has no dimension for. Valid takeaway (program-success metrics understate distress) belongs in the caveats narrative only. |

### Do NOT
- Import any **Edmonton/Calgary/CMA** figure into any scored output or evidence panel.
- Use any report number as a dashboard value or to fill a NaN column (violates "every number traces
  to source" + "never invent/impute").
- Implement any of the 4 integration variables as scoring or auto-escalation logic.
- Let eligibility/benefit/need/clawback/"deep poverty"/"crisis" language leak into output (except a refusal).
- Add a disability, household-archetype, or benefit-recipient **axis** to the panel on the basis of
  this report. The connected grain is province × month (Total-Gender / 15+, youth as a column).
- Cite this as a StatCan source or merge it into `data_sources.md` as a connected dataset.

---

## Panel cross-check (grounding note)

Where this report states **labour-market rates**, they happen to agree with our panel because both
ultimately derive from the same StatCan LFS — but **the panel remains the authority and the report is
not the citation.** Verified 2026-06-26 against `policy_triage_panel.csv` at `2026-05`:

| Claim in report | Panel value (2026-05) | Match |
|---|---|---|
| National unemployment 6.6% | Canada U = 6.6 | ✓ |
| National youth (15–24) 13.4% | Canada youth U = 13.4 | ✓ |
| Newfoundland & Labrador unemployment 9.6% | NL U = 9.6 | ✓ |

Everything else in this dossier — **poverty rates, welfare incomes, caseloads, dollar figures, the
"Black youth 23.2%" figure, per-capita spending, budget numbers, program parameters** — is **not in
the panel** and must never be presented as a panel/score value. For the current
`policy_review_priority_score` per province, read `Knowledge/processed/policy_triage_panel.csv`
directly (the panel is the authority) — live scores are deliberately **not** reproduced here so this
quarantined file is never the citation for a score.

---

# PART A — Federal + Alberta synthesis (Report 1)

## A1. The architecture of Canadian social protection and fiscal federalism

The Canadian social safety net is shaped by **fiscal federalism**: under the Constitution, health
care, education, and social programs fall almost exclusively under **provincial** jurisdiction, but
the federal government uses its superior revenue capacity (its **spending power**) to shape these
domains through transfer payments.

- **Canada Assistance Plan (CAP), 1966** — a shared-cost model: the federal government matched ~**50%**
  of eligible provincial expenditures on welfare services, social assistance, and institutional care.
  This open-ended matching grant incentivised provinces to expand safety nets and professionalise
  delivery.
- **1990 "cap on CAP"** — for the three non-equalization-receiving provinces at the time (Alberta,
  BC, Ontario), federal contribution growth was limited to a max of **5%** annually.
- **1995 federal budget** — abolished both CAP and Established Programs Financing (EPF), merging them
  into the **Canada Health and Social Transfer (CHST)**, a single block fund. The shift from
  cost-matching to a block grant meant the marginal cost of every additional welfare dollar fell
  **entirely on provincial treasuries** — precipitating late-1990s provincial welfare reforms
  (reduced rates, stringent conditional eligibility).
- The CHST later split into the **Canada Health Transfer (CHT)** and **Canada Social Transfer (CST)**.
  The CST (nominally: social assistance, early childhood development, post-secondary education)
  operates as an **equal per-capita transfer with virtually no conditionality** — the one statutory
  condition being a prohibition on minimum residency requirements for social-assistance eligibility.
- **Dilution of earmarked social-assistance funding:** federal contributions to social assistance fell
  from **34%** of all federal spending on provincial social transfers in **1993–94** to **13%** by
  **2015–16** — a sustained prioritisation of health over direct poverty alleviation.
- **CST 2025–26 (all of Canada): $17.416 billion** (modest increase, per-capita).

## A2. Macroeconomic expenditure profiles — Consolidated General Government

- **Consolidated General Government (CGG)** — federal + provincial + territorial + local — spent
  **$1,137.1 billion in 2024** (excl. consumption of fixed capital and non-financial asset
  acquisition); second consecutive year above the trillion-dollar threshold first breached in the
  2020 COVID response.
- **Social protection** was the highest functional expense for the CGG: **24.9% ($283.1B)**, ahead of
  **health 23.7%** — the **seventh consecutive year** social protection > health at the national level.
  Growth driven by **direct federal transfers to individuals** (OAS, CPP, EI, settlements), not
  transfers to provinces for welfare.

**Per-capita functional expenditure (Consolidated CGG, 2024, national average):**

| Function | Per capita |
|---|---:|
| Social Protection | $6,805 |
| Health | $6,468 |
| General Public Services | $4,143 |
| Education | $3,370 |
| Economic Affairs | $2,590 |

- **Inverted priorities at the provincial/territorial/local (PTLG) level:** health dominates at
  **34.2% ($258.9B in 2024)** vs **$111.6B** for social protection; hospital services are >two-thirds
  of health expense. So the federal government delivers broad social-protection transfers to cohorts
  (seniors, unemployed, children) while provincial/local governments concentrate on acute health —
  leaving provincial social assistance vulnerable to **fiscal crowding-out**.
- **Debt service:** driven by 2022–23 rate hikes, interest payments rose to **9.0% ($102.6B)** of
  all-government spending in 2024 (8.7% in 2023) — mechanically restricting fiscal space for
  discretionary social supports.

## A3. Federal direct-delivery mechanisms — pensions, employment, disability

- **ESDC** statutory budget: planned gross spending **$208.2B (2025–26) → $218.7B (2026–27)**, mostly
  through "Pensions and Benefits" (universal/broad-based preference over means-tested welfare).
- **OAS + CPP:** **$137B** to **8.5M** seniors and persons with disabilities (2023–24). OAS is
  CPI-indexed quarterly; for **Apr–Jun 2026** the max monthly OAS is **$743.05** (65–74) / **$817.36**
  (75+), with **GIS up to $1,109.85**/mo for single low-income seniors. CPP enhancements continue;
  **YMPE rises to $74,600 in 2026**; new monthly benefits for dependent children of deceased/disabled
  contributors.
- **EI** (social *insurance*, not assistance): 2026 max insurable earnings **$68,900**, max weekly
  benefit **$729**, employee rate **1.63%**; a new **15-week adoption benefit** is being added.
- **Canada Disability Benefit (CDB):** regulations enacted **May 2025**, full rollout following;
  federal investment **$6.1B over six years**; **max $200/mo ($2,400/yr)**; eligibility requires an
  approved **Disability Tax Credit (DTC)** certificate and a recent tax return. Advocates argue $200
  is insufficient to its poverty-reduction goal; efficacy depends heavily on **provincial treatment of
  the income** (see the Alberta clawback, J3).

## A4. The economic & fiscal context of Alberta

- Historically highest GDP per capita; output tied to energy cycles. Economic distress is estimated to
  cost the Alberta economy **$7.1B–$9.5B annually** (downstream health, justice, lost productivity).
- Fiscal swings: **$8.3B surplus (2023–24)** → forecast **$4.1B deficit (2025–26)**, **$9.4B (2026–27)**,
  **$6.9B (2028–29)** — breaking the province's own balanced-budget framework rules.
- Provincial revenues projected to fall from **16.1% of GDP (2024–25) to 15.4% (2026–27)**. Competitive
  tax regime: **8% corporate rate**; new **8% personal bracket for earnings up to $60,000** (~$1.4B/yr
  revenue reduction).
- **2025–26 total expenses ~$79.3B.** Health largest at **$28B (+5.4% YoY)**; K-12 operating **$9.9B**.
- **Ministry of Seniors, Community and Social Services (SCSS): $10.6B (2025–26)** — but the surge is
  largely a machinery-of-government change moving continuing care / home support out of Health into the
  new **Assisted Living Alberta (ALA)** agency (**$3.848B**). Excluding that transfer, core social
  services focus on disability supports, homeless shelters, affordable housing, and income support.

**Major federal transfers to Alberta (provincial treasury):**

| Transfer | 2024–25 | 2025–26 | 2026–27 (proj.) |
|---|---:|---:|---:|
| Canada Health Transfer (CHT) | $6,373M | $6,664M | $6,973M |
| Canada Social Transfer (CST) | $1,971M | $2,089M | $2,197M |
| Equalization | $0 (non-recipient) | $0 | $0 |

Total transfers from Canada ≈ **17.9% of Alberta's total revenue.**

## A5. Alberta's social-assistance architecture & caseload dynamics

Two primary tracks: **Income Support (IS)** and **Assured Income for the Severely Handicapped (AISH)**.
IS is bifurcated into **Expected to Work (ETW)** and **Barriers to Full Employment (BFE)** (chronic
conditions / multiple persistent barriers). AISH is a higher flat-rate allowance requiring medical
evidence of a permanent, severe handicap.

- **2024–25:** avg **134,994 cases** (family units / unattached singles), **+9,871** YoY → ~**4.3%** of
  the under-65 population (~1 in 23 working-age).

| Stream (Alberta) | Avg cases 2024–25 | Avg beneficiaries | YoY caseload growth |
|---|---:|---:|---:|
| Income Support (total) | 57,347 | 98,159 | +15.0% |
| — Barriers to Full Employment (BFE) | 18,188 | 26,681 | +5.0% |
| AISH | 77,647 | (case-specific) | +3.0% |

*Source: Maytree Social Assistance Summaries, fiscal-year averages.*

- The **+15% IS surge** is the third consecutive year of rapid expansion, following CERB-era artificial
  decline — underscoring structural reliance on provincial nets when federal emergency measures recede.
- **Composition:** unattached single adults dominate — **69%** of IS, **78%** of BFE, **86%** of AISH.
  Gender split: unattached singles predominantly male; single-parent recipients overwhelmingly female.
  Largest head-of-household cohort is **age 30–54** across all three (refuting the "youth-transitional"
  assumption).
- **Labour-market attachment is very low** ("welfare wall"): only **4.2%** of IS and **0.4%** of BFE
  cases reported any employment income; **16.5%** of AISH did — suggesting AISH's more generous earnings
  exemptions facilitate participation vs IS's punitive clawbacks.

## A6. Depth of poverty — income adequacy vs the Market Basket Measure (Alberta)

The **Market Basket Measure (MBM)** is Canada's Official Poverty Line. **Deep Income Poverty (MBM-DIP)**
= disposable income **< 75%** of MBM. *(MBM thresholds quoted for Edmonton/Calgary are CMA-level —
**city granularity the panel cannot carry**; recorded as context only.)*

"Total welfare income" aggregates basic provincial assistance + federal/provincial child benefits +
federal credits (GST/HST, Canada Carbon Rebate). For 2024, **every Alberta archetype on assistance
lived below the poverty line**, most in deep poverty:

| Household archetype (Alberta, 2024) | Total annual welfare income | % of poverty line (MBM) | Status |
|---|---:|---:|---|
| Unattached single (employable) | $11,089 | ~27–40% | Deep poverty |
| Unattached single w/ disability (BFE) | $12,714 | 43% | Deep poverty |
| Unattached single w/ disability (AISH) | $23,732 | ~80% | Poverty (above DIP) |
| Single parent (one child, age 2) | $26,770 | ~63% | Deep poverty |
| Couple (two children, 10 & 15) | $39,022 | ~66% | Deep poverty |

*Assumes zero employment earnings across 2024. 2024 MBM (Edmonton reference family) ≈ **$58,876**;
unattached individual ≈ $27,000–$29,000 by CMA. **⚠ CMA-level figures — context only; never a scored
row or driver (automatic fail).***

The employable single's **$11,089** is ~a **$16,000+ annual poverty gap**. Federal credits (GST/HST
~$332.50, Canada Carbon Rebate ~$868) are a crucial but insufficient lifeline; even a single parent
maximising CCB + Alberta Child and Family Benefit (ACFB) sits at ~63% of MBM.

## A7. Inflation, indexation & erosion of purchasing power (Alberta)

- Low-income households spend disproportionately on shelter and food, so they face an **effective
  inflation rate above headline CPI**. In 2025, national annual CPI rose **2.1%**, but five-year
  cumulative inflation reached **19.9%**. Alberta rent surged **12.5% (2024)**, decelerating to **3.8%
  (2025)**. *(These are advocacy/article-level figures — NOT the panel's Shelter-CPI proxy.)*
- **Indexation history (politicised):** linked AISH/IS to cost of living in **2018**, de-indexed in
  **2019**; the 2021–22 inflation shock then cut real welfare incomes. Re-indexed in **2023** (one-time
  **+6.0%**), then **+4.25% (2024)**.
- **Bill 32 (Financial Statutes Amendment Act, Nov 2024):** default statutory cap of **2.0%** on annual
  indexation for nine major programs (incl. AISH, Income Support, Alberta Child & Family Benefit,
  Alberta Seniors Benefit). Cabinet *may* authorise more; if CPI < 2.0%, indexation defaults to the
  lower CPI — an asymmetric risk that mechanically degrades real purchasing power and widens the
  income-vs-MBM gap (a "stealth" real-terms reduction).

## A8. Policy convergence — the welfare wall (Alberta)

Program interactions create punitive **Marginal Effective Tax Rates (METRs)** — the "welfare wall" —
where entering work or receiving an external benefit triggers aggressive clawbacks. Three 2025–2026
Alberta shifts reshape it:

- **A8.1 ADAP (Alberta Disability Assistance Program), July 2026.** Replaces AISH for those deemed to
  have "some work capacity"; enforces labour attachment (mandatory case management, career planning,
  supported placements). Base assistance capped at **$1,740/mo**; earnings exemption **$700/mo** before
  aggressive clawbacks. Advocates warn reassessment could cut incomes by **up to $200/mo** for those
  moved off AISH, penalising fluctuating disabilities. *Maintains health benefits regardless of
  employment income — one positive lowering of the wall.*
- **A8.2 SHAR (Social Housing Accommodation Regulation), phasing Oct 2025–Jan 2026.** Rent for social
  housing / Rent Assistance Benefit (RAB), managed by **municipal** bodies like **Civida**, becomes a
  strict **30% of gross household income**. Removes the historic **$735/mo AISH exemption** → an
  AISH recipient earning $1,901/mo sees rent rise from ~$349 to **$570 (+$220/mo)**, nullifying recent
  benefit increases. From 2027–28, CCB and ACFB also count as eligible income for rent. Every labour
  dollar triggers a 30¢ subsidy cut, stacking with benefit clawbacks. *(Civida/municipal + household —
  city-level locus; quarantined.)*
- **A8.3 CDB clawback.** Alberta designates the federal **CDB as "non-exempt income"** for AISH/IS →
  **100% clawback** (dollar-for-dollar provincial reduction). The federal funds become a **fiscal
  offset for the provincial treasury** rather than net income to the individual — distress for disabled
  populations stays elevated despite the federal announcement.

## A9. Sub-provincial reality — the municipal "shadow state" (⚠ CITY-LEVEL — QUARANTINED)

> **Everything in A9 is Edmonton/Calgary city-level and/or non-StatCan. It must NEVER appear as a
> scored row, driver, or sub-provincial claim — automatic fail. Recorded for narrative understanding
> only.**

A **HelpSeeker** systems-mapping/financial audit for the **Edmonton Police Commission** found:
- ~**$7.5B/yr** circulating in Edmonton's social-support & community-services ecosystem;
  **2,033 entities**, ~**12,900** service elements.
- ~**$3.0B** direct government cash transfers to Edmontonians; registered-charity revenue **$6.1B**
  (**60%** from Government of Alberta grants/contracts), of which **$2.1B** for community/social
  services and **$1.1B** for crisis interventions (poverty/housing/homelessness/addictions).
- Edmonton first responders (Police/Fire/EMS) combined **$782M (2020 budgets)**; addictions/mental
  health **$1.3–1.5B/yr (2019 data)**.
- Only **23% (460 entities)** of flows were traceable — 77% opaque.
- **City of Edmonton 2026** operating budget needs a **6.9%** residential property-tax increase;
  **City of Calgary** estimates a **$14M** shortfall to subsidise its Low-Income Transit Pass (LITP).

This represents a **downloading of poverty costs** from province to municipality and the charitable
sector as provincial benefits erode in real terms.

## A10. Program evaluation, efficacy & GBI modelling

- **Auditor General of Alberta (OAG):** the SCSS Income Support program ensured technical eligibility
  but **failed to measure** whether it met its legislated objectives (basic needs, long-term
  resiliency); removed evaluative targets; and **declined to implement** an MBM-benchmark metric
  comparing average benefits to the cost of living — avoiding statistical accountability for deep
  poverty. Employability tracking shrank to clients in specific **CEIS** programs (~**25%** of the ETW
  cohort) and **ignores the BFE population entirely**.
- **Parliamentary Budget Officer (PBO) — Guaranteed Basic Income (GBI, negative-income-tax model):**
  gross cost **$107B (nuclear family)** or **$53B (economic family)** in 2025; national MBM poverty
  reduction **34% / 40%**; **Alberta 14.4%–39.2%**; behavioural cost ~**1.1–1.4%** fewer hours worked
  nationally; much of gross cost potentially recouped via tax adjustments.
- **U Calgary School of Public Policy:** Alberta could implement a provincial GBI by converting
  non-refundable provincial tax credits to refundable ones — a revenue-neutral restructuring delivering
  a guaranteed annual income **>$6,000** for single adults via the tax system rather than casework.

## A11. Report 1's proposed dashboard-integration variables (recorded; see firewall verdicts above)
1. **Indexation-deprivation trigger** — escalate distress for unattached singles on IS when shelter/food
   CPI outpaces the 2.0% Bill 32 cap.
2. **Housing-subsidy clawback vulnerability** — flag working-age disabled in subsidised municipal
   housing; weight the housing proxy from rent-shock data.
3. **Federal–provincial efficacy gap (CDB offset)** — neutralise CDB's expected poverty-reduction in
   Alberta due to the 100% clawback; keep disabled-population distress elevated.
4. **Demographic blind spots (BFE)** — proxy distress via municipal datasets (the $7.5B HelpSeeker
   ecosystem, shelter/charity access).

---

# PART B — National / cross-province expansion (Report 2)

*Report 2 broadens Report 1 from federal+Alberta to national/cross-province. Province-level content
matches the panel's grain, but remains **secondary, non-StatCan, context-only**.*

## B1. Macro expenditure — regional priorities
- Per-capita **provincial health spending, 2024**: highest **NL $8,026**, **NS $7,252**, **NB $7,036**;
  lowest **AB $5,669**, **ON $5,679**, **PEI $6,150**.
- **Social protection**: provincial-local spending up **5.7%** nationally in 2024 (notable rises in QC,
  BC, ON, MB); **NL and Alberta were the only provinces to report per-capita declines.**

## B2. National poverty baselines & labour-market distress
- **2024 national poverty rate 11.0%** (~**4.5M** people). Seniors **5.4%**; working-age 18–64 **12.6%**;
  **unattached working-age singles 33.3%**; **Indigenous people 17.9%**.
- **Provincial poverty 2024:** **BC 13.0%** and **ON 12.5%** highest; **QC lowest 7.0%**; **NL 11.5%
  (2023)**.
- **Labour (note: rate items match the panel — see cross-check):** national unemployment **6.6%** (May
  2026); **NL 9.6%** (May 2026). Youth (15–24) national **13.4%** (May 2026); **Black youth 23.2%**
  (Feb 2026) *(racialised-youth figure is NOT in the panel)*.

## B3. Cross-Canada welfare incomes & adequacy (2024, vs MBM)
Virtually every unattached single on assistance lived below **MBM-DIP** (<75% of poverty line).

| Group | Notable provincial values (2024) |
|---|---|
| Unattached single (employable) | Adequacy **27%–107%** of poverty line by province. Lowest **NS $9,415**; highest **QC $26,341** (Manpower Training measure, small fraction); **ON $10,455**. |
| Unattached single w/ disability | Most adequate **AB (AISH $23,732)** & **NL ($22,907)**; lowest **AB (BFE $12,714)**. |
| Families with children | Single-parent-one-child highest **PEI $32,320**, lowest **NB $25,604** (lifted by federal CCB). |

## B4. Caseload dynamics by province (2024–25)
- **Ontario:** **654,692** cases (972,979 beneficiaries) = **7.4%** of under-65; Ontario Works **+15%** YoY.
- **British Columbia:** **191,654** cases = **5.6%** of under-65 (Income Assistance stream dominant).
- **Alberta:** **134,994** cases = **4.3%** of under-65; Income Support **+15%**.

## B5. Indexation policy by province
- **Index basic social assistance to inflation:** **ONLY Alberta, New Brunswick, Quebec, Yukon.**
- **Do NOT routinely index:** **Ontario (OW), BC, NL, NS** (and others) → compounding real-dollar cuts
  during inflation.
- Alberta previously re-indexed (+6.0% 2023, +4.25% 2024) but **Bill 32 caps default indexation at 2.0%**.

## B6. The CDB & inter-jurisdictional friction
- **CDB:** rolled out **July 2025**; max **$200/mo ($2,400/yr)** to low-income working-age with a valid DTC.
- **Exempt (no clawback):** **BC, MB, NB, NL, NS, NU, ON, PEI, QC, SK, YT, NWT** — 12 jurisdictions.
- **NL** adds its own provincial disability benefit (up to **$400/mo**) + **$1,200/yr** RDSP contribution.
- **Clawback (non-exempt):** **Alberta is the only province** treating the CDB as non-exempt →
  dollar-for-dollar AISH reduction. *(Point-in-time as of this 2026-06 synthesis — policy can change;
  re-verify before relying.)*

## B7. Alberta case study & welfare wall
High macroeconomic wealth coexisting with structural poverty: **$8.3B surplus (2023–24)** → **$4.1B
deficit (2025–26)**, **$9.4B (2026–27)**. SCSS manages IS + AISH; unattached singles 69% of IS / 86%
of AISH. Welfare-wall shifts: **ADAP** ($1,740 base, $700 exemption), **SHAR** (30% gross, removes $735
exemption, +$220 shock), **Bill 32** (2.0% indexation cap). *(See A8 for detail.)*

## B8. Municipal ecosystem & accountability — Edmonton (⚠ CITY-LEVEL — QUARANTINED)
> Same automatic-fail quarantine as A9.

Edmonton ecosystem ~**$7.5B/yr**: **$3B** direct government cash transfers + **$6.1B** charity revenue
(**60%** from GoA grants); first responders combined **>$782M**. AG of Alberta: IS program lacks
processes to measure basic-needs/resiliency; **refused to benchmark benefits to the MBM**.

## B9. Report 2's proposed dashboard-integration variables (recorded; see firewall verdicts above)
1. **Indexation-deprivation triggers (national)** — differentiate indexing provinces (AB, NB, QC, YT)
   from non-indexing (ON, BC, NL, NS, PEI); escalate score for unattached singles on regional CPI
   spikes; track Alberta's 2.0% cap.
2. **Labour-market stress multipliers** — weight structurally-high-unemployment regions (e.g. NL 9.6%)
   differently; elevate youth / racialised-youth intersections (up to 23.2%).
3. **Federal–provincial efficacy gaps (CDB offsets)** — for 12 exempt jurisdictions CDB is a net gain
   (NL +$400 top-up); for Alberta neutralise expected poverty-reduction (100% clawback).
4. **Housing-subsidy clawback vulnerability** — flag working-age disabled in subsidised municipal
   housing in Alberta (SHAR +$220 shock).

---

## Sources cited by the syntheses (secondary / advocacy / policy — NOT the project's StatCan WDS pipeline)

**Government finance / StatCan publications (articles, not our connected tables):** The Daily —
Government spending by function 2022/2023/2024; Consolidated per-capita spending by CCOFOG, 2024;
Provisional poverty estimates for 2024; Market Basket Measure (MBM) thresholds; Consumer Price Index
Annual Review 2025. **Federal program docs (Canada.ca):** Major federal transfers; ESDC Departmental
Plans 2025–26 / 2026–27; Old Age Security payment amounts; CDB facts. **Alberta government:** Budget
2025/2026 docs, Open Government year-end results, Bill 32, SHAR (Civida FAQ), ADAP materials.
**Advocacy / research bodies:** Maytree (Welfare in Canada 2024, Social Assistance Summaries,
Methodology, Overview of welfare incomes); Parliamentary Budget Officer (Distributional Analysis of a
National GBI); Office of the Auditor General of Alberta (Income Support — Assessment of
Implementation); HelpSeeker (Edmonton Police Commission systems map); C.D. Howe Institute (Mending the
Safety Net); University of Calgary School of Public Policy (An Alberta Guaranteed Basic Income; Income
Support, Inflation, and Homelessness); Policy Options; Canada Without Poverty; ASCHA; Edmonton Chamber
of Voluntary Organizations; Voice of Albertans with Disabilities; CBC News; To Do Canada; PBI Actuarial
Consultants; St. Albert Gazette.

*(Full source lists are preserved in the raw inputs; the two original Gemini outputs are archived in
the session scratchpad.)*

---

## Provenance & change log

| Date | Note |
|---|---|
| 2026-06-26 | Created from two Gemini deep-research syntheses provided by the user (Report 1: federal + Alberta; Report 2: national / cross-province). Stored as quarantined background context under `Knowledge/reference/`. Three-lens audit (governance / source-grounding / utility) run the same day; conclusions folded into the "How to use" firewall. Labour-rate claims cross-checked against `policy_triage_panel.csv` @2026-05 (matched). **Not** added as a StatCan source; **not** AI-Council-reviewed; prototype status unchanged. |
