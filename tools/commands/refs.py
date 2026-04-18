"""Command: refs.

Cross-reference and citation validator. Walks every .tex file and the
bibliography, then reports:

  - labels defined but never referenced
  - refs/cites with no matching label / bib entry
  - duplicate labels
  - duplicate bib entries
  - bib entries never cited
"""

import re
from collections import Counter, defaultdict

from . import all_tex_files, BIB, read_file


LABEL_RE = re.compile(r'\\label\{([^{}]+)\}')
REF_CMDS = r'(?:ref|autoref|cref|Cref|eqref|pageref|nameref|vref|vpageref)'
REF_RE = re.compile(rf'\\{REF_CMDS}\*?\{{([^{{}}]+)\}}')
CITE_CMDS = r'(?:cite|autocite|textcite|parencite|footcite|nocite|citeauthor|citeyear|citetitle)'
CITE_RE = re.compile(rf'\\{CITE_CMDS}(?:\[[^\]]*\])*\{{([^{{}}]+)\}}')
BIB_ENTRY_RE = re.compile(r'^@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,', re.MULTILINE)


def _collect_labels() -> dict[str, list[str]]:
    """Return {label: [file_origins]}."""
    labels: dict[str, list[str]] = defaultdict(list)
    for name, path in all_tex_files():
        text = read_file(path)
        for match in LABEL_RE.finditer(text):
            labels[match.group(1)].append(name)
    return labels


def _collect_refs() -> dict[str, list[str]]:
    """Return {referenced-label: [file_origins]}."""
    refs: dict[str, list[str]] = defaultdict(list)
    for name, path in all_tex_files():
        text = read_file(path)
        for match in REF_RE.finditer(text):
            # \cref supports comma-separated keys; split on commas.
            for key in match.group(1).split(","):
                key = key.strip()
                if key:
                    refs[key].append(name)
    return refs


def _collect_cites() -> dict[str, list[str]]:
    """Return {citation-key: [file_origins]}."""
    cites: dict[str, list[str]] = defaultdict(list)
    for name, path in all_tex_files():
        text = read_file(path)
        for match in CITE_RE.finditer(text):
            keys = match.group(1)
            for key in keys.split(","):
                key = key.strip()
                if key:
                    cites[key].append(name)
    return cites


def _collect_bib_entries() -> dict[str, int]:
    """Return {bib-key: count_of_definitions}."""
    text = read_file(BIB)
    entries: Counter[str] = Counter()
    for match in BIB_ENTRY_RE.finditer(text):
        entries[match.group(1)] += 1
    return dict(entries)


def cmd_refs(target: str = ""):
    """Validate cross-references and citations book-wide. Target is ignored."""
    labels = _collect_labels()
    refs = _collect_refs()
    cites = _collect_cites()
    bib = _collect_bib_entries()

    print("=== REFERENCE AUDIT ===\n")
    print(f"  \\label entries:      {sum(len(v) for v in labels.values()):>5}  ({len(labels)} unique)")
    print(f"  \\ref-family uses:    {sum(len(v) for v in refs.values()):>5}  ({len(refs)} unique)")
    print(f"  \\cite-family uses:   {sum(len(v) for v in cites.values()):>5}  ({len(cites)} unique)")
    print(f"  bib entries:         {sum(bib.values()):>5}  ({len(bib)} unique)")

    # Duplicate labels.
    dup_labels = {k: v for k, v in labels.items() if len(v) > 1}
    if dup_labels:
        print(f"\n  WARN  duplicate \\label definitions ({len(dup_labels)})")
        for key, files in sorted(dup_labels.items()):
            print(f"    {key:<40} {', '.join(files)}")

    # Duplicate bib entries.
    dup_bib = {k: v for k, v in bib.items() if v > 1}
    if dup_bib:
        print(f"\n  WARN  duplicate bib entries ({len(dup_bib)})")
        for key, count in sorted(dup_bib.items()):
            print(f"    {key:<40} defined {count} times")

    # Broken refs.
    broken_refs = [k for k in refs if k not in labels]
    if broken_refs:
        print(f"\n  FAIL  \\ref to undefined label ({len(broken_refs)})")
        for key in sorted(broken_refs):
            files = ", ".join(sorted(set(refs[key])))
            print(f"    {key:<40} referenced in {files}")

    # Broken cites.
    broken_cites = [k for k in cites if k not in bib]
    if broken_cites:
        print(f"\n  FAIL  \\cite to missing bib key ({len(broken_cites)})")
        for key in sorted(broken_cites):
            files = ", ".join(sorted(set(cites[key])))
            print(f"    {key:<40} cited in {files}")

    # Orphan labels.
    orphan_labels = [k for k in labels if k not in refs]
    # Chapter/section labels are often defined for TOC use, not ref use; mark as info.
    if orphan_labels:
        ch_prefixes = ("ch:", "sec:", "subsec:", "app:", "part:")
        structural = sorted(k for k in orphan_labels if k.startswith(ch_prefixes))
        other = sorted(k for k in orphan_labels if not k.startswith(ch_prefixes))
        if other:
            print(f"\n  INFO  labels defined but never \\ref'd ({len(other)})")
            for key in other[:40]:
                print(f"    {key}")
            if len(other) > 40:
                print(f"    ... and {len(other) - 40} more.")
        if structural:
            print(f"\n  INFO  structural labels (ch:/sec:/app:) never \\ref'd: {len(structural)}")
            print(f"        (often acceptable; they anchor sections for future use)")

    # Unused bib entries.
    unused_bib = [k for k in bib if k not in cites]
    if unused_bib:
        print(f"\n  INFO  bib entries never cited ({len(unused_bib)})")
        for key in sorted(unused_bib)[:40]:
            print(f"    {key}")
        if len(unused_bib) > 40:
            print(f"    ... and {len(unused_bib) - 40} more.")

    print()
    hard = len(broken_refs) + len(broken_cites) + len(dup_labels) + len(dup_bib)
    if hard == 0:
        print("  OK   no hard reference errors.")
    else:
        print(f"  {hard} hard error(s) that should be resolved.")
