#!/usr/bin/env python3
"""Generate HANDOFF.md (and handoff.json) from repo state + OPEN.yml,
then pack it as a catbus packet in ~/code/handoffs/.ket linked to the
previous packet. Never hand-write a handoff: the WHERE/STATE blocks
are computed, the rest is OPEN.yml verbatim. Usage:
    python3 scripts/handoff.py            # write HANDOFF.md only
    python3 scripts/handoff.py --pack     # also catbus pack
"""
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORE = Path(os.environ.get("HANDOFF_STORE", Path.home() / "code" / "handoffs"))
sys.path.insert(0, str(ROOT / "scripts"))
import check_claims as cc  # noqa: E402


def sh(*cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True).stdout.strip()


def load_open():
    # minimal YAML reader for OPEN.yml's fixed shape (no pyyaml on this box)
    data = {"owner": [], "agent": [], "decided_since_parent": [], "retracted_since_parent": [],
            "do_not_recompute": [], "artifact": ""}
    section, cur = None, None
    for raw in (ROOT / "OPEN.yml").read_text().splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw.startswith(" ") and raw.endswith(":"):
            section = raw[:-1]
            continue
        m = re.match(r'^artifact:\s*"?([^"]*)"?$', raw)
        if m:
            data["artifact"] = m.group(1)
            continue
        if raw.strip().startswith("- id:"):
            cur = {"id": raw.split(":", 1)[1].strip()}
            data[section].append(cur)
        elif raw.strip().startswith("- "):
            data[section].append(raw.strip()[2:].strip().strip('"'))
        elif cur is not None and ":" in raw:
            k, v = raw.strip().split(":", 1)
            cur[k.strip()] = v.strip().strip('"')
    return data


def main() -> int:
    errors = []
    claims = cc.load_claims(ROOT / "claims", errors)
    census = Counter(d.get("status") for d in claims.values())
    preds = re.findall(r"^## (P-\d+)", (ROOT / "PREDICTIONS.md").read_text(), re.M)
    resolved = re.findall(r"^## (R-\d+) .* resolves (P-\d+)", (ROOT / "PREDICTIONS.md").read_text(), re.M)
    laws = re.findall(r"^## (LAW-\d+)", (ROOT / "LAWCHANGES.md").read_text(), re.M)
    lcs = re.findall(r"^## (LC-\d+)", (ROOT / "LITCHECKS.md").read_text(), re.M)
    gates = sh(sys.executable, "scripts/run_all.py").splitlines()
    worst = next((l for l in gates if "worst rc" in l and "all checks" in l), "gates: not run")
    o = load_open()
    where = {
        "repo": str(ROOT), "branch": sh("git", "rev-parse", "--abbrev-ref", "HEAD"),
        "tip": sh("git", "rev-parse", "--short", "HEAD"),
        "last_link": sh("git", "describe", "--tags", "--match", "link-*", "--abbrev=0"),
        "gates": worst.strip("= "),
    }
    state = {"claims": dict(census), "predictions": preds, "resolved": resolved,
             "laws": laws[-1] if laws else "", "litchecks": lcs[-1] if lcs else ""}
    lines = [f"# HANDOFF {where['last_link']} @ {where['tip']} ({where['branch']})", ""]
    lines += ["WHERE", f"  {where['repo']} | {where['branch']} {where['tip']} | {where['last_link']} | {where['gates']}", ""]
    lines += ["STATE", "  claims " + ", ".join(f"{k}={v}" for k, v in sorted(census.items())),
              f"  predictions {', '.join(preds)}; resolved {', '.join(f'{r}->{p}' for r, p in resolved)}",
              f"  law through {state['laws']}; litchecks through {state['litchecks']}", ""]
    lines += ["DECIDED (since parent)"] + [f"  - {d}" for d in o["decided_since_parent"]] + [""]
    lines += ["RETRACTED (since parent)"] + [f"  - {d}" for d in o["retracted_since_parent"]] + [""]
    lines += ["OPEN (owner)"] + [f"  {i['id']} {i['item']}" + (f"\n      $ {i['command']}" if i.get("command") else "") for i in o["owner"]] + [""]
    lines += ["NEXT (agent, in order)"] + [f"  {i['id']} {i['item']}" for i in o["agent"]] + [""]
    lines += ["DO-NOT-RECOMPUTE"] + [f"  - {d}" for d in o["do_not_recompute"]] + [""]
    lines += ["POINTERS", f"  artifact {o['artifact']}", "  notes/ claims/ PREDICTIONS.md LITCHECKS.md LAWCHANGES.md CATALOG.md RELEASES.md OPEN.yml"]
    text = "\n".join(lines) + "\n"
    (ROOT / "HANDOFF.md").write_text(text)
    (ROOT / "handoff.json").write_text(json.dumps({"where": where, "state": state, "open": o}, indent=1))
    n = len(lines)
    print(f"HANDOFF.md written ({n} lines{'; OVER the 80-line cost rule' if n > 80 else ''})")
    if "--pack" in sys.argv:
        last = STORE / "LAST_CID"
        parent = last.read_text().strip() if last.exists() else ""
        cmd = ["catbus", "--ket-home", str(STORE / ".ket"), "pack",
               "--title", f"{where['last_link']} @ {where['tip']}",
               "--summary", f"{where['last_link']} {where['tip']}; " + "; ".join(o["decided_since_parent"][:2]),
               "--agent", "claude-code", "--file", str(ROOT / "HANDOFF.md"), "--file", str(ROOT / "handoff.json"),
               "--meta", f"tip={where['tip']}", "--meta", f"link={where['last_link']}", "--json"]
        if parent:
            cmd += ["--parent", parent]
        out = subprocess.run(cmd, capture_output=True, text=True)
        print(out.stdout.strip() or out.stderr.strip())
        m = re.search(r'"(?:cid|node_cid|node)"\s*:\s*"([^"]+)"', out.stdout)
        cid = m.group(1) if m else (out.stdout.strip().split()[-1] if out.returncode == 0 else "")
        if cid:
            last.write_text(cid + "\n")
            print(f"packed {cid} (parent {parent or 'none'})")
        return out.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
