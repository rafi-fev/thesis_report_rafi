# LaTeX Cheat Sheet for Thesis Writing

This cheat sheet focuses on commands you will use frequently in this repository.

## 1) Document and Chapter Basics

```tex
\chapter{Introduction}
\chaptermark{Introduction}
\label{ch:introduction}

\section{Background}
\label{sec:background}
```

- `\chapter{...}` creates a chapter.
- `\chaptermark{...}` sets short header text for page headers.
- `\label{...}` creates an anchor for references.

## 2) Cross-Referencing

```tex
As shown in Chapter \cref{ch:introduction} and Section \sref{sec:background}.
See Figure \fref{fig:system_arch} and Table \tref{tab:results}.
Equation \eqref{eq:loss} defines the objective.
```

In this template, shortcuts are available from `Thesis.cls`:

- `\cref{...}` chapter reference
- `\sref{...}` section reference
- `\fref{...}` figure reference
- `\tref{...}` table reference
- `\aref{...}` appendix reference
- Standard `\eqref{...}` for equation number

## 3) Equations

```tex
\begin{equation}
\label{eq:loss}
\mathcal{L}(\theta)=\sum_{i=1}^{N} \ell_i(\theta)
\end{equation}
```

- Put `\label` inside equation environment.
- Reference later with `\eqref{eq:loss}`.

## 4) Figures

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{Chapter1/demo1}
  \caption{System overview.}
  \label{fig:system_arch}
\end{figure}
```

- Path is relative to `Figures/` because `mythesis.tex` sets `\graphicspath`.
- Keep `\label` after `\caption` for safe numbering.

## 5) Tables

```tex
\begin{table}[htbp]
\centering
\begin{tabular}{lcc}\toprule
Method & Accuracy & F1\\ \midrule
A & 0.91 & 0.89\\
B & 0.93 & 0.92\\
\bottomrule
\end{tabular}
\caption{Main results.}
\label{tab:results}
\end{table}
```

- `\toprule`, `\midrule`, `\bottomrule` come from `booktabs` (already loaded).

## 6) Lists

```tex
\begin{itemize}
  \item First bullet
  \item Second bullet
\end{itemize}

\begin{enumerate}
  \item First numbered item
  \item Second numbered item
\end{enumerate}
```

## 7) Citations and Bibliography

### In text

```tex
Prior work studied this setting \cite{smith2024transformers}.
\citet{smith2024transformers} reported improved robustness.
```

- `\cite{...}`: numeric citation in brackets.
- `\citet{...}`: author-style textual citation.

### In `.bib`

```bibtex
@article{smith2024transformers,
  author  = {John Smith and Jane Doe},
  title   = {A Strong Paper Title},
  journal = {Journal Name},
  year    = {2024}
}
```

- Key (`smith2024transformers`) must be unique.
- Match exact key in `\cite{...}`.

### Intuition for automation

- You only add BibTeX entries and call `\cite{key}`.
- Build recipe (`pdflatex -> bibtex -> pdflatex -> pdflatex`) runs LaTeX + BibTeX passes and updates numbering/order automatically.

## 8) Appendix

```tex
% in mythesis.tex
\appendix
\input{./Appendices/AppendixA}
```

```tex
% in Appendices/AppendixA.tex
\chapter{Additional Proofs}
\label{app:proofs}
```

- `\appendix` switches chapter lettering to appendix mode.

## 9) Helpful Writing Patterns

### Definition/Theorem style blocks (already defined)

```tex
\begin{definition}[Feasible Set]
A set is feasible if ...
\end{definition}

\begin{theorem}[Convergence]
Assume A1--A3. Then ...
\end{theorem}

\begin{proof}
Proof sketch ...
\end{proof}
```

### Part separation (optional)

```tex
\part{Part I: Fundamentals}
\input{./Chapters/Chapter2}
\input{./Chapters/Chapter3}
```

## 10) Frequent Errors and Fixes

- `Undefined control sequence`
  - Usually typo in command name or missing package.
- `Citation ... undefined`
  - Key missing/mismatched in `.bib`, or build needs another pass.
- `Reference ... undefined`
  - Missing `\label` or needs another build pass.
- `File ... not found`
  - Wrong figure path/filename or extension mismatch.

## 11) Recommended Daily Mini-Checklist

1. Write in `Chapters/*.tex`.
2. Add labels while writing (not later).
3. Add citations immediately with proper BibTeX entry.
4. Save and inspect PDF.
5. Resolve warnings early.
