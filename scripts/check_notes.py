#!/usr/bin/env python3
"""Notes gate (LAW-20): prose carries no load. Every notes/*.md must
open with a declaration:
    <!-- commentary -->                       no load; may not issue verdicts
    <!-- evidence: path1, path2, ... -->     load borne by executable artifacts
Evidence paths must exist and be executable artifacts or their outputs
(.py, .js, .json, .ipynb, .yml, .html under compendium/notebooks);
prose (.md) is not evidence. A commentary note may not use the settled-
status words proven / verified / refuted as verdicts ("is proven",
"was refuted", ...). Root overridable via PROS_ROOT for the spec gate."""
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("PROS_ROOT", Path(__file__).resolve().parents[1]))
DECL = re.compile(r"^\s*<!--\s*(commentary|evidence:\s*(?P<paths>[^>]*?))\s*-->", re.M)
EXEC_SUFFIX = {".py", ".js", ".json", ".ipynb", ".yml", ".yaml"}
VERDICT = re.compile(r"\b(?:is|are|was|were|be|been|hereby|now)\s+(proven|verified|refuted)\b", re.I)


def check_notes(root: Path) -> list:
    errors = []
    for note in sorted((root / "notes").glob("*.md")):
        text = note.read_text()
        head = "\n".join(text.splitlines()[:3])
        m = DECL.search(head)
        rel = f"notes/{note.name}"
        if not m:
            errors.append(f"{rel}: no declaration (<!-- commentary --> or <!-- evidence: ... -->) in the first three lines")
            continue
        if m.group(1).startswith("commentary"):
            v = VERDICT.search(text)
            if v:
                errors.append(f"{rel}: commentary uses a settled-status verdict ({v.group(0)!r})")
            continue
        paths = [p.strip() for p in (m.group("paths") or "").split(",") if p.strip()]
        if not paths:
            errors.append(f"{rel}: evidence declaration lists no paths")
        for p in paths:
            q = root / os.path.normpath(p)
            if not q.exists():
                errors.append(f"{rel}: declared evidence {p!r} does not exist")
                continue
            ok = q.suffix in EXEC_SUFFIX or (q.suffix == ".html" and q.parts[-2] in ("compendium", "notebooks"))
            if not ok:
                errors.append(f"{rel}: declared evidence {p!r} is not executable (prose is not evidence)")
    return errors


def main() -> int:
    errors = check_notes(ROOT)
    n = len(list((ROOT / "notes").glob("*.md")))
    if errors:
        print(f"notes gate: {len(errors)} violation(s)")
        for e in errors:
            print(f"  {e}")
        return 2
    print(f"notes gate: clean ({n} notes declared)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
