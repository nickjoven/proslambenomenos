#!/usr/bin/env python3
"""Red/green fixtures for the intake gate. Every rule must be able to fail."""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_claims as cc  # noqa: E402


def run_fixture(files: dict) -> tuple:
    """files: {name: yaml-text}. Returns (errors, claims)."""
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        for name, text in files.items():
            (d / name).write_text(text)
        errors: list = []
        claims = cc.load_claims(d, errors)
        cc.detect_cycles(claims, errors)
        lcs = cc.litcheck_ids()
        for cid, doc in sorted(claims.items()):
            computed = cc.compute_status(doc, claims, errors, cid)
            if doc.get("status") != computed:
                errors.append(f"{cid}: recorded != computed ({computed})")
            cc.check_novelty(doc, errors, cid, lcs)
        return errors, claims


def expect(cond, label):
    status = "ok" if cond else "FAIL"
    print(f"  {status}: {label}")
    return cond


def main() -> int:
    ok = True

    # RED: declared proven with no evidence -> computed asserted
    e, _ = run_fixture({"a.yml": "id: a\nstatement: x\nstatus: proven\n"})
    ok &= expect(any("recorded != computed (asserted)" in x for x in e),
                 "label-without-evidence blocks")

    # RED: pigeonhole p=0.13 caps at coincidence-unruled
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: proof, ref: r}]\n"
        "numeric_match: {observable: o, pigeonhole_p: 0.13}\n"
        "status: proven\n")})
    ok &= expect(any("coincidence-unruled" in x for x in e),
                 "pigeonhole p>=0.05 caps proven")

    # GREEN: pigeonhole p<0.05 does not cap
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: proof, ref: r}, {kind: computation, ref: c, method: reimplementation}]\n"
        "numeric_match: {observable: o, pigeonhole_p: 0.001}\n"
        "status: proven\n")})
    ok &= expect(not e, "pigeonhole p<0.05 passes")

    # RED: prose-only proof is argued, not proven
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: proof, ref: prose argument}]\n"
        "status: proven\n")})
    ok &= expect(any("recorded != computed (argued)" in x for x in e),
                 "prose-only proof cannot claim proven")

    # RED: proof + rerun-only computation is still argued
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: proof, ref: prose}, {kind: computation, ref: r, method: rerun}]\n"
        "status: proven\n")})
    ok &= expect(any("recorded != computed (argued)" in x for x in e),
                 "proof + same-algorithm rerun cannot claim proven")

    # RED (LAW-3): machine: flag is disabled until an executor exists
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: proof, ref: lean, machine: true}]\n"
        "status: proven\n")})
    ok &= expect(any("disabled" in x for x in e),
                 "machine flag blocked until an executor exists")

    # RED (F3): numeric-agreement vocabulary without numeric_match
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: the ratio agrees with the observed value to 0.1%\n"
        "evidence: [{kind: citation, ref: r}]\n"
        "status: imported\n")})
    ok &= expect(any("pigeonhole cap is not optional" in x for x in e),
                 "agreement vocabulary forces numeric_match")

    # GREEN: proof + independent reimplementation is proven
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: proof, ref: prose}, {kind: computation, ref: r, method: reimplementation}]\n"
        "status: proven\n")})
    ok &= expect(not e, "proof + reimplementation derives proven")

    # RED: argued premise caps downstream proven at conditional
    e, _ = run_fixture({
        "a.yml": ("id: a\nstatement: x\n"
                  "evidence: [{kind: proof, ref: prose}]\nstatus: argued\n"),
        "b.yml": ("id: b\nstatement: y\npremises: [a]\n"
                  "evidence: [{kind: proof, ref: p}, {kind: computation, ref: r, method: reimplementation}]\nstatus: proven\n")})
    ok &= expect(any("recorded != computed (conditional)" in x for x in e),
                 "argued premise caps downstream proven")

    # RED: rerun-only computation is reproduced, not verified
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: computation, ref: r, method: rerun}]\n"
        "status: verified\n")})
    ok &= expect(any("recorded != computed (reproduced)" in x for x in e),
                 "rerun-only cannot claim verified")

    # RED: unsettled premise caps at conditional
    e, _ = run_fixture({
        "a.yml": "id: a\nstatement: x\nstatus: asserted\n",
        "b.yml": ("id: b\nstatement: y\npremises: [a]\n"
                  "evidence: [{kind: proof, ref: r}]\nstatus: proven\n")})
    ok &= expect(any("recorded != computed (conditional)" in x for x in e),
                 "unsettled premise caps proven at conditional")

    # RED: novelty vocabulary while unchecked
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: a novel identity\n"
        "evidence: [{kind: proof, ref: r}]\nstatus: proven\n")})
    ok &= expect(any("novelty vocabulary" in x for x in e),
                 "novelty vocab banned while unchecked")

    # RED: checked-novel with bogus litcheck ref
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: proof, ref: r}]\n"
        "novelty: {status: checked-novel, litcheck: LC-999}\n"
        "status: proven\n")})
    ok &= expect(any("LITCHECKS" in x for x in e),
                 "checked-novel requires real litcheck entry")

    # RED: refutation wins over proof
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: proof, ref: r}, {kind: refutation, ref: r2}]\n"
        "status: proven\n")})
    ok &= expect(any("recorded != computed (refuted)" in x for x in e),
                 "refutation evidence wins")

    # RED: premise cycle detected
    e, _ = run_fixture({
        "a.yml": "id: a\nstatement: x\npremises: [b]\nstatus: asserted\n",
        "b.yml": "id: b\nstatement: y\npremises: [a]\nstatus: asserted\n"})
    ok &= expect(any("cycle" in x for x in e), "premise cycles detected")

    # message gate rules (pure function, no git needed)
    import check_messages as cm
    statuses = {"good": "proven", "weak": "argued"}
    v = cm.check_commit("abc", "routine refactor", set(), statuses)
    ok &= expect(not v, "message gate: plain engineering message passes")
    v = cm.check_commit("abc", "proves the theorem", set(), statuses)
    ok &= expect(bool(v), "message gate: conclusive language without tag blocks")
    v = cm.check_commit("abc", "proves it [claim weak]", set(), statuses)
    ok &= expect(bool(v), "message gate: conclusive language on argued claim blocks")
    v = cm.check_commit("abc", "proves it [claim good]", set(), statuses)
    ok &= expect(not v, "message gate: conclusive language on proven claim passes")
    v = cm.check_commit("abc", "proves it [claim good] [claim weak]", {"good", "weak"}, statuses)
    ok &= expect(not v,
                 "message gate: coverage tag of capped claim allowed when a supporting tag exists")
    v = cm.check_commit("abc", "tweak wording", {"good"}, statuses)
    ok &= expect(any("touches claims/good.yml" in x for x in v),
                 "message gate: touched claim without tag blocks")
    v = cm.check_commit("abc", "tweak wording [claim good]", {"good"}, statuses)
    ok &= expect(not v, "message gate: touched claim with tag passes")

    # RED: evidence citing a nonexistent repo path (G3)
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: computation, ref: 'scripts/verify/nonexistent_xyz.py - check', method: reimplementation}]\n"
        "status: verified\n")})
    ok &= expect(any("does not exist" in x for x in e),
                 "evidence citing a missing repo path blocks")

    # GREEN: evidence citing a real repo path
    e, _ = run_fixture({"a.yml": (
        "id: a\nstatement: x\n"
        "evidence: [{kind: computation, ref: 'scripts/verify/q1_saddle_node.py - check', method: reimplementation}]\n"
        "status: verified\n")})
    ok &= expect(not e, "evidence citing an existing repo path passes")

    # append-only gate: pure diff parser (restored after the reset incident)
    import check_append_only as cao
    diff = ("commit abcdef1234567\n--- a/DECLINED.md\n+++ b/DECLINED.md\n"
            "@@ -1,3 +1,3 @@\n+added line\n context\n")
    ok &= expect(cao.parse_removals(diff) == [],
                 "append-only: insertions and headers produce no removals")
    ok &= expect(cao.parse_removals(diff + "-a past ruling\n") ==
                 [("abcdef123", "a past ruling")],
                 "append-only: removed line detected with its commit")

    # law gate: last-entry hash parsing (restored after the reset incident)
    import check_lawchanges as cl
    ledger = ("# L\n\n## LAW-1 x\ndirection: neutral\nhashes:\n"
              "  " + "a" * 64 + "  scripts/check_claims.py\n"
              "\n## LAW-2 y\ndirection: strengthen\nhashes:\n"
              "  " + "b" * 64 + "  scripts/check_claims.py\n")
    ok &= expect(cl.last_entry_hashes(ledger) ==
                 {"scripts/check_claims.py": "b" * 64},
                 "law gate: last entry wins, hash parsed")

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
