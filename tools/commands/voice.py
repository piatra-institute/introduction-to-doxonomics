"""Command: voice.

LaTeX-aware voice scanner for Introduction to Doxonomics.

Implements the patterns defined in docs/voice.md. Strips LaTeX markup before
matching so math, citations, labels, and cross-references do not produce
false positives. Line numbers reported correspond to the source .tex file.
"""

import re
from pathlib import Path

from . import (
    resolve_target,
    read_file,
    strip_latex,
    strip_quoted,
    _strip_inline,
)


# Pattern list: (label, regex, description-optional-None).
# Each regex runs against the stripped, quoted-content-removed prose.
VOICE_PATTERNS: list[tuple[str, str]] = [
    ("AI-tic: generic intensifier",
     r"\b(?:fundamentally|essentially|at its core|in many ways|in a very real sense|quite literally)\b"),
    ("AI-tic: generic filler-hedge",
     r"\b(?:it is worth (?:noting|mentioning|pausing)|it is important to note|it should be emphasized|crucially|notably|interestingly)\b"),
    ("AI-tic: transitional cliche",
     r"(?:^|\. )(?:Furthermore|Moreover|Ultimately|In essence|In fact|That said)\b"),
    ("AI-tic: 'landscape' metaphor",
     r"\b(?:epistemic|political|conceptual|moral|intellectual|ideological) landscape\b"),
    ("AI-tic: 'delve'/'unpack'/'nuanced'/'multifaceted'",
     r"\b(?:delve|unpack|nuanced|multifaceted|intricate web|tapestry)\b"),
    ("AI-tic: over-explanation tail",
     r"\b(?:in other words|simply put|put differently|what this means is|which tells us something about|which is another way of saying)\b"),
    ("Pedagogical: self-announcing topic sentence",
     r"\b(?:this (?:chapter|section) (?:will|aims to|seeks to) (?:examine|explore|show|demonstrate|argue|present)|in what follows,? we (?:will |shall )?(?:show|examine|demonstrate|argue)|we will (?:show|see|examine|demonstrate|argue) (?:that|how))\b"),
    ("Pedagogical: meta-explanation tail",
     r"\b(?:having (?:shown|established) that|as we have (?:seen|shown|established)|as noted (?:above|earlier))\b"),
    ("Pattern 2: 'not just X but Y' / 'not only X but Y'",
     r"\bnot (?:just|merely|only|simply) .{3,60}?,? but\b"),
    ("Pattern 2: 'not X but Y' inline",
     r"\bnot (?:a|an|the|his|her|their) \w+(?:,| but| --| -- ) (?:but|--) (?:a|an|the|his|her|their)?"),
    ("Rhetorical question immediately answered (heuristic)",
     r"\?\s+(?:It|The|This|That|These|Those|He|She|They|We)\b"),
    ("Breathless: announcement of interest",
     r"\b(?:here(?:'s| is) (?:where|what|the thing|why)|let us (?:pause|unpack)|this is where .{2,30} (?:really |truly )?(?:begins|gets interesting))\b"),
    ("Equivocation filler",
     r"\b(?:it (?:could|might) be (?:argued|said|claimed) that|some would (?:argue|say) that|one (?:could|might) (?:argue|say) that)\b"),
    ("Generic masculine for generic agent",
     r"\ba (?:reader|agent|citizen|worker|believer|subject|actor|scientist|economist|researcher|analyst|observer|policymaker|scholar)\b[^.\n]{0,80}\b(?:he|him|his)\b"),
    ("Unqualified universal noun (review for jurisdiction)",
     r"(?<!\w)\b(?:the market|the state|the government|the public|regulators|the media|the university|the press)\b"),
]


# Globalize check: US-frame markers that should sit alongside a non-US parallel.
# Each entry signals a US-centric instance. A violation is raised only if no
# parallel marker (country/region/named non-US figure or institution) appears
# in the surrounding window. A line that ends with the comment
# `% globalize-exempt: <reason>` is skipped.
GLOBALIZE_US_MARKERS: list[str] = [
    r"\bHeritage Foundation\b",
    r"\bCato Institute\b",
    r"\bAmerican Enterprise Institute\b",
    r"\bAEI\b",
    r"\bFox News\b",
    r"\bManhattan Institute\b",
    r"\bBrookings(?: Institution)?\b",
    r"\bFederal Reserve\b",
    r"\bCitizens United\b",
    r"\bPATRIOT Act\b",
    r"\bAmerican Dream\b",
    r"\bSilicon Valley\b",
    r"\bin the U\.?S\.?(?:\b|$)",
    r"\bin the United States\b",
    r"\bAmerican (?:economy|public|voters|media|consumers|workers|households|conservatives|liberals|politics|culture)\b",
    r"\bReagan(?:'s)?\b",
    r"\bTrump(?:'s)?\b",
    r"\bMAGA\b",
    r"\bWall Street\b",
]

