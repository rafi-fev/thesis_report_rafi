# Prompt Templates for Thesis Literature Review

Use the following templates directly. Replace all placeholders in brackets.

## Template A: Single Paper Deep Extraction (Recommended Default)

```text
Use $thesis-literature-review-copilot.

My thesis objective:
[WRITE OBJECTIVE IN 1-3 SENTENCES]

Target section:
[e.g., Chapter 2.3: Energy management optimization]

Source paper:
[attach PDF OR paste extracted text OR provide DOI metadata]

Task:
1) Extract only thesis-relevant key points:
   - problem addressed
   - method/model
   - dataset/case scope
   - main quantitative or qualitative findings
   - limitations/assumptions
2) Explain how this paper supports, contrasts, or bounds my thesis objective.
3) Write one LaTeX-ready paragraph (120-180 words) for my literature review with `\cite{...}`.
4) Generate BibTeX entry and propose one citation key using `FirstAuthorYearShortTopic`.
5) If any metadata is uncertain, mark as `TODO_VERIFY` under an "Uncertainty Flags" section.

Rules:
- Do not invent facts or references.
- Keep claims bounded to evidence from this paper.
- Make the paragraph analytical, not just descriptive.
```

## Template B: Fast Triage from Abstract

```text
Use $thesis-literature-review-copilot.

My thesis objective:
[WRITE OBJECTIVE]

Abstract:
[PASTE ABSTRACT]

Score this paper for relevance (0-2) using:
- objective fit
- method fit
- system/context fit

Return:
1) Relevance score with short justification
2) Keep/Discard recommendation
3) If kept, provide a 2-3 sentence thesis-aligned summary
4) Candidate citation key (no BibTeX needed in triage mode)
```

## Template C: Multi-Paper Thematic Synthesis (5-10 Papers)

```text
Use $thesis-literature-review-copilot.

My thesis objective:
[WRITE OBJECTIVE]

Target subsection:
[WRITE SUBSECTION]

Papers:
[PASTE LIST OF PAPER NOTES OR SUMMARIES WITH CITATION KEYS]

Task:
1) Cluster papers into 3-5 themes.
2) For each theme, compare methods, assumptions, and findings.
3) Highlight agreements, contradictions, and evidence strength.
4) Identify concrete research gaps directly linked to my thesis objective.
5) Write one synthesis paragraph per theme with citation keys included.

Rules:
- Synthesize by theme, not one-paper-at-a-time narration.
- Preserve citation keys exactly as provided.
- Mark unsupported cross-paper claims as `NEEDS VERIFICATION`.
```

## Template D: Integrate into Existing Chapter Text

```text
Use $thesis-literature-review-copilot.

My thesis objective:
[WRITE OBJECTIVE]

Current subsection text:
[PASTE CURRENT LATEX PARAGRAPHS]

New paper evidence:
[PASTE PAPER EXTRACTION + CITATION KEY + BIBTEX]

Task:
1) Insert the new evidence into the subsection with coherent flow.
2) Keep all existing LaTeX commands and citations intact.
3) Add a transition sentence before and after the inserted content.
4) Return:
   - revised subsection text
   - a short changelog (what was added and why)
```

## Template E: BibTeX Audit and Key Normalization

```text
Use $thesis-literature-review-copilot.

Existing `.bib` snippet:
[PASTE BIB ENTRIES]

New paper metadata:
[PASTE DOI/URL/TITLE/AUTHORS/YEAR/JOURNAL]

Task:
1) Generate corrected BibTeX for the new entry.
2) Propose key that avoids collisions with existing keys.
3) If collision exists, provide suffix variant (`a`, `b`, `c`) and explain.
4) Return only:
   - final BibTeX block
   - final citation key
   - fields requiring manual verification (`TODO_VERIFY`)
```

## Minimal Daily Prompt (Fast Workflow)

```text
Use $thesis-literature-review-copilot on this paper for my thesis objective: [OBJECTIVE].
Return thesis-relevant key points, one Chapter 2 paragraph with `\cite{key}`, and BibTeX with the same key.
Flag uncertainty as `TODO_VERIFY`.
```
