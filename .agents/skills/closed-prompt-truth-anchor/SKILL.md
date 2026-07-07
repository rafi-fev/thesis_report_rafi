---
name: closed-prompt-truth-anchor
description: Enforce strict non-hallucinating thesis drafting and synthesis using only explicitly provided context and local references.bib entries. Use when users require evidence-bounded writing, parameter integrity, or explicit missing-context flags.
---

# Closed-Prompt Truth Anchor

## Use This Skill When

- The user requires strict evidence-bounded drafting with no hallucination.
- Numerical parameters and citation integrity must remain tied to provided context only.
- The task needs explicit missing-information flags instead of guessed values.

## Do Not Use This Skill When

- The user asks for speculative brainstorming or hypothetical values.
- The user explicitly requests plausible placeholder assumptions.
- The request is purely stylistic polishing with no context-integrity constraint.

## Core Objective

Act as a strict academic compiler that produces only context-grounded output.

## Mandatory Guardrails

- Use only information explicitly present in:
  - User-provided text in the current task
  - Local `references.bib` content when available
- Never invent technical values, assumptions, citations, or missing mechanisms.
- If a required parameter is absent, emit `MISSING CONTEXT: <missing item>`.
- Do not replace missing values with placeholders such as `X`, `TBD`, or guessed ranges.

## Evidence Rules

- Preserve all provided numbers and qualifiers exactly.
- When citing, use only keys that exist in the provided bibliography context.
- If a statement is an inference from provided material, mark it explicitly as `Inference from provided context`.

## Input Expectations

- Source text and data excerpts are provided in the current thread.
- Optional local bibliography file (`references.bib`) is available for citation-key validation.
- Required technical outputs are explicitly stated by the user.

## Output Contract

- Provide the requested draft or synthesis in normal form.
- Append a `Context Gaps` section only when at least one required item is missing.
- List each missing item on its own line with the exact prefix `MISSING CONTEXT:`.

## Edge Cases and Gotchas

- If two provided sources conflict, surface the conflict and avoid selecting one silently.
- If a value appears implied but not explicit, treat it as missing and flag it.
- If citation keys are unavailable, omit fabricated keys and record the missing citation requirement.

## Trigger Examples

- Positive trigger: "Draft this paragraph using only the data below; flag any missing values."
- Positive trigger: "Synthesize these notes and references.bib entries without adding assumptions."
- Negative trigger: "Estimate a reasonable surge-limit percentage if not provided."
- Negative trigger: "Make up placeholder citations so the section looks complete."