GLOBALIZE_PARALLEL_REGEX = re.compile(
    r"\b(?:UK|United Kingdom|Britain|British|Brazil(?:ian)?|India(?:n)?|"
    r"France|French|Germany|German|EU|European|Japan(?:ese)?|China|Chinese|"
    r"Romania(?:n)?|Sweden|Norway|Denmark|Nordic|Scandinavia(?:n)?|"
    r"Argentina|Chile|Mexico|Russia(?:n)?|Hungary|Hungarian|"
    r"South Africa(?:n)?|Spain|Spanish|Italy|Italian|Australia(?:n)?|"
    r"Canada|Canadian|Korea(?:n)?|Pakistan(?:i)?|Bangladesh|Turkey|Turkish|"
    r"Thatcher|Bolsonaro|Modi|Macron|Merkel|Orb[aá]n|Le Pen|Berlusconi|Lula|"
    r"IEA\b|Adam Smith Institute|Mont P[èe]lerin|Atlas Network|"
    r"Latin America(?:n)?|Global South|sub-Saharan|Africa(?:n)?|"
    r"Eastern Europe(?:an)?|Western Europe(?:an)?)\b",
    re.IGNORECASE,
)

GLOBALIZE_EXEMPT_REGEX = re.compile(r"%\s*globalize-exempt\b", re.IGNORECASE)

# Per-marker compiled regex with IGNORECASE for case-tolerant matching of
# institution names while still anchoring on word boundaries.
GLOBALIZE_US_COMPILED = [
    (pattern, re.compile(pattern, re.IGNORECASE)) for pattern in GLOBALIZE_US_MARKERS
]


def _globalize_hits(
    lines: list[str],
    scrubbed: list[str],
    window: int = 15,
) -> list[tuple[int, str, str]]:
    """Return (line_no, source_line, matched_phrase) for US markers lacking a
    non-US parallel within ±window lines of scrubbed prose.

    The exempt comment `% globalize-exempt:` on the source line suppresses the
    check for that line. A parallel marker anywhere in the window neutralizes
    the violation.
    """
    hits: list[tuple[int, str, str]] = []
    n = len(scrubbed)
    for i, prose in enumerate(scrubbed):
        source = lines[i] if i < len(lines) else ""
        if GLOBALIZE_EXEMPT_REGEX.search(source):
            continue
        for pattern, compiled in GLOBALIZE_US_COMPILED:
            m = compiled.search(prose)
            if not m:
                continue
            lo = max(0, i - window)
            hi = min(n, i + window + 1)
            window_text = " ".join(scrubbed[lo:hi])
            # Remove the matched US phrase from the window before checking
            # parallels: avoids "in the US" inside the window text counting
            # as its own parallel.
            window_text = compiled.sub(" ", window_text)
            if GLOBALIZE_PARALLEL_REGEX.search(window_text):
                continue
            phrase = m.group(0)
            hits.append((i + 1, source.strip() or prose.strip(), phrase))
            break  # one hit per line is enough
    return hits


def _flag_matches(label: str, pattern: str, lines: list[str], scrubbed: list[str]) -> list[tuple[int, str]]:
    """Scan scrubbed prose lines; return (line_no, original_source_line) tuples.

    scrubbed[i] is the prose-stripped form of lines[i] with quoted content removed;
    reporting uses the original source line for readability.
    """
    compiled = re.compile(pattern, re.IGNORECASE)
    hits: list[tuple[int, str]] = []
    for i, prose in enumerate(scrubbed, 1):
        if compiled.search(prose):
            src = lines[i - 1].strip()
            if not src:
                src = prose.strip()
            hits.append((i, src))
    return hits


def _emdash_hits(lines: list[str]) -> list[tuple[int, str]]:
    """Return lines containing authorial em-dashes.

    Excludes em-dashes inside inline math, inside \\begin{verbatim} environments,
    inside LaTeX-style ``...'' quoted spans, and inside primary-source quoted
    `"..."` spans. Per voice.md, the ban applies only to authorial em-dashes.
    """
    hits: list[tuple[int, str]] = []
    in_verbatim = False
    in_math_env = False

    math_envs = {"equation", "align", "gather", "multline", "eqnarray",
                 "displaymath", "tikzpicture", "verbatim", "lstlisting"}

    begin_re = re.compile(r'\\begin\{([a-zA-Z*]+)\}')
    end_re = re.compile(r'\\end\{([a-zA-Z*]+)\}')

    for i, line in enumerate(lines, 1):
        if in_verbatim or in_math_env:
            m = end_re.search(line)
            if m and m.group(1).rstrip('*') in math_envs:
                in_verbatim = False
                in_math_env = False
            continue

        m = begin_re.search(line)
        if m and m.group(1).rstrip('*') in math_envs:
            # Does the same line also end it?
            env = m.group(1).rstrip('*')
            same_line_end = re.search(rf'\\end\{{{env}\*?\}}', line)
            if not same_line_end:
                in_math_env = True
            # still check the remainder of this line for em-dashes outside the env
            # For simplicity, skip the whole line when a math env opens on it.
            continue

        # Strip inline math and quoted content before scanning.
        scrub = line
        scrub = re.sub(r'(?<!\\)\$[^$\n]*\$', '', scrub)
        scrub = re.sub(r'\\\([^)]*\\\)', '', scrub)
        scrub = re.sub(r'\\\[.*?\\\]', '', scrub)
        scrub = re.sub(r"``[^`']*''", "", scrub)
        scrub = re.sub(r'"[^"]*"', '', scrub)

        # Look for authorial em-dash markers.
        # LaTeX source often contains '---' which renders as em-dash.
        # Also check for the Unicode em-dash.
        if "\u2014" in scrub or "---" in scrub:
            hits.append((i, line.strip()))

    return hits


