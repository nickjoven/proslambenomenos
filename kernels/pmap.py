#!/usr/bin/env python3
"""Parallel-map kernel: a minimal multiprocessing map over independent
cells with deterministic per-cell seeds (the second performance
minimum). Chunked stdlib multiprocessing; falls back to serial when
processes are unavailable or unwanted, with identical results either
way because every cell carries its own seed.

Admission (two-artifact rule for the SEEDING pattern; the pool itself
is new, admitted as the performance route to the same ensembles):
  cell_seed       scripts/experiments/p10_mm_dimension.py:221-226
                  (random.Random(f"{SEED}:{d}:{N}:sample:{run}")),
                  scripts/experiments/p23_protect.py:47 and
                  scripts/experiments/p22_locking.py:89 (arithmetic
                  per-cell seed offsets) - every registered ensemble
                  in the repo already derives one independent seed
                  per cell so cells are order-free; pmap only
                  exploits what that discipline already earned.

Selftest anchors:
  - identical results serial vs parallel on a toy ensemble of seeded
    random walks (bitwise equality of every cell's output).
  - determinism under chunking: chunksize 1 and 3 agree.
  - the parallel path reports its wall-time beside the serial path.

stdlib only.
"""
import math
import os
import random


def cell_seed(seed0, *key):
    """Deterministic per-cell seed in the repo's registered style:
    the string f"{seed0}:k1:k2:..." fed to random.Random
    (p10_mm_dimension.py:221)."""
    return ":".join(str(k) for k in (seed0,) + key)


def pmap(fn, cells, processes=None, chunksize=1):
    """Map fn over the cells, order-preserving. Uses a
    multiprocessing.Pool with the given chunksize when more than one
    process is requested and available; any failure to parallelize
    falls back to the serial map, which is result-identical because
    each cell is independent and self-seeded. fn must be a module-
    level callable (picklable)."""
    cells = list(cells)
    if processes is None:
        processes = os.cpu_count() or 1
    if processes <= 1 or len(cells) <= 1:
        return [fn(c) for c in cells]
    try:
        import multiprocessing as mp
        with mp.Pool(processes) as pool:
            return pool.map(fn, cells, chunksize)
    except Exception:
        return [fn(c) for c in cells]


# ---------------------------------------------------------------- selftest
def _toy_cell(cell):
    """One toy ensemble cell: a seeded overdamped walk in a cosine
    well; returns (final phase, <cos theta>) - deterministic in the
    cell's own seed."""
    seed, D, T, dt = cell
    rng = random.Random(seed)
    g = rng.gauss
    amp = math.sqrt(2 * D * dt)
    th = 0.0
    acc = 0.0
    n = int(T / dt)
    for _ in range(n):
        th += -math.sin(th) * dt + amp * g(0.0, 1.0)
        acc += math.cos(th)
    return th, acc / n


def _selftest():
    import time
    ok = True
    cells = [(cell_seed(20260827, "toy", m), 0.4, 400.0, 0.002)
             for m in range(8)]

    t0 = time.perf_counter()
    serial = [_toy_cell(c) for c in cells]
    t_ser = time.perf_counter() - t0
    t0 = time.perf_counter()
    par = pmap(_toy_cell, cells)
    t_par = time.perf_counter() - t0
    good = par == serial
    ok &= good
    print(f"serial vs parallel on 8 cells: bitwise identical: {good} "
          f"({t_ser:.2f} s vs {t_par:.2f} s, x{t_ser / max(t_par, 1e-9):.1f}, "
          f"{os.cpu_count()} cpus)")

    chunked = pmap(_toy_cell, cells, chunksize=3)
    good = chunked == serial
    ok &= good
    print(f"chunksize 3: bitwise identical: {good}")

    forced_serial = pmap(_toy_cell, cells, processes=1)
    good = forced_serial == serial
    ok &= good
    print(f"forced serial path: bitwise identical: {good}")

    print("pmap selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
