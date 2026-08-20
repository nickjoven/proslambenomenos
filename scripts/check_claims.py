#!/usr/bin/env python3
"""Intake gate: statuses are computed, never declared.

Claim schema (claims/<id>.yml):

    id: kebab-case, must equal filename stem
    statement: >            # standalone; no framework jargon
      ...
    premises: [other-claim-id, ...]        # optional; ids must exist
    evidence:                              # optional list
      - kind: proof | computation | citation | refutation
        ref: path or citation string      # required
        method: rerun | reimplementation | external   # computation only
    novelty:
      status: unchecked | classical | folklore | checked-novel
      citation: "..."       # required for classical/folklore
      litcheck: "LC-n"      # required for checked-novel; must exist in LITCHECKS.md
    numeric_match:                         # required iff the claim asserts
      observable: "..."                    # numeric agreement with a measured
      pigeonhole_p: 0.13                   # observable; p from permutation null
    status: <derived>       # MUST equal the computed status

Derivation rules (fixed; changing them is a repo-law change):
    refuted        -- any refutation evidence
    conditional    -- any premise not in SETTLED statuses (cap)
    coincidence-unruled -- numeric_match with p >= 0.05 or missing (cap)
    proven         -- proof evidence that is machine-checked
                      (proof entry carries machine: true) OR proof
                      corroborated by computation with method
                      reimplementation/external. A prose proof alone,
                      or a proof backed only by same-algorithm rerun,
                      derives `argued`, not `proven`.
    argued         -- proof evidence, prose-grade only (attested, not
                      enforced); NOT settled for premise propagation
    verified       -- computation evidence with method reimplementation/external
    reproduced     -- computation evidence, rerun only
    imported       -- citation evidence only
    asserted       -- no evidence

Exit codes: 0 clean, 2 violations.
"""

import re
import sys
from pathlib import Path

# G3: any repo-path-shaped token inside an evidence ref must exist on
# disk. v1 refs (sync_cost/...) live in the archive repo and are not
# resolved here.
REF_PATH = re.compile(r"\b((?:scripts|notes|tests|compendium|claims)/[A-Za-z0-9_./-]+)")

try:
    import yaml
