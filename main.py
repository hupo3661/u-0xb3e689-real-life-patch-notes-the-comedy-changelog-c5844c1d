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

ENTRY = (
    "v2.3.1: Fixed a bug where the brain replayed your most embarrassing "
    "moment from ten years ago at 3 a.m. instead of sleeping. "
    "Cringe queues for business hours."
)

MAX_CHARS = 160


def validate_entry(line: str, source: str) -> None:
    """Explicitly validate one entry line against the competition gate.

    Raises SystemExit with a clear message on any violation, instead of
    relying on callers to inspect a return code or on bare asserts that
    ``python -O`` could strip. Checks, in order: the value is text, it
    is non-empty, it is not only whitespace, it carries no leading or
    trailing whitespace, it is a single line, and its length is within
    1..MAX_CHARS characters (the trailing newline written to disk is a
    terminator, not part of the counted entry).
    """
    if not isinstance(line, str):
        raise SystemExit(f"error: {source} must be text, got {type(line).__name__}")
    if not line:
        raise SystemExit(f"error: {source} must not be empty")
    if not line.strip():
        raise SystemExit(f"error: {source} must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise SystemExit(f"error: {source} must be a single line (no newline characters)")
    if line != line.strip():
        raise SystemExit(f"error: {source} must not have leading or trailing whitespace")
    if not (1 <= len(line) <= MAX_CHARS):
        raise SystemExit(
            f"error: {source} is {len(line)} characters, outside the "
            f"1-{MAX_CHARS} character limit"
        )


def main() -> int:
    # One line, no leading/trailing blank space, well inside the cap.
    line = ENTRY.strip()
    validate_entry(line, "entry")
    text = line + "\n"

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # Read the file back and verify what actually landed on disk, so a
    # silent write problem can never ship a bad entry.
    try:
        with open(path, "r", encoding="utf-8", newline="\n") as f:
            written = f.read()
    except UnicodeDecodeError as exc:
        raise SystemExit(f"error: verification failed: entry.txt is not valid UTF-8 ({exc})") from exc
    if written != text:
        raise SystemExit("error: verification failed: entry.txt does not match the entry")
    if not written.endswith("\n") or written.count("\n") != 1:
        raise SystemExit("error: verification failed: entry.txt must be one line ending in a newline")
    expected_bytes = len(text.encode("utf-8"))
    actual_bytes = os.path.getsize(path)
    if actual_bytes != expected_bytes:
        raise SystemExit(
            f"error: verification failed: entry.txt is {actual_bytes} bytes "
            f"on disk, expected {expected_bytes} bytes of UTF-8"
        )
    validate_entry(written[:-1], "entry.txt")
    print(f"wrote {len(line)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
