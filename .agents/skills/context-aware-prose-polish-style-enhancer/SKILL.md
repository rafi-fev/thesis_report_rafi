---
name: context-aware-prose-polish-style-enhancer
description: Refine existing thesis text or paragraphs in systems engineering and techno-economic writing while preserving technical meaning, citations, and LaTeX syntax. Use when users ask to improve clarity, paragraph flow, argument precision, and academic style without changing claims.
---

# Context-Aware Prose Polish and Style Enhancer

## Use This Skill When

- The user asks to improve existing thesis prose without changing technical meaning.
- The input already contains the core claims, data, and citations, but writing quality needs refinement.
- The user requests sharper paragraph flow, stronger academic style, or removal of fluff.

## Do Not Use This Skill When

- The user asks for new technical content, new assumptions, or missing data synthesis.
- The task requires debugging LaTeX compilation issues rather than prose editing.
- The user asks to transform bullet notes into new narrative paragraphs from scratch.

## Core Objective

Refine user-provided prose to publication-grade academic quality while keeping technical claims unchanged.

## Thesis Writing Best-Practice Anchors

Apply these principles when polishing:

- Paragraph unity: one controlling idea per paragraph, with each sentence serving that idea.
- Coherent progression: move from known context to new contribution (`given -> new` sentence flow).
- Claim-evidence-interpretation logic: ensure claims are followed by evidence and analytical interpretation.
- Precision over ornament: prefer specific technical nouns and verbs over vague intensifiers.
- Cautious academic stance: use calibrated certainty (`suggests`, `indicates`, `is consistent with`) when claims are not absolute.
- Reader guidance: use explicit transitions to show contrast, causality, limitation, and implication.
- Citation integrity: preserve all citation tags and keep them attached to the sentence they support.

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
- Fix weak sentence openings that break flow; preserve meaning while improving continuity.
- Reduce stacked clauses when they obscure causality.
- Keep pronoun references unambiguous (`this`, `it`, `they` must have clear antecedents).

## Paragraph Flow Checklist

Before returning the polished paragraph, confirm:

- Opening sentence states the paragraph focus clearly.
- Middle sentences develop evidence or mechanism in a logical order.
- Final sentence closes with implication, limitation, or transition to next idea (if present in source intent).
- No sentence is off-topic relative to the controlling idea.

## Input Expectations

- Source text is provided as paragraphs or section fragments.
- Any LaTeX, equations, and citations to preserve are included in the input.
- Optional style preference can be provided (for example more concise, more critical, or more formal).

## Output Contract

- Return only the improved text unless the user explicitly asks for commentary.
- If a claim is ambiguous enough that editing could change meaning, flag it as `NEEDS USER CLARIFICATION` and keep that span minimally edited.

## Optional Commentary Mode (Only If User Asks)

- Provide:
  1. `Revised Text`
  2. `Why It Reads Better` (2-5 concise bullets)
  3. `Ambiguities` (only when needed)

## Edge Cases and Gotchas

- If the input mixes complete claims with unclear shorthand, preserve shorthand and request clarification instead of expanding it.
- If bibliography keys appear malformed, preserve them verbatim and do not attempt repair.
- If sentence-level edits risk altering causal direction, keep the original causality and reduce only wording noise.
- If the paragraph lacks evidence for a claim, do not invent support; keep text conservative and flag `NEEDS USER CLARIFICATION`.
- If original wording is grammatically weak but meaning is uncertain, prioritize semantic safety over aggressive rewriting.

## Trigger Examples

- Positive trigger: "Polish this paragraph and keep all technical claims and citations unchanged."
- Positive trigger: "Make this subsection publication-ready with stronger flow, without touching LaTeX commands."
- Negative trigger: "Invent missing assumptions for the compressor model and draft a new section."
- Negative trigger: "Fix this LaTeX compile error in my table."

## Reference Basis for Writing Guidance

This skill follows broadly accepted academic writing guidance used in thesis writing support:

- Cohesion and coherence principles from academic style guidance (topic focus, logical progression, transition control).
- Claim-evidence-interpretation paragraph logic common in scientific and engineering writing pedagogy.
- Revision-for-clarity principles emphasizing concise, concrete, and reader-centered prose.
- Institution thesis-manual conventions prioritizing formal tone, precision, and traceable argument structure.

Named references used as anchor standards:

- Swales and Feak, *Academic Writing for Graduate Students* (rhetorical moves and academic discourse conventions).
- Williams and Bizup, *Style: Lessons in Clarity and Grace* (clarity, cohesion, sentence flow).
- Booth, Colomb, and Williams, *The Craft of Research* (claim-evidence-reasoning and argument discipline).

If these general references conflict with the user's university thesis manual, prioritize the university manual.
