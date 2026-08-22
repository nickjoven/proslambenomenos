#!/usr/bin/env python3
"""Notebook gate (stdlib only): execute every code cell of every
notebooks/*.ipynb in order, each notebook in a fresh namespace, with
cwd = notebooks/. Exit nonzero on any exception. This is the check that
the curriculum actually runs; nb_html.py reuses run_notebook() to
capture the outputs it renders.

Usage: python3 scripts/nb_run.py [--quiet] [name ...]"""
import contextlib
import io
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NBDIR = ROOT / "notebooks"


def load(path: Path) -> dict:
    nb = json.loads(path.read_text())
    assert nb.get("nbformat") == 4, f"{path.name}: not nbformat 4"
    for c in nb["cells"]:
        assert c["cell_type"] in ("markdown", "code"), path.name
        if c["cell_type"] == "code":
            assert "outputs" in c and "execution_count" in c, f"{path.name}: code cell lacks outputs/execution_count"
    return nb


def source(cell) -> str:
    s = cell["source"]
    return "".join(s) if isinstance(s, list) else s


def run_notebook(path: Path, quiet: bool = True):
    """Yield (cell, captured_stdout, error_or_None) for each cell in order.
    Raises nothing; the caller decides what a failure means."""
    nb = load(path)
    ns = {"__name__": "__main__", "__file__": str(path)}
    old_cwd = os.getcwd()
    old_argv = sys.argv
    os.chdir(NBDIR)
    sys.argv = [path.name]
    try:
        for cell in nb["cells"]:
            if cell["cell_type"] != "code":
                yield cell, "", None
                continue
            buf = io.StringIO()
            err = None
            try:
                with contextlib.redirect_stdout(buf):
                    exec(compile(source(cell), f"{path.name}:cell", "exec"), ns)
            except BaseException as e:  # noqa: BLE001 - a gate reports everything
                err = e
            out = buf.getvalue()
            if not quiet and out:
                print(out, end="")
            yield cell, out, err
            if err is not None:
                return
    finally:
        os.chdir(old_cwd)
        sys.argv = old_argv


def main(argv) -> int:
    quiet = "--quiet" in argv
    names = [a for a in argv if not a.startswith("--")]
    paths = sorted(NBDIR.glob("*.ipynb"))
    if names:
        paths = [p for p in paths if p.stem in names or p.name in names]
    if not paths:
        print("nb gate: no notebooks found")
        return 2
    worst = 0
    t_all = time.perf_counter()
    for p in paths:
        t0 = time.perf_counter()
        ncode = 0
        failed = None
        for cell, out, err in run_notebook(p, quiet=quiet):
            if cell["cell_type"] == "code":
                ncode += 1
            if err is not None:
                failed = (ncode, err, out)
                break
        dt = time.perf_counter() - t0
        if failed:
            k, err, out = failed
            worst = 1
            print(f"  FAIL: {p.stem} - code cell {k}: {type(err).__name__}: {err}  ({dt:.1f}s)")
            tail = out.strip().splitlines()[-5:]
            for line in tail:
                print("    | " + line)
        else:
            print(f"  ok: {p.stem} - {ncode} code cells ({dt:.1f}s)")
    print(f"nb gate: {len(paths)} notebook(s); worst rc {worst}; {time.perf_counter() - t_all:.1f}s total")
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
