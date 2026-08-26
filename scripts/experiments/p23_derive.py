#!/usr/bin/env python3
"""P-23 derivation layer (pre-registration): the mod-pi protection
clause of P-22, re-registered with the equilibrium DERIVED instead
of guessed after R-17's firing. For the two-photon locked phase at
delta = 0 the stationary density is the von Mises form
p(theta) ~ exp(kappa cos 2 theta), kappa = eps/(2D), so

    <cos 2 theta> = I1(kappa)/I0(kappa)     (exact)
    <cos theta>   = 0                        (exact, by the
                    theta -> theta + pi symmetry of p)

EQ1  the Bessel ratio two independent ways: the continued fraction
     (P-15's instrument, with its loop stopping at k = 2 - the
     R-11-era lesson) against direct quadrature of the von Mises
     average; agreement to 1e-12 on the registered kappa ladder.
EQ2  <cos theta> = 0 exactly: the quadrature of cos theta over the
     full 2 pi stationary density vanishes to 1e-14 (symmetry).
EQ3  hop budgets for the fresh-seed runs: per-cell durations chosen
     so every ensemble member expects > 50 committed hops (rates
     from the P-22 MFPT pins), so both wells are genuinely visited.
Pinned -> p23_registration.json: kappa ladder, I1/I0 values, cell
durations, ensemble size M = 8, fresh seeds, and the registered
test form: ensemble mean within 4 SEM of the pin with SEM < 0.01,
and |<cos theta>| < 4 SEM_1.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

OUT, FAILED = [], []


def eq(n, ok, statement, detail):
    line = f"EQ {n} {'PASS' if ok else 'FAIL'}  {statement}  | {detail}"
    OUT.append(line)
    print(line)
    if not ok:
        FAILED.append(n)


def bessel_ratio(x, depth=60):
    """I1(x)/I0(x) by continued fraction (P-15 instrument)."""
    r = 0.0
    for k in range(depth, 1, -1):
        r = x / (2 * k + x * r) if (2 * k + x * r) != 0 else 0.0
    return x / (2 + x * r)


def vm_avg(fun, kappa, n=20000):
    h = 2 * math.pi / n
    num = den = 0.0
    for i in range(n):
        t = -math.pi + (i + 0.5) * h
        w = math.exp(kappa * (math.cos(2 * t) - 1.0))
        num += fun(t) * w
        den += w
    return num / den


CELLS = [(1.0, 0.2, 20000.0), (1.0, 0.25, 10000.0), (1.0, 0.3, 8000.0)]
HOP_PIN = {"0.2": 0.00188, "0.25": 0.00496, "0.3": 0.00940}

ok1, rows1, pins = True, [], {}
for (epsv, D, T) in CELLS:
    kappa = epsv / (2 * D)
    cf = bessel_ratio(kappa)
    qd = vm_avg(lambda t: math.cos(2 * t), kappa)
    ok1 = ok1 and abs(cf - qd) < 1e-12
    pins[f"{D}"] = cf
    rows1.append(f"kappa={kappa:.4g}: CF {cf:.10f} vs quad {qd:.10f}")
eq(1, ok1, "I1/I0 continued fraction = von Mises quadrature on the ladder",
   "; ".join(rows1[:2]))

worst2 = max(abs(vm_avg(math.cos, epsv / (2 * D))) for (epsv, D, _) in CELLS)
eq(2, worst2 < 1e-14, "<cos theta> = 0 by theta -> theta + pi symmetry",
   f"worst quadrature residual {worst2:.1e}")

budgets = {str(D): 2 * HOP_PIN[str(D)] * T for (e_, D, T) in CELLS}
eq(3, all(b > 50 for b in budgets.values()),
   "every ensemble member expects > 50 committed hops",
   "; ".join(f"D={k}: N~{v:.0f}" for k, v in budgets.items()))

pin = {"cells": [list(c) for c in CELLS], "cos2_pin": pins,
       "M": 8, "dt": 0.002, "seed0": 424271,
       "test": "ensemble mean within 4 SEM of pin, SEM < 0.01; |cos1 mean| < 4 SEM1",
       "hop_min_per_member": 50}
(HERE / "p23_registration.json").write_text(json.dumps(pin, indent=1) + "\n")
(HERE / "p23_derive_out.txt").write_text("\n".join(OUT) + "\n")
print(f"\npinned: {pins}")
sys.exit(1 if FAILED else 0)
