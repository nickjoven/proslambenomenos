#!/usr/bin/env python3
"""G2 gate: every scripts/verify/*.py runs on every gate pass, so
cited computational evidence cannot rot silently. New verify scripts
are rostered automatically by the glob."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FALSIFIER = re.compile(r'^falsifier:\s*"?([^"\n]+?)"?\s*$', re.M)


def run_falsifiers() -> int:
    """LAW-11: every falsifier command in claims/*.yml must FAIL
    (rc != 0). A falsifier that passes means the mutant did not
    change the verdict - the script is not testing the discriminator."""
    worst = 0
    n = 0
    for y in sorted((ROOT / "claims").glob("*.yml")):
        for cmd in FALSIFIER.findall(y.read_text()):
            n += 1
            r = subprocess.run([sys.executable] + cmd.split(), cwd=ROOT,
                               capture_output=True, text=True, check=False)
            status = "fails as required" if r.returncode != 0 else "PASSES (bad)"
            print(f"  falsifier {y.stem}: {status}")
            if r.returncode == 0:
                worst = 2
    print(f"falsifier check: {n} mutant(s) run; all failed: {worst == 0}")
    return worst


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
    return max(worst, run_falsifiers())


if __name__ == "__main__":
    sys.exit(main())
