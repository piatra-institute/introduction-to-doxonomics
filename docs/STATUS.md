# Status

One-page index of editorial state across the book. Per-chapter work is tracked in the individual research dossiers; this file is the book-wide view. Update when a tier of work completes or a priority shifts.


## At a glance

All 44 `.tex` files are authorial-em-dash clean except one preserved primary-source epigraph (Huxley, `ch19-experimental-doxonomics.tex` L4). Four chapters carry research dossiers with landed citations; the remaining 32 chapters and 8 appendices do not yet have dossiers. Refs audit is clean (zero hard errors). The PDF builds at 510 pages.


## Book-wide metrics

| Metric | Value |
|---|---|
| Pages | 510 |
| Authorial em-dash lines remaining | **1** (preserved Huxley epigraph, ch19 L4) |
| Bibliography entries | 199 |
| Cite-family uses | 645 (190 unique keys) |
| Cross-reference labels | 915 |
| Cross-reference uses | 394 |
| Hard ref errors | **0** |


## Completed

### Infrastructure (2026-04-18)

- `docs/voice.md` — voice guide. Em-dash ban, Pattern 2 ban, AI-tic hit-list, pedagogy rules, rhythm and register, dated-statistics rule, no-invented-figures rule.
- `docs/diagnostic.md` — 40-question pre-publish pass across 7 sections. Four disqualifying questions (Q5, Q10, Q23, Q37).
- `docs/research-pipeline.md` — methodology for producing and applying per-chapter research dossiers. Source tiers, confidence/priority markers, 5-phase research pass, 5-step application protocol.
- `tools/doxo.py` — dispatcher for `voice`, `stats`, `refs`, `structure`, `all`.
- `tools/commands/__init__.py` — LaTeX-aware stripper, line-number-preserving. Strips math, tikz, verbatim; removes invisible commands; unwraps text commands.
- `tools/commands/voice.py` — 15 regex patterns + em-dash scanner with primary-source-quote filtering.
- `tools/commands/stats.py` — word/sentence counts, Flesch Reading Ease, Flesch-Kincaid Grade, Latinate-suffix ratio, top-20 non-stopword tokens.
- `tools/commands/refs.py` — book-wide audit: labels/refs/cites/bib with duplicate, broken, and orphan detection.
- `tools/commands/structure.py` — per-chapter 7-element structural check.

### Research dossiers (2026-04-18)

- `docs/research/book.md` — field-level landscape: foundational traditions, recent scholarship (2020–2026), non-English traditions, adjacent fields, consolidated P1/P2/P3 additions, open empirical questions.
- `docs/research/ch01.md` — 12-row claim inventory, applied-today block, P1/P2/P3 additions, proposed prose revisions.
- `docs/research/ch11.md` — 10-row inventory, opinion-dynamics tradition, complex contagion, Bayesian agreement fragility.
- `docs/research/ch21.md` — 12-row inventory, selfishness-regime empirical updates, neuroscience primaries, WEIRD critique.
- `docs/research/ch25.md` — 12-row inventory, coloniality scholarship, colorblind-racism literature, intersectionality primary sources.

### Voice refresh — em-dash sweep (2026-04-18)

All 35 chapters + 2 dirty appendices + `frontmatter/preface.tex` + `main.tex` interludes. **522 → 1 authorial em-dashes.** Case-by-case editorial per the 5-strategy taxonomy (appositive → parens/commas; pivot → period split; gloss → colon; enumeration → comma; emphasis-built-around-dash → sentence rewrite). Tabular `---` placeholders converted to `--` (en-dash). `appendices/appH-reading.tex` converted via uniform `textcite-colon` substitution (51 lines) because the em-dashes there were bibliographic separators, not authorial voice.

### Voice refresh — full pass (on two files so far)

- `chapters/ch01-what-is-doxonomics.tex` — em-dash + Pattern 2 + AI-tic + universal-noun cleaned. Voice scan reports only the known-acceptable rhetorical-question-count flag (exercise prompts + load-bearing framing questions).
- `frontmatter/preface.tex` — same. Clean on all voice categories.

