---
name: thesis-literature-review-copilot
description: Extract, structure, and write thesis literature-review content from papers, including thesis-objective relevance mapping, key-point synthesis, LaTeX paragraph drafting with citation keys, and BibTeX generation. Use when the user provides a paper PDF/text/DOI and asks for per-paper insights, Chapter 2 writing support, citation-ready paragraphs, or multi-paper thematic synthesis.
---

# Thesis Literature Review Copilot

## Core Objective

Turn paper-level evidence into thesis-ready literature review writing with traceable claims and citation-safe outputs.

## Use This Skill When

- Receive one paper and need key points linked to a thesis objective.
- Need a literature-review paragraph with LaTeX citation keys.
- Need a BibTeX entry draft for `.bib` files.
- Need theme-level synthesis across multiple papers.

## Do Not Use This Skill When

- Need full systematic-review statistics (for example PRISMA flow counts) without curated data from the user.
- Need to invent missing evidence, missing metadata, or missing references.
- Need only language polishing of text already written (use prose-polishing skills).

## Required Inputs

Collect or request these inputs before writing:

- Thesis objective or research question.
- Target chapter/subsection in the thesis.
- Source artifact for the paper (PDF, extracted text, abstract, or DOI metadata).
- Preferred citation style and key pattern (if already defined in project).

If one input is missing, proceed with conservative assumptions and label the assumption explicitly.

## Execution Workflow

1. Parse the paper artifact and isolate thesis-relevant content.
2. Extract structured evidence:
   - Problem context
   - Method/model
   - Data or case setup
   - Main findings
   - Limitations and assumptions
3. Map findings to thesis objective:
   - Explain direct relevance
   - Explain boundaries or mismatch
4. Draft thesis paragraph with explicit citation key insertion (`\cite{...}`).
5. Draft BibTeX and citation key candidate.
6. Add confidence flags for uncertain metadata or claims.

## Output Contract

Unless the user requests another format, return:

1. `Paper Key Points (Thesis-Relevant)`
2. `Objective Alignment`
3. `Chapter Draft Paragraph (LaTeX-ready with \cite{})`
4. `BibTeX Draft + Citation Key`
5. `Uncertainty Flags`

Keep claims concise and evidence-bound. Do not return generic summaries without relevance mapping.

## Citation Integrity Guardrails

- Never invent bibliographic fields.
- Mark unknown fields as `TODO_VERIFY`.
- If only partial metadata is available, return a minimal BibTeX draft and flag missing fields.
- Keep one claim-to-source chain: each critical claim in the drafted paragraph must be attributable to the provided paper notes.
- Preserve existing citation keys if the user already uses them.

## Citation Key Rules

- Default pattern: `FirstAuthorYearShortTopic` (for example `Smith2024MicrogridPlanning`).
- Append letter suffix for duplicates in same year (`a`, `b`, `c`).
- Avoid punctuation and spaces in keys.

## Prompt Templates

Use the templates in [references/prompt_templates.md](references/prompt_templates.md) based on task type:

- `Template A`: single-paper deep extraction and paragraph draft.
- `Template B`: abstract-only triage.
- `Template C`: multi-paper synthesis by theme.
- `Template D`: chapter integration with transition writing.

## Quality Checklist Before Returning

- Verify every paragraph sentence supports the stated thesis objective.
- Verify the paragraph includes at least one explicit limitation when present in source.
- Verify citation key in paragraph exactly matches BibTeX key.
- Verify uncertain information is flagged and not silently assumed.

## Trigger Examples

- Positive trigger: "Read this paper and write a thesis-ready paragraph with BibTeX."
- Positive trigger: "Connect this article to my Chapter 2 objective and add citation key."
- Positive trigger: "Synthesize these 8 papers into themes and identify research gaps."
- Negative trigger: "Polish this paragraph only for style while preserving meaning."
