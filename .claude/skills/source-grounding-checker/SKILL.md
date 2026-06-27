---
name: source-grounding-checker
description: Check that Claude's claims are grounded in approved sources before they are relied on. Use before final submission, presentation slides, and any output presented as reliable. Flags claims that are unsupported, vague, or invented, and names the source each supported claim rests on.
---

# Source Grounding Checker

## Purpose
Enforce the rule that Claude's outputs are claims, not facts: every claim must trace to an approved source. Catch hallucinated, vague, or invented statements before they reach a slide, a user, or the AI Council.

## When to use
- Before final submission and presentation slides.
- Before any output is presented as reliable or shown to a user.

## Approved sources (a claim must rest on at least one)
- Course materials (`knowledge/managing-intelligence/`)
- Assignment rubric / brief (`knowledge/assignment/assignment-brief.md`)
- Uploaded class documents
- The dataset (`data/`) and its codebook
- Dashboard output (recomputed/verified)
- Human notes (deployment log, reviewer notes)
- AI Council review records

## Procedure
1. Extract each factual claim from the output under review (numbers, recommendations, statements about policy, the data, or what the tool does).
2. For each claim, identify the supporting source and quote/locate it.
3. Flag claims that are **unsupported** (no source), **vague** (can't be checked), or **invented** (contradicted by or absent from sources).
4. For numeric claims, confirm they were recomputed/verified, not asserted.
5. Recommend a fix for each flagged claim: cite a source, soften to a hedge, or remove.

## Output format
```
Claim:
Status: Grounded | Unsupported | Vague | Invented
Source (if grounded):
Fix (if flagged): cite / hedge / remove
```

## Guardrails
- A claim with no approved source does not ship — it is cited, hedged, or removed.
- Do not invent course policies, grades, or instructor expectations.
- Flag uncertainty explicitly; route anything you can't ground to a human.
