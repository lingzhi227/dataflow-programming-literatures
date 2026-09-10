# From Algorithm Semantics to Processing Elements

**A Survey of Spatial High-Level Synthesis**

Lingzhi Yang — Department of Applied Mathematics and Statistics, Stony Brook University

Research manuscript, 10 September 2026

**[Read the PDF](spatial-hls-survey.pdf)** · **[TeX source](spatial-hls-survey.tex)** · **[Portable source package](spatial-hls-survey-source.zip)** · **[References](../papers/references.bib)**

The manuscript connects two problems: constructing useful spatial algorithms and realizing them as finite PE programs. It studies the mathematical and operational objects used at each stage, rather than treating all graph representations as equivalent or equating a list of implemented operators with a general compiler.

| Chapters | Content |
|---|---|
| 1–3 | Scope, historical distinctions, values/state, stream semantics, rates, finite storage and progress |
| 4 | Constructive methods: program invariants, FLAME, recurrence localization, a worked FIR chain, projection/offsets and retiming |
| 5–7 | Scheduling and routing, memory costs, SPL/Sigma-SPL/HSPL, a two-PE FFT derivation and modern compiler representations |
| 8–9 | GEMM recurrence and SUMMA realization; a bounded-deadlock counterexample; actual CSL, IRON and Metalium interfaces |
| 10 | Interval dynamic programming, sparse iteration, streaming Givens QR versus TSQR, iterative solvers, attention and wafer-scale state |
| 11–12 | A constructive compiler design, cross-family comparison, search/acceptance conditions, numerical composition and research questions |
| Appendix A | Finite prototype, original bounded SDK evidence, commands and a conditional ownership proof |
| Appendix B | Pinned source versions, reading scope and limits |

The paper is a selective technical synthesis, not an exhaustive bibliometric review. Mathematical derivations, attributed literature results, inspected software behavior and measurements are distinguished. The prototype does not implement the proposed multi-backend compiler. Its single SDK experiment does not establish hardware performance or full-model inference.

## Build

From the repository root, using Tectonic 0.17.0:

```sh
tectonic notes/spatial-hls-survey.tex
```

The manuscript uses `elsarticle` 3.3 (2020-11-20) with the exact options `[final,3p,times,authoryear]` and the `elsarticle-harv` bibliography style, matching the supplied [formatting reference, version 1](https://arxiv.org/abs/2310.18345v1). The layout is A4, single column, with Times-family text and parenthetical author–year citations. The centered frontmatter has one author and one italic affiliation line; the paper makes no journal-submission or publication claim.

Tectonic resolves the standard TeX dependencies, including `elsarticle`, `txfonts`, `fontenc`, `natbib`, `amsmath`, `amsthm`, `mathtools`, `booktabs`, `tabularx`, `listings`, TikZ, `hyperref`, `xurl`, `iftex` and `newunicodechar`. Explicit T1 encoding preserves the template's Times fonts under Tectonic; two XeTeX-only accent mappings preserve Unicode author names. The bibliography is `papers/references.bib`. All four figures are inline TikZ, so no external images are required.

The portable ZIP contains the TeX source, BibTeX database, generated bibliography, license and build note in one directory. After extraction, run `tectonic spatial-hls-survey.tex`. Its bibliography path is adjusted for that directory; the rebuilt 30-page PDF has identical extracted text on every page to the repository PDF.

The [reading notes](reading-notes.md) and [research revisions](research-revisions.md) record the evidence and substantive changes behind the manuscript. The supporting [Pragma experiment](https://github.com/lingzhi227/MIMD_dataflow/blob/main/docs/research/spatial-contracts.md) has its own reproduction requirements.