except ImportError:
    print("error: pyyaml required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]

SETTLED = {"proven", "verified", "imported"}  # argued is NOT settled
EVIDENCE_KINDS = {"proof", "computation", "citation", "refutation"}
METHODS = {"rerun", "reimplementation", "external"}
NOVELTY = {"unchecked", "classical", "folklore", "checked-novel"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
# Vocabulary banned in statements while novelty is unchecked.
NOVELTY_VOCAB = re.compile(
    r"(?i)\b(novel|original|new result|first (?:proof|derivation)|"
    r"previously unknown|discover\w*)\b")
PIGEONHOLE_ALPHA = 0.05


def load_claims(claims_dir: Path, errors: list) -> dict:
    claims = {}
    for path in sorted(claims_dir.glob("*.yml")):
        try:
            doc = yaml.safe_load(path.read_text())
        except yaml.YAMLError as e:
            errors.append(f"{path.name}: unparseable YAML ({e})")
            continue
        if not isinstance(doc, dict):
            errors.append(f"{path.name}: not a mapping")
            continue
        cid = doc.get("id")
        if cid != path.stem:
            errors.append(f"{path.name}: id {cid!r} != filename stem")
            continue
        if not ID_RE.match(str(cid)):
            errors.append(f"{path.name}: id not kebab-case")
            continue
        claims[cid] = doc
    return claims


def litcheck_ids() -> set:
    lc = ROOT / "LITCHECKS.md"
    if not lc.exists():
        return set()
    return set(re.findall(r"^## (LC-\d+)", lc.read_text(), re.M))


def compute_status(doc: dict, claims: dict, errors: list, cid: str) -> str:
    ev = doc.get("evidence") or []
    kinds = set()
    methods = set()
    for i, e in enumerate(ev):
        kind = (e or {}).get("kind")
        if kind not in EVIDENCE_KINDS:
            errors.append(f"{cid}: evidence[{i}].kind {kind!r} invalid")
            continue
        ref = (e.get("ref") or "").strip()
        if not ref:
            errors.append(f"{cid}: evidence[{i}] missing ref")
        else:
            for tok in REF_PATH.findall(ref):
                tok = tok.rstrip(".")
                if not (ROOT / tok).exists():
                    errors.append(f"{cid}: evidence[{i}] cites repo path "
                                  f"{tok!r} which does not exist")
        if kind == "computation":
            m = e.get("method")
            if m not in METHODS:
                errors.append(f"{cid}: evidence[{i}] computation requires "
                              f"method in {sorted(METHODS)}")
            else:
                methods.add(m)
        kinds.add(kind)

    if "refutation" in kinds:
        return "refuted"

    # base status from evidence; prose proofs are graded down.
    machine_proof = any((e or {}).get("kind") == "proof" and (e or {}).get("machine") is True
                        for e in ev)
    independent_comp = bool(methods & {"reimplementation", "external"})
    if "proof" in kinds:
        base = "proven" if (machine_proof or independent_comp) else "argued"
    elif "computation" in kinds:
        base = "verified" if methods & {"reimplementation", "external"} \
            else "reproduced"
    elif "citation" in kinds:
        base = "imported"
    else:
        base = "asserted"

    # pigeonhole cap
    nm = doc.get("numeric_match")
    if nm is not None:
        p = nm.get("pigeonhole_p")
        if not isinstance(p, (int, float)) or p >= PIGEONHOLE_ALPHA:
            return "coincidence-unruled"

    # premise cap
    for pid in doc.get("premises") or []:
        if pid not in claims:
            errors.append(f"{cid}: premise {pid!r} names no claim")
            continue
        # settled = the premise's own computed status; use recorded (checked
        # elsewhere to equal computed) to avoid recursion order issues,
        # then verify recorded==computed globally.
        if claims[pid].get("status") not in SETTLED:
            return "conditional" if base in ("proven", "argued", "verified",
                                             "reproduced") else base
    return base


def check_novelty(doc: dict, errors: list, cid: str, lcs: set) -> None:
    nov = doc.get("novelty") or {"status": "unchecked"}
    st = nov.get("status")
    if st not in NOVELTY:
        errors.append(f"{cid}: novelty.status {st!r} invalid")
        return
    if st in ("classical", "folklore") and not (nov.get("citation") or "").strip():
        errors.append(f"{cid}: novelty={st} requires a citation")
    if st == "checked-novel":
        ref = nov.get("litcheck")
        if ref not in lcs:
            errors.append(f"{cid}: novelty=checked-novel requires litcheck "
                          f"ref present in LITCHECKS.md (got {ref!r})")
    if st == "unchecked":
        m = NOVELTY_VOCAB.search(doc.get("statement") or "")
        if m:
            errors.append(f"{cid}: novelty=unchecked but statement uses "
                          f"novelty vocabulary ({m.group(0)!r})")


def detect_cycles(claims: dict, errors: list) -> None:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}

    def dfs(c, stack):
        color[c] = GRAY
        for nxt in claims.get(c, {}).get("premises") or []:
            if nxt not in claims:
                continue
            if color.get(nxt, WHITE) == GRAY:
                errors.append("premise cycle: " + " -> ".join(stack + [nxt]))
            elif color.get(nxt, WHITE) == WHITE:
                dfs(nxt, stack + [nxt])
        color[c] = BLACK

    for c in claims:
        if color.get(c, WHITE) == WHITE:
            dfs(c, [c])


def main(claims_dir: Path = None) -> int:
    errors: list = []
    cdir = claims_dir or ROOT / "claims"
    claims = load_claims(cdir, errors)
    lcs = litcheck_ids()
    detect_cycles(claims, errors)
    for cid, doc in sorted(claims.items()):
        computed = compute_status(doc, claims, errors, cid)
        recorded = doc.get("status")
        if recorded != computed:
            errors.append(
                f"{cid}: recorded status {recorded!r} != computed "
                f"{computed!r} — statuses are derived, not declared; "
                f"change the evidence, not the label")
        check_novelty(doc, errors, cid, lcs)
    if errors:
        print(f"intake gate: {len(errors)} violation(s)")
        for e in errors:
            print(f"  {e}")
        return 2
    from collections import Counter
    dist = Counter(d.get("status") for d in claims.values())
    print(f"intake gate: clean ({len(claims)} claims; "
          + ", ".join(f"{k}={v}" for k, v in sorted(dist.items())) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
