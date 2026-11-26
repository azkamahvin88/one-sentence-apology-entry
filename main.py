"""Write the one-sentence apology to /output/entry.txt.

Deterministic, stdlib only: no network, no model calls, no randomness.
The entry is a single fixed line chosen after brainstorming and scoring
24 candidates against the judge's brief (see the submission notes):
one sentence, funny and human at once, owning a real failure.

Usage:
    python3 main.py

Writes the line to $MAKEFUN_OUTPUT_DIR/entry.txt when set,
otherwise to ./output/entry.txt (created if needed).
The file holds exactly the line, with no trailing newline, so its
bytes are identical to the chosen sentence.
"""

import os
import sys

ENTRY = (
    "I'm sorry I kept your secret so well I forgot it myself, "
    "then asked you to remind me what I wasn't supposed to tell anyone."
)


def validate(line: str) -> None:
    """Enforce the competition gate before writing anything."""
    if not line or not line.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(line) > 200:
        raise ValueError(f"entry is {len(line)} characters, over the 200 limit")
    if any(ord(ch) < 0x20 and ch not in "\t" for ch in line):
        raise ValueError("entry must not contain control characters")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    # One sentence: exactly one sentence-terminating mark, at the end.
    terminators = sum(line.count(mark) for mark in ".!?")
    if terminators != 1 or not line.endswith("."):
        raise ValueError("entry must be exactly one sentence ending in '.'")
    # The brief requires a funny AND human apology: a real comic turn about
    # a real failure, in a voice that means it — so the line must apologise
    # in the first person and name the concrete failure it owns.
    lowered = line.lower()
    if "sorry" not in lowered and "apolog" not in lowered:
        raise ValueError("entry must apologise")
    if not any(w in lowered for w in ("i ", "i'm", "i've", "my ")):
        raise ValueError("apology must be owned in the first person")
    failure_cues = ("forgot", "deleted", "lost", "sent", "broke", "leaked", "told", "kept")
    if not any(cue in lowered for cue in failure_cues):
        raise ValueError("apology must name the real failure it owns")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print(f"wrote {len(ENTRY)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
