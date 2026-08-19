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
        "evidence: [{kind: proof, ref: r}]\n"
        "numeric_match: {observable: o, pigeonhole_p: 0.001}\n"
        "status: proven\n")})
    ok &= expect(not e, "pigeonhole p<0.05 passes")

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

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
