#!/usr/bin/env python3
"""Notebook gate (LAW-18): every code cell of every notebooks/*.ipynb
runs, in order, in a fresh namespace, with stdlib Python only. The
curriculum is evidence-grade only while it executes; a notebook that
does not run is prose. Delegates to scripts/nb_run.py."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "nb_run.py")],
                       cwd=ROOT, capture_output=True, text=True, check=False)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(no output)"
    print(f"notebook gate: {tail}")
    if r.returncode:
        print(r.stdout[-600:])
        print(r.stderr[-600:])
    return 2 if r.returncode else 0


if __name__ == "__main__":
    sys.exit(main())
