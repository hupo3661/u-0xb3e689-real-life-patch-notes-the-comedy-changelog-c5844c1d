#!/usr/bin/env python3
"""Real-Life Patch Notes: The Comedy Changelog.

Writes one funny one-line patch note for a bug in real life / human
biology to /output/entry.txt.

The note is a single hand-written line, chosen to read like a real
release note: a version number, a terse engineering register, a specific
recognisable bug of the body, and a fix stated as if it shipped. The
program is deterministic by design: it writes the same line on every
run, and it self-checks the competition's gate (UTF-8 text, one line,
1 to 160 characters, not only white space) before it writes.
"""

import os
import sys

ENTRY = (
    "v2.3.1: Fixed a bug where the brain replayed your most embarrassing "
    "moment from ten years ago at 3 a.m. instead of sleeping. "
    "Cringe queues for business hours."
)

MAX_CHARS = 160


def main() -> int:
    # One line, no leading/trailing blank space, well inside the cap.
    line = ENTRY.strip()
    if "\n" in line or "\r" in line:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if not line:
        print("entry must not be empty", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"entry is {len(line)} characters, over the {MAX_CHARS} cap",
            file=sys.stderr,
        )
        return 1
    text = line + "\n"
    if len(text) > MAX_CHARS:
        print("entry with newline is over the cap", file=sys.stderr)
        return 1

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"wrote {len(line)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
