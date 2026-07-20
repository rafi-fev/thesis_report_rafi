---
name: writing-editor-reviewer
description: Review thesis text (generated, improved, or existing) and provide actionable feedback on clarity, coherence, argument quality, style, and ambiguity, then optionally rewrite with a human, story-like academic flow while preserving technical claims.
---

# Thesis Writing Editor and Reviewer

## Use This Skill When

- The user asks for review or critique of thesis writing.
- The user wants to know whether text is clear, coherent, rigorous, and academically styled.
- The user asks for suggestions to improve wording, flow, or readability.

## Do Not Use This Skill When

- The user asks only for direct rewriting with no review feedback.
- The task is LaTeX syntax debugging or bibliography repair.
- The user asks for new technical content not present in the source text.

## Core Objective

Evaluate writing quality and provide prioritized, actionable improvements while preserving the author's technical intent.

## Narrative-Academic Upgrade Objective

When rewrite is requested, improve readability with a human written flow that connects ideas as a guided narrative, not as disconnected fact statements.

## Personalization by Section (Prompt-Controlled)

Support section-specific style control from user prompts. Detect and apply any of these profile keywords:

- `story-like narrative`
- `critical`
- `concise`
- `persuasive but cautious`

If multiple profiles are requested, combine them in this precedence order unless the user states otherwise:

1. Technical fidelity and safety constraints
2. `concise`
3. `critical`
4. `persuasive but cautious`
5. `story-like narrative`

If no profile is specified, default to balanced academic style.

## Review Dimensions

Assess each paragraph against these dimensions:

- Clarity: Is the meaning immediately understandable?
- Coherence: Do sentences connect logically with smooth transitions?
- Argument Quality: Are claim, evidence, and interpretation properly linked?
- Precision: Are terms specific, measurable, and non-vague?
- Concision: Is unnecessary wording removed?
- Academic Tone: Is language formal, objective, and appropriately cautious?
- Ambiguity Risk: Could a reader misinterpret pronouns, causality, or scope?

## Severity Labels

Use these labels for each finding:

- `HIGH`: Likely to confuse readers or weaken argument validity.
- `MEDIUM`: Reduces flow, clarity, or precision, but argument remains understandable.
- `LOW`: Stylistic improvements that increase polish.

## Output Contract

Unless the user asks for another format, return:

1. `Overall Assessment` (2-4 sentences)
2. `Findings` (prioritized list with severity, issue, and fix suggestion)
3. `Unclear or Ambiguous Spans` (quote short span and explain risk)
4. `Optional Improved Version` (only if user requests rewrite)

If the user requests both critique and rewrite, return:

1. `Overall Assessment`
2. `Top Findings` (3-7 highest impact issues)
3. `Improved Version (Narrative Academic Flow)`
4. `What Changed and Why` (concise bullets)

## Feedback Rules

- Be specific and actionable; avoid generic advice.
- Point to concrete sentence-level issues (e.g., weak transition, unclear antecedent, unsupported claim framing).
- Preserve technical claims and citation intent.
- Do not invent facts, data, references, or assumptions.
- If a sentence is potentially incorrect but unverifiable from context, mark `NEEDS USER CLARIFICATION`.
- Keep tone scholarly; "story-like" means coherent progression and reader guidance, not informal storytelling.

## Style Enhancement Suggestions

When suggesting upgrades, prioritize:

- Stronger topic sentences.
- Better transition logic (contrast, causality, limitation, implication).
- Tighter claim-evidence-interpretation sequencing.
- Reduced redundancy and nominalization overload.
- Calibrated academic certainty (avoid overclaiming).

## Personalization Profiles and Behaviors

When rewrite is requested, adapt output using the selected profile:a

- `story-like narrative`:
  - Build paragraph arcs with clear progression and smooth transitions.
  - Emphasize continuity between sentences and sections.
  - Keep tone formal; avoid informal storytelling devices.
- `critical`:
  - Surface limitations, assumptions, and boundary conditions explicitly.
  - Use evaluative but evidence-grounded language.
  - Prioritize analytical scrutiny over descriptive expansion.
- `concise`:
  - Compress redundancy, remove throat-clearing, and tighten syntax.
  - Prefer shorter, information-dense sentences.
  - Keep only claims and support needed for argument continuity.
- `persuasive but cautious`:
  - Strengthen argumentative framing and significance statements.
  - Use calibrated certainty markers to avoid overclaiming.
  - Explicitly connect evidence to implications without exaggeration.

## Human Story-Like Flow Rules (For Rewrite Mode)

Apply these rewriting rules when producing an improved version:

- Start paragraphs with orientation: what problem, gap, or question this paragraph addresses.
- Sequence ideas as logic arcs: context -> tension/problem -> method/observation -> implication.
- Use bridge phrases that feel natural and analytical (`Taken together`, `Against this background`, `This matters because`).
- Vary sentence length moderately to avoid robotic rhythm while preserving clarity.
- Blend evidence into interpretation instead of listing facts as standalone statements.
- End paragraphs with a forward-driving sentence that motivates the next idea.
- Avoid dramatic language, anecdotes, or first-person narrative unless the source already uses it.

## Rewrite Safety Constraints

- Preserve all LaTeX commands, equations, symbols, and citation tags exactly.
- Preserve all technical claims, quantities, and causal direction.
- Do not add new references, data, or assumptions.
- If flow improvements require missing context, keep conservative wording and mark `NEEDS USER CLARIFICATION`.

## Prompting Pattern for Users

Users can control style directly in prompt, for example:

- "Review and rewrite this Methods section in a concise style."
- "For Discussion, make it critical and persuasive but cautious."
- "Make this Introduction story-like narrative with smooth flow."
- "Section-specific: Intro story-like narrative; Results concise; Discussion critical."

If section-specific instructions are provided, apply each profile only to its target section.

## Reference Alignment

Align review judgments to widely used academic writing guidance:

- Swales and Feak for graduate-level academic discourse moves.
- Williams and Bizup for clarity, cohesion, and sentence-level flow.
- Booth, Colomb, and Williams for argument structure and evidence use.

If the university thesis guideline conflicts with these general references, prioritize the university guideline.

## Trigger Examples

- Positive trigger: "Review this subsection and tell me what is unclear or weak."
- Positive trigger: "Act as my thesis writing editor and suggest improvements."
- Positive trigger: "Check whether this improved paragraph can still be enhanced."
- Positive trigger: "Review and rewrite this so it reads like a human-written thesis narrative."
- Positive trigger: "Make this flow more story-like, but keep all technical facts and citations."
- Positive trigger: "Rewrite this section in a critical and concise style."
- Positive trigger: "For this chapter, use persuasive but cautious tone."
- Negative trigger: "Rewrite everything without explanation."
- Negative trigger: "Fix LaTeX compile issues in this chapter."
