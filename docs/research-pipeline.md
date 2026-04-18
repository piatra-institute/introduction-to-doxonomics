# Research Pipeline

How per-chapter research dossiers are produced, how they are read, and how they get folded back into the book. This document is the methodology paired with `docs/voice.md` and `docs/diagnostic.md`.

The pipeline exists because a field-founding book makes empirical and scholarly claims whose sourcing must be honest and current. The book's credibility rests on the specific source behind each structural claim. The pipeline is the discipline that keeps that sourcing honest across 36 chapters and 8 appendices.


## What a research dossier is

A per-chapter file at `docs/research/chXX.md` (or `appX.md`) that captures, for one chapter:

1. **Load-bearing claims inventory** — the specific empirical and interpretive claims the chapter rests on, with current citation, confidence level, and proposed action.
2. **Recent scholarship** — peer-reviewed work that postdates the chapter's original drafting and that the chapter should engage (cite, acknowledge, or rebut).
3. **Non-English sources** — scholarship in languages other than English that the chapter's topic makes load-bearing.
4. **Candidate bibliography additions** — specific entries proposed for `bibliography/references.bib`, with proposed bib-keys and priority (P1/P2/P3).
5. **Proposed prose revisions** — concrete, line-numbered edits the research surfaces.
6. **Open questions** — research questions the chapter raises that the pipeline cannot yet answer.

A book-level dossier at `docs/research/book.md` covers the same territory for the field surrounding the book (neighboring disciplines, broad traditions, contemporary landscape).


## The source-tier conventions

Shared with `book.md` §"Source-tier conventions":

- **T1 — primary sources.** Charter texts, statutes, court decisions, annual reports, government inquiries, original data releases, original papers introducing a concept. For doxonomic claims about institutional funding, T1 means IRS Form 990s, SEC filings, OpenSecrets data, or equivalent.
- **T2 — scholarly sources.** Peer-reviewed journal articles, university-press monographs, scholarly edited volumes.
- **T3 — authoritative reference.** Stanford Encyclopedia of Philosophy, Oxford DNB, major institutional encyclopedias. Useful as orienting references, rarely the sole support for a structural claim.
- **T4 — secondary journalism.** Quality press, magazine essays. Useful for leads, contemporary figures, and as entry points; never the sole support for a structural claim.

Every citation in the book should ideally map to a T1 or T2 source. Where only a T3 or T4 source is available, the confidence is lower and the claim should be phrased accordingly.


## Confidence and priority markers

Each proposed addition in a dossier carries two tags:

