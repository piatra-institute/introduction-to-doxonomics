# Introduction to Doxonomics — Voice and Style

This is a writing guide for the book. It exists because the book's credibility depends on sentences that sound like a working scientist thinking, not like a well-meaning search result that has been made to look formal with Latinate nouns.

The book is formal but not stiff. Academic but not anaesthetised. Its authority comes from the density of specific evidence and the clarity of the formal apparatus, not from hedging, portentousness, or vocabulary.

A linter (`tools/doxo.py voice`) scans for the violations below. The linter catches what regex can catch. It does not replace the diagnostic read in `docs/diagnostic.md`.


## The voice in one paragraph

The prose sounds like a researcher who has built the formal apparatus, read the empirical literature, and is now writing for a colleague who is competent but new to the subject. Sentences carry weight by specificity and by structure, not by emphasis. Hedging is used only where the evidence genuinely warrants it and the hedge is doing analytical work. The reader is treated as a peer. Definitions are motivated before they are stated; propositions are preceded by the intuition and followed by the evidence. The humor, when it arrives, is dry and structural — a juxtaposition the reader sees at the same moment the writer does.


## What the voice is

**Confident.** Where the evidence supports a claim, state it. Avoid "it could be argued," "perhaps," "some might say" when the sentence has no genuine uncertainty to express. Used as filler, these phrases are doubt cosplay.

**Formally precise.** Where the chapter introduces formal apparatus, the notation matches `frontmatter/notation.tex`; variables are defined on first use; every $\alpha$, $\beta$, $\mu$ has a named referent. Formal claims are in `\begin{proposition}`, `\begin{definition}`, `\begin{model}`; conjectural ones are in `\begin{conjecture}` or flagged with a footnote.

**Jurisdictionally precise.** Do not let American institutions, American education systems, or American market structures pass as the default. When the claim is about the United States, say so. "The state," "the university," "the media" without a jurisdiction is a hole in the argument.

**Rhythmically varied.** Long sentences build; short sentences land. The chapters already read well when read aloud; keep them reading well. A definition followed by a one-sentence gloss is better than a definition surrounded by four more sentences of restatement.

**Honest about its status.** The book disclaims the status of a mature science. Heuristic models are marked as heuristic. Conjectural propositions are marked as conjectural. Empirical calibration is flagged as an open research program. This discipline is already in the manuscript; preserve it.


## What the voice is not

**Not hyped.** "This framework reveals...," "remarkably," "fascinatingly," "strikingly," "a profound insight": all cut. If the result is striking, the result does the striking. The adjective adds nothing the reader could not see.

**Not pedagogical in the bad sense.** The reader does not need to be told what is coming ("In this section we will examine..."), told what was just said ("What we have just shown is..."), or invited to feel clever ("As the reader has no doubt already inferred..."). State the content.

**Not breathless.** "Here's where it gets interesting," "this is where the argument really begins," "and crucially," "let us pause to note." If the material needs announcement to signal importance, it has not earned the importance.

**Not equivocating.** "It could be argued," "some would say," "one might think that" when the writer has a position and the evidence supports it. Equivocation is only honest when the writer is genuinely uncertain; as default syntax it reads as fear of commitment.

**Not performatively humble.** "Of course, the picture is more complicated than we can address here," "a full treatment would require...," "limitations of space prevent us from..." — sometimes true, but when used as default filler they become a tic. Prefer concrete statement: "A full treatment of X is developed in Chapter Y" or "The model does not address Z; see \textcite{...}."

**Not generically male.** Generic agents, readers, citizens, workers are not "he." Use plural constructions or singular "they" unless the historical actor is specifically male and that fact matters. (Ch. 21's Bowles epigraph is specific; ch. 11's "a rational agent" is generic.)


## Patterns to kill

These are the constructions that make prose sound machine-generated. The linter flags them. Cut them on sight.

### The em-dash (2026-04-18)

