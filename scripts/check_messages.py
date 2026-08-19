#!/usr/bin/env python3
"""Message-layer gate: conclusive claim vocabulary in commit messages must
reference an existing claim whose computed status supports the language.

v1's history reads as completed discovery at every claim moment ("gives
S_v(K=1) = 16 exactly", "independent derivation confirms", "3 Class 5
closures") because no tool ever read the messages. This gate scans a
commit range and blocks messages that use conclusive vocabulary without a
`[claim <id>]` tag naming a claim in claims/ whose status is one of
proven/verified/refuted (refuted supports "refutes"-style language).

Second rule (mechanical coverage): any commit whose diff touches
claims/*.yml must carry a [claim <id>] tag for EVERY touched claim id
(file stem = id), so the narrative layer cannot silently modify the
evidence layer. Both rules live in check_commit(), which is unit-tested
in tests/test_checks.py.

Usage:
    check_messages.py                # checks HEAD only
    check_messages.py RANGE          # e.g. origin/main..HEAD

Exit codes: 0 clean, 2 violations.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CONCLUSIVE = re.compile(
    r"(?i)\b(proves?|proof of|exact(?:ly)?|confirms?|closes?|novel|"
    r"first (?:proof|derivation)|zero free parameters|class 5)\b")
TAG = re.compile(r"\[claim ([a-z0-9-]+)\]")
SUPPORTING = {"proven", "verified", "refuted"}


def claim_statuses() -> dict:
    try:
        import yaml
    except ImportError:
        return {}
    out = {}
    for p in (ROOT / "claims").glob("*.yml"):
        try:
            d = yaml.safe_load(p.read_text())
            out[d.get("id")] = d.get("status")
        except Exception:
            continue
    return out


def check_commit(sha, msg, touched_claim_ids, statuses):
    """Both message rules on one commit; returns a list of violations.
    Pure function of its inputs — unit-testable without git."""
    violations = []
    tags = TAG.findall(msg)
    hits = sorted({m.group(0).lower() for m in CONCLUSIVE.finditer(msg)})
    if hits:
        if not tags:
            violations.append(f"{sha}: uses {hits} with no [claim <id>] tag")
        for t in tags:
            if t not in statuses:
                violations.append(f"{sha}: [claim {t}] names no claim")
            elif statuses[t] not in SUPPORTING:
                violations.append(
                    f"{sha}: [claim {t}] has status {statuses[t]!r}, which "
                    f"does not support conclusive language {hits}")
    # coverage rule: every touched claim must be tagged
    for cid in sorted(touched_claim_ids):
        if cid not in tags:
            violations.append(
                f"{sha}: touches claims/{cid}.yml without a [claim {cid}] tag")
    return violations


def touched_claims(sha):
    r = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", sha],
        capture_output=True, text=True, cwd=ROOT, check=False)
    out = set()
    for line in r.stdout.splitlines():
        line = line.strip()
        if line.startswith("claims/") and line.endswith(".yml"):
            out.add(line[len("claims/"):-len(".yml")])
    return out


def main() -> int:
    rng = sys.argv[1] if len(sys.argv) > 1 else "HEAD^..HEAD"
    r = subprocess.run(
        ["git", "log", "--format=%H%x00%B%x01", rng],
        capture_output=True, text=True, cwd=ROOT, check=False)
    if r.returncode != 0:
        # single-commit repos have no HEAD^; fall back to HEAD alone
        r = subprocess.run(
            ["git", "log", "-1", "--format=%H%x00%B%x01"],
            capture_output=True, text=True, cwd=ROOT, check=False)
        if r.returncode != 0:
            print(f"(git log failed: {r.stderr.strip()})")
            return 0
    statuses = claim_statuses()
    violations = []
    for entry in r.stdout.split("\x01"):
        if "\x00" not in entry:
            continue
        sha, msg = entry.split("\x00", 1)
        sha = sha.strip()
        violations += check_commit(sha[:9], msg, touched_claims(sha), statuses)
    if violations:
        print(f"message gate: {len(violations)} violation(s)")
        for v in violations:
            print(f"  {v}")
        return 2
    print("message gate: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
