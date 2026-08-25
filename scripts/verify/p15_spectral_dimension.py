#!/usr/bin/env python3
"""Verification for the P-15 claim spectral-dimension-instrument, by
independent reimplementation - nothing read from the experiment's
results; every number recomputed here from scratch:

  1. line anchor by the OTHER route: d_s(20) on Z from the Bessel
     continued fraction, 2t(2 - 2 I1(2t)/I0(2t)) = 1.0064126931,
     against a fresh C_4096 eigen-sum (both to 1e-9);
  2. dense-circulant crossover: fresh eigen-sum gives d_s(0.2) =
     2.9520 (the short-walk three-dimensional peak of a 1D ring)
     and d_s(80) = 1.0004 (the true plateau);
  3. window rule: at t = 3/lambda_1 the cycle's d_s equals the
     two-mode closed form 12 e^-3/(1 + 2 e^-3) = 0.5433 within 1e-3
     - reporting it as a dimension would be wrong by half;
  4. chain drift at a grid the experiment never used (n = 749,
     150 modes): Delta d_s(300) / (2 Vbar 300) in [0.5, 2.0].

--mutant past-window            asserts d_s(3 t_mix) is still the
    dimension (= 1 within 0.1) and must FAIL: it is 0.54.
--mutant squared-generator generates the walk from L^2 (the
    biharmonic) instead of L - its line dimension is 1/2, not 1 -
    and must FAIL the line anchor.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "experiments"))

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"past-window", "squared-generator"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

VBAR = 3.416182e-08


def spectrum(n, S, mutant_squared=False):
    lap = [sum(2 * (1 - math.cos(2 * math.pi * k * s / n)) for s in S)
           for k in range(n)]
    # the wrong-operator mutant walks under L^2: line d_s becomes 1/2
    return [x * x for x in lap] if mutant_squared else lap


def ds(spec, t):
    mx = min(l * t for l in spec)
    num = sum(l * math.exp(-(l * t - mx)) for l in spec)
    den = sum(math.exp(-(l * t - mx)) for l in spec)
    return 2 * t * num / den


def bessel_ratio(x, depth=80):
    q = 0.0
    for k in range(depth, 1, -1):
        q = (x * x / 4) / (k + q)
    return (x / 2) / (1 + q)


def sturm_lowest(diag, off, kmax):
    n = len(diag)

    def count(lam):
        cnt = 0
        q = diag[0] - lam
        if q < 0:
            cnt += 1
        for i in range(1, n):
            e2 = off[i - 1] * off[i - 1]
            q = diag[i] - lam - (e2 / q if q != 0 else e2 / 1e-300)
            if q < 0:
                cnt += 1
        return cnt

    hi = max(dd + (abs(off[i - 1]) if i else 0) + (abs(off[i]) if i < n - 1 else 0)
             for i, dd in enumerate(diag))
    out = []
    for kk in range(1, kmax + 1):
        a_, b_ = 0.0, hi
        for _ in range(80):
            mid = 0.5 * (a_ + b_)
            if count(mid) >= kk:
                b_ = mid
            else:
                a_ = mid
        out.append(0.5 * (a_ + b_))
    return out


def main():
    n = 4096
    # 1. line anchor, both routes
    line = spectrum(n, (1,), mutant_squared=(MUTANT == "squared-generator"))
    d20 = ds(line, 20.0)
    r = bessel_ratio(40.0)
    d20_cf = 2 * 20.0 * (2 - 2 * r)
    if abs(d20 - 1.0064126931) > 1e-9 or abs(d20_cf - 1.0064126931) > 1e-9:
        print(f"FAIL: line anchor d_s(20) = {d20:.10f} (CF route {d20_cf:.10f}) "
              "!= 1.0064126931")
        return 1

    # 2. dense crossover
    dense = spectrum(n, tuple(range(1, 7)))
    peak = ds(dense, 0.2)
    plat = ds(dense, 80.0)
    if abs(peak - 2.9520) > 2e-4 or abs(plat - 1.0004) > 2e-4:
        print(f"FAIL: crossover d_s(0.2) = {peak:.4f} (want 2.9520), "
              f"d_s(80) = {plat:.4f} (want 1.0004)")
        return 1

    # 3. window rule (always on the true Laplacian line spectrum)
    d_past = ds(spectrum(n, (1,)), 3.0 / spectrum(n, (1,))[1])
    two_mode = 12 * math.exp(-3) / (1 + 2 * math.exp(-3))
    if MUTANT == "past-window":
        if abs(d_past - 1.0) > 0.1:
            print(f"FAIL: d_s(3 t_mix) = {d_past:.4f} is not the dimension - "
                  "past the window the walk has mixed and the reading collapses")
            return 1
    elif abs(d_past - two_mode) > 1e-3:
        print(f"FAIL: window decay {d_past:.6f} vs two-mode closed form {two_mode:.6f}")
        return 1

    # 4. chain drift on a fresh grid
    from p14_spectral_shadow import chain  # guarded module
    eig = {}
    for prof in ("ramp", "zramp"):
        _, m, J = chain(prof, 749)
        diag = [(J[i] + J[i + 1]) / m[i] for i in range(749)]
        off = [-J[i + 1] / math.sqrt(m[i] * m[i + 1]) for i in range(748)]
        eig[prof] = sturm_lowest(diag, off, 150)
    drift = (ds(eig["ramp"], 300.0) - ds(eig["zramp"], 300.0)) / (2 * VBAR * 300.0)
    if not (0.5 <= drift <= 2.0):
        print(f"FAIL: chain trace drift ratio {drift:.3f} outside [0.5, 2.0] at n = 749")
        return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print(f"PASS: line anchor by two routes (1.0064126931); dense peak {peak:.4f} "
          f"-> plateau {plat:.4f}; window decay on the two-mode curve; chain "
          f"trace drift ratio {drift:.3f} at a fresh grid - the instrument "
          "reads the metric, then the impedance, in that order")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
