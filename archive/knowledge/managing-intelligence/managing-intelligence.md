# Managing Intelligence: Strategic Leadership in the Age of AI

**Authors:** Vern L. Glaser and Jennifer Kotadia
**Alberta School of Business, University of Alberta**
**MMA 616 — Managing Intelligence (2026)**

> *Markdown conversion of the course textbook for reference inside this project. Source: `2026.06.22 - Managing Intelligence.pdf`. Figures are described in captions rather than reproduced. This is a faithful capture of the book's text for grounding our own work; quotations and citations are preserved as in the original.*

---

## About this book

Copyright © 2026 Vern L. Glaser and Jennifer Kotadia. Prepared for MMA 616, Managing Intelligence, Master of Management Analytics, Alberta School of Business, University of Alberta.

This book is organized around one model, **Agentic Project Design**: a loop (Plan, Build, Use, Evaluate) run around a living specification, inside a workspace stocked with knowledge and skills, bounded by a governance membrane that human judgment controls.

The running example throughout, **Kinquiry** — an interactive research workbench built on the SPGC-KPMG Global Family Business Survey 2023-24 — is the instructor's own project. Its figures and mockup screenshots are presented illustratively: the numbers are computed in the project's repository, not published estimates, and the mockups show the method rather than report results.

For permissions and correspondence: vglaser@ualberta.ca

---

## Table of Contents

1. **Introduction** — What is an agent? · What is vibe coding? · Why learn to vibe code? · Agentic Project Design: a method, not a mindset
2. **Part I: Plan**
   - Ch 2 — Knowledge: Setting Up the Workspace and Stocking It
   - Ch 3 — The Living Spec
   - Ch 4 — Deliverables: Mockups and the HTML Prototype
3. **Part II: Build**
   - Ch 5 — Identifying the Agentic Capabilities You Need
   - Ch 6 — Building the Agentic Capabilities
   - Ch 7 — Building the App
4. **Part III: Use & Evaluate**
   - Ch 8 — Use: Putting the Dashboard to Work
   - Ch 9 — Evaluate: Reading the Dashboard Against the Spec
   - Ch 10 — Conclusion: What You Leave With

---

# 1 · Introduction

## 1.1 What is an agent?

For most of its short history, using AI meant asking and answering. You posed a question, a model returned text, and nothing changed in the world until you acted on it. An **AI agent** breaks that pattern. It is software that pursues a goal by reasoning about a situation and acting on it, step by step, rather than answering a single question and stopping.

An agent's autonomy rests on three capabilities it exercises together. It is **goal-oriented**, holding to an objective across several steps and adjusting as it learns. It **observes and reasons**, taking in information, working out what it means, and using that reading to decide what to do next. And it **acts**, using tools to read a database, search a source, send a message, or write a file, so that it produces real effects in the world.

> *Example:* A sales team points an agent at its order data each morning. The agent reads the overnight figures, notices returns in one region have roughly doubled, queries the order records to find the product driving the spike, scans the support log for matching complaints, and drafts a brief note naming the likely cause. It does not send the note on its own; it puts the draft in front of a manager and waits for the decision.

Every agent is built from three parts:

- **The model** — the decision-maker, a large language model (LLM) such as Claude that reads the situation, reasons, and chooses what to do next; on its own it produces only text.
- **The tools** — the agent's reach: functions that let it act beyond the conversation (pull current information, query a database, run code, write a file).
- **The orchestration layer** — the loop that runs the other two: the model acts, the layer feeds the result back, the model reasons and acts again, until the goal is met or it hands control back to you.

An agent is "typically just LLMs using tools based on **environmental feedback** in a loop" (Anthropic, 2024). At each step the agent reads the actual result of what it just did and judges its progress against that result rather than against its own confidence.

> **Morgan Stanley (2023).** ~16,000 financial advisors got an assistant built on GPT-4 designed to support them, not replace them. The advisor describes a client situation in plain language; the model interprets and plans; the tools search ~100,000 internal research reports, compliance policies, and product documents; the orchestration layer runs the search-and-synthesize cycle and returns an answer **with citations**. The advisor, not the agent, decides what to recommend.

An agent differs from a simple tool in what happens after the first answer. A **workflow** moves through steps fixed in advance; an agent "dynamically direct[s] [its] own processes and tool usage," choosing the steps itself (Anthropic, 2024). *Deciding where to let it choose and where to fix the path is much of the design work this course teaches.*

## 1.2 What is vibe coding?

If the agent is what you build, **vibe coding** is how you build it: creating software by describing what you want in plain language and letting a model write and run the code, steering by what comes back rather than by reading every line. Karpathy named the practice in early 2025 (Karpathy, 2025); it spread far enough within the year to be named a dictionary word of the year (Collins Dictionary, 2025).

Vibe coding's deepest change is in **who gets to build at all**. If you can describe what you want clearly and judge whether the result is any good, you can build it, even if you have never written a line of code. For analysts and managers, the ability to build is no longer gated by the ability to code. (The book uses producer Rick Rubin — whose instrument is judgment, not technical execution — as the emblem of this shift.)

The ease of building this way **obliges you to verify what the software actually does**, because you steer by results rather than by reading the code. Reading the code line by line is an engineer's job — the point at which the work stops being vibe coding and becomes ordinary software development (Willison, 2025). *Judging whether the result is right is yours, and that is the discipline this book teaches.*

> **The unit this course works in:** a data-based app with an agentic intelligence layer, vibe-coded into existence in Claude Code, on a data source you choose.

## 1.3 Why should we learn to vibe code?

In early February 2026, a wave of selling erased ~$285 billion from software companies in about two days — the "**SaaSpocalypse**" — after AI agents began taking on white-collar work end to end (Contreras, 2026). When building software becomes nearly free, the buy-versus-build calculus tilts toward build, and software whose only value was convenience looks exposed.

**Leverage is the smaller half of the reason to learn vibe coding.** The larger half: being able to build tells you nothing about whether what you build is **worth building**. The most costly AI failures are not failures of capability — they are capable builds aimed at the wrong target.

> **Common failure — Klarna: the bot that hit every number.** In Feb 2024 Klarna reported its AI assistant handled 2.3M conversations in its first month, two-thirds of support volume and the work of 700 agents, resolution time down from 11 minutes to under 2. By every dashboard number, a triumph. Fifteen months later it reversed course: cost "seems to have been a too predominant evaluation factor … what you end up having is lower quality," and Klarna began rehiring (Fortune, 2025). The system optimized exactly what it was told to — cost and speed — while accuracy and trust were never on the board. **The failure was judgment about what to build and what "good" had to mean.**

Klarna is the common case. IBM (2025): only ~25% of AI initiatives delivered the promised return, only 16% scaled. BCG (2025): 60% of companies generated no material value from AI. The bottleneck has moved off the technology and onto the judgment around it. Mollick (2026): when fluent output is abundant, "**what's scarce is knowing what to ask for.**"

## 1.4 Agentic Project Design: a method, not a mindset

The second skill is not a mindset you adopt; it is a **method you run**: **Agentic Project Design**, a repeatable loop that names where judgment enters, what it is written into, how it is tested, and how its lessons carry forward.

> **The model (Figure 1.4).** A four-step loop — **Plan, Build, Use, Evaluate** — runs around a **Living Spec**, inside a workspace stocked with **Knowledge** and **Skills** and producing **Deliverables**, all bounded by a **Governance** membrane that human judgment controls.

- The **Living Spec** at the center states the objective, the scope, what success looks like, and the conventions the work must follow. In Claude Code it is the `CLAUDE.md` the agent reads before it acts. *Living* means you revise it whenever your understanding changes. A convention as small as "always show the number of responses behind a percentage," once written, is applied every time.
- **Around it runs the loop:** Plan the opportunity and write it into the spec → Build against the spec → Use the result in real conditions → Evaluate what the system enacted against what the spec specified, folding what you learn back into the spec so the next Plan starts smarter.
- **Three stocks feed the loop:** **Knowledge** (data, readings, exemplars — the data source and the documents that explain it), **Skills** (packaged, reusable expertise), and **Deliverables** (the outputs the project exists to produce — for you, a deployed app and its evaluation).
- **Governance surrounds the whole workspace** rather than sitting inside the loop. It is the membrane that every input and output crosses under human review. The agent drafts a result; you decide whether it ships, because the agent does the work and you own the outcome.

