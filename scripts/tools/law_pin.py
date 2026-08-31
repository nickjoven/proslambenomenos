#!/usr/bin/env python3
"""law_pin.py - append a LAW entry with the full covered-set pin.

Usage: law_pin.py <N> <why-file>

Reads the entry prose from <why-file> (the 'why:' body, written by
the integrator - the judgment stays human/model), writes the header,
the prose, and the sha256 of every covered file (per
check_lawchanges.covered_files), then runs the law gate. The hash
loop is the part that was being retyped per entry; it is now here.
"""
import datetime
import hashlib
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    n, why_file = sys.argv[1], sys.argv[2]
    root = Path(subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True,
        text=True, check=True).stdout.strip())
    sys.path.insert(0, str(root / "scripts"))
    from check_lawchanges import covered_files  # noqa: E402
    why = Path(why_file).read_text().rstrip()
    today = datetime.date.today().isoformat()
    ledger = root / "LAWCHANGES.md"
    txt = ledger.read_text()
    if f"## LAW-{n} " in txt:
        sys.exit(f"law_pin: LAW-{n} already exists")
    with ledger.open("a") as fh:
        fh.write(f"\n## LAW-{n} — {today} — {why.splitlines()[0]}\n")
        fh.write("\n".join(why.splitlines()[1:]).rstrip() + "\n")
        fh.write("hashes:\n")
        count = 0
        for f in sorted(covered_files()):
            h = hashlib.sha256((root / f).read_bytes()).hexdigest()
            fh.write(f"  {h}  {f}\n")
            count += 1
    r = subprocess.run(["python3", "scripts/check_lawchanges.py"],
                       cwd=root, capture_output=True, text=True)
    print(f"LAW-{n}: pinned {count} files")
    print(r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
