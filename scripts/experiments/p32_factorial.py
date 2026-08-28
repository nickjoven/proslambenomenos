#!/usr/bin/env python3
"""P-32 experiment: the drive-geometry parity factorial. Runs AFTER
the registration commit; cells and clauses as registered.

Results -> p32_results.json.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import p32_derive as D
from kernels.pmap import pmap

NU = D.NU
TOL = D.TOL
FLOOR = 1e-5
RES_W = 3e-3


def plateau_width(N, geom, K, A, target, lo, hi, n=120):
    def r(I):
        return D.rho(N, geom, K, 0.6, I, A)
    xs = [lo + (hi - lo) * k / n for k in range(n + 1)]
    inside = [x for x in xs if abs(r(x) - target) < TOL]
    if not inside:
        return 0.0
    a, b = inside[0], inside[-1]
    step = (hi - lo) / n

    def bisect(out, inn):
        for _ in range(30):
            m = 0.5 * (out + inn)
            if abs(r(m) - target) < TOL:
                inn = m
            else:
                out = m
        return inn
    return bisect(b + step, b) - bisect(a - step, a)


def cell_worker(cell):
    kind, geom, N, target = cell
    if kind == "pin":
        w = plateau_width(N, geom, 1.0, 0.0, 0.5, 0.30, 0.80, n=160)
    else:
        w = plateau_width(N, geom, 0.0, 0.9, target,
                          target - 0.06, target + 0.06)
    return {"kind": kind, "geom": geom, "N": N, "target": target,
            "width": w}


def alternates(vals, res):
    d = [b - a for a, b in zip(vals, vals[1:])]
    signs = [1 if x > res else (-1 if x < -res else 0)
             for x in d]
    runs = [s for s in signs if s != 0]
    return all(a * b < 0 for a, b in zip(runs, runs[1:])) and \
        len(runs) >= 3


def main():
    reg = json.load(open(os.path.join(HERE, "p32_registration.json")))
    pins = reg["EQ4"]
    out = {"clauses": {}}

    cells = []
    for N in range(4, 10):
        cells.append(("pin", "seam", N, 0.5))
        cells.append(("pin", "control", N, 0.5))
        cells.append(("pin", "alt", N, 0.5))
        for geom in ("control", "seam", "alt"):
            for target in (NU, NU / 2):
                cells.append(("bias", geom, N, target))
    rows = pmap(cell_worker, cells, processes=16)
    table = {(r["kind"], r["geom"], r["N"], r["target"]): r["width"]
             for r in rows}
    out["table"] = [{"kind": k[0], "geom": k[1], "N": k[2],
                     "target": k[3], "width": w}
                    for k, w in sorted(table.items(),
                                       key=lambda x: (x[0][0], x[0][1],
                                                      x[0][2], x[0][3]))]

    print("== (a) P-9 reproduction (seam + pinning, K = 1.0)")
    ok_a = True
    seam_r = []
    for N in range(4, 10):
        wt = table[("pin", "seam", N, 0.5)]
        wc = table[("pin", "control", N, 0.5)]
        for key, w in ((f"{N}_tw", wt), (f"{N}_ctl", wc)):
            if abs(w - pins[key]) > 5e-3:
                ok_a = False
                print(f"  miss {key}: {w:.5f} vs pin {pins[key]:.5f}")
        seam_r.append(wt / wc)
    if alternates(seam_r, 0.03):
        ok_a = False
        print("  parity alternation appeared in r(N)")
    print(f"  r(N) = {[f'{x:.3f}' for x in seam_r]}  "
          f"{'ok' if ok_a else 'FAIL'}")
    out["clauses"]["a"] = ok_a
    out["seam_pin_ratio"] = seam_r

    print("== (b) ALT + bias half-step: f vs parity")
    wh = {N: table[("bias", "alt", N, NU / 2)] for N in range(4, 10)}
    print(f"  W_half: {[f'{N}:{wh[N]:.5f}' for N in wh]}")
    f_half = [wh[6], wh[7]]
    f_zero = [wh[4], wh[5], wh[8], wh[9]]
    gap = min(f_half) - max(f_zero)
    all_floor = all(w <= FLOOR for w in wh.values())
    ok_b = gap >= RES_W and not all_floor
    even_odd_gap = min(wh[4], wh[6], wh[8]) - max(wh[5], wh[7],
                                                 wh[9])
    print(f"  f-gap (min{{6,7}} - max{{4,5,8,9}}) = {gap:+.5f}  "
          f"even/odd gap = {even_odd_gap:+.5f}  "
          f"{'ok' if ok_b else 'FAIL'}")
    out["clauses"]["b"] = ok_b
    out["f_gap"] = gap
    out["even_odd_gap"] = even_odd_gap
    out["all_floor"] = all_floor

    print("== (c) seam + bias: no parity alternation")
    ws = [table[("bias", "seam", N, NU / 2)] for N in range(4, 10)]
    ok_c = not alternates(ws, RES_W)
    print(f"  W_half(seam): {[f'{x:.5f}' for x in ws]}  "
          f"{'ok' if ok_c else 'FAIL'}")
    out["clauses"]["c"] = ok_c

    print("== (d) the drive factor (ALT + pinning f-gap)")
    wp = {N: table[("pin", "alt", N, 0.5)] for N in range(4, 10)}
    gap_pin = min(wp[6], wp[7]) - max(wp[4], wp[5], wp[8], wp[9])
    ok_d = (abs(gap_pin) < RES_W) and (gap >= RES_W)
    print(f"  pinning f-gap = {gap_pin:+.5f} vs bias f-gap "
          f"{gap:+.5f}  {'ok' if ok_d else 'FAIL'}")
    out["clauses"]["d"] = ok_d
    out["gap_pin"] = gap_pin
    out["alt_pin_widths"] = wp

    print("== (e) positive control: integer step everywhere")
    ok_e = True
    for geom in ("control", "seam", "alt"):
        for N in range(4, 10):
            if table[("bias", geom, N, NU)] <= FLOOR:
                ok_e = False
                print(f"  integer step missing: {geom} N={N}")
    print(f"  {'ok' if ok_e else 'FAIL'}")
    out["clauses"]["e"] = ok_e

    json.dump(out, open(os.path.join(HERE, "p32_results.json"), "w"),
              indent=1)
    print("results -> p32_results.json")
    print("clauses:", out["clauses"])
    return 0 if all(out["clauses"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
