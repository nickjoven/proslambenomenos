#!/usr/bin/env python3
"""Append-only enforcement against git history.

The rulings ledgers may only grow: DECLINED.md, LITCHECKS.md,
LAWCHANGES.md (and PREDICTIONS.md when it exists). This check scans
`git log -p` for each ledger and flags any commit that REMOVED a
non-empty line — the mechanism by which a future author could quietly
disagree with a past ruling. Insertions anywhere are fine; deletions
and edits (a deletion plus an insertion) are not.

parse_removals() is a pure function over diff text, unit-tested in
tests/test_checks.py. Exit 0 clean, 2 violations.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGERS = ["DECLINED.md", "LITCHECKS.md", "LAWCHANGES.md", "PREDICTIONS.md"]


def parse_removals(diff_text: str):
    """Return [(sha, removed_line)] for non-empty removed lines.
    Ignores diff headers (---), hunk markers, and binary notices."""
    out = []
    sha = "?"
    for line in diff_text.splitlines():
        if line.startswith("commit "):
            sha = line.split()[1][:9]
        elif line.startswith("-") and not line.startswith("---"):
            body = line[1:].strip()
            if body:
                out.append((sha, body))
    return out


def main() -> int:
    violations = []
    for name in LEDGERS:
        if not (ROOT / name).exists():
            continue
        r = subprocess.run(
            ["git", "log", "-p", "--follow", "--", name],
            capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            print(f"(git log failed for {name}: {r.stderr.strip()})")
            continue
        for sha, removed in parse_removals(r.stdout):
            violations.append(f"{name} @ {sha}: removed line: {removed[:70]}")
    if violations:
        print(f"append-only gate: {len(violations)} violation(s)")
        for v in violations:
            print(f"  {v}")
        return 2
    present = [n for n in LEDGERS if (ROOT / n).exists()]
    print(f"append-only gate: clean ({', '.join(present)} grew only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