def _now_opener_hits(lines: list[str]) -> list[tuple[int, str]]:
    """Return lines starting (after markup strip) with 'Now,'."""
    hits: list[tuple[int, str]] = []
    for i, raw in enumerate(lines, 1):
        stripped = _strip_inline(raw).lstrip()
        if stripped.startswith("Now,"):
            hits.append((i, raw.strip()))
    return hits


def _question_density(scrubbed: list[str]) -> int:
    """Count sentences ending with '?' in the prose-stripped text."""
    joined = " ".join(scrubbed)
    return len(re.findall(r"\?\s", joined))


def _scrub_prose(text: str) -> list[str]:
    """Strip LaTeX and quoted primary-source spans; return line-aligned list."""
    stripped = strip_latex(text, keep_lines=True)
    out = []
    for line in stripped.splitlines():
        out.append(strip_quoted(line))
    return out


def cmd_voice(target: str):
    """Scan a chapter (or all chapters) for voice.md violations."""
    targets = resolve_target(target)
    if not targets:
        return

    total_issues = 0
    total_files = 0
    total_globalize = 0

    for name, path in targets:
        raw = read_file(path)
        if not raw:
            print(f"  {name}: (file empty or missing)")
            continue

        total_files += 1
        lines = raw.splitlines()
        scrubbed = _scrub_prose(raw)

        print(f"\n=== VOICE CHECK: {name} ===")

        file_issues = 0
        file_globalize = 0

        # Pattern-based checks.
        for label, pattern in VOICE_PATTERNS:
            hits = _flag_matches(label, pattern, lines, scrubbed)
            if hits:
                file_issues += 1
                print(f"\n  WARN  {label} ({len(hits)})")
                for num, text in hits[:8]:
                    print(f"        L{num}: {text[:140]}")
                if len(hits) > 8:
                    print(f"        ... and {len(hits) - 8} more.")

        # Em-dash check (LaTeX-aware).
        em_hits = _emdash_hits(lines)
        if em_hits:
            file_issues += 1
            print(f"\n  WARN  em-dash in authorial prose ({len(em_hits)})")
            for num, text in em_hits[:8]:
                print(f"        L{num}: {text[:140]}")
            if len(em_hits) > 8:
                print(f"        ... and {len(em_hits) - 8} more.")

        # "Now," paragraph openers.
        now_hits = _now_opener_hits(lines)
        if len(now_hits) > 1:
            file_issues += 1
            print(f"\n  WARN  'Now,' paragraph opener ({len(now_hits)}; max 1 per chapter)")
            for num, text in now_hits[:6]:
                print(f"        L{num}: {text[:140]}")

        # Rhetorical question density (soft).
        q_count = _question_density(scrubbed)
        if q_count > 8:
            file_issues += 1
            print(f"\n  WARN  high rhetorical-question count: {q_count}")
            print( "        check for questions immediately answered in the next sentence")

        # Globalize check: US frame markers without a non-US parallel within ±15 lines.
        glob_hits = _globalize_hits(lines, scrubbed)
        if glob_hits:
            file_issues += 1
            file_globalize = len(glob_hits)
            print(f"\n  WARN  globalize: US framing without non-US parallel ({len(glob_hits)})")
            for num, text, phrase in glob_hits[:8]:
                print(f"        L{num} [{phrase}]: {text[:120]}")
            if len(glob_hits) > 8:
                print(f"        ... and {len(glob_hits) - 8} more.")

        if file_issues == 0:
            print("  OK   no voice violations detected.")
        else:
            print(f"\n  -- {file_issues} issue category/ies in {name}")
        total_issues += file_issues
        total_globalize += file_globalize

    if total_files > 1:
        print(f"\n=== SUMMARY ===")
        print(f"  {total_files} files scanned, {total_issues} issue categor{'y' if total_issues == 1 else 'ies'} total.")
        print(f"  globalize hits: {total_globalize}")
