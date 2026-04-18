"""Shared utilities for the Introduction to Doxonomics toolkit."""

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
CHAPTERS = BASE / "chapters"
APPENDICES = BASE / "appendices"
FRONTMATTER = BASE / "frontmatter"
DOCS = BASE / "docs"
BIB = BASE / "bibliography" / "references.bib"


# --- chapter/appendix resolution ---

def all_chapters():
    """Yield (name, path) for every chapter file, sorted."""
    for path in sorted(CHAPTERS.glob("ch*.tex")):
        yield path.stem, path


def all_appendices():
    for path in sorted(APPENDICES.glob("app*.tex")):
        yield path.stem, path


def all_frontmatter():
    for path in sorted(FRONTMATTER.glob("*.tex")):
        yield path.stem, path


def all_tex_files():
    """Yield every .tex file across frontmatter, chapters, appendices."""
    yield from all_frontmatter()
    yield from all_chapters()
    yield from all_appendices()


def resolve_target(arg: str):
    """Resolve a reference to a list of (name, path) tuples.

    Accepts: "ch21", "21", "ch21-human-nature-narrative",
    "ch21-human-nature-narrative.tex", "appA", "appA-glossary", or "" (all).
    """
    if not arg:
        return list(all_chapters()) + list(all_appendices())

    arg = arg.strip()
    # chapter number like "21" or "ch21"
    m = re.match(r'^(?:ch)?(\d+)$', arg, re.IGNORECASE)
    if m:
        num = int(m.group(1))
        prefix = f"ch{num:02d}"
        for name, path in all_chapters():
            if name.startswith(prefix):
                return [(name, path)]
        print(f"Error: no chapter matching '{arg}' (tried prefix '{prefix}')")
        return []

    # appendix letter like "appA", "A"
    m = re.match(r'^(?:app)?([A-H])$', arg, re.IGNORECASE)
    if m:
        letter = m.group(1).upper()
        prefix = f"app{letter}"
        for name, path in all_appendices():
            if name.startswith(prefix):
                return [(name, path)]
        print(f"Error: no appendix matching '{arg}'")
        return []

    # strip .tex extension
    stem = arg[:-4] if arg.endswith(".tex") else arg
    for name, path in all_tex_files():
        if name == stem:
            return [(name, path)]

    # partial match
    for name, path in all_tex_files():
        if name.startswith(stem) or stem in name:
            return [(name, path)]

    print(f"Error: '{arg}' not recognized as a chapter, appendix, or file.")
    return []


def read_file(path: Path) -> str:
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


# --- LaTeX stripping ---

# Block environments whose contents are not prose (math, figures, code).
# Keys are the environment base name; regex matches both name and name*.
BLOCK_ENVS = [
    "equation", "align", "gather", "multline", "eqnarray", "displaymath",
    "verbatim", "lstlisting", "minted",
    "tikzpicture", "pgfplot", "pgfpicture",
    "figure", "table", "tabular",
    "itemize", "enumerate", "description",  # lists have prose, leave them
]

# Environments whose content should be scanned as prose.
PROSE_ENVS = {
    "itemize", "enumerate", "description",
    "definition", "proposition", "theorem", "lemma", "corollary",
    "remark", "example", "exercise", "model", "axiom", "principle",
    "conjecture", "proof",
}

NON_PROSE_ENVS = {
    "equation", "align", "gather", "multline", "eqnarray", "displaymath",
    "verbatim", "lstlisting", "minted",
    "tikzpicture", "pgfplot", "pgfpicture",
    "figure", "table", "tabular",
    "center",  # usually wraps a figure/tabular; leave prose inside alone though
}

# Commands whose content is invisible to the reader (remove entirely).
INVISIBLE_COMMANDS = [
    "label", "ref", "autoref", "cref", "Cref", "eqref", "pageref",
    "nameref", "vref", "vpageref",
    "cite", "autocite", "textcite", "parencite", "footcite", "nocite",
    "citeauthor", "citeyear", "citetitle",
    "index",
    "input", "include", "includegraphics",
    "bibliographystyle", "addbibresource", "usepackage", "documentclass",
]

# Commands whose braced argument is visible prose (unwrap to keep content).
TEXT_COMMANDS = [
    "emph", "textbf", "textit", "textsc", "texttt", "textmd", "textsl",
    "textnormal", "textup", "textrm", "textsf",
    "uline", "underline",
    "text", "mbox", "footnote", "marginpar",
    "chapter", "section", "subsection", "subsubsection", "paragraph",
    "subparagraph", "chapter*", "section*", "subsection*",
    "title", "subtitle", "author",
    "caption",
]