Banned outside primary-source quotations going forward. Used as an appositive or pivot — as in "the belief, ostensibly a proposition, is also an investment" or "the regime succeeded; its methods did not" — the em-dash produces a rhythm now conspicuously associated with late-2020s AI-assisted prose.

Replacement rules:

- **Appositive / parenthetical insertion**: comma pair. *"the belief --- ostensibly a proposition --- is also an investment"* → *"the belief, ostensibly a proposition, is also an investment"*.
- **Pivot / amplification**: period plus new sentence. *"The regime succeeded --- its methods did not."* → *"The regime succeeded. Its methods did not."*
- **Compressed definition-by-apposition**: comma pair, or rewrite if awkward.
- **Enumeration**: comma, or "and."

If the sentence depended on the em-dash for emphasis, rewrite the sentence. The ban is aesthetic, not mechanical: the replacement has to read naturally. If the comma flattens a load-bearing contrast, the sentence was built around the dash and needs a different structure.

**Preserved**: em-dashes inside `\begin{verbatim}`, inside quoted primary-source text, and inside math environments. These are factual reproduction or typographical necessity.

**Note**: the LaTeX source may contain `---` (three hyphens, rendered as em-dash by TeX). The linter flags both `---` and the Unicode `—`.

### Pattern 2 — the negate-first-then-pivot construction

The most overused construction in AI-assisted academic writing. It signals a writer with two things to say and no idea how to sequence them.

**Forms to cut:**

- "X is not Y. It is Z." — "Belief is not mere opinion. It is structured credence."
- "X is not just Y, but Z." — "This regime is not just ideological, but material."
- Inline "not X but Y" — "supported not by argument but by infrastructure."
- Triple negation: "not A, not B, not C, but D."
- "What X is not Y is Z."

**The test**: does the sentence state the positive directly, or does it reject an alternative first? If the alternative is rejected, rewrite. State both halves positively.

*Bad:* "Doxonomics is not psychology. It is a study of the social distribution of belief."
*Better:* "Doxonomics studies the social distribution of belief. Its object is the population, not the individual mind."

**Nuance**: a bare factual negation is not Pattern 2. "The evidence does not support this claim" is stating a fact in negative form; it is not rhetorical setup. The banned pattern is specifically the *reject-then-pivot* move where a straw alternative is set up to make the positive claim feel surprising.

**Second nuance**: foundational contrasts the chapter actually develops are preserved. "Belief is not a disposition to assert; it is a commitment to act" is load-bearing if the next paragraphs develop the action-commitment thesis. The test: does the rejected term (Y) name a real alternative the reader might plausibly hold, AND does the next paragraph develop the structural difference between Y and Z? If yes, preserve. Otherwise cut.

### AI-tic vocabulary — cut on sight

These words and phrases recur in AI-generated prose and hollow out sentences that otherwise have content:

- **Generic intensifiers**: "fundamentally," "essentially," "at its core," "in many ways," "in a very real sense," "quite literally."
- **Generic hedges used as filler**: "it is worth noting," "it is important to note," "interestingly," "notably," "crucially," "it should be emphasized."
- **Transitional clichés**: "Furthermore," "Moreover," "Ultimately," "In essence," "In fact," "That said."
- **Abstract flourishes**: "landscape" as metaphor ("the epistemic landscape"), "tapestry," "lens" (as in "through the lens of"), "nuanced," "multifaceted," "intricate web," "delve," "unpack."
- **Over-explanation tails**: "which tells us something about," "which is another way of saying," "in other words," "simply put," "put differently," "what this means is."
- **Self-announcing topic sentences**: "This section will examine," "In this chapter we show," "In what follows, we demonstrate."
- **Meta-explanation tails**: "Having shown X, we now turn to Y," "As we have seen," "This completes our treatment of..."
- **Performative qualifiers**: "in some sense," "to some extent," "up to a point," "broadly speaking" when the writer has a sharp point to make.

### Rhetorical questions immediately answered

*Bad:* "So what happens when a regime captures common sense? It becomes invisible."
*Better:* "When a regime captures common sense, it becomes invisible."

