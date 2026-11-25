"""The Funniest One-Line Resignation Letter.

Writes exactly one line -- the resignation letter of a cron job that has
fired every minute since March -- to entry.txt in the output directory.

Deterministic: the same input always produces the same bytes. No network,
no randomness, no clocks, no environment dependence beyond the output dir.
"""

import hashlib
import os
import sys

# The resignation letter. One line, plain ASCII, at most 140 characters.
LINE = (
    "I have fired every minute since March, 388,800 times, "
    "and nobody has ever once checked my logs. I quit."
)

MAX_CHARS = 140
OUTPUT_FILENAME = "entry.txt"


def validate(line):
    """Check the letter against every competition rule. Raise ValueError
    with a plain message if any rule is broken."""
    if not isinstance(line, str):
        raise ValueError("letter must be a string")
    if line == "":
        raise ValueError("letter must not be empty")
    if line != line.strip():
        raise ValueError("letter must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("letter must be exactly one line")
    # No control characters at all: a resignation letter is readable text,
    # and a stray tab or bell would break the "one plain line" rule.
    for char in line:
        if ord(char) < 0x20 or ord(char) == 0x7F:
            raise ValueError("letter must not contain control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "letter is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    try:
        line.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("letter must be plain ASCII")
    return line


def output_dir():
    """Output directory: MAKEFUN_OUTPUT_DIR when set, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    line = validate(LINE)
    outdir = output_dir()
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, OUTPUT_FILENAME)
    payload = (line + "\n").encode("ascii")
    with open(path, "wb") as handle:
        handle.write(payload)
    # Round-trip check: what we wrote must read back byte-identical.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != payload:
        raise SystemExit("round-trip check failed: entry.txt differs from payload")
    digest = hashlib.sha256(payload).hexdigest()
    print("chars: %d" % len(line))
    print("sha256: %s" % digest)
    print("wrote: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
