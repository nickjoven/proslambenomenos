"""Shared helpers for the curriculum notebooks (stdlib only).

ROOT          repo root (the directory holding CATALOG.md)
show_svg(s)   display an SVG string inline if IPython is present,
              otherwise print the path data as text (the notebooks
              never import numpy or matplotlib)
catalog(name, mutant=False)
              run catalog/<name>.py as a subprocess; return (rc, stdout)
verify(path, mutant=None)
              run scripts/verify/<path> as a subprocess; return (rc, stdout)
falsify(check, mutants)
              the compendium's register(id, fn, mutants) pattern in
              Python: `check()` must be True, every mutant must make it
              False; raise otherwise (so nb_run.py gates it)
"""
import subprocess
import sys
from pathlib import Path

ROOT = next(p for p in [Path(__file__).resolve(), *Path(__file__).resolve().parents]
            if (p / "CATALOG.md").exists())
for _d in ("scripts", "catalog", "scripts/verify", "scripts/experiments"):
    _p = str(ROOT / _d)
    if _p not in sys.path:
        sys.path.append(_p)


SVG_SINK = None   # nb_html.py sets this to a list to capture inline SVGs


def show_svg(svg: str, fallback_label: str = "svg") -> None:
    if SVG_SINK is not None:
        SVG_SINK.append(svg)
        return
    try:
        from IPython.display import SVG, display  # type: ignore
        display(SVG(svg))
    except Exception:
        import re
        paths = re.findall(r'\bd="([^"]+)"', svg)
        print(f"[{fallback_label}: {len(svg)} bytes; {len(paths)} path(s); IPython absent - path data follows]")
        for p in paths[:4]:
            print("  " + (p[:160] + ("..." if len(p) > 160 else "")))


def _run(cmd, cwd) -> tuple:
    r = subprocess.run([sys.executable, *cmd], cwd=str(cwd), capture_output=True, text=True, check=False)
    return r.returncode, (r.stdout + r.stderr).strip()


def catalog(name: str, mutant: bool = False) -> tuple:
    """Run a catalog entry the way scripts/check_catalog.py does (cwd = catalog/)."""
    args = [name + ".py"] + (["--mutant"] if mutant else [])
    rc, out = _run(args, ROOT / "catalog")
    print(f"$ python3 catalog/{args[0]}{' --mutant' if mutant else ''}\n{out}\n-> exit {rc}")
    return rc, out


def verify(script: str, mutant=None) -> tuple:
    args = [str(ROOT / "scripts" / "verify" / script)] + (["--mutant", mutant] if mutant else [])
    rc, out = _run(args, ROOT)
    tail = "\n".join(out.splitlines()[-6:])
    print(f"$ python3 scripts/verify/{script}{' --mutant ' + mutant if mutant else ''}\n{tail}\n-> exit {rc}")
    return rc, out


def mutant_must_fail(name: str, rc: int, out: str) -> None:
    """LAW-16 shape (scripts/check_verify_scripts.py): a failing mutant exits 1,
    prints a FAIL (or NOT CONFIRMED) line, and leaves no traceback."""
    ok = rc == 1 and ("FAIL" in out or "NOT CONFIRMED" in out) and "Traceback" not in out
    print(f"mutant {name}: {'fails as required' if ok else 'DID NOT FAIL - not a test'}")
    if not ok:
        raise AssertionError(f"mutant {name} did not fail (rc={rc})")


def falsify(check, mutants: dict) -> None:
    """check() -> bool with no knobs set must pass; each mutant (a callable
    that sets a knob) must make check() return False. Mirrors
    compendium/index.html register(id, fn, mutants) + KNOBS."""
    base = check()
    print(f"check: {'PASS' if base else 'FAIL'}")
    if not base:
        raise AssertionError("check failed on the unmutated statement")
    if not mutants:
        raise AssertionError("no mutant registered - a check without a failing mutant is a restatement")
    for name, apply in mutants.items():
        knobs = apply()
        r = check(**knobs)
        print(f"mutant {name} {knobs}: {'FAIL (as required)' if not r else 'PASSED - mutant too weak'}")
        if r:
            raise AssertionError(f"mutant {name} survived")
