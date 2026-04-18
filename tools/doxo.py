#!/usr/bin/env python3
"""
doxo.py — Introduction to Doxonomics quality toolkit.

Usage:
    python3 tools/doxo.py voice [CHAPTER]
    python3 tools/doxo.py stats [CHAPTER]
    python3 tools/doxo.py refs
    python3 tools/doxo.py structure [CHAPTER]
    python3 tools/doxo.py all [CHAPTER]

CHAPTER accepts: chapter number ("21", "ch21"), appendix letter
("A", "appA"), or filename stem ("ch21-human-nature-narrative").
Omit to run across the whole book.
"""

import sys
from pathlib import Path

# Make the commands/ package importable when running via
# `python3 tools/doxo.py ...` from the project root.
_THIS = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else ""

    if cmd == "voice":
        from commands.voice import cmd_voice
        cmd_voice(arg)
    elif cmd == "stats":
        from commands.stats import cmd_stats
        cmd_stats(arg)
    elif cmd == "refs":
        from commands.refs import cmd_refs
        cmd_refs(arg)
    elif cmd == "structure":
        from commands.structure import cmd_structure
        cmd_structure(arg)
    elif cmd == "all":
        from commands.voice import cmd_voice
        from commands.stats import cmd_stats
        from commands.refs import cmd_refs
        from commands.structure import cmd_structure
        print("### STRUCTURE ###\n")
        cmd_structure(arg)
        print("\n\n### VOICE ###\n")
        cmd_voice(arg)
        print("\n\n### STATS ###\n")
        cmd_stats(arg)
        print("\n\n### REFS ###\n")
        cmd_refs("")  # book-wide regardless
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
