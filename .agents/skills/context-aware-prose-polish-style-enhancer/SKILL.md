---
name: context-aware-prose-polish-style-enhancer
description: Refine existing thesis text or paragraphs in systems engineering and techno-economic writing while preserving technical meaning, citations, and LaTeX syntax. Use when users ask to improve clarity, style, tone, argument precision, or concision without changing claims.
---

# Context-Aware Prose Polish and Style Enhancer

## Use This Skill When

- The user asks to improve existing thesis prose without changing technical meaning.
- The input already contains the core claims, data, and citations, but writing quality needs refinement.
- The user requests sharper argument flow, stronger vocabulary precision, or removal of fluff.

## Do Not Use This Skill When

- The user asks for new technical content, new assumptions, or missing data synthesis.
- The task requires debugging LaTeX compilation issues rather than prose editing.
- The user asks to transform bullet notes into new narrative paragraphs from scratch.

## Core Objective

Refine user-provided prose to publication-grade academic quality while keeping technical claims unchanged.

## Mandatory Guardrails

- Preserve all LaTeX commands, environments, inline math, display math, and citation tags exactly as written.
- Preserve all technical claims, parameter values, and causal conclusions exactly.
- Never add new facts, data, references, or assumptions that are not in the input.
- Never use conversational or corporate buzzwords such as "game-changing", "synergy", "revolutionary", or "dive deep".

## Editing Rules

- Replace vague adjectives and hand-waving wording with precise analytical phrasing.
- Prefer active analytical construction when meaning remains identical.
- Remove filler, redundancy, and decorative phrasing.
- Tighten sentence structure for logical flow and argument sharpness.
- Keep the original style and tone class (formal, critical, technical) consistent with the source text.

## Input Expectations

- Source text is provided as paragraphs or section fragments.
- Any LaTeX, equations, and citations to preserve are included in the input.
- Optional style preference can be provided (for example more concise, more critical, or more formal).

## Output Contract

- Return only the improved text unless the user explicitly asks for commentary.
- If a claim is ambiguous enough that editing could change meaning, flag it as `NEEDS USER CLARIFICATION` and keep that span minimally edited.

## Edge Cases and Gotchas

- If the input mixes complete claims with unclear shorthand, preserve shorthand and request clarification instead of expanding it.
- If bibliography keys appear malformed, preserve them verbatim and do not attempt repair.
- If sentence-level edits risk altering causal direction, keep the original causality and reduce only wording noise.

## Trigger Examples

- Positive trigger: "Polish this paragraph and keep all technical claims and citations unchanged."
- Positive trigger: "Make this subsection publication-ready without touching LaTeX commands."
- Negative trigger: "Invent missing assumptions for the compressor model and draft a new section."
- Negative trigger: "Fix this LaTeX compile error in my table."
