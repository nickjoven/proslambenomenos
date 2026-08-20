#!/usr/bin/env python3
"""Preregistration gate: predictions precede the work they cover.

Rules (see PREDICTIONS.md header):
  A. Every `prediction: P-n` reference in a claim resolves to an
     entry in PREDICTIONS.md carrying `expects:` and
     `changes-my-mind:` lines.
  B. Ordering — the earliest commit containing the prediction's
     heading must be an ancestor of the earliest commit adding the
     claim file. An uncommitted claim passes only if its cited
     prediction is already committed: register first, then claim.
     The protected remote makes this ordering third-party-attested.
  C. Scope — claims whose file first appears after the ledger's
     enactment commit and which carry `numeric_match` or
     `novelty: checked-novel` MUST cite a prediction.
  D. LITCHECKS entries whose heading first appears after enactment
     must contain a `prediction:` line. (LC entries predating the
     ledger are exempt automatically.)

Pure helpers (parse_predictions, scope_requires) are unit-tested in
tests/test_checks.py; the git plumbing is exercised live. Exit 0
clean, 2 violations.
"""

import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: pyyaml required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "PREDICTIONS.md"

P_HEAD = re.compile(r"^## (P-\d+) — (\d{4}-\d{2}-\d{2}) — (.+)$", re.M)


def parse_predictions(text: str) -> dict:
    """{pid: {'expects': bool, 'changes': bool}} per entry."""
    out = {}
    parts = re.split(r"^## ", text, flags=re.M)[1:]
    for part in parts:
        m = re.match(r"(P-\d+) — \d{4}-\d{2}-\d{2} — ", part)
        if not m:
            continue
        out[m.group(1)] = {
            "expects": bool(re.search(r"^expects:", part, re.M)),
            "changes": bool(re.search(r"^changes-my-mind:", part, re.M)),
        }
    return out


def scope_requires(doc: dict) -> bool:
    """Pure scope rule: does this (post-enactment) claim need one?"""
    if doc.get("numeric_match") is not None:
        return True
    if (doc.get("novelty") or {}).get("status") == "checked-novel":
        return True
    return False


def _git(*args) -> str:
    r = subprocess.run(["git", *args], capture_output=True, text=True,
                       cwd=ROOT, check=False)
    return r.stdout.strip()


def earliest_commit_with(pattern: str, path: str) -> str:
    out = _git("log", "--reverse", "--format=%H", "-S", pattern, "--", path)
    return out.splitlines()[0] if out else ""


def earliest_commit_of_file(path: str) -> str:
    out = _git("log", "--reverse", "--format=%H", "--", path)
    return out.splitlines()[0] if out else ""


def is_ancestor(a: str, b: str) -> bool:
    if not a or not b:
        return False
    r = subprocess.run(["git", "merge-base", "--is-ancestor", a, b],
                       cwd=ROOT, check=False)
    return r.returncode == 0


def main() -> int:
    errors = []
    if not LEDGER.exists():
        print("prediction gate: no PREDICTIONS.md — ledger missing")
        return 2
    preds = parse_predictions(LEDGER.read_text())
    for pid, flags in preds.items():
        if not flags["expects"]:
            errors.append(f"{pid}: missing expects: line")
        if not flags["changes"]:
            errors.append(f"{pid}: missing changes-my-mind: line")

    enactment = earliest_commit_of_file("PREDICTIONS.md")

    for path in sorted((ROOT / "claims").glob("*.yml")):
        try:
            doc = yaml.safe_load(path.read_text()) or {}
        except yaml.YAMLError:
            continue  # intake gate owns parse errors
        cid = path.stem
        rel = f"claims/{path.name}"
        pref = doc.get("prediction")
        claim_first = earliest_commit_of_file(rel)
        post_enactment = (not claim_first) or (
            enactment and claim_first != enactment
            and is_ancestor(enactment, claim_first))
        if pref is not None:
            if pref not in preds:
                errors.append(f"{cid}: prediction {pref!r} not in ledger")
            else:
                p_first = earliest_commit_with(f"## {pref} —",
                                               "PREDICTIONS.md")
                if claim_first:
                    if not (p_first and (p_first == claim_first or
                                         is_ancestor(p_first, claim_first))):
                        errors.append(
                            f"{cid}: prediction {pref} does not predate the "
                            f"claim in history — register first, then claim")
                elif not p_first:
                    errors.append(
                        f"{cid}: cites uncommitted prediction {pref} — "
                        f"commit the registration before the claim")
        elif post_enactment and scope_requires(doc):
            errors.append(
                f"{cid}: post-enactment claim with numeric_match or "
                f"checked-novel novelty requires a prediction: reference")

    # Rule D: post-enactment LITCHECKS entries cite predictions
    lc = ROOT / "LITCHECKS.md"
    if lc.exists() and enactment:
        text = lc.read_text()
        for part in re.split(r"^## ", text, flags=re.M)[1:]:
            m = re.match(r"(LC-\d+)", part)
            if not m:
                continue
            lcid = m.group(1)
            first = earliest_commit_with(f"## {lcid} ", "LITCHECKS.md")
            after = (not first) or (first != enactment
                                    and is_ancestor(enactment, first))
            if after and "prediction:" not in part:
                errors.append(f"LITCHECKS {lcid}: post-enactment entry "
                              f"lacks a prediction: line")

    if errors:
        print(f"prediction gate: {len(errors)} violation(s)")
        for e in errors:
            print(f"  {e}")
        return 2
    n = len(preds)
    print(f"prediction gate: clean ({n} prediction(s) registered)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