def _strip_inline(line: str) -> str:
    """Strip inline LaTeX markup from a single line. Preserves visible prose."""
    # Remove % comments (but not \%). Replace with empty string.
    line = re.sub(r'(?<!\\)%.*', '', line)

    # Strip \begin{env}[opts] and \end{env} entirely (env name and option brackets
    # must not leak into prose).
    line = re.sub(r'\\(?:begin|end)\{[a-zA-Z*]+\}(?:\[[^\]]*\])*', '', line)

    # Remove inline math $...$, \(...\), \[...\] on a single line.
    line = re.sub(r'(?<!\\)\$[^$\n]*\$', ' ', line)
    line = re.sub(r'\\\([^)]*\\\)', ' ', line)
    line = re.sub(r'\\\[.*?\\\]', ' ', line)

    # Remove invisible commands with their braced arg and optional bracket arg.
    for cmd in INVISIBLE_COMMANDS:
        # \cmd[opt]{arg} with possible multiple args
        line = re.sub(
            rf'\\{cmd}\*?(?:\[[^\]]*\])*\{{[^{{}}]*\}}',
            '',
            line,
        )
        # Bare \cmd with no argument (rare but possible)
        line = re.sub(rf'\\{cmd}\b', '', line)

    # Unwrap text commands: \cmd{content} -> content.
    # Do multiple passes to handle simple nesting.
    for _ in range(4):
        changed = False
        for cmd in TEXT_COMMANDS:
            new = re.sub(
                rf'\\{cmd}\*?\{{([^{{}}]*)\}}',
                r'\1',
                line,
            )
            if new != line:
                changed = True
                line = new
        if not changed:
            break

    # Remove any remaining \cmd{arg} by keeping arg (for unknown text commands).
    line = re.sub(r'\\[a-zA-Z]+\*?\{([^{}]*)\}', r'\1', line)

    # Remove bare macros like \noindent, \newline, \\
    line = re.sub(r'\\\\', ' ', line)
    line = re.sub(r'\\[a-zA-Z]+\*?', '', line)

    # Remove ~ (non-breaking space) and replace with space
    line = line.replace('~', ' ')

    # Collapse multiple spaces.
    line = re.sub(r'  +', ' ', line)

    return line


def strip_latex(text: str, keep_lines: bool = True) -> str:
    """Strip LaTeX markup and return prose-like text.

    If keep_lines is True, line numbers are preserved: non-prose environments
    (math, tikz, figure) have their contents replaced with blank lines so that
    a scanner finding at line N in the stripped text corresponds to line N
    in the source.
    """
    lines = text.splitlines()
    out: list[str] = []
    in_env: str | None = None

    begin_re = re.compile(r'\\begin\{([a-zA-Z*]+)\}')
    end_re = re.compile(r'\\end\{([a-zA-Z*]+)\}')

    for line in lines:
        if in_env:
            # Look for the matching \end{env}
            m = end_re.search(line)
            if m and m.group(1).rstrip('*') == in_env:
                in_env = None
            out.append("")
            continue

        # Check for beginning of non-prose environment.
        m = begin_re.search(line)
        entered = False
        if m:
            env = m.group(1).rstrip('*')
            if env in NON_PROSE_ENVS:
                # Does it also \end on the same line?
                same_line_end = re.search(
                    rf'\\begin\{{{env}\*?\}}.*?\\end\{{{env}\*?\}}',
                    line,
                )
                if same_line_end:
                    cleaned = re.sub(
                        rf'\\begin\{{{env}\*?\}}.*?\\end\{{{env}\*?\}}',
                        '',
                        line,
                    )
                    out.append(_strip_inline(cleaned))
                else:
                    in_env = env
                    out.append("")
                entered = True

        if not entered:
            out.append(_strip_inline(line))

    return "\n".join(out) if keep_lines else " ".join(l for l in out if l.strip())


def strip_quoted(line: str) -> str:
    """Remove content inside LaTeX-style and ASCII-style quote pairs.

    Used to exclude primary-source quotations from scans that should only
    look at authorial prose.
    """
    # LaTeX-style ``...''
    line = re.sub(r"``[^`']*''", "", line)
    # ASCII "..."
    line = re.sub(r'"[^"]*"', "", line)
    # Single-quoted 'x' is almost always an apostrophe or short quote; leave it.
    return line


# --- counting ---

def count_words(text: str) -> int:
    """Count words in stripped prose text."""
    return len(re.findall(r"\b[a-zA-Z][a-zA-Z'-]*\b", text))


def count_sentences(text: str) -> int:
    """Naive sentence counter: split on .!? followed by whitespace or EOL."""
    # Guard against common abbreviations that end in "." but are not sentence boundaries.
    abbrevs = [
        "e.g.", "i.e.", "cf.", "etc.", "vs.", "viz.", "No.", "Fig.",
        "Eq.", "Ch.", "Sec.", "p.", "pp.", "vol.",
    ]
    guarded = text
    for ab in abbrevs:
        guarded = guarded.replace(ab, ab.replace(".", "<DOT>"))
    sentences = re.split(r'[.!?]+(?:\s|$)', guarded)
    sentences = [s for s in sentences if s.strip()]
    return max(1, len(sentences))


def count_syllables(word: str) -> int:
    """Heuristic syllable count for English words."""
    word = word.lower()
    word = re.sub(r"[^a-z]", "", word)
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for c in word:
        if c in vowels:
            if not prev_vowel:
                count += 1
            prev_vowel = True
        else:
            prev_vowel = False
    if word.endswith("e") and count > 1:
        count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        count += 1
    return max(1, count)