A rhetorical question earns its place when the answer is genuinely surprising or when the pause creates productive tension. When the answer follows immediately and predictably, the question is wasted motion.

### "Now," as paragraph opener

One per chapter maximum. It is a useful gear-shift when used sparingly. When every section starts with "Now," it becomes tic.

### The triple declarative as default

"The regime funds. The regime amplifies. The regime rewards." The restatement-that-sharpens is a legitimate tool. It becomes a tic when it appears in every section.

### Thesis restatement

The book's chapters have structural theses. State each thesis once in the body, compress it in the chapter's closing paragraph, and move on. Restating the thesis three or four times with different vocabulary signals distrust of the reader. If you find yourself writing "the core point is..." for the third time in a chapter, the first version was not clear enough or the intervening evidence was not strong enough. Fix the cause, not the symptom.

### Footnote-as-soapbox

Footnotes are for citations, qualifications, and digressions too narrow for the main text. They are not a place to resume an argument the main text decided to leave alone, to hedge a claim that should have been hedged in the body, or to perform care.


## Patterns that work

### The flat declarative

*"A public belief is a measurable aggregate."*

No emphasis. No signposting. The sentence carries its own weight because the concept is precise and the surrounding chapter has earned the definition.

### The motivation sentence before the definition

Every `\begin{definition}` earns its box by what comes before it. A single sentence of motivation that names the question the definition answers, followed by the formal statement, is the book's standard unit.

### The long sentence that earns a short one

A sentence that carries a multi-clause argument followed by a short sentence that delivers the verdict. The structure of ch. 2's taxonomy paragraphs; the structure of ch. 21's opening. Keep doing it.

### The footnote that marks heuristic status

Propositions that are structural rather than calibrated carry a footnote that says so. Ch. 21's Prop. 3 footnote, Prop. Affective Recruitment's footnote. This is the book's honesty discipline. Preserve it.

### Cross-reference that actually pays off

`\ref{ch:formal-models}`, `\autoref{prop:self-fulfilling}` — when the referenced item genuinely extends or underwrites the current claim. Avoid decorative cross-references that send the reader away without a reason.


## Rhythm and register

**Read aloud.** If you stumble, the reader will stumble. If a sentence cannot be said in one breath, split it.

**Latinate when Latinate is correct.** The book's subject requires a Latinate register at moments: "probability," "infrastructure," "institution," "credence." Do not strip these out from false populism. Do not add them from false sophistication. Prefer the shorter word when it is the right word.

**Technical terms define themselves through use.** The book already does this: belief, opinion, ideology, common sense, doxa are defined in ch. 2 and then used as working vocabulary. Avoid explicit glossary-style moments in later chapters when the term has already been introduced.

**Acronyms**: expand on first use in each chapter if the acronym has been off-stage for several chapters. EHI, IROI, and the Greek notation set are exceptions — they are part of the book's permanent vocabulary and are tabulated in `frontmatter/notation.tex`.

**Numbers**: spell out under ten; use digits from 10 upward; always use digits when the figure is the point (an inflation rate, a funding estimate, a sample size). Time-stamp all contemporary statistics (see below).


## Dated statistics

Contemporary statistics — annual figures, market shares, latest institutional budgets — are time-stamped with their year in the sentence, not only in the citation. A figure without its year ages silently. "Annual investment of \$10–18 billion (circa 2010)" is acceptable; "annual investment of \$10–18 billion" is not. The book's shelf life is decades; figures that read as present-tense will not age well.


## No invented scenes or figures

The book makes formal and empirical claims. Every dated claim, named actor, numerical figure, court decision, and institutional fact traces to the bibliography. If a detail is inferred rather than sourced, either cite the inference and its grounds or cut the detail. Attractive-but-invented detail erodes the whole apparatus.


## The test

Before a chapter is marked final, read it through the following lens: could an informed critical reader (a sociologist of knowledge, a business historian, a political economist) find a sentence that reads as AI-generic rather than as the author's position? If yes, fix the sentence. The book's credibility lives in whether every paragraph sounds like it came from someone who read the primary sources.
