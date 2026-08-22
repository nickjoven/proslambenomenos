#!/usr/bin/env python3
"""Catalog gate: every catalog/c*.py is a runnable mathematical fact.
Each must exit 0 plainly and exit nonzero with --mutant (LAW-11
discipline applied to imported facts). Prints the index."""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("PROS_ROOT", Path(__file__).resolve().parents[1]))   # spec gate points this at a fixture tree


def main() -> int:
    entries = sorted((ROOT / "catalog").glob("c*.py"))
    if not entries:
        print("catalog gate: no entries")
        return 0
    worst = 0
    for e in entries:
        parts = e.read_text().split('"""')
        if len(parts) < 2 or not parts[1].strip():
            print(f"  FAIL (no docstring): {e.stem}")
            worst = 2
            continue
        fact = parts[1].strip().splitlines()[0]
        plain = subprocess.run([sys.executable, e.name], cwd=ROOT / "catalog",
                               capture_output=True, text=True, check=False)
        mut = subprocess.run([sys.executable, e.name, "--mutant"], cwd=ROOT / "catalog",
                             capture_output=True, text=True, check=False)
        # LAW-16: the mutant must RUN and FAIL through the harness
        # (rc 1 + 'MUTANT FAIL' sentinel, no traceback) - a crash is not
        # a failing mutant.
        mut_ok = (mut.returncode == 1 and "MUTANT FAIL" in mut.stdout
                  and "Traceback" not in mut.stderr)
        status = "ok" if plain.returncode == 0 and mut_ok else "FAIL"
        why = "" if status == "ok" else (" (plain failed)" if plain.returncode else
                                         (" (mutant crashed)" if "Traceback" in mut.stderr else " (mutant passed)"))
        print(f"  {status}{why}: {e.stem} - {fact}")
        if status != "ok":
            worst = 2
            print("    " + (plain.stdout + plain.stderr).strip()[-300:].replace("\n", "\n    "))
    print(f"catalog gate: {len(entries)} fact(s); worst rc {worst}")
    return worst


if __name__ == "__main__":
    sys.exit(main())
