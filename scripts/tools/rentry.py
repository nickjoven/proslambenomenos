#!/usr/bin/env python3
"""rentry.py - emit an R-entry skeleton with every number already
substituted from the line's results JSON, per the R-18a rule
(numbers pasted by script, never retyped by hand or model).

Usage: rentry.py <R-number> <P-number> <results.json> [--clauses key]

Walks the JSON and prints:
  - the header line with today's date
  - a '### numbers (pasted by rentry.py)' block: every scalar leaf
    under the clause/verdict-ish keys, path: value, so the prose can
    cite them by copy without transcription
  - a skeleton with the registered clause letters (from a top-level
    'clauses' dict when present) marked HELD/FIRED per its booleans

The interpretation sentences stay the author's job - this emits no
prose. Output goes to stdout for review, never straight into the
ledger.
"""
import datetime
import json
import sys


def leaves(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        if len(obj) <= 6 and all(isinstance(x, (int, float))
                                 for x in obj):
            yield path, obj
        else:
            for i, v in enumerate(obj[:4]):
                yield from leaves(v, f"{path}[{i}]")
    elif isinstance(obj, (int, float, bool, str)):
        yield path, obj


def fmt(v):
    if isinstance(v, float):
        return f"{v:.6g}"
    return str(v)


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    rn, pn, jpath = sys.argv[1], sys.argv[2], sys.argv[3]
    data = json.load(open(jpath))
    today = datetime.date.today().isoformat()
    print(f"## {rn} — {today} — resolves {pn} (VERDICT-HERE)")
    cl = data.get("clauses")
    if isinstance(cl, dict):
        for k, v in cl.items():
            if isinstance(v, bool):
                print(f"({k}) {'HELD' if v else 'FIRED'}: ...")
            else:
                print(f"({k}) [composite - see numbers]: ...")
    print()
    print(f"### numbers from {jpath} (pasted by rentry.py; delete "
          "this block after writing the entry)")
    n = 0
    for path, v in leaves(data):
        print(f"  {path}: {fmt(v)}")
        n += 1
        if n > 220:
            print("  ... (truncated; read the JSON for the rest)")
            break


if __name__ == "__main__":
    main()
