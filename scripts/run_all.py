#!/usr/bin/env python3
"""Run every gate; exit nonzero if any fails."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ("intake gate", ["scripts/check_claims.py"]),
    ("gate fixtures", ["tests/test_checks.py"]),
    ("message gate", ["scripts/check_messages.py"]),
]


def main() -> int:
    worst = 0
    for label, cmd in CHECKS:
        print(f"=== {label} ===")
        r = subprocess.run([sys.executable, *cmd], cwd=ROOT, check=False)
        worst = max(worst, r.returncode)
        print()
    print(f"=== all checks done; worst rc: {worst} ===")
    return worst


if __name__ == "__main__":
    sys.exit(main())
