# Thesis Template Structure and Workflow

This repository is organized so that you usually write content in chapter files while `mythesis.tex` orchestrates the full thesis build.

## 1) Repo Structure

- `mythesis.tex`
  - Main entrypoint (root document).
  - Defines front matter (title, declarations, acknowledgements, abstract, ToC/LoF/LoT, symbols).
  - Includes chapters and appendices via `\input{...}`.
  - Defines bibliography style and bibliography sources.
- `Thesis.cls`
  - Custom class with layout/margins and many NTU-specific macros.
  - Contains thesis metadata placeholders (`\thesistitle`, `\authors`, `\degree`, etc.).
  - Usually edit metadata section only; avoid changing internals unless necessary.
- `Chapters/`
  - Main writing files (e.g., `Chapter1.tex`, `Chapter2.tex`, ...).
  - This is where you will spend most of your time.
- `Appendices/`
  - Appendix chapter files.
- `References/`
  - BibTeX databases (`*.bib`) that store reference entries.
- `Figures/`
  - Image assets grouped by chapter.
- `Styles/`
  - Supporting style assets (logo, signature image, custom style files).
- `.vscode/settings.json`
  - VS Code LaTeX Workshop build settings (created for this repo).

## 2) How Compilation Works

This project uses:

- `natbib` in `mythesis.tex`
- BibTeX databases under `References/`
- `\bibliographystyle{unsrtnat}` and `\bibliography{References/first_paper,References/second_paper}`

Build flow (automated by LaTeX Workshop recipe `pdflatex -> bibtex -> pdflatex -> pdflatex`):

1. LaTeX pass creates auxiliary files and citation placeholders.
2. BibTeX reads citations and `*.bib` entries, then generates bibliography output.
3. Additional LaTeX passes resolve references, citation numbers, and links.

You do not manually run these steps when using LaTeX Workshop; one build command handles it.

## 3) Frequent Editing Loop (Daily Workflow)

Use this repeated loop while writing:

1. Edit chapter content in `Chapters/*.tex`.
2. Add labels for anything you may reference (`\label{...}`).
3. Add citations (`\cite{key}` / `\citet{key}`) where needed.
4. Save the file.
5. Auto-build runs on save (configured in `.vscode/settings.json`).
6. Check PDF preview and problems panel.
7. Fix warnings/errors and save again.

## 4) Where to Change What

- Thesis identity (title, author, degree, supervisor, department): `Thesis.cls` metadata section.
- Front matter text (acknowledgements, abstract, declaration body): `mythesis.tex`.
- Core research writing: `Chapters/*.tex`.
- Appendix material: `Appendices/*.tex`.
- Citation records: `References/*.bib`.

## 5) Adding a New Chapter

1. Create a file such as `Chapters/Chapter6.tex`.
2. Start with:

```tex
%!TEX root=../mythesis.tex
\chapter{Your Chapter Title}
\chaptermark{Short Header Title}
\label{ch:your_label}
```

3. Include it in `mythesis.tex` with:

```tex
\input{./Chapters/Chapter6}
```

## 6) Add and Cite References (Important)

For each paper/book/source you want to use:

1. Add one BibTeX entry in a `.bib` file under `References/`.
2. Give it a unique citation key, e.g. `smith2024transformers`.
3. Cite in chapter text using:
   - `\cite{smith2024transformers}` for numeric citation
   - `\citet{smith2024transformers}` for author-style text citation
4. Save; LaTeX Workshop triggers the multi-pass build.
5. Verify the citation appears and bibliography updates in PDF.

Example BibTeX entry:

```bibtex
@article{smith2024transformers,
  author  = {John Smith and Jane Doe},
  title   = {A Strong Paper Title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {12},
  number  = {3},
  pages   = {100--120},
  doi     = {10.1000/example-doi}
}
```

Example usage in chapter:

```tex
Recent findings support this direction \cite{smith2024transformers}.
Smith and Doe argue that ... \citet{smith2024transformers}.
```

## 7) What Is Automated vs Manual

Automated:

- Running multi-pass compilation
- Running BibTeX
- Regenerating bibliography ordering/numbering
- Resolving cross-references and hyperlinks

Manual (you must do):

- Add accurate BibTeX entries
- Use correct citation keys in text
- Keep labels unique and meaningful
- Fix LaTeX syntax or missing-file errors

## 8) Practical Guardrails

- Keep `\label` close to `\chapter`, `\section`, `\caption`, or equation.
- Use consistent label prefixes:
  - `ch:...`, `sec:...`, `fig:...`, `tab:...`, `eq:...`, `app:...`
- Store figures under chapter-specific subfolders in `Figures/`.
- Commit frequently after each stable change.
- Avoid heavy class-level edits in `Thesis.cls` until content is mature.

## 9) First-Time Environment Checklist

1. Install a TeX distribution (MiKTeX or TeX Live).
2. Ensure `pdflatex` and `bibtex` are available in PATH.
3. Install VS Code extension: LaTeX Workshop.
4. Open this repo root in VS Code.
5. Build `mythesis.tex` using recipe `pdflatex -> bibtex -> pdflatex -> pdflatex`.