### The Six Principles

1. **Cultivate Taste.** Know what's worth building. For the technically fluent, value is bound by judgment, not capability; when in doubt, spend more on the objective.
2. **Write What Good Looks Like.** Make standards testable. If you cannot test it, you have not yet written it.
3. **Curate Context.** Keep it fresh and tight. The workspace's quality ceiling is its context; staleness and bloat degrade output directly.
4. **Verify, Then Trust.** Outputs are claims, not facts. A confident answer is not a correct one; read the work rather than its confidence.
5. **Expect the Gap.** Divergence is signal. What you specified and what the system enacts will diverge in real use; instrument for it, and read each gap for the standard it reveals.
6. **Delegate Work, Not Accountability.** Outcomes stay yours. Agents do the work, and you own the result, along review lines you draw in advance.

> **The running example — Kinquiry.** A finished hypothesis-testing app, vibe-coded in Claude Code on the SPGC-KPMG Global Family Business Survey (2,683 firms across 83 countries). A researcher hands it a rough question; it picks the right statistical test, runs it on the raw data, interprets the result, and drafts a research presentation with appropriate caveats — or refuses when the data cannot honestly answer the question. It deliberately climbs higher than the one-week target: it pairs an exploratory dashboard with a guided agent and runs true inferential statistics on a dedicated service.
>
> **The realistic target for your own one-week build is the lean version:** a client-side dashboard or data explorer that changes a real decision, paired with a thin Claude reasoning layer, shipped as a single app with no separate statistics service. *A dashboard that changes a decision is a fully legitimate center of gravity, not a lesser cousin of an agent.*

By the end you have three things: a **deployed app**, a **repeatable loop** you can run again on any data, and a **working vocabulary** (the loop, the Living Spec, the stocks, the Governance boundary, the six principles) for naming where judgment has to enter.

---

# Part I: Plan

Plan is the first step of the loop, and it has one job: get you to the right thing to build, written down precisely enough that the Build, the week of real use, and the evaluation can all run against it. Capability is settled; what is open is judgment about what is worth building and what good output looks like.

Part I follows the order you actually do the work: stock the workspace with **Knowledge** (Ch 2) → crystallize what is worth building into the **Living Spec** / `CLAUDE.md` (Ch 3) → give the deliverable a visible shape with an HTML prototype (Ch 4). By the end of Day 1 you hold three artifacts that let a stranger open the workspace, read the spec, see the mockup, and know exactly what to build.

> **Opportunity-first is a discipline, not a timing rule.** The locked stance of this course is opportunity-first: the decision and the user drive the project, and the data is a **gate, not a generator**. You read the data to ask whether it can carry the opportunity you chose, never to let its columns invent one. You may stock the data first and still refuse to let it choose the opportunity. **Curation, not accumulation, is the judgment Part I teaches.**

### The running example: Kinquiry on the STEP family-business survey

The dataset is the **SPGC-KPMG Global Family Business Survey 2023-24** (STEP Project Global Consortium + KPMG Private Enterprise): 2,683 family-business leaders across 83 countries, asked about legacy and socioemotional wealth, transgenerational entrepreneurship, self-rated performance vs. competitors, CSR, succession, and governance. Its public report (*Unlocking Legacy*) leads with a pattern: 43% reported both strong legacies and high performance, and the highest-performing firms carried the strongest legacy scores. It also names the **legacy paradox** — legacy as a source of identity yet a liability when tradition blocks change.

---

# 2 · Knowledge: Setting Up the Workspace and Stocking It

The first physical act of a project is creating a workspace and putting material in it, and **the quality ceiling of everything that follows is set by what you choose to put there.** Hold the question *what is worth building, and for whom*, and let it govern what is worth gathering. Gathering is not choosing.

Getting the Knowledge stock right is two moves and a habit: **connect** the primary material so the agent reads it first-class; **curate** it so the binding facts are tight and current; then **augment** with the domain understanding the raw data cannot supply.

## 2.1 Create the workspace, stock the primary material

The materials stocked into the STEP workspace make this concrete:

1. **The survey data** — a single Excel file (`Final dataset_Survey 2023 (updated Nov 12, 2024).xlsx`), 2,683 responses, one row per firm, ~145 columns of raw survey codes.
2. **The codebook** (`SPGC-KPMG Global FB Survey 2023_Codebook.pdf`) — what those codes mean. *Numbers without their meaning are a grid the agent will read confidently and wrongly.* The data + its codebook is **the smallest complete unit of Knowledge for a data app.**
3. **Reports derived from the survey** — the published report, executive summary, and a regional benchmarking report. Stocked for the **interpretation they carry** (what the field already concluded), not for bulk.

> **Connect the source; do not paste it.** A connected source is one the agent reads in full and can re-query. Pasted data is a frozen snapshot the agent completes confidently without any way to tell you the rows it never saw would have changed the answer. *If the app's whole value rests on the data, the data is the one thing you connect rather than paste.*

## 2.2 Think carefully about what you add

Connecting solves **reach**; it does not solve **attention**. Every line competes for the model's attention, and a bloated context degrades output before the window is full. **Curation, not capacity, is the judgment.**

> **Common failure — loading the whole codebook "to be safe" buries the one line that mattered.** A team pastes the full 40-page codebook plus questionnaire and methodology notes. The agent then builds a "Family Strength Index" that averages the survey's two 1–5 scales into one meaningless number. The one annotation that would have stopped it — *never average the legacy agreement scale with the performance scale* — was on page 31, drowned among hundreds of lines. **More context made the output worse.**

**The Deletion Test, applied to Knowledge:** for every line you are tempted to add, ask *would removing this cause the agent to make a mistake?* If not, cut it.

The five curated STEP traps (these five carry the weight of forty pages):

- **Two scales that look identical and are not.** Legacy/CSR items run "strongly disagree → strongly agree"; performance items run "much worse → much better." Both 1–5, so a 5 on one ≠ a 5 on the other; **never average them into a composite.**
- **A proportion masquerading as a percent.** Family-ownership runs 0–1, so 1.0 = 100%, not 1%. Multiply by 100 before reporting as a percent.
- **Answers that exist only for some firms.** Succession questions were asked only of the ~half of firms that had a succession; a finding across all 2,683 rows silently describes a smaller, different group.
- **Codes that need a lookup.** Country is stored as integers, not names.
- **A data-entry outlier.** One firm reports 300,290 employees where the next-largest reports 50,000; any average is wrong until that value is capped.

**How bad Knowledge fails, and the defense:**

| What can go wrong | What you do about it |
|---|---|
| **It buries what matters.** | Keep context tight; put the few binding facts where they're read (start or end). |
| **It drifts over a long session.** | Re-anchor durable standards in `CLAUDE.md` (re-read every run); restart a thread gone off course. |
| **It invents what isn't there.** | Don't let the agent tell you what the data contains; have it work only from the curated codebook. |
| **It sounds sure either way.** | Don't read confidence off the tone; decide up front what good is, check each output, route high-stakes ones to a human. |

## 2.3 Augment with research

An agent can read what a column means but not the world it came from — the decision the user faces, the methods that produced the measure, the prior findings. That world is Knowledge too. A deep-research tool can generate a structured survey of a field in minutes, but **the tight-not-dumped rule still applies**: distill it to the framings the project will lean on. A research report is itself a set of claims — **treat it as a claim to check before you rely on it.**

> **What the STEP workspace adds:** (1) **domain research** — key family-business articles plus a distilled deep-research report; (2) **"how" material** — the course's method documents and analysis conventions (what counts as an honest hedge, which test fits which hypothesis, how to report an effect size). *Keep Knowledge fresh as well as tight: a stale source degrades output as surely as a bloated one, with no error to warn you.*

