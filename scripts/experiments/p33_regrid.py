#!/usr/bin/env python3
"""P-33 experiment: the factorial re-registered - corrected null
(per-cell tolerance smear), declared (A, nu) grid, fresh-K pinning
clause. Runs AFTER the P-33 registration commit.

Results -> p33_results.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import p32_derive as D
import p32_factorial as F
from kernels.pmap import pmap

GRID_A = (0.5, 0.9, 1.3, 1.7)
GRID_NU = (1.0 / 8.0, 1.0 / 6.0)
RES_W = 3e-3


def bias_cell(cell):
    geom, N, A, nu = cell
    # temporarily set the drive frequency
    old = D.NU
    D.NU = nu
    try:
        target = nu / 2
        w = F.plateau_width(N, geom, 0.0, A, target,
                            target - 0.06, target + 0.06)
        I0 = target + 0.01
        r1 = D.rho(N, geom, 0.0, 0.6, I0, A)
        r2 = D.rho(N, geom, 0.0, 0.6, I0 + 2e-3, A)
        slope = (r2 - r1) / 2e-3
        w0 = 2 * D.TOL / max(slope, 1e-6)
        wi = F.plateau_width(N, "control", 0.0, A, nu,
                             nu - 0.06, nu + 0.06) if geom == \
            "control" and N == 4 else None
    finally:
        D.NU = old
    return {"geom": geom, "N": N, "A": A, "nu": nu, "w": w,
            "w0": w0, "locked": w > 2 * w0, "w_int_ctrl4": wi}


def pin_cell(cell):
    N, = cell
    return {"N": N, "w": F.plateau_width(N, "alt", 1.2, 0.0, 0.5,
                                         0.30, 0.85, n=160)}


def main():
    out = {"clauses": {}}

    cells = [(geom, N, A, nu)
             for geom in ("control", "seam", "alt")
             for N in range(4, 10)
             for A in GRID_A for nu in GRID_NU]
    rows = pmap(bias_cell, cells, processes=16)

    print("== (a) the grid: half-step vs corrected null")
    locked_cells = [r for r in rows if r["locked"]]
    sup = {}
    for r in rows:
        if r["geom"] != "alt":
            continue
        key = r["N"]
        exc = r["w"] - 2 * r["w0"]
        if key not in sup or exc > sup[key]["excess"]:
            sup[key] = {"excess": exc, "w": r["w"], "w0": r["w0"],
                        "A": r["A"], "nu": r["nu"]}
    print(f"  locked cells anywhere on the grid: {len(locked_cells)}")
    for r in locked_cells[:12]:
        print(f"    {r['geom']} N={r['N']} A={r['A']} nu={r['nu']:.4f}"
              f" w={r['w']:.5f} (null {r['w0']:.5f})")
    for N in range(4, 10):
        s = sup[N]
        print(f"  ALT sup N={N}: w={s['w']:.5f} null={s['w0']:.5f} "
              f"at A={s['A']}, nu={s['nu']:.4f}")
    any_alt_locked = any(r["locked"] for r in rows
                         if r["geom"] == "alt")
    if any_alt_locked:
        wh = {N: sup[N]["w"] for N in range(4, 10)}
        f_gap = min(wh[6], wh[7]) - max(wh[4], wh[5], wh[8], wh[9])
        eo_gap = min(wh[4], wh[6], wh[8]) - max(wh[5], wh[7], wh[9])
        organized = abs(f_gap) >= RES_W
        parity_instead = (not organized) and eo_gap >= RES_W
        ok_a = organized and not parity_instead
        out["outcome"] = "transfer-with-f" if ok_a else \
            ("parity-instead" if parity_instead else "unorganized")
        print(f"  f-gap {f_gap:+.5f} eo-gap {eo_gap:+.5f} -> "
              f"{out['outcome']}")
    else:
        ok_a = True
        out["outcome"] = "transfer-failure-confirmed-on-grid"
        print("  no ALT cell exceeds 2 w0 anywhere on the grid: "
              "transfer failure CONFIRMED across the declared grid")
    out["clauses"]["a"] = ok_a
    out["bias_rows"] = rows
    out["locked_count"] = len(locked_cells)

    print("== (b) pinning f-organization at fresh K = 1.2")
    prows = pmap(pin_cell, [(N,) for N in range(4, 10)], processes=6)
    wp = {r["N"]: r["w"] for r in prows}
    gap_pin = min(wp[6], wp[7]) - max(wp[4], wp[5], wp[8], wp[9])
    ok_b = gap_pin <= -RES_W
    print(f"  widths {[f'{N}:{wp[N]:.5f}' for N in wp]}")
    print(f"  f-gap_pin(K=1.2) = {gap_pin:+.5f}  "
          f"{'ok' if ok_b else 'FAIL'}")
    out["clauses"]["b"] = ok_b
    out["pin_K12"] = wp
    out["gap_pin_K12"] = gap_pin

    print("== (c) integer-step positive control per grid point")
    ok_c = True
    for r in rows:
        if r["w_int_ctrl4"] is not None and r["w_int_ctrl4"] <= \
                2 * r["w0"]:
            ok_c = False
            print(f"  integer step missing at A={r['A']} "
                  f"nu={r['nu']:.4f}")
    print(f"  {'ok' if ok_c else 'FAIL'}")
    out["clauses"]["c"] = ok_c

    json.dump(out, open(os.path.join(HERE, "p33_results.json"), "w"),
              indent=1)
    print("results -> p33_results.json")
    print("clauses:", out["clauses"], "outcome:", out["outcome"])
    return 0 if all(out["clauses"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
