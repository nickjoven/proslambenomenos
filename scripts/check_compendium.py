#!/usr/bin/env python3
"""G1 gate: the compendium's own verification checks must pass, re-run
from the tree via scripts/run_compendium_checks.js. Requires node; a
missing node is a hard failure (evidence that cannot be re-run is a
rumor, not a pass)."""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if shutil.which("node") is None:
        print("compendium gate: node not found — checks cannot be re-run "
              "(hard failure by design)")
        return 2
    r = subprocess.run(
        ["node", str(ROOT / "scripts" / "run_compendium_checks.js")],
        cwd=ROOT, check=False)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