## 2.4 A note on the working session

The session you work in carries its own context and degrades as it grows. The discipline does not stop at the folder's edge — keep what you are working with tight and current in the session as much as in the folder. (Session-management habits come in Part II.)

> **What this makes possible.** The workspace is stocked and curated. Because the folder is now rich, you can point Claude at it and have it **draft the Living Spec from the material already there.**

---

# 3 · The Living Spec

> **What Kinquiry is for.** A researcher brings a hypothesis in plain language — *firms with stronger binding social ties perform better*. Kinquiry picks the test, runs it on the raw survey, and drafts a memo: the association is small but reliable, ~0.16 on the standardized scale (95% CI [0.11, 0.20], p < 0.001). Then it writes one more line: *causal interpretation is not warranted, because the data is a single survey wave with one respondent per firm.* No prompt told it to hedge — **a single file, read at the start of the run, said the data was one wave with one respondent per firm.** Strike that line and the next run drops the caveat. Nobody touches the code. **The behavior moved because the spec moved.** *That file is the product. The Python around it is plumbing.*

The `CLAUDE.md` is the model's **Living Spec**: the single file the agent reads at the start of every run, stating what the app is for, what good output looks like, and the rules the agent must follow. *Living* means you keep it updated as you work the loop.

> **The spec is causal, not descriptive.** It is not a record of what the app does; it is the *reason* the app does it. Change the file and you change the app's behavior on the next run, with no code edit. **If you cannot say what your app is, for whom, and what good output looks like, in two tight pages, you do not yet know.**

## 3.1 Deciding what's worth building

A good data app does **three things at once**, and missing any one sinks it:

1. **Focuses on a specific decision that adds value.** Not "surface insights" — a *named decision someone makes, that the app changes.*
2. **Targets the people who make that decision.** A user who owns the decision and both can and will act on the output.
3. **Is grounded in accurate analysis.** A claim the data can honestly carry. (Miss this and someone acts on a confident, wrong answer.)

*How impressive the build is sits nowhere on the list.*

> **Common failure — the dashboard nobody opened.** A team starts from the data, ships filters/drill-downs/clustering/a chart for every variable within a day. A week later nobody has opened it twice, because it was built to display what the data *had*, not to change what anyone *did*. Pressed to describe the app, they can only list features. *A capability looking for a problem.*

**Four moves, in fixed order:**

- **Move 1 — Frame from the work, not the data.** Name three things without reaching for a column: the **decision** the app changes, the **user** who owns it, the **leverage** the agent adds (what the user could not do, or not do well, without it). Then state the **center of gravity**: a dashboard a human reads and steers, or an agent that runs while a human oversees? *Good means something different for each.* The test of a real frame is one sentence with no dataset named: *this lets [user] do [X] they couldn't do before.*

  > **Framing the STEP agent.** Kinquiry's opportunity was reverse-engineered (survey + dashboard already in hand), but the user and decision **pre-existed the dataset**. User: a researcher/advisor who must understand what the survey says and find research opportunities worth pursuing. Decision owned: *what to claim, in writing, to someone who will act on it.* Leverage: move the work from navigation to judgment — the user states a plain-language hypothesis; the agent supplies the test selection and hedging. One sentence: *this lets a researcher turn a plain-language hypothesis into an honestly hedged finding they could not have produced without already being a methodologist.*

  > **The Slightly-Slower Test.** Ask of your favorite concept: *what does the user do today, without my app?* If the honest answer is "the same thing, slightly slower," there is no real leverage and the concept should die cheaply, now.

- **Move 2 — Read the data as a gate.** Now, and only now, turn to the data and ask: *can it honestly support the claim the app needs to make?* The output is the **CAN / CANNOT scope statement**, every line carrying its structural reason. This becomes the spec's Scope and Data sections, and the CANNOT list becomes the agent's refusals.

  > **STEP, CAN:** descriptive comparison/benchmarking across generation, region, size (with sample imbalance flagged on every output); associating one scale with another inside a model (a relationship, not an average).
  > **STEP, CANNOT:** causal claims (single wave, one respondent/firm — say "associated with," never "causes"); any trend (no time dimension); firm-level identification (anonymized, no firm ID); national-prevalence claims (unweighted convenience network); any composite that averages the two differently-anchored scales.

- **Move 3 — Name what you will refuse.** Move 2 kills what the data *cannot* compute; Move 3 refuses a **framing** the clean output invites, on judgment about how it will be read downstream. *Anyone can refuse what the data cannot do. The discipline is refusing what it can.* Three reasons recur: the output would be **misread as a verdict** (a ranking as a league table), **mistaken for advice** (an association read as a recommendation), or **read as representative** (a convenience sample projected onto a population). *A refusal without a reason is a preference; a refusal with a reason is judgment.*

- **Move 4 — Converge on one concept.** Surface ≥3 candidates before judging any; lock criteria before looking at options; criteria must be **dominated by one-week deployability** (can you genuinely *use* it for a week, not demo it once?). Score, resolve ties on cleaner data support and a real owner, commit, and **write down the alternative you rejected and why.** Tie-breaker (from MMA 608): the *How to Win* question — what does this app do that a plain dashboard on the same data could not?

## 3.2 What goes in the file

The `CLAUDE.md` is a plain-text Markdown file at the project root (or in `.claude/`) that Claude Code reads automatically at the start of every session — "persistent context it can't infer from code alone" (Anthropic, 2026b).

> **Common failure — a spec that says everything tells the agent nothing.** A nine-page `CLAUDE.md` opening with industry history, every column retyped, a beloved charting library — and on page seven, "surface useful insights for stakeholders." The agent produced a confident unsupported answer and invented a column. The one line that mattered — *never claim causation from a single survey wave* — was never written.

**What Anthropic's guidance says about `CLAUDE.md`:**

- **Keep it short and human-readable.** "Bloated CLAUDE.md files cause Claude to ignore your actual instructions." Aim under ~200 lines.
- **Be specific and concrete.** Write "say 'associated with,' never 'causes,'" not "interpret results carefully."
- **Include what the agent cannot infer; leave out what it can.**
- **Add emphasis where a rule keeps getting missed** ("IMPORTANT," "YOU MUST").
- **Treat it as advisory, not enforced** — put the few hard guarantees in code.
- **Start with `/init`, then refine.** "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly."

**The six parts of the spec** (each maps to a Move from §3.1):

- **Objective** (Move 1): the decision, the user, the judgment layer, the center of gravity.
- **What "good" looks like** (the hardest part; the whole evaluation turns on it): standards written concretely enough to score — the caveats it must carry, the claims it may not make, a **gold example** (one input + its exact good output), and a short **must-never-produce list**.
- **Scope** (Moves 2 & 3): the smallest version that delivers value, one named stretch layer, and an explicit refusal list (each non-goal tied to a structural reason).
- **Data / knowledge** (Move 2): point at the codebook; don't retype it. Record what one row *is*, sample representativeness, what blanks mean, and the encoding traps.
- **Capabilities and boundaries**: the reusable capabilities, the data it must read directly, and where the agent is trusted to decide vs. fixed in advance.
- **Human-in-the-loop**: where the human gets the final word, and the rule that an override is logged with the value it protected.