### Bibliography additions (2026-04-18)

25 net-new entries added from the research passes: `bourdieu1977`, `gneezy2000`, `ostrom2010`, `bonilla-silva2018`, `quijano2000`, `mignolo2011`, `crenshaw1989`, `butler1990`, `gould1981`, `gilens1999`, `sterman2000`, `pastor-satorras2015`, `centola2007`, `centola2018`, `hegselmann2002`, `degroot1974`, `acemoglu2016`, `epstein2006`, `chamley2004`, `glaeser2009`, `rilling2002`, `sanfey2003`, `henrich2020`, `lugones2010`, `herrnstein1994`.


## In progress

None actively. The sweep paused here for review.


## Backlog (prioritized)

### P1 — next pick-up

- **Pattern 2 / AI-tic / universal-noun full voice-refresh for ch02–ch36 + appendices.** The em-dash sweep only handled em-dashes. The linter still flags residual voice issues per chapter. Same editorial pattern as `ch01`, per-chapter.
- **Contemporary-figure URL citations in ch01**: WARC 2024 *Global Ad Spend Outlook*, OpenSecrets 2025 federal-lobbying record. Cited by URL + access date (not traditional bib entries).
- **Journal-venue verification for deferred dossier items**: Girardi 2024 *Southern Economic Journal* (ch21 §5), Fosgaard 2023 *Experimental Economics* (ch21 §2.1). Requires institutional-access verification before the bib entries land.

### P2 — when the chapter is touched

- **ch25 non-English additions**: Mbembe 2019 *Necropolitics*, Mbembe 2017 *Critique of Black Reason*, Segato 2016 *La guerra contra las mujeres*, Fanon 1952 *Peau noire, masques blancs* (French original), Dussel 1993, Mignolo & Walsh 2018 *On Decoloniality*, Collins & Bilge 2020 *Intersectionality*.
- **ch11 §11.6 model-comparison table**: add Opinion Dynamics as a sixth row (structural change, not a punctuation swap).
- **ch21 dossier-deferred items**: time-stamp on the 100:1 funding-ratio table, Frey 2017/2021 restatement citation.

### P3 — future

- **Per-chapter research dossiers for ch02–ch20 + ch22–ch36 + appendices A–H.** Only 4 chapters carry dossiers today.
- **Full voice-refresh pass beyond the em-dash layer for remaining 34 chapters.**
- **Unused bib entries** flagged by `refs` audit: `baier2023`, `buchanan1962`, `chomsky1988`, `frank2020`, `fraser2014`, `olson1965`, and 2 more. Cite or remove.
- **402 labels defined but never `\ref`'d** from the refs audit. Most are structural `ch:`/`sec:`/`app:` anchors and are safe to keep; a targeted cleanup pass on the ~106 non-structural ones would trim the long tail.


## Where state lives

- `docs/voice.md` — voice rules (the definition of "clean").
- `docs/diagnostic.md` — 40-question pre-publish pass (qualitative check).
- `docs/research-pipeline.md` — how to run a research pass.
- `docs/research/book.md` — field-level landscape.
- `docs/research/ch*.md` — per-chapter dossiers with "Applied YYYY-MM-DD" blocks listing what has landed.
- `bibliography/references.bib` — 199 entries.
- `tools/doxo.py` — linter suite.
- `main.pdf` — current build artifact.


## How to check current state

From the project root:

```sh
# Book-wide em-dash count (should be 1 — the Huxley epigraph)
grep -c -- '---' chapters/*.tex appendices/*.tex | awk -F: '{sum+=$2} END {print sum}'

# Voice scan across all chapters (flags remaining Pattern 2, AI-tics, etc.)
python3 tools/doxo.py voice

# Citation and cross-reference audit (should show 0 hard errors)
python3 tools/doxo.py refs

# Word counts, readability, top tokens
python3 tools/doxo.py stats

# Clean rebuild, verify page count
make distclean && make
```


## Maintenance note

Update this file when a tier of work completes or a priority shifts. Per-chapter progress stays in the dossiers; this file is the book-wide index, not a per-edit log.
