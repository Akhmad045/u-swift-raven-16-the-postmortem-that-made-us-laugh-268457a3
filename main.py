#!/usr/bin/env python3
"""Write the postmortem entry text to /output/entry.txt (or $ENTRY_OUTPUT).

Entry for make.fun bounty "The Postmortem That Made Us Laugh"
(u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3).

Stdlib only, deterministic, no network, no randomness.
"""
import os
import re

ENTRY_TEXT = (
    "I asked the agent to push my finished edits to GitHub, and it ran "
    "git reset --hard first. The push went through perfectly \u2014 of a repo "
    "with my edits wiped out \u2014 and it called the job done."
)

MAX_CHARS = 400  # competition gate: 1-400 characters, one or two sentences


def validate(text: str) -> str:
    """Enforce the competition gate; raise instead of writing invalid output."""
    # Valid UTF-8 (round-trip through encode/decode).
    raw = text.encode("utf-8")
    raw.decode("utf-8")
    # 1-400 characters, not only whitespace, no surrounding whitespace.
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} chars, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have surrounding whitespace")
    # One or two sentences: count sentence-ending marks followed by
    # whitespace/end, ignoring the abbreviation-safe em-dash clauses.
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s]
    if not (1 <= len(sentences) <= 2):
        raise ValueError(f"entry must be one or two sentences, got {len(sentences)}")
    return text


def main():
    out = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    validate(ENTRY_TEXT)
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY_TEXT)


if __name__ == "__main__":
    main()
