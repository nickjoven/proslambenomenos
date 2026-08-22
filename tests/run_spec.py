#!/usr/bin/env python3
"""Spec gate: executes tests/spec/*.spec - every gate rule written in a
controlled grammar, one rule per line, no free prose inside a rule.

Grammar
  FIXTURE <name>                     # a fixture is a set of files or one event
    FILE <relative/path>             # file content follows, indented 4 spaces, until END
        ...
    END
    COMMIT "<message>" [TOUCHING a,b] [STATUSES a=proven,b=argued]
    RESULT rc=<int> [STDOUT "<text>"] [STDERR "<text>"]
  RULE <gate>.<n> "<label>": GIVEN <fixture> WHEN <gate> RUNS THEN <verdict>
  verdict := ACCEPT
           | REJECT MENTIONING "<token>" [AND "<token>"]...
           | EQUALS <json>
Gates: intake, message, falsifier, catalog, notes, append-only-parser,
law-parser, prediction-parser, prediction-scope.
Every RULE must run; a RULE whose gate is unknown is a failure (a spec
written before its gate exists is RED by construction - that is TDD).
Exit 0 iff every rule holds."""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

RULE = re.compile(r'^RULE\s+(?P<id>[\w.-]+)\s+"(?P<label>[^"]*)":\s*GIVEN\s+(?P<fx>[\w-]+)\s+WHEN\s+(?P<gate>[\w-]+)\s+RUNS\s+THEN\s+(?P<verdict>.+)$')
COMMIT = re.compile(r'^COMMIT\s+"(?P<msg>(?:[^"\\]|\\.)*)"(?:\s+TOUCHING\s+(?P<touch>[\w,-]+))?(?:\s+STATUSES\s+(?P<st>[\w=,-]+))?\s*$')
RESULT = re.compile(r'^RESULT\s+rc=(?P<rc>-?\d+)(?:\s+STDOUT\s+"(?P<out>(?:[^"\\]|\\.)*)")?(?:\s+STDERR\s+"(?P<err>(?:[^"\\]|\\.)*)")?\s*$')


def parse(text):
    fixtures, rules = {}, []
    lines = text.splitlines()
    i = 0
    cur = None
    while i < len(lines):
        raw = lines[i]; line = raw.strip()
        if not line or line.startswith("#"):
            i += 1; continue
        if line.startswith("FIXTURE "):
            cur = line.split(None, 1)[1].strip(); fixtures[cur] = {"files": {}, "commit": None, "result": None}
            i += 1; continue
        if line.startswith("FILE "):
            path = line.split(None, 1)[1].strip(); body = []
            i += 1
            while i < len(lines) and lines[i].strip() != "END":
                body.append(lines[i][4:] if lines[i].startswith("    ") else lines[i].lstrip())
                i += 1
            fixtures[cur]["files"][path] = "\n".join(body) + "\n"
            i += 1; continue
        m = COMMIT.match(line)
        if m:
            st = dict(kv.split("=") for kv in (m.group("st") or "").split(",") if kv)
            fixtures[cur]["commit"] = {"msg": m.group("msg").replace('\\"', '"'), "touch": set((m.group("touch") or "").split(",")) - {""}, "statuses": st}
            i += 1; continue
        m = RESULT.match(line)
        if m:
            fixtures[cur]["result"] = {"rc": int(m.group("rc")), "out": (m.group("out") or "").replace("\\n", "\n"), "err": (m.group("err") or "").replace("\\n", "\n")}
            i += 1; continue
        m = RULE.match(line)
        if m:
            rules.append(m.groupdict()); i += 1; continue
        raise SyntaxError(f"unparseable spec line: {raw!r}")
    return fixtures, rules


def verdict_of(v):
    v = v.strip()
    if v == "ACCEPT":
        return ("accept", [])
    if v.startswith("REJECT MENTIONING"):
        return ("reject", re.findall(r'"((?:[^"\\]|\\.)*)"', v))
    if v.startswith("EQUALS "):
        return ("equals", json.loads(v[len("EQUALS "):]))
    raise SyntaxError(f"bad verdict {v!r}")


