# Status

One-page index of editorial state across the book. Per-chapter work is tracked in the individual research dossiers; this file is the book-wide view. Update when a tier of work completes or a priority shifts.


## At a glance

All 44 `.tex` files are authorial-em-dash clean except one preserved primary-source epigraph (Huxley, `ch19-experimental-doxonomics.tex` L4). The book is also globalize-clean: every US-centric example now sits beside a non-US parallel within ±15 lines, enforced by the `globalize` check in `tools/doxo.py voice`. Four chapters carry research dossiers with landed citations; the remaining 32 chapters and 8 appendices do not yet have dossiers. Refs audit is clean (zero hard errors). The PDF builds at 520 pages.


## Book-wide metrics

| Metric | Value |
|---|---|
| Pages | 520 |
| Authorial em-dash lines remaining | **1** (preserved Huxley epigraph, ch19 L4) |
| Globalize hits (US framing without non-US parallel) | **0** |
| Bibliography entries | 218 (199 + 19 globalization additions) |
| Cite-family uses | 645+ (190+ unique keys) |
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

### Voice refresh — globalization sweep (2026-05-15)

The book-wide de-US-ing pass. The `Jurisdictionally precise` rule in `docs/voice.md` is now strengthened from "label US claims as US" to "state the principle jurisdiction-neutral first; the US case is one instance alongside at least one non-US parallel." A new `globalize` check in `tools/commands/voice.py` enforces it: any US frame marker (Heritage, Cato, AEI, Fox News, Federal Reserve, Citizens United, PATRIOT Act, American Dream, Silicon Valley, "in the US", "in the United States", "American [economy/public/voters/...]", Reagan, Trump, MAGA, Wall Street) without a non-US parallel marker (UK, Brazil, India, France, Germany, EU, Nordic, South Africa, Japan, China, Romania, etc., plus Thatcher/Bolsonaro/Modi/Macron/Le Pen/etc., plus IEA/Mont Pèlerin/Atlas Network) within ±15 lines is flagged. Inline opt-out: `% globalize-exempt: <reason>`.

Baseline: 47 globalize hits across 16 files. Post-sweep: **0 hits**.

- **Cohort A (5 chapters, structural rewrites):** ch07 (5→0; Mont Pèlerin / IEA-ASI / US 1971–1996 / Atlas Network as four documented build-outs), ch16 (5→0; Fox News IV joined by Mediaset, Russian NTV, pre-Nazi German radio), ch22 (4→0; mobility table widened with Italy, India, Brazil, South Africa; CEO-pay ratio with UK/France/Germany/Japan; Silicon Valley generalized to Shenzhen/Bangalore/Berlin/Tallinn/Tel Aviv tech-meritocracy), ch28 (Civil War memory paired with Partition, Apartheid TRC, German Vergangenheitsbewältigung, Northern Irish Troubles, Spanish *transición*), ch30 (the user's flagged §30.5 partisan-pandemic-belief line now reads "in polarized democracies… in the US [Druckman]; in Brazil [Ajzenman]; in the UK [Roozenbeek]"; 9/11 rally-around-the-flag paired with Madrid 2004, London 2005, Mumbai 2008).
- **Cohort B (~22 chapters, sentence-level supplements):** ch01, ch05, ch09, ch10, ch11, ch14, ch15 (6→0), ch17, ch19, ch21, ch23, ch24, ch27, ch29 (3→0), appG.
- **Bibliography additions:** 19 net-new non-US entries: `druckman2021`, `ajzenman2020`, `roozenbeek2020`, `argomaniz2009`, `walker2011`, `kalhan2010`, `cockett1994`, `stedmanjones2012`, `plehwe2006`, `djelic2014`, `durante2019`, `enikolopov2011`, `adena2015`, `ewing2017`, `corak2013`, `asher2024`, `souza2017`, `finn2017`, `painter2014`, `hope2019`. Brings bib to 218.
- **Infrastructure:** `docs/voice.md` §"Jurisdictionally precise" rewritten; `docs/diagnostic.md` gains §VIII "Jurisdictional reach" Q41 (disqualifying); `tools/commands/voice.py` carries the `globalize` check.

Build verification: `make distclean && make` produces a clean 520-page PDF (was 510 — the +10 pages match the predicted 3–5% word-count increase from supplemental parallel sentences). `python3 tools/doxo.py refs`: zero hard errors.


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
- **Unused bib entries** flagged by `refs` audit: `baier2023`, `buchanan1962`, `chomsky1988`, `frank2020`, `fraser2014`, `olson1965`, and 3 more. Cite or remove.
- **402 labels defined but never `\ref`'d** from the refs audit. Most are structural `ch:`/`sec:`/`app:` anchors and are safe to keep; a targeted cleanup pass on the ~106 non-structural ones would trim the long tail.
- **Per-chapter research dossiers for ch07, ch16, ch22, ch28, ch30** documenting the globalization additions in "Applied 2026-05-15" blocks (the chapters now carry the globalized prose; dossier-level documentation of the non-US sources is a future tidy-up).


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