**Confidence** (how well the source matches the book's intended use):
- **HIGH**: the source directly supports the claim, the metadata is verified, and the citation would survive peer review.
- **MED**: the source is plausible but the metadata needs verification OR the source is one of several possible; a better primary may exist.
- **LOW**: the source is a lead, not yet a citation. Needs further research before adoption.

**Priority** (how urgent):
- **P1**: the bib entry should land before the chapter is next built. Load-bearing; its absence would be noticed by a critical reader.
- **P2**: add when the chapter is next touched substantively.
- **P3**: add if and when the chapter is rewritten or the book is re-released. Optional.


## How to run a new research pass for a chapter

The following is a bounded protocol. It should take 2–4 hours per chapter for a first pass, less for a refresh.

### Phase 0 — pre-read

1. Read the current `chapters/chXX.tex` (or `appendices/appX.tex`) front to back.
2. Read the existing dossier if one exists (`docs/research/chXX.md`).
3. Read `docs/voice.md` §"What the voice is not" and `docs/diagnostic.md` §IV "Citations and empirical grounding."

### Phase 1 — claim inventory (30–60 min)

Walk the chapter. For each factual sentence that is not a logical consequence of the formal framework:

1. Record the claim (paraphrased).
2. Record the current citation (look for `\autocite{...}` or `\textcite{...}` in context).
3. Assess confidence: HIGH if the cited source directly supports the claim; MED if the source is adjacent; LOW if uncited or mismatched.
4. Propose action: sharpen the citation, add a citation, soften the claim to match the evidence, or cut.

Output: a table (`| # | Claim | Location | Current cite | Confidence | Action |`) at the top of the dossier.

### Phase 2 — recent scholarship search (30–60 min)

For each topic the chapter engages, do targeted WebSearch/WebFetch passes:

1. Search for peer-reviewed work post-2020 on the topic.
2. For each promising hit, verify the source metadata (author, title, venue, year, volume, pages, DOI) against a T1/T2 primary page — publisher catalog, journal record, DOI landing page. Search snippets are not authoritative.
3. Note each candidate in the dossier with its proposed bib-key, tier, confidence, and priority.

Search strategy hints:

- **Author-first**: `"Author LastName" topic 2024` often finds direct follow-ups.
- **Review-first**: `"systematic review" OR "meta-analysis" topic 2023 2024` surfaces consolidating work.
- **Venue-first**: if the chapter cites *Journal of X*, search for recent *Journal of X* on the topic.

### Phase 3 — non-English sources (20–40 min)

For each topic where the chapter risks an Anglo-Saxon default:

1. Identify the language(s) of the most relevant primary sources.
2. Search in English for translations and English-language scholarship engaging the non-English tradition.
3. For languages the researcher can read (or translate with reasonable confidence), search directly in the native language.
4. A non-English source counts as a citable addition even if the book does not quote from it; the citation establishes that the author consulted the tradition.

### Phase 4 — proposed prose revisions (20–40 min)

Walk back through the chapter with the research findings in hand. For each place where:

- a claim is uncited but a candidate source now exists, propose a specific `\autocite{...}` addition with line number;
- a claim is cited to a secondary when a primary is now available, propose the primary as a replacement or supplement;
- a contemporary figure needs a time-stamp or fresh citation (global ad spend, lobbying expenditure, etc.), propose the edit with an access-date URL;
- the research surfaces a tension (e.g., a 2023 meta-analysis that complicates the chapter's claim), propose a hedge or acknowledge the complication.

Output: a numbered list of proposed revisions with line numbers.

### Phase 5 — open questions (10–20 min)

List the research questions the chapter raises that the pipeline cannot yet answer. These are not failings; they are the research agenda that the chapter leaves for future work. Each entry should be specific enough that a researcher could start on it.


## Applying a dossier to the chapter

Once the dossier is written, applying its findings is a separate operation. Do these in the stated order:

### Step 1 — verify each proposed bib entry

For each P1 entry in the dossier:

1. Visit the publisher's page, journal record, or DOI landing page.
2. Confirm: author(s), full title, year, venue, volume/issue, pages, DOI.
3. If any detail cannot be confirmed from a T1 source, downgrade the entry to P2 or P3 and flag in the dossier.

Never add a bib entry whose metadata you have not verified from a T1/T2 primary page. Search-result snippets are leads, not citation data.

### Step 2 — add verified entries to `references.bib`

For each verified entry:

1. Choose the bib-key. Convention for this book: `<firstauthor-lowercase><year>`, e.g., `mirowski2009`, `bourdieu1977`, `henrich2020`. Multi-author works use first-author only. Disambiguate collisions with `a`/`b` suffix (`bourdieu1977a`, `bourdieu1977b`).
2. Use the most specific `@article`/`@book`/`@incollection` type.
3. Include DOI when available.
4. Run `python3 tools/doxo.py refs` to confirm no duplicate keys and no broken refs.

### Step 3 — apply prose revisions

Working chapter by chapter:

1. For each proposed revision in the dossier, apply it as an `Edit` to the `.tex` file.
2. Preserve the voice guide (`docs/voice.md`): do not introduce em-dashes, Pattern 2, or AI-tic vocabulary when adding citations.
3. When adding a citation to a sentence that previously stood alone, choose `\autocite` (parenthetical) over `\textcite` (inline name-and-year) unless the name matters in the prose.

### Step 4 — rebuild and verify

1. Touch the edited chapter and run `make` (or `make distclean && make` for a force-rebuild).
2. Check that the build completes without errors.
3. Run `python3 tools/doxo.py voice <chapter>` to confirm no new voice violations were introduced.
4. Run `python3 tools/doxo.py refs` to confirm no broken `\cite` or `\ref`.
5. Confirm `main.pdf` page count is stable (or that changes are intentional).

### Step 5 — update the dossier

After applying the revisions:

1. Mark each applied revision in the dossier with a date ("[applied 2026-04-18]").
2. Update the claims inventory: items that are now properly cited move from MED to HIGH.
3. Move any remaining P1 items that were deferred to P2 with a note explaining the deferral.


## When to run the pipeline

- **Once per chapter** when the chapter is newly drafted, to produce the initial dossier.
- **Refresh per chapter** annually, or before a major release (paperback edition, translation, omnibus).
- **On request** when a reviewer, colleague, or external reader surfaces a credible correction.

Do not run the pipeline because a sentence "feels thin." The pipeline is for structural sourcing, not rhythm. If the issue is voice, run the voice pass instead (`docs/diagnostic.md`).


## Constraints (non-negotiable)

1. **No invented sources, no fabricated metadata, no citations to works the researcher has not verified.** A single fabricated citation would corrode the book's authority across 40 chapters.
2. **Contemporary statistics are time-stamped in the sentence.** See `docs/voice.md` §"Dated statistics." A global-ad-spend figure without "as of 2024" ages silently.
3. **Non-English sources count as legitimate citations even if the book does not quote them.** The citation establishes engagement with the tradition; the direct quote is optional.
4. **The chapter's thesis is fixed once approved.** Research passes sharpen evidence and sourcing; they do not reopen the chapter's argumentative structure. For structural rewrites, start with `docs/diagnostic.md`, not the research pipeline.
5. **The dossier is the citable artifact.** Even if a finding does not make it into the chapter, it belongs in the dossier. The dossier is the ground on which future editorial decisions stand.


## When to use an external model for research

The dossier pipeline is designed so that a capable external model (or a capable research assistant) can execute Phases 1–3 given:

- the chapter's `.tex` file,
- the existing dossier (if any) and `book.md`,
- the source-tier conventions above,
- WebSearch/WebFetch access.

The external pass should produce line-referenced findings with clear T1/T2 sources and verified metadata. Wholesale chapter rewrites should be rejected; per-line citation additions and prose revisions should be triaged into P1/P2/P3 before any land in the `.tex`.

Common failure modes observed from external passes (adapted from CYK's `refresh-pipeline.md`):

- Wholesale rewrites that compress away research-grounded material. Always extract the specific line-level findings and apply them surgically.
- Pattern-matching flags that over-trigger on foundational contrasts. Apply the second-nuance test from `voice.md` before cutting.
- "Needs stronger sourcing" flags that are actually dossier items, not script fixes. Triage into: script fix (rewrite the claim to match the evidence), dossier fix (add a citation without changing the claim), or research-pass item (log as outstanding source-upgrade work).
- Paywalled-source metadata that the external model reconstructs from snippets. Always verify from a T1/T2 primary page before landing in `.bib`.


## Interaction with the other tools

- `docs/voice.md` — voice guide. The research pipeline must preserve voice.md compliance; new citations should not smuggle in em-dashes, Pattern 2 constructions, or AI-tic vocabulary.
- `docs/diagnostic.md` — 40-question pre-publish pass. Section IV ("Citations and empirical grounding") of the diagnostic overlaps with Phase 1 of this pipeline.
- `tools/doxo.py voice` — runs the voice linter. Re-run after research-driven edits.
- `tools/doxo.py refs` — validates cross-references and citations book-wide. Run after adding any bib entry.
- `tools/doxo.py stats` — reports word-count drift, useful if a research pass adds substantial prose.


## Output

Per chapter, a complete research pass produces:

- `docs/research/chXX.md` (or `appX.md`) with the six sections above.
- Net-new entries in `bibliography/references.bib` (verified, keyed, referenced from the chapter).
- Line-level edits in `chapters/chXX.tex` (or the relevant file) reflecting the dossier's proposed revisions.
- A voice scan, refs audit, and timing check showing no regressions.
