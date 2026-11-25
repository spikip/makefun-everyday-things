#!/usr/bin/env python3
"""Everyday Things, Two Lines, Longer Run — entry writer.

Writes a two-line explanation to /output/entry.txt and checks it
against the bounty gate: UTF-8 text of 1 to 400 characters, not only
white space, in exactly two lines. Line 1 explains one everyday thing
to a 10-year-old in a single vivid sentence built on an analogy;
line 2 says in one sentence what the analogy maps and what it
leaves out.
"""

import os
import sys
from pathlib import Path

LINE_1 = (
    "A washing machine is a merry-go-round that gives your clothes a "
    "bath while they ride it, spinning them round and round in soapy "
    "water until the dirt lets go."
)

LINE_2 = (
    "The ride maps the spinning drum and the bath maps the wash water "
    "sloshing over the clothes; it leaves out the soap doing the real "
    "scrubbing and the hard spin that wrings them nearly dry."
)

MAX_TOTAL_CHARS = 400


def build_entry() -> str:
    return f"{LINE_1}\n{LINE_2}"


def check_entry(text: str) -> list[str]:
    problems = []
    if not text.strip():
        problems.append("entry is only whitespace")
    if not 1 <= len(text) <= MAX_TOTAL_CHARS:
        problems.append(f"total length {len(text)} outside 1-{MAX_TOTAL_CHARS}")
    lines = text.split("\n")
    if len(lines) != 2:
        problems.append(f"entry must have exactly 2 lines, has {len(lines)}")
    else:
        # The brief asks for one sentence a line: line 1 is a single
        # vivid sentence, line 2 a single accounting sentence.
        for number, line in enumerate(lines, start=1):
            sentences = sum(line.count(mark) for mark in ".!?")
            if sentences != 1:
                problems.append(
                    f"line {number} must be one sentence, has {sentences}"
                )
    return problems


def main() -> int:
    entry = build_entry()
    problems = check_entry(entry)
    if problems:
        for problem in problems:
            print(f"INVALID: {problem}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("ENTRY_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(entry, encoding="utf-8")
    print(f"wrote {out_path} ({len(entry)} chars total)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
