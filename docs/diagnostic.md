# The Diagnostic Read

A structured pre-publish pass on a chapter. The voice linter (`tools/doxo.py voice`) encodes what can be matched by regex: em-dashes, AI-tic vocabulary, banned constructions. This document encodes what cannot: thesis discipline, formal-apparatus integrity, citation load, rhythm, reader-fit.

The linter says yes or no on specific patterns. This pass asks questions the writer has to answer.


## How to use

1. Read the whole chapter through, top to bottom, without jumping to fix.
2. Work through the forty questions in order. Each takes ten to thirty seconds unless it is flagging something.
3. Mark each question **Pass**, **Flag**, or **Rewrite**. "Rewrite" means the answer is no and the fix is not mechanical.
4. Apply the fixes. Read again. Re-check any question whose answer might have changed.
5. If more than six questions are flagged, the chapter is not yet ready for a final build. Return to the draft.

Running time: roughly 45–60 minutes per chapter for a writer who has done the pass before.

The questions are not equally weighted. Four are disqualifying (Q5, Q10, Q23, Q37). A chapter that passes the disqualifying questions and flags half the polish ones is closer to shippable than one that fails a disqualifying question and passes the rest.


## Section I — Opening discipline (Q1–5)

**Q1. Does the chapter open with an epigraph that does work?**
*Why:* The book uses epigraphs that frame the chapter's structural claim, not decorative quotations. The Bourdieu epigraph on ch. 2 frames the opacity-of-the-taken-for-granted thesis. The Bowles epigraph on ch. 21 frames the malleability thesis.
*Fix:* If the epigraph is decorative (author + general aphorism, no relationship to the chapter's claim), replace or remove.

**Q2. Does the opening paragraph (\noindent after the epigraph) state what the chapter is about without announcing it?**
*Pattern to avoid:* "In this chapter we examine..." "This chapter argues that..." "The aim of this chapter is to..."
*Pattern to use:* Direct statement of the problem, followed by a sentence that locates the chapter's contribution to it.
*Fix:* Rewrite the opening as a direct statement of the conceptual question the chapter answers.

**Q3. Does the opening avoid the correction-gambit ("The folk version says X. The real story is Y.")?**
*Why:* The book's register is direct-statement, not corrective framing. Occasional use is fine; default use becomes wallpaper.
*Fix:* State the operational claim. Trust the reader to calibrate against whatever folk version they arrived with.

**Q4. Is the chapter's structural thesis stated once, explicitly, in the first two pages?**
*Why:* A chapter that withholds its thesis reads as a wandering survey; a chapter that repeats its thesis in paragraph one and paragraph three reads as anxious.
*Fix:* Mark the one sentence that is the chapter's thesis. Confirm it appears once in the opening and is later elaborated, not restated.

**Q5. Does the chapter's first page avoid em-dashes, generic intensifiers, and AI-tic vocabulary?**
*Why:* First impressions. A reader who hits "fundamentally," "at its core," or an em-dash pivot in the opening paragraph is reading a different book than the one the manuscript wants to be.
*Disqualifying if:* the first page fails the em-dash ban or contains two or more AI-tic vocabulary items from `voice.md`.


## Section II — Thesis and architecture (Q6–10)

**Q6. Can the chapter's thesis be stated in one sentence without opening the file?**
*Fix:* Write the sentence. If it takes three attempts, the chapter is about more than one thing — either split it, or compress.

**Q7. Is the thesis stated in the body of the chapter at most twice (once early, once in the closing passage)?**
*Why:* See `voice.md` §"Thesis restatement."
*Fix:* Grep for paraphrases of the thesis sentence. Cut to two.

**Q8. Does the chapter have a clear structural progression (hook → motivation → apparatus → consequences → ties-to-other-chapters)?**
*Fix:* Read just the section titles. Do they tell a coherent story? If the section titles read as a list of topics, the structure is not yet carrying the argument.

**Q9. Does each formal definition, proposition, or model have a motivating paragraph before it and an interpretive paragraph after it?**
*Why:* A chapter of definitions without motivations is a glossary. A chapter of propositions without interpretations is a textbook appendix.
*Fix:* For each `\begin{definition}` / `\begin{proposition}` / `\begin{model}`: is there a sentence before that names the question it answers? Is there a sentence after that says what follows from it?

**Q10. Does the chapter resist the lecture-with-excellent-prose failure mode?**
*Pattern:* Paragraph of abstraction, one paragraph of example, paragraph of abstraction, one paragraph of example. The book wants claim → evidence → consequence → next claim.
*Disqualifying if:* three or more consecutive paragraphs are entirely abstract with no instantiation.


## Section III — Formal apparatus (Q11–17)

**Q11. Is every variable defined on first use, and does the notation match `frontmatter/notation.tex`?**
*Why:* The book's notation is centralized. A chapter that introduces $\phi_i$ without checking that $\phi_i$ is already the narrative flow in ch. 11 creates drift that propagates.
*Fix:* Check each Greek / Latin variable in the chapter against the notation table. Flag any new symbols that should be added to the table.

**Q12. Is every proposition marked with its epistemic status?**
*Why:* The book's discipline: formal propositions that follow from model assumptions carry a footnote if they are not empirically calibrated; conjectural propositions use `\begin{conjecture}`; heuristic models are flagged in the paragraph that introduces them.
*Fix:* For each `\begin{proposition}`: is there a footnote or nearby sentence that says whether this is structural, heuristic, or calibrated? If not, add one.

**Q13. Do examples follow, rather than precede, the definitions they illustrate?**
*Why:* Examples before definitions teach the reader a working example, which then competes with the formal definition for space.
*Fix:* Check the order. If an example arrives first, either the definition should be moved earlier or the example should be labeled as motivation rather than illustration.

**Q14. Are heuristic models, stylized models, and toy examples flagged as such in the text?**
*Why:* The book's status disclaimer (the README: "Many models are heuristic or conjectural; they are marked as such") is load-bearing. If a heuristic is not marked, the reader will take it as empirically supported.
*Fix:* For each model: is its status named in the paragraph before or inside the environment?

**Q15. Does the chapter avoid calibrated-sounding claims where the calibration is not in evidence?**
*Pattern:* "The elasticity is approximately 0.15" without a source is a calibration claim. If the source is the author's intuition, either source it, mark it as illustrative, or rewrite as a range.
*Fix:* Flag any numerical claim that does not cite a source. Mark illustrative parameter values explicitly ("plausible values," "illustrative parameters").

**Q16. Are cross-references to other chapters specific enough to be load-bearing?**
*Why:* `\ref{ch:formal-models}` by itself is decoration unless the reader learns what they will find there. "See ch.~\ref{ch:formal-models} for the dynamic extension" is load-bearing.
*Fix:* For each `\ref{ch:...}` or `\autoref{...}`: what will the reader find? If the answer is vague, specify.

**Q17. Does the chapter avoid introducing notation that it does not use?**
*Why:* Dead notation signals a chapter that was revised without cleanup.
*Fix:* For each defined variable, check that it is used at least once later in the chapter. If it is not, either use it or remove the definition.


## Section IV — Citations and empirical grounding (Q18–24)

**Q18. Is every empirical claim (historical fact, funding figure, court case, named study) cited?**
*Why:* The book's authority lives here. An uncited empirical claim is equivalent to an invented one.
*Fix:* Walk the chapter. For each factual statement that is not a logical consequence of the framework, confirm a `\autocite` or `\textcite` is present.

**Q19. Is every citation in the chapter present in `bibliography/references.bib`?**
*Fix:* Run `tools/doxo.py refs`. Every unresolved citation is a broken reference.

**Q20. Are contemporary statistics time-stamped in the sentence, not only in the citation?**
*Why:* See `voice.md` §"Dated statistics."
*Fix:* For each figure that describes present-day quantities (budgets, reaches, shares): does the sentence include "as of X" or "(circa Y)"?

**Q21. Are conjectural or hypothetical claims distinguished from empirically supported ones?**
*Fix:* Could an informed reader tell, from the language alone, which claims rest on evidence and which are analytic extensions of the model? If the linguistic registers are indistinguishable, add markers.

**Q22. Where the literature is genuinely contested, does the chapter acknowledge the disagreement rather than paper over it?**
*Why:* Omitting the disagreement buys a sharper sentence at the cost of later credibility. See ch. 21's treatment of the "commons" debate for the template.
*Fix:* Identify any claim in the chapter where the scholarly literature is genuinely split; either cite both sides or acknowledge the scope limit.

**Q23. Does the bibliography reflect the chapter's actual intellectual debts, not only the citations that made it into the text?**
*Disqualifying if:* A chapter makes claims clearly derived from a body of literature (e.g., Bourdieu on symbolic violence, Scott on legibility, Bowker & Star on classification) without citing any entry point to that literature.

**Q24. Are footnotes used for qualifications and narrow citations, not for parallel arguments?**
*Fix:* For each footnote longer than two sentences: is the content narrow enough that it does not belong in the main text? If the footnote is performing analytical work the main text should have performed, move it up or cut it.


## Section V — Language, voice, and tics (Q25–32)

**Q25. Are there zero authorial em-dashes (`---` in LaTeX or `—` Unicode) outside primary-source quotations and math?**
*Why:* `voice.md` §"The em-dash."
*Fix:* Run the linter. Rewrite per the replacement rules.

**Q26. Are there zero instances of AI-tic vocabulary from the `voice.md` hit-list?**
*Fix:* "fundamentally," "essentially," "at its core," "landscape" (metaphor), "delve," "unpack," "nuanced," "multifaceted," "interestingly," "it is worth noting," "furthermore," "moreover" — replace with the flat declarative.

**Q27. Are there zero "not X but Y" / "X is not Y. It is Z." constructions that do not pass the second-nuance test?**
*Why:* `voice.md` §"Pattern 2."
*Fix:* For each flagged instance, check whether the next 100–300 words develop the contrast. If yes, preserve; if no, rewrite.

**Q28. Are "Now," paragraph openers limited to one per chapter?**
*Fix:* Grep for `^Now,`. More than one: pick the most load-bearing and rewrite the rest.

**Q29. Are rhetorical questions earned, or filler?**
*Pattern to cut:* A question immediately answered in the next sentence.
*Fix:* If the next sentence answers the question, delete the question.

**Q30. Are abstract nouns ("the market," "the state," "the public," "regulators") qualified with a specific referent?**
*Why:* `voice.md` §"Jurisdictionally precise."
*Fix:* Qualify or delete. "The U.S. financial press" means something; "the media" does not.

**Q31. Are generic readers, agents, subjects, and workers rendered as plurals or singular "they" rather than default "he"?**
*Fix:* Rewrite to plural or singular "they."

**Q32. Is the language Anglo-Saxon where Anglo-Saxon is the right register, Latinate where Latinate is the right register?**
*Pattern:* Latinate abstractions do structural work poorly when they could be named concretely. "Institutional reproduction mechanisms" → "how the institution reproduces itself." Reserve Latinate registers for their technical moments, not as default prose.


## Section VI — Rhythm and mouth-feel (Q33–36)

**Q33. Does sentence length vary deliberately across each paragraph?**
*Fix:* After a complex build, land on a short sentence. After two shorts, a longer one.

**Q34. Can each sentence be spoken in one breath without gasping?**
*Fix:* Read aloud. If you run out of air, split the sentence.

**Q35. Are there no tongue-twisters, consonant pileups, or sibilance clusters in prose the reader might encounter aloud (e.g., in a talk based on the chapter)?**
*Fix:* Read aloud. Rewrite offending phrases.

**Q36. Are numbers rendered consistently (spelled-out under ten unless the figure is the point; digits from 10; always digits for money, percentages, years)?**
*Fix:* Walk the numbers. Pick one convention per kind of figure and hold to it.


## Section VII — Consequence and close (Q37–40)

**Q37. Does the chapter close by stating what the reader now knows that they did not know before, without restating the thesis in a fourth paraphrase?**
*Why:* The closing passage compresses the chapter's contribution and points forward. It is not the thesis restated in sharper vocabulary.
*Disqualifying if:* the closing paragraphs restate the thesis more than once without adding new compression or forward pointer.

**Q38. Is the "Notes and References" section present and does it correspond to the chapter's actual debts?**
*Fix:* Walk the section. Does it name the intellectual debts the chapter draws on? Does it flag the open problems or points of dispute?

**Q39. Are the exercises concrete, load-bearing, and tied to the chapter's formal apparatus?**
*Pattern to avoid:* Exercises that read as "discuss," "explain," or "comment on." The book's existing exercises (simulate a cascade, compute a threshold, estimate an investment) are the template.
*Fix:* For each exercise: does it require the reader to do something the chapter prepared them to do? If it is a homework-style prompt, strengthen it.

**Q40. At the end of the chapter, can the reader state what the chapter contributed to the book's overall argument, and why that matters?**
*Why:* The test of whether the chapter is load-bearing for the book, not merely adjacent.
*Fix:* Write the chapter's contribution in one sentence. If you cannot, the chapter may be a survey rather than an argument.


## When to run this

- Once, when the chapter is "structurally done" but before a final build.
- Again after fixes, abbreviated: re-check only the flagged questions.
- Optionally a third time, after a week's rest from the chapter.


## Pairing with the linter

- `tools/doxo.py voice <chapter>` — em-dashes, AI-tic vocabulary, Pattern 2, "Now," opener density, rhetorical-question density, unqualified universal nouns.
- `tools/doxo.py stats <chapter>` — word count, sentence-length distribution, readability, top-20 verbs and nouns (reveals tic words not on the hit-list).
- `tools/doxo.py refs` — broken cross-references, missing bib keys, orphan labels.
- `tools/doxo.py structure <chapter>` — presence of epigraph, intro paragraph, definitions, exercises, notes-and-references section.
- This document — the qualitative pass.

The linter can be wrong (false positives on math, rare LaTeX constructs); the forty questions cannot be wrong, only unanswered. If a linter flag and a diagnostic flag disagree, the diagnostic is authoritative.


## Running against an external model

The full chapter plus this document, `voice.md`, and a handful of surrounding chapters can be fed to an external model for a holistic review. The model should work through the forty questions with line references and produce a structured audit.

Limitations observed in similar pipelines elsewhere: external models over-produce "wholesale rewrites" that compress away load-bearing detail; Pattern 2 flags need the next-paragraph-developed check before acting; and "needs stronger sourcing" often means "dossier fix" or "log as research-pass item," not "rewrite the script." Apply the same triage discipline here: a flag is a hypothesis, not a verdict.
