#!/usr/bin/env python3
"""P-2 resolution experiment: the completeness of the critical
staircase, measured with the P-29 tongue instrument. Runs AFTER the
P-2a amendment commit; cells and bands as pinned there.

Results -> p2_results.json.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import p29_derive as T
from kernels.pmap import pmap

QMAX = 40
KS = (0.5, 1.0)


def fracs(qmax):
    out = []
    for q in range(2, qmax + 1):
        for p in range(1, q // 2 + 1):
            if math.gcd(p, q) == 1 and p / q <= 0.5:
                out.append((p, q))
    return out


def cell(job):
    p, q, K = job
    w = T.tongue_width(p, q, K)
    return {"p": p, "q": q, "K": K, "w": w}


def main():
    out = {"clauses": {}}
    jobs = [(p, q, K) for K in KS for (p, q) in fracs(QMAX)]
    rows = pmap(cell, jobs, processes=16)
    table = {}
    for r in rows:
        table.setdefault(r["K"], {})[(r["p"], r["q"])] = r["w"]

    # symmetry spot pair (rho <-> 1 - rho), instrument sanity
    w13 = table[1.0][(1, 3)]
    w13m = T.tongue_width(2, 3, 1.0)
    sym = abs(w13 - w13m)
    print(f"symmetry spot: |D(1/3) - D(2/3)| = {sym:.2e} at K = 1")
    out["symmetry_spot"] = sym

    # rho = 0 tongue width (exact K/pi) counts once; interior
    # tongues in (0, 1/2) count twice by symmetry; rho = 1/2 once
    def locked_total(K, qmax):
        tot = K / math.pi  # the rho = 0 tongue (exact, P-29 EQ2)
        for (p, q), w in table[K].items():
            if q > qmax:
                continue
            tot += w if (p / q == 0.5) else 2 * w
        return tot

    print("== (a) disjoint totals")
    ok_a = True
    totals = {}
    for K in KS:
        t = locked_total(K, QMAX)
        totals[str(K)] = t
        neg = sum(1 for w in table[K].values() if w < 0)
        print(f"  K={K}: locked total {t:.5f} (negatives: {neg})")
        if t > 1 + 1e-9 or neg:
            ok_a = False
    out["clauses"]["a"] = ok_a
    out["totals"] = totals

    print("== (b) K = 0.5 convergence and positive complement")
    c32 = 1 - locked_total(0.5, 32)
    c40 = 1 - locked_total(0.5, 40)
    ok_b = (c32 - c40 < 0.005) and (0.15 <= c40 <= 0.60)
    print(f"  complement: q<=32 {c32:.5f}, q<=40 {c40:.5f}  "
          f"{'ok' if ok_b else 'FAIL'}")
    out["clauses"]["b"] = ok_b
    out["c_sub"] = {"32": c32, "40": c40}

    print("== (c) K = 1.0 completing staircase")
    comp = {}
    prev = None
    ok_c = True
    for Q in (8, 16, 24, 32, 40):
        c = 1 - locked_total(1.0, Q)
        comp[str(Q)] = c
        if prev is not None and c >= prev:
            ok_c = False
        prev = c
        print(f"  complement at q<={Q}: {c:.5f}")
    if comp["40"] >= 0.12:
        ok_c = False
    print(f"  {'ok' if ok_c else 'FAIL'}")
    out["clauses"]["c"] = ok_c
    out["c_crit"] = comp

    print("== (d) the dimension of the unlocked set at K = 1")
    widths = []
    for (p, q), w in table[1.0].items():
        if w > 0:
            widths.append((w, p, q))
    widths.append((1.0 / math.pi, 0, 1))  # rho = 0 (K/pi at K=1)
    pts = []
    for r in [3e-2, 1e-2, 3e-3, 1e-3, 3e-4]:
        mu = 1.0
        for (w, p, q) in widths:
            if w >= r:
                mu -= w if (p == 0 or p / q == 0.5) else 2 * w
        if mu > 0:
            pts.append((math.log(r), math.log(mu)))
        print(f"  mu(r={r:.0e}) = {mu:.5f}")
    n = len(pts)
    sx = sum(x for x, _ in pts) / n
    sy = sum(y for _, y in pts) / n
    slope = sum((x - sx) * (y - sy) for x, y in pts) / \
        sum((x - sx) ** 2 for x, _ in pts)
    D = 1 - slope
    ok_d = 0.84 <= D <= 0.90
    print(f"  slope 1-D = {slope:.4f}  ->  D = {D:.4f}  "
          f"(JBB 0.870)  {'ok' if ok_d else 'FAIL'}")
    out["clauses"]["d"] = ok_d
    out["D"] = D

    # 8a completeness null: measure carried by q > 40 tongues in
    # the window, bounded by the measured tail constant
    cmax = max(w * q ** 3 for (w, p, q) in widths if q >= 20)
    tail = 2 * cmax * sum(T_phi(q) / q ** 3
                          for q in range(QMAX + 1, 400))
    print(f"  (8a) missed-measure bound from q > {QMAX}: "
          f"{tail:.2e} (c_max = {cmax:.3f})")
    out["tail_bound"] = tail

    json.dump(out, open(os.path.join(HERE, "p2_results.json"), "w"),
              indent=1)
    print("results -> p2_results.json")
    print("clauses:", out["clauses"])
    return 0 if all(out["clauses"].values()) else 1


def T_phi(q):
    r = q
    n = q
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            r -= r // p
        p += 1
    if n > 1:
        r -= r // n
    return r


if __name__ == "__main__":
    sys.exit(main())