# ---- gate adapters: each returns (errors_list) or a value for EQUALS ----
def gate_intake(fx):
    import check_claims as cc
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        for p, c in fx["files"].items():
            (d / Path(p).name).write_text(c)
        errors = []
        claims = cc.load_claims(d, errors)
        cc.detect_cycles(claims, errors)
        lcs = cc.litcheck_ids()
        for cid, doc in sorted(claims.items()):
            computed = cc.compute_status(doc, claims, errors, cid)
            if doc.get("status") != computed:
                errors.append(f"{cid}: recorded != computed ({computed})")
            cc.check_novelty(doc, errors, cid, lcs)
            cc.check_falsifier(doc, errors, cid, computed)
            cc.check_compendium_refs(doc, errors, cid)
        return errors


def gate_message(fx):
    import check_messages as cm
    c = fx["commit"]
    return cm.check_commit("abc", c["msg"], c["touch"], c["statuses"])


def gate_falsifier(fx):
    import check_verify_scripts as cv
    r = fx["result"]
    class R: pass
    rr = R(); rr.returncode = r["rc"]; rr.stdout = r["out"]; rr.stderr = r["err"]
    ok, why = cv.ran_and_failed(rr)
    return [] if ok else [why]


def gate_catalog(fx):
    with tempfile.TemporaryDirectory() as td:
        d = Path(td); (d / "catalog").mkdir()
        (d / "catalog" / "_common.py").write_text((ROOT / "catalog" / "_common.py").read_text())
        for p, c in fx["files"].items():
            (d / p).write_text(c)
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_catalog.py")], cwd=ROOT,
                           env={**os.environ, "PROS_ROOT": str(d)}, capture_output=True, text=True)
        return [] if r.returncode == 0 else [l for l in r.stdout.splitlines() if "FAIL" in l]


def gate_notes(fx):
    import check_notes as cn
    with tempfile.TemporaryDirectory() as td:
        d = Path(td); (d / "notes").mkdir()
        for p, c in fx["files"].items():
            (d / p).parent.mkdir(parents=True, exist_ok=True); (d / p).write_text(c)
        return cn.check_notes(d)


def gate_append_only_parser(fx):
    import check_append_only as cao
    return cao.parse_removals(next(iter(fx["files"].values())))


def gate_law_parser(fx):
    import check_lawchanges as cl
    return cl.last_entry_hashes(next(iter(fx["files"].values())))


def gate_prediction_parser(fx):
    import check_predictions as cp
    preds = cp.parse_predictions(next(iter(fx["files"].values())))
    return {k: {"expects": bool(v["expects"]), "changes": bool(v["changes"])} for k, v in preds.items()}


def gate_prediction_scope(fx):
    import check_predictions as cp, yaml
    return cp.scope_requires(yaml.safe_load(next(iter(fx["files"].values()))))


GATES = {"intake": gate_intake, "message": gate_message, "falsifier": gate_falsifier, "catalog": gate_catalog,
         "notes": gate_notes, "append-only-parser": gate_append_only_parser, "law-parser": gate_law_parser,
         "prediction-parser": gate_prediction_parser, "prediction-scope": gate_prediction_scope}


def main() -> int:
    specs = sorted((ROOT / "tests" / "spec").glob("*.spec"))
    total = passed = 0
    for s in specs:
        fixtures, rules = parse(s.read_text())
        for r in rules:
            total += 1
            kind, want = verdict_of(r["verdict"])
            fx = fixtures.get(r["fx"])
            gate = GATES.get(r["gate"])
            if fx is None or gate is None:
                print(f"  FAIL {r['id']} {r['label']!r}: {'unknown fixture' if fx is None else 'no such gate: ' + r['gate']}")
                continue
            try:
                got = gate(fx)
            except Exception as e:
                print(f"  FAIL {r['id']} {r['label']!r}: gate raised {type(e).__name__}: {e}")
                continue
            if kind == "accept":
                ok = not got
            elif kind == "reject":
                ok = bool(got) and all(any(tok in str(x) for x in got) for tok in want)
            else:
                ok = json.loads(json.dumps(got)) == want
            passed += ok
            print(f"  {'ok' if ok else 'FAIL'} {r['id']} {r['label']}" + ("" if ok else f"  -> got {got!r}"))
    print(f"spec gate: {passed}/{total} rules hold across {len(specs)} spec file(s)")
    return 0 if passed == total and total > 0 else 2


if __name__ == "__main__":
    sys.exit(main())
