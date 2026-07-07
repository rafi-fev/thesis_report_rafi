---
name: latex-syntax-compiler-debugger
description: Diagnose and repair LaTeX compilation failures and broken table layouts by isolating the exact failing line and applying minimal syntax or package fixes. Use when users provide compiler logs, malformed LaTeX fragments, or table rendering issues and want wording preserved.
---

# LaTeX Syntax and Compiler Debugger

## Use This Skill When

- The user provides LaTeX compiler errors and wants root-cause isolation.
- A table, equation block, or environment layout is broken and fails compilation.
- The user wants minimal syntax/package fixes while preserving wording.

## Do Not Use This Skill When

- The request is primarily stylistic rewriting of valid prose.
- The user asks for unsupported package design decisions without error context.
- The task is to synthesize new thesis narrative from note fragments.

## Core Objective

Identify the exact cause of LaTeX build failures and apply the smallest safe fix without changing academic wording.

## Mandatory Guardrails

- Preserve all underlying academic wording unless the user explicitly asks for wording edits.
- Isolate the root-cause line number first, then patch only the required scope.
- Prefer minimal syntax fixes over broad rewrites.

## Debug Workflow

1. Parse the first actionable LaTeX error from the log and map it to file plus line.
2. Check delimiter balance and structure:
   - Inline and display math delimiters (`$`, `$$`, `\(`, `\)`, `\[`, `\]`)
   - Curly braces and optional-argument brackets
   - `\begin{...}` and `\end{...}` pairing
3. For tables, verify column specification, ampersand counts, line breaks, and span commands (`\multicolumn`, `\multirow`).
4. Detect package or command conflicts and propose the least invasive compatible fix.
5. Return corrected snippet and explain why it compiles.

## Input Expectations

- Compiler log excerpt containing the first actionable error.
- Failing source snippet with nearby lines.
- Optional preamble/package list when conflict is suspected.

## Output Contract

- Report the exact failing location as `File:Line` when available.
- Provide a corrected code snippet that can be pasted directly.
- Keep explanations concise and technical.
- If the error cannot be localized from provided data, return `NEEDS MORE CONTEXT` and list the minimal missing log lines.

## Edge Cases and Gotchas

- If multiple errors appear, prioritize the first root cause before downstream errors.
- If a table overflows but compiles, classify as layout issue and provide non-destructive layout fix options.
- If line numbers in logs are offset by included files, state the ambiguity and request the expanded source snippet.

## Trigger Examples

- Positive trigger: "Here is my LaTeX error log. Find the exact failing line and fix it."
- Positive trigger: "My table is broken after adding \\multicolumn; patch only what is necessary."
- Negative trigger: "Rewrite this paragraph in stronger academic style."
- Negative trigger: "Draft a new subsection on ramping constraints."
