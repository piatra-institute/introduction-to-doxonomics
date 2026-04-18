"""Command: stats.

Quantitative analysis of chapters: word count, sentence-length distribution,
readability (Flesch Reading Ease and Flesch-Kincaid Grade), Latinate-register
heuristic, and top-frequency tokens.
"""

import re
from collections import Counter

from . import (
    resolve_target,
    all_chapters,
    all_appendices,
    read_file,
    strip_latex,
    count_words,
    count_sentences,
    count_syllables,
)


# English stopwords for the top-token frequency report.
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "of", "in", "on", "at", "to",
    "for", "with", "as", "by", "is", "are", "was", "were", "be", "been", "being",
    "it", "its", "this", "that", "these", "those", "which", "what", "who", "whom",
    "whose", "when", "where", "why", "how", "so", "not", "no", "nor", "yet",
    "from", "into", "about", "than", "then", "there", "here", "also", "such",
    "only", "just", "more", "most", "many", "much", "some", "any", "all",
    "each", "every", "both", "either", "neither", "one", "two", "three",
    "i", "we", "you", "he", "she", "they", "them", "their", "our", "my",
    "us", "him", "her", "his", "hers", "its", "ours", "yours", "theirs",
    "do", "does", "did", "have", "has", "had", "can", "could", "should",
    "would", "may", "might", "must", "shall", "will", "being", "am", "does",
    "up", "down", "out", "over", "under", "again", "further", "once",
    "other", "same", "own", "too", "very", "s", "t", "d", "ll", "m", "re", "ve",
}


# Latinate heuristic: suffixes that mark Latin- or Greek-derived polysyllabic words.
LATINATE_SUFFIXES = (
    "tion", "sion", "ment", "ance", "ence", "ity", "ism", "ology", "ography",
    "ize", "ise", "ate", "able", "ible", "ous", "ive", "al", "ic", "ical",
    "istic", "ical", "arily",
)


def _latinate_ratio(words: list[str]) -> float:
    """Share of words with a Latinate/Greek suffix. Rough heuristic."""
    if not words:
        return 0.0
    latinate = sum(
        1 for w in words
        if len(w) >= 6 and w.lower().endswith(LATINATE_SUFFIXES)
    )
    return latinate / len(words)


def _tokenize(text: str) -> list[str]:
    """Simple tokenizer: alphabetic, lowercased."""
    return re.findall(r"[a-zA-Z][a-zA-Z'-]*", text.lower())


def _flesch_reading_ease(words: int, sentences: int, syllables: int) -> float:
    if words == 0 or sentences == 0:
        return 0.0
    return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)


def _flesch_kincaid_grade(words: int, sentences: int, syllables: int) -> float:
    if words == 0 or sentences == 0:
        return 0.0
    return 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59


def _sentence_lengths(prose: str) -> list[int]:
    """Return word counts per sentence for the prose-stripped text."""
    # Split on sentence-ending punctuation followed by whitespace.
    sentences = re.split(r'[.!?]+(?:\s|$)', prose)
    return [len(re.findall(r"[a-zA-Z'-]+", s)) for s in sentences if s.strip()]


def _file_stats(path) -> dict:
    raw = read_file(path)
    if not raw:
        return {}
    prose = strip_latex(raw, keep_lines=False)
    tokens = _tokenize(prose)
    words = len(tokens)
    sentences = count_sentences(prose)
    syllables = sum(count_syllables(t) for t in tokens)
    lengths = _sentence_lengths(prose)
    lengths.sort()

    def percentile(p: float) -> int:
        if not lengths:
            return 0
        idx = min(len(lengths) - 1, int(p * len(lengths)))
        return lengths[idx]

    non_stop = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    top = Counter(non_stop).most_common(20)

    return {
        "words": words,
        "sentences": sentences,
        "syllables": syllables,
        "avg_sentence": (words / sentences) if sentences else 0.0,
        "median_sentence": percentile(0.5),
        "p90_sentence": percentile(0.9),
        "max_sentence": max(lengths) if lengths else 0,
        "flesch_re": _flesch_reading_ease(words, sentences, syllables),
        "flesch_kg": _flesch_kincaid_grade(words, sentences, syllables),
        "latinate_ratio": _latinate_ratio(tokens),
        "top_tokens": top,
    }


def _print_file(name: str, stats: dict, show_tokens: bool):
    if not stats:
        print(f"  {name:<44} (empty)")
        return
    print(f"\n--- {name} ---")
    print(f"  words:              {stats['words']:>7,}")
    print(f"  sentences:          {stats['sentences']:>7,}")
    print(f"  avg sentence:       {stats['avg_sentence']:>7.1f} words")
    print(f"  median sentence:    {stats['median_sentence']:>7} words")
    print(f"  p90 sentence:       {stats['p90_sentence']:>7} words")
    print(f"  max sentence:       {stats['max_sentence']:>7} words")
    print(f"  Flesch Reading Ease:{stats['flesch_re']:>7.1f}   (higher = easier; academic prose typically 30-50)")
    print(f"  Flesch-Kincaid GL:  {stats['flesch_kg']:>7.1f}   (US grade-level; academic prose typically 12-18)")
    print(f"  Latinate ratio:     {stats['latinate_ratio']*100:>7.1f}%  (heuristic)")
    if show_tokens and stats.get("top_tokens"):
        print( "  top non-stopword tokens:")
        for tok, count in stats["top_tokens"]:
            print(f"    {tok:<24} {count:>4}")


def cmd_stats(target: str = ""):
    """Print quantitative statistics for one or more chapters."""
    targets = resolve_target(target) if target else (
        list(all_chapters()) + list(all_appendices())
    )
    if not targets:
        return

    print("=== QUANTITATIVE STATS ===")

    totals = {
        "words": 0, "sentences": 0, "syllables": 0,
    }
    single = len(targets) == 1

    for name, path in targets:
        stats = _file_stats(path)
        if not stats:
            continue
        _print_file(name, stats, show_tokens=single)
        totals["words"] += stats["words"]
        totals["sentences"] += stats["sentences"]
        totals["syllables"] += stats["syllables"]

    if len(targets) > 1:
        print(f"\n=== TOTALS ({len(targets)} files) ===")
        w = totals["words"]
        s = totals["sentences"]
        sy = totals["syllables"]
        print(f"  words:              {w:>7,}")
        print(f"  sentences:          {s:>7,}")
        if s:
            print(f"  avg sentence:       {w/s:>7.1f}")
        if w and s:
            print(f"  Flesch Reading Ease:{_flesch_reading_ease(w, s, sy):>7.1f}")
            print(f"  Flesch-Kincaid GL:  {_flesch_kincaid_grade(w, s, sy):>7.1f}")
