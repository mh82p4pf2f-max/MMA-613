---
name: opportunity-framing
description: Frame the project from a real user and a real classroom decision before any build. Use whenever the concept starts becoming broad, vague, or feature-led ("an AI classroom assistant"), or when starting/re-scoping a concept. Forces a single user, a single decision, and a defensible reason to build.
---

# Opportunity Framing

## Purpose
Keep the project opportunity-first: the **decision and the user drive it, the data is a gate not a generator**. Stop the project from drifting into a generic "AI classroom assistant." Produce a specific concept with a clear user, a clear classroom decision, and a defensible reason a dashboard/app is the right tool.

## When to use
- The concept is becoming too broad, vague, or impressive-but-pointless.
- You catch yourself describing what the data *has* instead of what a user *decides*.
- Starting a new concept, or choosing between candidate concepts.

## Inputs to read
`knowledge/assignment/assignment-brief.md`, `deliverables/project-memory.md`, `knowledge/managing-intelligence/managing-intelligence.md` (Ch 3.1), `CLAUDE.md`.

## Procedure
1. **Name three things without naming a data column:** the **decision** the tool changes, the **primary user** who owns that decision, and the **leverage** (what they could not do, or not do well, without it).
2. **State the center of gravity:** a dashboard a human reads and steers, or an agent that runs under oversight. (Good means something different for each.)
3. **Run the one-sentence test:** "This lets [user] do [X] they couldn't do before." If you can only describe what the data has, stop — it's a capability looking for a problem.
4. **Run the Slightly-Slower Test:** what does the user do today without the tool? If the answer is "the same thing, slightly slower," kill the concept.
5. **Define out-of-scope** explicitly, each non-goal tied to a structural reason.
6. If broad, converge: surface 3+ candidate framings, lock criteria (dominated by one-week deployability), pick one, and record the rejected alternative + why.

## Output format
```
Concept title:
Primary user:
Secondary users:
Classroom pain point:
Decision / workflow supported:
Leverage (why Claude/dashboard helps):
Why a dashboard/app is the right format:
One-sentence test: This lets ___ do ___ they couldn't do before.
Out of scope (with reasons):
Rejected alternative + reason:
```

## Guardrails
- A specific user and decision are mandatory; "students" or "instructors" in general is not specific enough — narrow it.
- This skill proposes framing; the team confirms it. Output is a claim to review, not a settled fact.
- Hand the result to the `claude-md-architect` skill to write it into the spec.
