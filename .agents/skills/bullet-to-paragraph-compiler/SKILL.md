---
name: bullet-to-paragraph-compiler
description: Transform fragmented bullet observations into cohesive thesis-grade technical paragraphs with explicit transitions, causal logic, and paragraph-level hierarchy. Use when users provide disjointed notes and need an integrated narrative arc.
---

# Synthesized Bullet-to-Paragraph Compiler

## Use This Skill When

- The user provides fragmented technical bullet points and wants coherent paragraphs.
- The task requires cause-to-effect flow and explicit academic transitions.
- Observations, metrics, and citations need to be integrated into a readable narrative arc.

## Do Not Use This Skill When

- The user asks to preserve exact original sentence structure.
- The request is only line-level language polishing of existing paragraphs.
- The task is debugging LaTeX compilation errors.

## Core Objective

Convert scattered bullet notes into coherent academic paragraphs with clear cause-to-effect reasoning.

## Mandatory Narrative Rules

- Build each paragraph with this structure:
  1. Topic sentence stating the main technical takeaway.
  2. Supporting evidence integrating observations and metrics.
  3. Systemic impact sentence explaining broader optimization relevance.
- Do not output bullet lists unless the user explicitly requests them.

## Transition and Flow Rules

- Use explicit transition phrases for logic control.
- Contrast transitions include: `Conversely,`, `In contrast to the static baseline,`, `While ... remains constrained,`.
- Causality transitions include: `Consequently,`, `This temporal coupling mandates,`, `Thereby triggering,`.
- Addition transitions include: `Furthermore,`, `Crucially, this is compounded by,`.

## Data and Citation Integration

- Integrate numbers and metrics into sentence flow rather than isolated statements.
- Keep citation tags (for example `\cite{...}`) attached to relevant clauses naturally.
- Preserve all provided technical values and causal relationships.

## Input Expectations

- Bullet-point observations include at least one technical claim and one supporting fact or metric.
- Any required citation tags are supplied in the notes.
- The user indicates target section context if cross-paragraph ordering matters.

## Output Contract

- Produce polished paragraphs in a logically ordered sequence.
- If source bullets are insufficient for a coherent causal chain, flag the gap as `NEEDS USER CLARIFICATION` before drafting uncertain links.

## Edge Cases and Gotchas

- If bullets contain conflicting metrics, retain both and frame the conflict explicitly.
- If notes are purely descriptive with no causal cue, avoid inventing mechanisms and request clarification.
- If transitions are overused, prioritize clarity over decorative connective phrases.

## Trigger Examples

- Positive trigger: "Turn these disjointed bullets into thesis-ready paragraphs with clear causal flow."
- Positive trigger: "Compile these optimization notes into cohesive narrative paragraphs and keep citations."
- Negative trigger: "Fix unbalanced braces in this LaTeX table."
- Negative trigger: "Only correct grammar line by line; do not restructure anything."
