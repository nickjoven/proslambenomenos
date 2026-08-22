#!/usr/bin/env python3
"""G2 gate: every scripts/verify/*.py runs on every gate pass, so
cited computational evidence cannot rot silently. New verify scripts
are rostered automatically by the glob."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def ran_and_failed(r) -> tuple:
    """LAW-16: a falsifier counts only if the mutant RAN and the check
    FAILED - rc == 1, a FAIL line on stdout, no traceback, no usage
    error. A crash, a missing file, or an unrecognised mutant name
    (rc 2) is an error, not a failure (audit 2026-08-22: single-quoted
    YAML made the old regex run a nonexistent file, rc 2, 'fails as
    required')."""
    if r.returncode != 1:
        return False, f"rc {r.returncode} (need 1)"
    if "Traceback" in r.stderr:
        return False, "crashed"
    if "FAIL" not in r.stdout and "NOT CONFIRMED" not in r.stdout:
        return False, "no FAIL line on stdout"
    return True, "mutant ran and failed as required"


def run_falsifiers() -> int:
    """LAW-11/16: every falsifier in claims/*.yml (parsed as YAML, not
    regexed) must run its mutant and fail."""
    import check_claims as cc
    errors = []
    claims = cc.load_claims(ROOT / "claims", errors)
    worst = 0
    n = 0
    for cid, doc in sorted(claims.items()):
        fal = doc.get("falsifier")
        if not isinstance(fal, str) or not fal.strip():
            continue
        n += 1
        r = subprocess.run([sys.executable] + fal.split(), cwd=ROOT,
                           capture_output=True, text=True, check=False)
        ok, why = ran_and_failed(r)
        print(f"  falsifier {cid}: {why}")
        if not ok:
            worst = 2
    print(f"falsifier check: {n} mutant(s) run; all ran-and-failed: {worst == 0}")
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
