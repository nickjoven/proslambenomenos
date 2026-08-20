#!/usr/bin/env python3
"""G2 gate: every scripts/verify/*.py runs on every gate pass, so
cited computational evidence cannot rot silently. New verify scripts
are rostered automatically by the glob."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    scripts = sorted((ROOT / "scripts" / "verify").glob("*.py"))
    if not scripts:
        print("verify gate: no scripts/verify/*.py found")
        return 0
    worst = 0
    for s in scripts:
        r = subprocess.run([sys.executable, str(s)], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        status = "pass" if r.returncode == 0 else "FAIL"
        print(f"  {s.name}: {status}")
        if r.returncode != 0:
            print(r.stdout[-400:])
            worst = max(worst, r.returncode)
    print(f"verify gate: {len(scripts)} script(s) run; worst rc {worst}")
    return worst


if __name__ == "__main__":
    sys.exit(main())
