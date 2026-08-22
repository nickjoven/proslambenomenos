#!/usr/bin/env python3
"""Constitutional layer: the gates cannot be edited silently.

Covered files: every scripts/check_*.py, scripts/run_all.py, and
tests/test_checks.py — the law and its teeth, including this file.
LAWCHANGES.md is an append-only ledger; each entry records date,
direction (strengthen | weaken | neutral), a why, and the SHA-256 of
every covered file AFTER the change. This check recomputes current
hashes and compares them to the LAST entry:

  - any covered file whose hash differs -> red (edit without an entry)
  - any covered file absent from the entry -> red (new gate, no entry)
  - any entry file that no longer exists -> red (gate deleted silently)

Amending the law stays legal; amending it without a dated, directed,
justified ledger entry does not. Exit 0 clean, 2 violations.
"""

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "LAWCHANGES.md"

HASH_LINE = re.compile(r"^  ([0-9a-f]{64})  (\S+)$")
DIRECTION = re.compile(r"^direction: (strengthen|weaken|neutral)$", re.M)


def covered_files():
    files = sorted(str(p.relative_to(ROOT))
                   for p in (ROOT / "scripts").glob("check_*.py"))
    files += sorted(str(p.relative_to(ROOT))
                    for p in (ROOT / "scripts").glob("*.js"))
    files += sorted(str(p.relative_to(ROOT))
                    for p in (ROOT / "scripts" / "verify").glob("*.py"))
    files.append("scripts/run_all.py")
    files.append("tests/test_checks.py")
    files.append("catalog/_common.py")   # LAW-16: the catalog harness decides what self-testing means
    return sorted(set(files))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def last_entry_hashes(text: str) -> dict:
    entries = re.split(r"^## ", text, flags=re.M)[1:]
    if not entries:
        return {}
    last = entries[-1]
    out = {}
    for line in last.splitlines():
        m = HASH_LINE.match(line)
        if m:
            out[m.group(2)] = m.group(1)
    return out


def main() -> int:
    errors = []
    if not LEDGER.exists():
        print("law gate: LAWCHANGES.md missing — the constitution has no ledger")
        return 2
    text = LEDGER.read_text()
    recorded = last_entry_hashes(text)
    if not recorded:
        errors.append("no hash block found in the last LAWCHANGES entry")
    entries = re.split(r"^## ", text, flags=re.M)[1:]
    if entries and not DIRECTION.search(entries[-1]):
        errors.append("last entry missing a direction: strengthen|weaken|neutral")

    current = {f: sha256(ROOT / f) for f in covered_files()}
    for f, h in current.items():
        if f not in recorded:
            errors.append(f"{f}: covered gate file has NO entry in the ledger")
        elif recorded[f] != h:
            errors.append(f"{f}: edited since the last LAWCHANGES entry "
                          f"(recorded {recorded[f][:12]}…, current {h[:12]}…)")
    for f in recorded:
        if f not in current:
            errors.append(f"{f}: in the ledger but gone from the tree")

    if errors:
        print(f"law gate: {len(errors)} violation(s)")
        for e in errors:
            print(f"  {e}")
        return 2
    print(f"law gate: clean ({len(current)} covered files match entry "
          f"LAW-{len(entries)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