> **The STEP Living Spec, condensed (`CLAUDE.md`):**
>
> ```markdown
> # CLAUDE.md: STEP Hypothesis-Testing Agent (Kinquiry)
>
> ## Objective
> Turn a plain-language hypothesis into an honestly hedged finding on the
> STEP/KPMG 2023-24 survey: pick the test, run it, interpret it, flag the
> limits, draft a memo — or refuse what the data can't answer. Center of
> gravity: agent (a dashboard already exists; the value is the judgment layer).
>
> ## Scope
> - Core: hypothesis → plan; a group comparison or simple regression on the
>   clean scales; a hedged memo with a numeric table and a "what this can't
>   support" rider; or a refusal.
> - Non-goals (refuse): causal, longitudinal, firm-level, national-prevalence,
>   predictive, or a new front-end.
>
> ## Data and its shape (point at the codebook; don't retype it)
> 2,683 rows; one row = one firm, reported by one family member. No firm ID,
> no time dimension. Over-represents Latin American / Southern European firms;
> unweighted. Traps: never average the two differently-anchored 1-5 scales;
> ownership is a 0-1 proportion, not a percent; succession items apply only to
> firms that had a succession. (Full schema in the codebook.)
>
> ## What "good" looks like (testable)
> - Says "associated with," never "causes." Flags common-method bias on every
>   scale-to-scale finding and flags the sample. Reports an effect size, not
>   just a p-value. Suppresses groups < 10; flags groups < 30.
> - Gold example: "binding ties and performance" → 0.16, 95% CI [0.11, 0.20],
>   N≈2,180, p<0.001, "causal interpretation not warranted." (Illustrative.)
> - Never: a causal verb; a column that doesn't exist; a composite averaging
>   the two scales; a succession finding on the full sample.
>
> ## Boundaries & human-in-the-loop
> Agent decides whether to refuse and which test fits; everything after follows
> a fixed routine. Agent drafts, human decides; every memo ends with a
> "Reviewer check:" and overrides are logged with the value protected.
> ```

## 3.3 Why a good spec works

- **Causal, not descriptive.** Test of any line: *if I delete this, does the agent do something different on the next run?* If yes, load-bearing; if no, decoration — and decoration is not free.
- **Every line competes for attention.** A bloated spec degrades output; cut any line that would not change behavior.
- **The boundary object.** The spec coordinates people who do not share your assumptions (Star & Griesemer, 1989): plastic enough that the agent, a teammate, and a stakeholder each read it through their own lens, yet robust enough to hold one identity — *what this app is, and is not, for.*

**Write "good" concretely.** Your spec is your app's *espoused theory*; a week of real work is its *theory-in-use* (Argyris & Schön, 1974) — the two will diverge, and the only way to see the gap is to have written "good" concretely enough to check against. A standard is sharpest paired with its violation. The STEP spec carries four **evil twins**: the hallucinated column (a "+12% revenue impact" with no revenue variable); the misaggregated scale (the Family Strength Index); the overconfident small-cell chart (a clean bar on 65 firms with no n shown); the correct-but-useless answer (significance with no effect size).

## 3.4 How to create it: let Claude draft, then sharpen to taste

Because the folder is rich, point Claude at the stocked workspace and have it draft a first spec. The draft is a starting point, never the spec. **The craft lives in four edits:**

- **Run the deletion test.** Cut every line whose removal would not change the next run.
- **Fix position.** Move the most load-bearing line to where attention is highest (start or end).
- **Make "good" testable.** Replace vague standards with scoreable ones; add the gold example.
- **Keep it living.** When the deployment week surfaces a divergence, fold the fix back in.

> **The cold read is the fix.** You cannot run it on yourself. Hand the file to a reader who was never in the room (a fresh Claude session or a person with none of your context) and watch where they stop. *Treat hesitation as signal and praise as noise.* Resist the urge to explain — every word you say out loud to rescue a confused reader is a word missing from the file.

> **You wrote a good spec when** a fresh Claude session, given only the file, builds something recognizably yours, and a cold reader can state back the decision it changes, the user, what good output looks like, and what the app refuses — without asking what you meant.

---

# 4 · Deliverables: Mockups and the HTML Prototype

> **Common failure — a correct output that fails because you never saw its shape.** Every standard met, but the memo buries the decision three paragraphs down and the dashboard leads with the variable that was easiest to chart. *They would have caught it in five minutes if they had mocked it before they built it.*

The spec says what good looks like in words, and **words under-determine the artifact.** A **mockup is the spec made visible** — the cheapest way to discover what you actually want before the real build commits you.

## 4.1 Why mock the deliverable

A mockup is a **boundary object** too: put it in front of the stakeholder and the disagreement that would otherwise surface in the deployment week surfaces now, in minutes. Build it as a **walking skeleton**: a thin end-to-end slice with every section/panel/control present and wired, content swapped for placeholders you fill by hand. *You are building the app's frame and will dress it with the real thing as you go.*

**The medium is HTML, by default** (Shihipar, 2026): it carries more information (tables, layout, diagrams, controls), is more readable at scale, and is more shareable (opens behind a link in any browser). Reach for HTML when a human has to read and act on the artifact; leave it alone when the output is a number you read once.

## 4.2 What a Plan-phase prototype is, and what it is not

**It is:** a self-contained HTML rendering of the deliverable's *shape*, filled with hardcoded output (the gold example typed in by hand). For a memo agent, the input-to-memo flow with the finding leading and the caveat where a reader will see it; for a dashboard, the panel layout with plausible placeholder numbers.

**It is not** the real app: data not connected, skills not built, result a placeholder. *Which prototype you build follows directly from the center of gravity.*

## 4.3 How to build it from the spec

Feed Claude the Objective and the gold example; ask for the HTML mockup with the gold example as centerpiece. **The cut comes here:** a **scope ladder** ranks features from the one thing the app cannot ship without, up through nice-to-haves; draw the line low. *A panel you cannot fill with a believable placeholder is a panel you have not really specified.* The prototype and spec **co-evolve**.

Two techniques (Shihipar, 2026): **generate several, then converge** (3–4 approaches in a grid); **close the loop with an export** (a "copy as prompt/JSON" button so an edit in the rendered view exports back as a spec revision).

> **Common failure — dressing up everything in HTML.** HTML costs more tokens; spend the richness where readability, shareability, or interactivity earns the cost.

## 4.4 The Day-1 trio, complete

Three artifacts let a stranger skip the meeting: the **workspace** (container), the `CLAUDE.md` (instructions), the **prototype** (target). The completeness test is the cold read across all three. This trio is the handoff into Build, which replaces the mocked output with the real thing.

### Part I references (selected)

Anthropic (2024) *Building effective agents*; Anthropic (2026b) *Best practices for Claude Code*; Anthropic (2026c) *How Claude remembers your project*; Argyris & Schön (1974); Lafley & Martin (2013) *Playing to Win*; Shihipar (2026) *The unreasonable effectiveness of HTML*; Star & Griesemer (1989) *boundary objects*; STEP Project Global Consortium & KPMG Private Enterprise (2024).

---

# Part II: Build

You arrive at Build holding something that looks finished and does nothing: a workspace of curated **Knowledge**, a `CLAUDE.md` a stranger could build from, and an HTML **walking skeleton** with every piece of content faked. Build draws on the second stock, **Skills** — the project's agentic capabilities, the packaged reusable expertise the agent applies. Build's task: construct the agentic capabilities the deliverable needs and assemble them into a working, deployed app. *For a room that can wire almost anything, the binding question is which capabilities are worth building at all, and in what form.*

Part II runs in three moves: **identify** (Ch 5), **build** (Ch 6), **assemble** (Ch 7).

---

# 5 · Identifying the Agentic Capabilities You Need

> **Common failure — you can build any capability, so you build all of them.** By mid-morning: six custom skills, three subagents, a hand-built connector. But the connector duplicates one of thousands off the shelf, two skills wrap things the model did natively, and the three subagents isolate no real decision. *Every component is a surface that can fail and a claim on attention; a build with six skills is more expensive to run and more likely to drift than one with two.*

