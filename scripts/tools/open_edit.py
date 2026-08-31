#!/usr/bin/env python3
"""open_edit.py - structured OPEN.yml edits, so ledger surgery is a
CLI call instead of ad-hoc splice code.

Usage:
  open_edit.py close <ID>                  remove an agent/owner item
  open_edit.py queue <ID> <text>           append an agent item
  open_edit.py retext <ID> <text>          replace an item's text
  open_edit.py decided <text>              prepend a decided_since_parent entry
Multiple subcommands can be chained with '--':
  open_edit.py close A-20 -- decided "..." -- queue A-21 "..."

Validates YAML after every mutation; refuses duplicate IDs; prints
one confirmation line per operation. Works on the OPEN.yml of the
current directory's repo root.
"""
import subprocess
import sys

import yaml


def repo_open():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True,
                          check=True).stdout.strip()
    return root + "/OPEN.yml"


def load(path):
    text = open(path).read()
    doc = yaml.safe_load(text)
    return text, doc


def find_item_block(lines, item_id):
    """Return (start, end) line indices of the '- id: <ID>' block."""
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == f"- id: {item_id}":
            start = i
            break
    if start is None:
        return None
    end = start + 1
    while end < len(lines):
        s = lines[end]
        if s.startswith("  - id:") or not s.startswith("    "):
            break
        end += 1
    return (start, end)


def close(path, item_id):
    text = open(path).read()
    lines = text.splitlines(keepends=True)
    blk = find_item_block(lines, item_id)
    if blk is None:
        sys.exit(f"open_edit: no item {item_id}")
    del lines[blk[0]:blk[1]]
    open(path, "w").write("".join(lines))
    print(f"closed {item_id}")


def queue(path, item_id, text_val):
    text = open(path).read()
    if f"- id: {item_id}\n" in text or f"- id: {item_id} " in text:
        sys.exit(f"open_edit: {item_id} already exists")
    lines = text.splitlines(keepends=True)
    for i, ln in enumerate(lines):
        if ln.startswith("agent:"):
            entry = (f"  - id: {item_id}\n"
                     f"    item: {yaml_quote(text_val)}\n")
            lines.insert(i + 1, entry)
            break
    else:
        sys.exit("open_edit: no agent: section")
    open(path, "w").write("".join(lines))
    print(f"queued {item_id}")


def retext(path, item_id, text_val):
    text = open(path).read()
    lines = text.splitlines(keepends=True)
    blk = find_item_block(lines, item_id)
    if blk is None:
        sys.exit(f"open_edit: no item {item_id}")
    keep = [lines[blk[0]]]
    for ln in lines[blk[0] + 1:blk[1]]:
        if ln.strip().startswith("command:"):
            keep.append(ln)
    keep.insert(1, f"    item: {yaml_quote(text_val)}\n")
    lines[blk[0]:blk[1]] = keep
    open(path, "w").write("".join(lines))
    print(f"retexted {item_id}")


def decided(path, text_val):
    lines = open(path).read().splitlines(keepends=True)
    for i, ln in enumerate(lines):
        if ln.startswith("decided_since_parent:"):
            lines.insert(i + 1, f"  - {yaml_quote(text_val)}\n")
            break
    else:
        sys.exit("open_edit: no decided_since_parent: section")
    open(path, "w").write("".join(lines))
    print("decided entry added")


def yaml_quote(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main(argv):
    path = repo_open()
    groups, cur = [], []
    for a in argv:
        if a == "--":
            groups.append(cur)
            cur = []
        else:
            cur.append(a)
    groups.append(cur)
    for g in groups:
        if not g:
            continue
        op = g[0]
        if op == "close" and len(g) == 2:
            close(path, g[1])
        elif op == "queue" and len(g) == 3:
            queue(path, g[1], g[2])
        elif op == "retext" and len(g) == 3:
            retext(path, g[1], g[2])
        elif op == "decided" and len(g) == 2:
            decided(path, g[1])
        else:
            sys.exit(__doc__)
        yaml.safe_load(open(path))  # validate after every op
    print("OPEN.yml valid")


if __name__ == "__main__":
    main(sys.argv[1:])
