#!/usr/bin/env python3
"""P-4 run 5: control ring, Guettler's recipe translated - low damping
(corner survives), slow bow (linear amplitudes, f_max reachable),
large N (corner exists). Looks for slip periods locked to INTEGER
multiples of the round trip (1, 2, 3 ...) and for +1 / x2 steps in
F_N. Parallel over runs (stdlib multiprocessing). Writes
p4_results_lowdamp.json."""

import json
import sys
from multiprocessing import Pool
sys.path.insert(0, "scripts/experiments")
from p4_twisted_inertial_ring import run  # noqa: E402

GRID = [(N, g, v, F)
        for N in (64, 128)
        for g in (0.01, 0.002)
        for v in (0.05, 0.1)
        for F in (0.3, 0.6, 0.9, 1.2, 1.5, 1.8)]


def job(args):
    N, g, v, F = args
    T = 40.0 * N          # 40 round trips (c = 1)
    r = run(N, False, F, v_bow=v, g=g, T=T, T_skip=10.0 * N, clamp=True)
    r.update({"N": N, "g": g, "v": v, "F_N": F})
    rat = r["ratio"]
    print(f"N={N:3d} g={g:.3f} v={v:.2f} F_N={F:.1f} slips={r['n_slips']:4d} "
          f"period/round={'%.2f' % rat if rat else '  - '} "
          f"{'[%.2f,%.2f]' % (r['gap_min']/r['T_round'], r['gap_max']/r['T_round']) if r.get('gap_min') else ''} "
          f"{r['regime']}", flush=True)
    return r


if __name__ == "__main__":
    with Pool(14) as p:
        rows = p.map(job, GRID, chunksize=1)
    with open("scripts/experiments/p4_results_lowdamp.json", "w") as f:
        json.dump(rows, f, indent=1)
