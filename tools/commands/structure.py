"""Command: structure.

Check each chapter against the book's structural template:

  - \\chapter{...} present and \\label{ch:...} present
  - \\epigraph{...} at or near the opening
  - at least one \\begin{definition} / \\begin{proposition} / \\begin{model}
    (skippable for overview chapters)
  - 'Notes and References' section
  - 'Exercises' section
"""

import re
from . import resolve_target, read_file, all_chapters


CHECKS = [
    ("chapter command",     r"\\chapter\*?\{"),
    ("chapter label",       r"\\label\{ch:"),
    ("epigraph",            r"\\epigraph\{"),
    ("formal apparatus",    r"\\begin\{(?:definition|proposition|theorem|lemma|model|axiom|principle|conjecture)\}"),
    ("example",             r"\\begin\{example\}"),
    ("notes & references",  r"(?i)\\section\*?\{notes\s+and\s+references\}|\\section\*?\{references\}|\\section\*?\{notes\}"),
    ("exercises",           r"(?i)\\section\*?\{exercises\}|\\begin\{exercise\}"),
]


def cmd_structure(target: str = ""):
    """Check chapter(s) against the structural template."""
    targets = resolve_target(target) if target else list(all_chapters())
    if not targets:
        return

    print("=== STRUCTURE CHECK ===\n")

    for name, path in targets:
        text = read_file(path)
        if not text:
            print(f"  {name}: (empty)")
            continue

        print(f"--- {name} ---")
        for label, pattern in CHECKS:
            if re.search(pattern, text):
                print(f"  OK   {label}")
            else:
                print(f"  MISS {label}")
        print()

    print("  Note: detection is pattern-based. A MISS may mean the element is")
    print("  present in a non-standard form and is acceptable. For overview")
    print("  chapters, 'formal apparatus' and 'example' are often missing.")