The fluency reflex from Plan (*I can build it, therefore it's valuable*) returns wearing a new costume: *I can build this capability, therefore I should.* **The judgment that gates a build is the worth of the capability, not your ability to build it.** Capability sprawl is the build's version of context bloat. **The right capabilities, not the most.**

- A **capability** is a thing the deliverable must be able to *do* — read the data, validate a column, run the test, write the claim — stated as a plain verb, before any tool is named.
- A **form** is *how* you supply that capability.

### The five forms a capability can take

For each capability, choose the **simplest sufficient form** — the cheapest one that does the job:

- **Native action.** Do nothing; the model already does it well enough. Wrapping it adds a surface and buys nothing.
- **Skill.** Package reusable expertise as a small named bundle when the same judgment recurs and must apply the same way every time — optionally with a check that runs in code.
- **Subagent.** Hand a scoped worker its own job and its own attention when a distinct decision deserves to live in one place.
- **Connector.** Reach an outside tool or source. **First check whether it already exists to connect**; building one you could configure pays a build cost for a setup step.
- **Fixed pipeline.** Hard-code the steps where determinism protects the integrity of the result.

> **The rule is one sentence: the cheapest capability is the one you do not build.**

## 5.1 Decompose the deliverable into capabilities

Walk the walking skeleton screen by screen; at each faked spot ask *what would the agent have to be able to do for this to be real?* and **write the answer as a verb.** Name the need first, the form second, and keep them apart on the page. *If an item names a form, it is not a capability yet.*

> **Kinquiry's capability list (six verbs, named before any tool):** read the survey file · validate any column against the codebook · turn a plain-language hypothesis into a validated test plan (or refuse) · run the chosen analysis · interpret the result with required caveats · render the result as a research presentation.

> **Common failure — naming tools before capabilities.** Opening with a shopping list of forms ("we'll need a skill and a connector and a couple of subagents") fixes the form before the need is written. *Solutioning first is how a job that needed two skills acquired six.*

## 5.2 Choose the cheapest form for each capability

Work down the list one capability at a time. **The signature judgment — the one that proves you ran this move — is the capability you choose *not* to build,** named with its structural reason.

> **Kinquiry's capability-to-form map.**
> - **Three skills** (expertise that must apply the same way every time): `codebook-guard` (a hard gate — `validate.py` checks every column against the 145-column manifest and exits non-zero on a hallucinated column or the no-averaging trap); `interpretation-guardrails` (advisory — a claim linter flagging causal language, missing effect size, missing caveat); `presentation-render` (fixes slide order and display rules — suppress n<10, flag n<30).
> - **Two subagents** (only two decisions worth isolating): `hypothesis-parser` (raw hypothesis → validated plan or refusal; consults `codebook-guard`); `interpreter` (the *only* component allowed to write natural-language claims, so caveat rules live in one place; consults `interpretation-guardrails`). *Subagents consult skills: the worker carries the decision, the skill carries the rule.*
> - **The connector form stays empty on purpose** — local file in, local file out, no external system to reach. The run is a **fixed pipeline**: `clean → test → effect size → reliability → robustness`, same order every time.

> **Common failure — capability sprawl, and its mirror.** Sprawl: a skill/subagent for every step, none concentrating a decision. Mirror: hand-building what already exists off the shelf. *They are the same mistake — a failure to choose the simplest sufficient form.*

> **The signature of taste is the form you refuse.** Refuse the *rebuild*, not the dashboard: a decision-changing dashboard with a thin reasoning layer is a lean surface and the realistic target this course teaches. Kinquiry already had a dashboard, so the agent's leverage was the judgment layer, not a second front end.

## 5.3 Key terms

- **Capability decomposition** — breaking the deliverable into verbs the agent must do, before any tool is named.
- **The five capability forms** — native action, skill, subagent, connector, fixed pipeline; a menu, not a ladder.
- **Build vs. reuse** — you do not build what you can connect; thousands of ready-made connectors exist.
- **The right capabilities, not the most** — a build is gated by which capabilities are worth building, not how many it can build.

---

# 6 · Building the Agentic Capabilities

> **Common failure — you can build the capability fast, which is exactly why you ship one you cannot stand behind.** You ask for a summary index, it returns in seconds, the check is green, you click Accept. Then someone asks what the index computes and you cannot say: a "Family Strength Index" averaging two differently-anchored scales, with no referent. *Building the capability was the easy part. Knowing whether you can trust what it produces is the part you skipped.*

**One discipline threads every form: treat its outputs as claims to check, not facts to accept.** For this cohort the check is **behavior-level** — you verify what the app *produces* (the number means what it says, the caveat matches the data, you can explain it in plain language), not the code. *A green checkmark certifies that the app ran, not that it is right.*

## 6.2 Claude Skills: package reusable expertise

A **Claude Skill** is a small named package: a short instruction sheet stating what it does and when to use it, optionally bundling a script so a check runs in code. The agent keeps a one-line summary on hand and loads full detail only when a task calls for it — **progressive disclosure** (Anthropic, 2025c), so installing expertise is nearly free.

A skill differs from a pasted prompt: it is **discoverable** (found via its description of when to use it), **composable**, and can **carry a check the agent runs in code**. "Because code is deterministic, this workflow is consistent and repeatable." *A prose instruction advises; a bundled check enforces.*

> **You know a skill is good when its description says both what it does and when to use it** — tightly enough that the agent reaches for it at the right moment and leaves it alone otherwise.

> **Kinquiry's `codebook-guard` skill** wraps Plan's curated codebook in executable validation as a hard gate: `validate.py` checks every variable against the 145-column manifest, exits non-zero on a hallucinated column, and fails the no-averaging trap before it computes. *In Plan the codebook was what the agent must honor; here it is the executable rule that enforces it.*

> **Common failure — the "skill" that is just a pasted prompt, and its mirror.** (1) A skill in name only — no executable guard, generic description that never triggers. (2) The over-stuffed skill that dumps the whole schema and re-states the `CLAUDE.md`. *A good skill is a sharp "when to use," a tight procedure, and a bundled check.*

## 6.3 Subagents: scoped workers

A **subagent** is a skill of a particular kind — a packaged *worker* you hand one job and get one answer from, running in its own context, seeing none of the main conversation. **Isolation is the whole point** (the finite-attention argument applied at build time) — and also the temptation. **Package only as many subagents as there are distinct decisions worth isolating.**

The empirical case misleads without its caveats: Anthropic's multi-agent system "outperformed single-agent Claude Opus 4 by 90.2%" but used "about 15× more tokens," and "token usage by itself explains 80% of the variance" (Anthropic, 2025d). *More agents is not more judgment.*

> **Kinquiry's two subagents** isolate exactly two decisions — `hypothesis-parser` (parse-and-gatekeep) and `interpreter` (write-the-claim). Rendering isolates no decision, so there is **no third worker** for it. *Count the decisions, not the steps.*

> **Common failure — subagent sprawl, and its mirror.** Plumbing that adds cost without judgment; or trusting a subagent's confident summary it cannot support (a subagent is itself an LLM — its output is still a claim to check).

## 6.4 Connectors: wire data and tools first-class

A **connector** wires a data source or outside tool to the agent once, so it reads and acts directly rather than over a pasted fragment. The signal: "when you find yourself copying data into chat from another tool" (Anthropic, 2025a). **Thousands of ready-made connectors exist (MCP Registry); the rule is configure, do not build.**

> **The connector Kinquiry didn't build.** Local data in, local file out — no external system to reach at runtime, so the connector form stays empty on purpose. (Version control and hosting are infrastructure for shipping, not connectors the agent invokes.) *A connector is right only when value rests on reaching a live outside system.*

## 6.5 Dynamic workflows: a harness for the task

A **harness** is the scaffolding around the model (how a task is planned, divided, checked, executed). The default Claude Code harness is built for coding and carries most of a build. A **dynamic workflow** is the model writing its own harness on the fly (Shihipar & Bidasaria, 2026), assembling six patterns: **classify-and-act, fan-out-and-synthesize, adversarial verification, generate-and-filter, tournament, loop-until-done.**

**The seam is now three-way:** let the default harness run a part, invoke a dynamic workflow, or hard-code a fixed pipeline. The governing discipline holds: "find the simplest solution possible, and only increase complexity when needed" (Anthropic, 2024).

**For this cohort, workflows are awareness-level** — they spend tokens a short build cannot spare; the realistic payoff is in Part III (Evaluate). Know that they fight three failure modes — **agentic laziness, self-preferential bias, goal drift** — by orchestrating isolated subagents, that you invoke one by asking Claude or with the trigger `ultracode`, and that it costs tokens.

> **The Kinquiry dashboard, built by a nine-subagent workflow.** The research agent needs no workflow, but the *dashboard* (eight cross-filtered sections + a landing page) was built by one: nine subagents in parallel, each writing one isolated file against a hand-scaffolded contract (schema, shared types, chart primitives, component interface, stubs so the app compiled first). Genuinely parallel, near-independent work — *precisely when a workflow earns its tokens.* The honest caveat: ~640,000 tokens, so the cost is real and stays an explicit opt-in.

> **Common failure — reaching for the orchestrator end because it is impressive.** Start at the simplest solution; add agency only where an open-ended decision genuinely needs the model's judgment.

## 6.6 Manage the build session

A Claude Code session's window fills fast and "performance degrades as it fills" (Anthropic, 2026b). Context is "a finite resource with diminishing marginal returns" (Anthropic, 2026d). **Managing the token budget:**

- **Bring the smallest high-signal slice, not the whole file.**
- **Convert heavy, reused sources to clean text once** and point the agent there (STEP's curated codebook).
- **Put what must persist into `CLAUDE.md`, and keep it lean.**
- **Reset on purpose** — `/clear` between unrelated tasks; `/compact` to shed weight without losing the thread.
- **Push exploration into subagents** (separate context windows, report back summaries).

**Group build mechanics (light here):** split work so two people aren't editing the same file blindly, keep a single shared `CLAUDE.md` as one source of truth, and commit often enough to recover a working state.

> **Common failure — letting the session bloat.** The forty-page mistake in real time: one long session across unrelated tasks, the window fills with stale exploration, the model forgets an early instruction and takes a confident wrong turn. *Reset on purpose; push exploration into subagents; keep durable standards in `CLAUDE.md`.*

> **Developing the Kinquiry agent (synthesis).** Skeleton → each capability in its chosen form (three skills, two subagents, no connector, a fixed `clean → test → effect size → reliability → robustness` pipeline, default harness, no dynamic workflow). Then the move the opener skipped: **check behavior end-to-end.** Feed the gold hypothesis; watch Sharpen fix the outcome first (self-rated performance vs. competitors, Q5.1_1–7), surface the contested "binding social ties" construct, propose a thin two-item proxy, **model the two scales rather than averaging them**, run standardized OLS with controls → β ≈ 0.16 (95% CI [0.11, 0.20], N ≈ 2,180), framed honestly (association, not cause; thin proxy flagged). Then confirm it **refuses** what it should.

## 6.7 Key terms

- **Verify, Then Trust (behavior-level)** — treat every output as a claim; verify what the app produces, not the code. A green check certifies it ran, not that it's right.
- **Claude Skill** — a discoverable, composable package of expertise that can carry a deterministic check.
- **Progressive disclosure** — a one-line summary on hand; full detail loads only when needed.
- **Subagent** — a scoped worker in its own context; earns its place only when a distinct decision is worth isolating.
- **Connector** — a source/tool wired once; configure, don't build.
- **Harness / dynamic workflow** — scaffolding around the model; Claude writing its own on the fly (awareness-level for this build).
- **The three-way seam** — default harness vs. dynamic workflow vs. fixed pipeline.
- **Managing the token budget** — finite-attention discipline applied to the working session.

---

# 7 · Building the App

> **Common failure — every number checked out, and the app still shipped broken.** The coefficient was right and the caveats clean, but the deployed page doesn't scroll past the input form on a phone, and the coefficient plot runs off its frame because the axis was hardcoded too narrow. *Neither defect touched a number. The build's last verification is of the running app, used the way a real person will use it.*

You ask Claude to **build** the app; you **test** it by using it; you ship and govern it with **GitHub.**

## 7.1 Vibe coding the app

Karpathy's "forget that the code even exists" was bounded to throwaway projects; a deployed app raises the bar Willison named: AI-assisted work becomes real development when "you then reviewed it, tested it thoroughly and made sure you could explain how it works to someone else" (Willison, 2025).

> **Three rules.** (1) You ask Claude to build it — describe in plain user language; you judge the result, you do not author or audit the code. (2) Steer by intent, judge by behavior — say what's wrong with what the app *does*, not with a line of code. (3) A deployed app raises the bar: you must test it, stand behind it, and explain it.

## 7.2 User testing

Verify a deployed app the only way you can — **by using it.** Four moves (none involve reading code):

- **Pin a regression oracle and confirm the live app returns it.** Fix one input whose correct output you've certified; hit the live app with exactly that input and confirm the number comes back.
- **Open the app and feed it varied questions, on the devices people use** (phone *and* laptop) — where the scroll bug and off-screen plot surface.
- **Judge outputs for plausibility** — a number technically computed correctly but that cannot be true.
- **Put it in front of someone who did not build it** — a cold read surfaces dead ends and unlabeled buttons.

> **The oracle, the varied questions, and a number that couldn't be true.** Kinquiry's oracle is β ≈ 0.16, N ≈ 2,180. Hitting the live route reproduced it; clicking every screen found the scroll bug and the off-screen plot; the explorer surfaced a firm listed at 300,290 employees in a \$20M–\$50M band — flagged on plausibility, traced to a data-entry typo (actual 290). *The pipeline was faithful: charts winsorize the outlier, the explorer shows the raw value on purpose. A surprise that validated the build.*

> **Common failure — a green script is not a correct app.** Kinquiry's scripts ran clean, yet running end-to-end surfaced a step invoking `python` where the environment needed `python3`. *A passing check certifies a piece ran, not that the assembled app works.* The defects that ship past a per-number check are system- and product-level — verify the product, not just the outputs.

> **Common failure — the deploy gotchas that waste an afternoon.** A nested repo so almost nothing uploads; a blanket `.env*` ignore that also hides the example template; a free hosting tier that sleeps and answers slowly. *None is a flaw in your app; all stall the ship.*

## 7.3 GitHub and branching

"GitHub is the new Google Drive" for AI-native work (Stulberg & Koh, 2026). You do not need to be a coder.

- **Repository** — a shared project folder with full change history.
- **Branch** — your private parallel copy; edit without touching the official version.
- **Commit** — a named checkpoint ("not done — a meaningful checkpoint").
- **Push / pull** — upload your work / download everyone else's latest.
- **Pull request** — "this is ready," reviewed before it joins the official version.
- **Merge** — accept the approved change.
- **Main** — "the official, trusted version everyone relies on."

Daily rhythm: pull main → branch → edit → commit (descriptive messages) → push → open a pull request → address feedback → merge → delete the branch. *You cannot permanently lose work; merge conflicts are normal and your AI handles the mechanics.*

> **Governance becomes concrete here.** A **pull request is the membrane in practice**: every change crossing into the trusted "main" version passes human review first. That is **Delegate Work, Not Accountability** in operating form — Claude does the work on the branch, a human owns what crosses into main.

> **How a collaborator contributes to Kinquiry.** The repo is private (proprietary STEP data) and on a free tier GitHub won't enforce branch protection. So the instructor set the collaborator to **read** access and used **fork-and-pull-request**: she works on her own copy, opens a PR he reviews and merges. *The review the free tier couldn't enforce automatically, he enforced by workflow — the PR stays the membrane.*

## 7.4 What this makes possible — the on-ramp to Use

You hold a deployed, version-controlled app you tested by using it. **The build's last act is using your own app adversarially** — pushing varied, awkward questions through it and judging the product the way the person who relies on it will. Carry it into the one-week **Use** phase and keep a structured **deployment log**: salient episodes, overrides and the value each protected, failures, predicted-versus-observed gaps, and outsiders' reactions.

## 7.5 Key terms

- **Vibe coding (deployed app)** — describe intent, judge behavior, never audit diffs; but you must test it, stand behind it, explain it.
- **User testing** — pin/reproduce an oracle, feed varied questions on real devices, judge plausibility, hand to an outsider.
- **Regression oracle** — one input whose correct output you've certified (Kinquiry: β ≈ 0.16, N ≈ 2,180).
- **Version control / GitHub** — repository, branch/main, commit, pull request (the governance membrane).

---

# Part III: Use & Evaluate

You reach the last two steps holding a dashboard that works and has proved nothing. **Use** puts it into real analytical work for a week. **Evaluate** holds what it did against what the spec said it should do, builds the evidence to settle the difference, and folds the lessons back into the spec. *Throughout, the test is what the dashboard produces and whether you can stand behind it, never the code underneath.*

---

# 8 · Use: Putting the Dashboard to Work

A dashboard that renders cleanly in a demo has told you almost nothing. **The only test that counts is a real person using it to make a real decision, on their own time, when you are not in the room.** The week is where the dashboard meets the one thing the spec could not anticipate — contact with a real user — and what you specified pulls apart from what the dashboard actually does. *That divergence is the most valuable thing the week produces.*

Three moves: **predict** what you expect, **document** the use, **put it in front of an outsider.**

## 8.1 Establishing the baseline standards

Before deployment, write down what you expect: who will open it, which views/filters they'll reach for, which they'll ignore, and above all **the analytical decision they'll make.** These predictions cost minutes and are **committed in advance** so you cannot revise them in hindsight. They run alongside the **quantitative measurement baseline** — the lightweight eval harness run once on Day 2 before deployment. *A week is too thin to reveal a pattern, but it can reveal a surprise — and a surprise only registers against an expectation committed in advance.*

## 8.2 Effective documentation of use

Keep an analyst's working notes, not a compliance log: what you asked, what it returned, which outputs you trusted, which you re-checked, where it changed or confirmed a decision. **Depth on a few revealing moments beats coverage of every click.**

### The structured deployment log: five fields

For each thing worth recording (an entry need not fill all five):

- **Salient episode** — the moment the dashboard caught something, misled you, came up empty, or produced a number you distrusted.
- **Override + the value it protected** — where your judgment went against the dashboard, and what that protected (a person who'd have been misclassified, a false finding, a wrong decision).
- **Failure** — a question it couldn't answer, a view that broke, a number that didn't reconcile.
- **Predicted-versus-observed** — how the moment compared to what you wrote down before the week.
- **Outside reaction** — what someone outside the build said or did when they used it cold.

*A one-week deployment cannot yield statistics, and the grading does not ask it to. A thin-but-deep week — three episodes worked through to what they reveal about the spec — scores better than a padded one. One episode that rewrites a line of the spec is worth more than twenty that confirm nothing.*

> **A week with Kinquiry's data explorer.** (1) Predicted she'd live in the regional view; instead lived in the country ranking — *the center of gravity was not where she'd built it.* (2) The small-cell flag stopped her on a 19-firm subgroup she'd been about to write up — *override protected a false result.* (3) A suspiciously round filtered count she recomputed against the raw file (it matched — the dashboard rose in her estimation); and a missing breakdown by ownership generation, logged as the thing she most wanted next.

> **You know the documentation is good when one episode rewrites a line of the spec you'd have defended on deploy morning.**

## 8.3 Obtaining alternative feedback

The builders are the worst judges of whether a stranger can use it. Recruit someone outside the build and watch them use it cold. What an outsider surfaces: where they **cannot find** the answer (usability), where they **misread** a chart (representational), where they **don't believe** a number (trust), where they **go looking for something not there** (scope). *Hand it over and stay quiet — treat hesitation as signal. This is the same cold read the spec received in Plan.*

## 8.4 Key terms

- **Effective documentation of use** — an analyst's record, reasoned from on evaluation day; depth over coverage.
- **Predicted-versus-observed** — expectations committed in advance so surprises become legible; the most informative evidence a one-week deployment produces.
- **Salient episode** — a single revealing moment; the unit of a good use log.
- **Override** — where judgment overruled the dashboard, recorded with the value it protected.
- **The cold read of use** — handing the dashboard to an outsider to surface what the team can no longer see.

---

# 9 · Evaluate: Reading the Dashboard Against the Spec

Evaluation is not *is the dashboard good?* It is the narrower, answerable question: **did the dashboard do what you said good would look like?** You wrote that standard down in Plan (the gold example and the must-never list); evaluation is where the spec stops describing an intention and starts serving as a test.

Compare two states: the behaviors the spec **configured** (`CLAUDE.md`) and the behaviors the dashboard **enacted** in use. Where they line up, the spec held; where they diverge, you've found a flaw in the app or a gap in the spec — both are the work. *(This is the Inherited-Configured-Enacted lens from MMA 608, turned on your own build.)* The Day-2 harness run is your **quantitative baseline**; this chapter is where the spec comes due.

## 9.1 The five-layer evaluation model

Walk the layers lowest to highest; a flaw at a low layer is not redeemed by strength at a high one. *(This is the Agent Audit — Map Workflow, Clarify Decision Rights, Define Metrics, Read Override Patterns — pointed at a data app's output quality.)*

| Layer | Question | How a manager checks it (by behavior) | Plausible-but-wrong twin |
|---|---|---|---|
| **Data integrity** | Are the numbers right? | Recompute a few independently (Python/R/Excel/SQL) and reconcile. | A clean number that double-counts or drops missing rows. |
| **Representational honesty** | Do the visuals/narrative tell the truth the numbers support? | Read each chart against the data and the question it claims. | A truncated axis manufacturing a trend. |
| **Decision fitness** | Does it serve the decision, for the named user? | Walk the decision through; could the user act? | A beautiful view answering a question no one needed. |
| **Usability** | Can a stranger use it cold? | Hand it over and watch. | A dashboard the builder demos flawlessly that a newcomer can't navigate. |
| **Trust & governance** | Can the organization rely on it? | Look for source, as-of date, caveats, a path for when it's wrong. | A confident dashboard with no provenance, running on stale data. |

> **Walking the five layers on Kinquiry's data explorer.** *Integrity:* recompute the 2,683 row count and a regional subtotal. *Honesty:* CEO gender is a donut (one categorical split), regional counts are bars, the two performance scales are never averaged. *Decision fitness:* the cautions panel and small-cell flags answer the researcher's real first question — is this subgroup large enough to trust? *Usability:* a newcomer can tell clicking a bar filters and clicking again clears. *Trust:* the source line names the survey, cautions spell out what the sample can/can't support, groups <30 flagged and <10 suppressed.

> **Designing your own evaluation.** The five layers are a teaching example, not a rubric to copy. Your checks come from *your* spec: each claim in the gold example becomes a check (figure to reconcile, chart to read, decision to walk); each must-never entry becomes a thing to test for.

## 9.2 Different types of evaluations

A dashboard needs two kinds of evidence, because its layers split into the ones a number can settle and the ones only a person can:

- **Deterministic evidence harness** (bottom two layers). A small set of known-answer checks: **reconciliation checks** (compute a total/subgroup independently and confirm the dashboard agrees) and **scenario checks** (filter to a known slice and confirm the figure). Cases come from the gold example and must-never list. Where the standard is a criterion not a figure, report a **pass-rate** (e.g., of small cells, what share carry the flag). *No model judges the output — these are questions with right answers.*
- **Structured self-audit** (top three layers — decision fitness, usability, trust). Walk the five-layer model as a human review against the source, fused with the use week's evidence (predicted-vs-observed, salient episodes, outsider reactions) and a human read of any narrative. *Trying to reduce these to an automatic score only launders a judgment into a number that hides it.*

**Run the harness before the revision (Day 2) and again after (Day 3)** — the difference is a measured before-and-after a single week could never produce. *You know the evidence works when a number moves and you can name the episode in the use log that told you to move it.*

> **Common failure — scoring what you should be judging.** Inventing a composite usability/trust score hides the judgment behind a figure that looks objective. *An honest "this confuses a new user, and here is where" is worth more than a usability score of 3.4.*

## 9.3 Evaluative workflows and agents

**This section teaches one move: attack your own confident output before you stand behind it.** The by-hand version — asking of each output what a skeptic would say to break it — is the floor every group must reach. The multi-agent version is an optional ceiling.

Three constructs from Build apply again, turned on evaluation: a **skill** packages a check you run more than once; a **subagent** does a scoped piece and reports back; a **dynamic workflow** settles how much to fix vs. leave to discretion. **The deterministic harness wants to be fixed** (it must run identically before and after so the before-and-after means something); **the exploratory part wants the opposite** (let an agent range over the dashboard and bring back candidates).

> **The line that keeps this honest runs between doing the labor and rendering the verdict.** A subagent can recompute a total and report match/mismatch; a critique pass can flag truncated axes. *What the agent never does is score the dashboard and hand back a verdict — a verdict is a judgment, and the judgment is the accountability you cannot delegate.* This is why the course keeps a model out of the judge's seat.

A model asked to check its own output carries **self-preferential bias** (Shihipar & Bidasaria, 2026); the remedy is structural — a separate worker with its own context, prompted only to attack. Three of the six workflow patterns carry the load:

- **Adversarial verification** (the core move) — spawn a worker whose only brief is to break each output, hunting the five-layer twins. *An output that survives a worker built to destroy it is far better evidenced.*
- **Fan-out-and-synthesize** — fan a worker across every chart and every logged episode in parallel, run the same twin-checks, gather failures into one assessment.
- **Tournament** — when a headline number depends on a defensible choice (missing-value handling, join grain, small-subgroup cutoff), compute it several ways and keep the reading that holds. *A figure that swings when one defensible choice changes is a figure not to trust.*

> **Knowing the move matters more than wiring up the machinery.** A group whose plan/budget won't run workflows should still do the manual version of each — the judgment is the same. *The move costs only the willingness to attack your own confident answer.*

> **Evaluating Kinquiry with its own workers.** A reconciliation worker recomputes each gold-example claim from the survey file (inside a fixed pipeline, run once before and once after the Day-3 revision). A skeptical critique worker fans out across all eight sections and flags the regional bar chart whose axis didn't start at zero. *The workers did the recomputing and looking; every verdict stayed with the researcher.*

## 9.4 Reconfigure, then re-test

Classify each gap with the **Triggers / Context / Workers** frame: a **trigger** gap (when it acts / what it surfaces by default — the regional view no one opened, a caution that fires too late); a **context** gap (what it worked from — a stale source, a wrong codebook note, a missing variable); a **worker** gap (how a piece was done — a truncated axis, a wrong-grain count). *Naming which one points you at the smallest change that closes it.*

Then make the change — usually an adjustment, not a rebuild (surface a caveat where users missed it, change the default view, redefine a metric to the right grain, fix a filter). Direct it in plain language; **re-test the behavior you changed** (re-run the harness for the post-revision reading, re-walk the layers you touched). *The test stays on what the dashboard now produces.*

## 9.5 Updating the Agentic Project Design using Evaluation results

**A revision that lives only in the app is half-finished.** Write what you learned back into the Living Spec — the spec carries forward and the app is downstream of it. Every confirmed finding becomes a line in `CLAUDE.md`: a sharper success criterion, a fresh must-never, a corrected data note. *The spec you end the week with is not the one you started; the difference is the record of what use taught you.*

The spec is the primary home but not the only one — **fold-back** can also land in the stocks or at the governance boundary: a check earns a permanent place in the harness; a repeated by-hand correction becomes a skill or guardrail rule; a data fact the codebook never stated joins the Knowledge stock; **a recurring override points to a governance change** (a review right to formalize, an escalation path to draw).

> **Where Kinquiry's findings landed.** Four findings, four homes: the small-cell episode → a must-never line + a hardened guardrail rule; the round-number count → a permanent reconciliation case in the harness; the missing generation breakdown → a sharpened scope line + a Knowledge-stock note; the truncated axis → an app fix + a representational must-never. *One week left the spec, the skills, the harness, and the Knowledge stock each a little truer.*

**Day 3 deliverable — the Deployment Assessment + improvement plan:** the five-layer findings, the before-and-after harness numbers, a prioritized improvement plan (which gap first and why), and the **spec diff**. One part is a governance output: the **decision rights and escalation path** the evaluation surfaced (who may rely on the dashboard, who reviews it, what happens when it's wrong). *An override that kept recurring is the signal that a right to override and a path to escalate should be written down.* This is the evidence you defend in the Day-4 capstone, including **who is accountable when the dashboard is wrong.**

> **The clearest proof that you ran the loop rather than merely shipped an app is the distance between your first spec and your last.**

## 9.6 Key terms

- **Enacted versus specified** — the core comparison; divergence means a flaw in the app or a gap in the spec.
- **The five-layer evaluation model** — data integrity, representational honesty, decision fitness, usability, trust & governance.
- **Deterministic evidence harness** — known-answer reconciliation/scenario checks; no model judges; run before and after for a measured before-and-after.
- **Structured self-audit** — human review for the layers a number can't settle.
- **Delegated evaluation** — the agent does the labor and surfaces candidates; the human renders the verdict.
- **Fold-back** — writing each confirmed finding back into the workspace (spec, harness, skills, Knowledge stock, governance).

---

# 10 · Conclusion: What You Leave With

> **The Builder Who Asked for the Next Dataset.** Handed a new dataset with none of the scaffolding, the old reflex was *what can I do with these columns?* This time the question comes before the file is even open: *what decision would this change, for whom, and what could the data honestly carry?* *They have not memorized an app. They have learned to run a loop, and the loop does not care which data it runs on.*

You arrived able to build; the course added the judgment that turns a build into something worth deploying. You leave with **three things:**

1. **A deployed app** you framed from a real decision and user, gated against the data, specced so a stranger could build it, built in the cheapest sufficient forms, verified by behavior, used for a week, and evaluated against what you specified. *You can say in one sentence what it claims and why that claim is warranted — more than most AI initiatives can say.*
2. **A repeatable loop** — Plan, Build, Use, Evaluate around a Living Spec, inside a workspace of Knowledge and Skills producing Deliverables, bounded by a governance membrane. *Portable in a way the app is not: point it at a new folder and run it again.*
3. **A working vocabulary** — the loop, the Living Spec, the three stocks, the governance boundary, the six principles. *What makes the judgment transmissible instead of trapped in one builder's head.*

**The through-line:** capability is abundant and getting cheaper; **what is scarce is judgment** — knowing what is worth building, what "good" must mean before the dashboard turns green, and whether a confident output is correct. Mollick (2026): "what's scarce is knowing what to ask for." *The method does not make you faster at building, which you already were. It makes you better at the part the build cannot supply.*

**The recursion:** the instructor did not teach this loop from the outside — he ran it. Kinquiry was built by the loop it illustrates, and its dashboard was assembled by the very kind of dynamic workflow the book asks you to recognize. *A method that cannot survive being turned on itself is a slogan. This one was, and it did.*

> **You know you carry the method when** a new dataset makes you reach for the decision and the user before the columns; when you can write down what "good" must mean tightly enough that a stranger could score it; when you treat a confident output as a claim to check rather than a fact to ship; and when you can name, in a sentence, the form you chose not to build and why. **The app was the assignment. The loop is what you keep.**

---

## Selected references (across the book)

- Anthropic (2024) *Building effective agents*; (2025a) *Connect Claude Code to tools via MCP*; (2025b) *Create custom subagents*; (2025c) *Equipping agents for the real world with Agent Skills*; (2025d) *How we built our multi-agent research system*; (2025e) *Extend Claude with skills*; (2026b) *Best practices for Claude Code*; (2026c) *How Claude remembers your project*; (2026d) *Effective context engineering for AI agents*.
- Argyris & Schön (1974) *Theory in Practice*; BCG (2025); Chroma (2025) *Context rot*; Collins Dictionary (2025); Contreras (2026) *SaaSpocalypse*; Fortune (2025); IBM (2025); Karpathy (2025); Lafley & Martin (2013) *Playing to Win*; Liu et al. (2024) *Lost in the middle*; MCP Registry (2026); Mollick (2024) *Co-Intelligence*, (2026) *Management as AI superpower*; Rubin (2025) *The Way of Code*; Shihipar (2026) *The unreasonable effectiveness of HTML*; Shihipar & Bidasaria (2026) *A harness for every task*; Son (2023); Star & Griesemer (1989); STEP Project Global Consortium & KPMG Private Enterprise (2024); Stulberg & Koh (2026) *GitHub is the new Google Drive*; Willison (2025).
