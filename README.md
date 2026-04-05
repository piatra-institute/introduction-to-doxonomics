# Introduction to Doxonomics

**Toward a Science of How Power Shapes Belief**

A research project of the [Piatra Institute](https://piatra.institute).

---

Doxonomics (from Greek *doxa* — opinion, common belief — and *-nomics*) is the study of how material power, institutions, and infrastructure shape public belief. This book develops the field's foundations, formal apparatus, methods, applications, and ethics.

## Structure

The book has 5 parts, 36 chapters, and 8 appendices:

| Part | Chapters | Contents |
|------|----------|----------|
| I — Foundations | 1–5 | What doxonomics is, ontology of belief, intellectual prehistory, units of analysis, belief production chain |
| II — Concepts and Models | 6–12 | Epistemic capital, narrative infrastructure, common-sense capture, doxonomic power, economics of belief, formal models, sheaf-theoretic coherence |
| III — Methods | 13–20 | Measurement, accounting, network analysis, causal inference, text/discourse analysis, historical methods, experiments, model validation |
| IV — Applications | 21–29+ | Human nature narratives, meritocracy, consumerism, inequality, race/coloniality/gender, austerity, work discipline, nation-myth, technology, crisis |
| V — Resistance | 30–35 | Regime fracture, counter-strategies, epistemic democracy, belief ecology design, ethics, open problems |

## Requirements

- A TeX distribution with `pdflatex`, `biber`, `makeindex`, and `latexmk` (e.g., [TeX Live](https://www.tug.org/texlive/) 2023+)
- GNU Make

## Build

```sh
make            # build main.pdf (auto-cleans build artifacts)
make watch      # live-rebuild on file changes
make clean      # remove build artifacts only
make distclean  # remove artifacts + PDF
```

The output is `main.pdf`. All intermediate files (`.aux`, `.bbl`, `.bcf`, `.log`, `.toc`, etc.) are removed automatically after a successful build.

## Project layout

```
.
├── main.tex                  # master document
├── preamble.tex              # packages, macros, theorem environments
├── Makefile
├── .latexmkrc
├── frontmatter/
│   ├── cover.tex             # full-black cover page
│   ├── titlepage.tex
│   ├── preface.tex
│   └── notation.tex          # symbol table
├── chapters/
│   ├── ch01-what-is-doxonomics.tex
│   ├── ch02-ontology-of-public-belief.tex
│   ├── ...
│   └── ch35-toward-social-self-understanding.tex
├── appendices/
│   ├── appA-glossary.tex
│   ├── ...
│   └── appH-reading.tex
├── bibliography/
│   └── references.bib        # ~175 entries
├── figures/                   # (empty — TikZ diagrams are inline)
└── docs/
    └── doxonomics-critique.md # external review
```

## Key notation

| Symbol | Meaning |
|--------|---------|
| $B_i(t)$ | Strength of belief $i$ at time $t$ |
| $F_k$ | Funding through channel $k$ |
| $C_k$ | Credibility of channel $k$ |
| $P_k$ | Population reach of channel $k$ |
| $\mathfrak{D}$ | Doxonomic system |
| $\mathcal{E}$ | Epistemic capital |
| $\mathcal{N}$ | Narrative infrastructure |
| EHI | Epistemic Herfindahl Index |
| IROI | Ideological return on investment |

See `frontmatter/notation.tex` for the complete table.

## Status

This is a field-founding book, not a report on a mature science. Many models are heuristic or conjectural; they are marked as such. The formal apparatus is intended to clarify structure and generate testable predictions. Empirical calibration is an open research program.

## License

A Piatra . Institute project.
