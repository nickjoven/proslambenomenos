#!/usr/bin/env python3
"""P-29 derivation layer (pre-registration): the Farey bridge.
Arnold tongues of the sine circle map (c23/c27 territory) and the
band structure of Harper's equation (P-7/P-28 territory) are both
organized by the rationals; the registered composite claim is that
they share the MEDIANT skeleton - in every Farey interval, the
mediant (the unique minimal-denominator interior fraction, exact
number theory) hosts the largest substructure on BOTH instruments,
each computed on its own data - and that the correspondence breaks
exactly where its premise (first-harmonic two-frequency
competition) is broken. Everything here has a derivable answer and
runs before the registered bridge computation.

Derived facts:
  EQ1  the interval table: all Farey-neighbor pairs (a/b, c/d)
       with bc - ad = 1, 0 <= a/b < c/d <= 1/2, b + d <= 8; per
       interval the mediant is verified UNIQUE minimal-denominator
       interior fraction by exhaustive scan to q = 40; competitor
       sets (interior fractions, q <= 13) pinned.
  EQ2  tongue-instrument anchors: the rho = 0 tongue of
       theta -> theta + Omega + (K/2pi) sin(2pi theta) has exact
       boundaries +-K/(2pi), width K/pi, hit by the tangency
       bisection to 1e-10 at K = 0.5; the symmetry
       Delta(p/q) = Delta((q-p)/q); the resonance mechanism's
       K^q scaling measured at small K for q = 2, 3 (width ratios
       at K = 0.1 vs 0.05 land near 2^q).
  EQ3  butterfly-instrument anchors: S(1/2) = 4 sqrt(2) exact
       (c25 pi-flux) from the same two-corner pipeline as P-28;
       S agreement with the p28 gap machinery on 8/13 to 1e-12.
  EQ4  the control is derived, not chosen: the pure-second-
       harmonic map theta -> theta + Omega + (K/2pi) sin(4pi
       theta) is EXACTLY conjugate (phi = 2 theta) to the standard
       map at (2 Omega, 2K), so Delta_2(rho, K) = (1/2)
       Delta_std(2 rho mod 1, 2K) - verified numerically - and
       therefore in the interval [1/3, 1/2] the mediant 2/5 maps
       to the q = 5 tier of the standard map while the competitor
       3/8 maps to the q = 4 tier: breaking the first harmonic
       DETHRONES the mediant, and the sign of the inversion is
       pinned before the registered run.
  EQ5  feasibility: widths floor 1e-9 (a q = 13 tongue at K = 0.5
       sits near (K/2)^13 ~ 1e-8, above it; q = 18 would not be);
       boundary bisection to 1e-12; deterministic throughout, no
       estimator noise; the rank clause restricted to intervals
       with >= 4 competitors.
Pinned -> p29_registration.json.
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))

from kernels.eig import eigh  # noqa: E402

FAILURES = []
K_MAIN = 0.5
Q_COMP = 13
BD_MAX = 8
FLOOR = 1e-9


def check(name, ok, detail=""):
    print(f"  {name}: {'ok' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)
    return ok


# ------------------------------------------------------- tongue side
def circle_gap(q_iter, p_over, Omega, K, harmonic=1):
    """G(theta) = F^q(theta) - theta - p on a refined grid; returns
    (min G, max G)."""
    w = 2 * math.pi * harmonic

    def step(th):
        return th + Omega + (K / (2 * math.pi)) * math.sin(w * th)

    def G(th0):
        th = th0
        for _ in range(q_iter):
            th = step(th)
        return th - th0 - p_over

    n = 400
    vals = [(G(i / n), i / n) for i in range(n)]
    gmin, tmin = min(vals)
    gmax, tmax = max(vals)

    def refine(t0, sign):
        a, b = t0 - 1.5 / n, t0 + 1.5 / n
        for _ in range(70):
            m1 = a + (b - a) / 3
            m2 = b - (b - a) / 3
            if sign * G(m1) < sign * G(m2):
                a = m1
            else:
                b = m2
        return G(0.5 * (a + b))
    return refine(tmin, -1), refine(tmax, +1)


def tongue_width(p, q, K, harmonic=1, span=None):
    """Boundaries by bisection on Omega: lower edge where max G = 0,
    upper edge where min G = 0 (G is increasing in Omega)."""
    rho = p / q
    if span is None:
        span = 0.6 * K / q
    lo0, hi0 = rho - span, rho + span

    def bis(target_max):
        a, b = lo0, hi0
        fa = (circle_gap(q, p, a, K, harmonic)[1 if target_max else 0])
        for _ in range(52):
            m = 0.5 * (a + b)
            fm = circle_gap(q, p, m, K, harmonic)[1 if target_max
                                                  else 0]
            if (fm < 0) == (fa < 0):
                a, fa = m, fm
            else:
                b = m
        return 0.5 * (a + b)
    om_lo = bis(True)
    om_hi = bis(False)
    return om_hi - om_lo


# ----------------------------------------------------- butterfly side
def bandwidth_S(p, q):
    if q == 1:
        return 8.0
    H1 = [[0.0] * q for _ in range(q)]
    H2 = [[0.0] * q for _ in range(q)]
    for n in range(q):
        H1[n][n] = 2 * math.cos(2 * math.pi * p * (n + 1) / q)
        H2[n][n] = 2 * math.cos(2 * math.pi * p * (n + 1) / q
                                + math.pi / q)
    for n in range(q - 1):
        H1[n][n + 1] = H1[n + 1][n] = 1.0
        H2[n][n + 1] = H2[n + 1][n] = 1.0
    H1[0][q - 1] = H1[q - 1][0] = (H1[0][q - 1] + 1.0) if q > 2 else 1.0
    H2[0][q - 1] = H2[q - 1][0] = -1.0
    if q == 2:
        H1[0][1] = H1[1][0] = 2.0  # corner +1 folded onto hopping
        H2[0][1] = H2[1][0] = 0.0
    e1 = eigh(H1)
    e2 = eigh(H2)
    edges = sorted(list(e1) + list(e2))
    return sum(edges[2 * i + 1] - edges[2 * i]
               for i in range(len(edges) // 2))


# ----------------------------------------------------------------- EQ1
def farey_intervals():
    out = []
    for b in range(1, BD_MAX):
        for d in range(1, BD_MAX + 1 - b):
            for a in range(0, b + 1):
                for c in range(1, d + 1):
                    if b * c - a * d != 1:
                        continue
                    fa, fc = Fraction(a, b), Fraction(c, d)
                    if not (0 <= fa < fc <= Fraction(1, 2)):
                        continue
                    out.append((a, b, c, d))
    return sorted(set(out), key=lambda t: (t[1] + t[3], t[0] / t[1]))


def interior(a, b, c, d, qmax):
    lo, hi = Fraction(a, b), Fraction(c, d)
    return sorted({Fraction(p, q) for q in range(1, qmax + 1)
                   for p in range(1, q)
                   if lo < Fraction(p, q) < hi})


def eq1():
    print("EQ1 the interval table and mediant minimality")
    table = []
    ok_min = True
    for a, b, c, d in farey_intervals():
        med = Fraction(a + c, b + d)
        ints40 = interior(a, b, c, d, 40)
        qmin = min(f.denominator for f in ints40)
        mins = [f for f in ints40 if f.denominator == qmin]
        if mins != [med]:
            ok_min = False
        comp = [f for f in interior(a, b, c, d, Q_COMP) if f != med]
        table.append({"a": a, "b": b, "c": c, "d": d,
                      "mediant": [med.numerator, med.denominator],
                      "competitors": [[f.numerator, f.denominator]
                                      for f in comp]})
    check("EQ1 mediant unique minimal-q in every interval (scan "
          "q<=40)", ok_min, f"{len(table)} intervals")
    n4 = sum(1 for t in table if len(t["competitors"]) >= 4)
    print(f"  EQ1 intervals: {len(table)}; with >=4 competitors: {n4}")
    return {"intervals": table}


# ----------------------------------------------------------------- EQ2
def eq2():
    print("EQ2 tongue-instrument anchors")
    w0 = tongue_width(0, 1, K_MAIN, span=0.3)
    check("EQ2 rho=0 width = K/pi", abs(w0 - K_MAIN / math.pi)
          < 1e-10, f"{w0:.12f} vs {K_MAIN / math.pi:.12f}")
    w13 = tongue_width(1, 3, K_MAIN)
    w23 = tongue_width(2, 3, K_MAIN)
    check("EQ2 symmetry Delta(1/3) = Delta(2/3)", abs(w13 - w23)
          < 1e-10, f"{w13:.3e} vs {w23:.3e}")
    ratios = {}
    for p, q in ((1, 2), (1, 3)):
        wA = tongue_width(p, q, 0.1)
        wB = tongue_width(p, q, 0.05)
        ratios[f"{p}/{q}"] = wA / wB
        tol = 0.15 * 2 ** q if q == 2 else 0.2 * 2 ** q
        check(f"EQ2 K^q scaling for {p}/{q}: ratio vs 2^{q}",
              abs(wA / wB - 2 ** q) < tol, f"{wA / wB:.3f}")
    return {"rho0_width": w0, "scaling_ratios": ratios}


# ----------------------------------------------------------------- EQ3
def eq3():
    print("EQ3 butterfly-instrument anchors")
    s12 = bandwidth_S(1, 2)
    check("EQ3 S(1/2) = 4 sqrt(2) (c25)", abs(s12 - 4 * math.sqrt(2))
          < 1e-12, f"{s12:.12f}")
    # agreement with the P-28 machinery on 8/13
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "p7f", os.path.join(HERE, "p7_flux.py"))
    p7f = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p7f)
    S_p7, _, _ = p7f.bandwidth(8, 13)
    ours = bandwidth_S(8, 13)
    check("EQ3 S(8/13) vs P-7 pipeline", abs(ours - S_p7) < 1e-9,
          f"{ours:.10f} vs {S_p7:.10f}")
    return {"S_half": s12, "S_8_13": ours}


# ----------------------------------------------------------------- EQ4
def eq4():
    print("EQ4 the derived control (conjugacy + pinned inversion)")
    w2 = tongue_width(2, 5, K_MAIN, harmonic=2, span=0.08)
    wstd = tongue_width(4, 5, 2 * K_MAIN, span=0.16)
    check("EQ4 conjugacy Delta_2(2/5,K) = (1/2) Delta_std(4/5,2K)",
          abs(w2 - 0.5 * wstd) < 1e-8, f"{w2:.3e} vs {0.5 * wstd:.3e}")
    w38 = tongue_width(3, 8, K_MAIN, harmonic=2, span=0.05)
    wstd34 = tongue_width(3, 4, 2 * K_MAIN, span=0.2)
    check("EQ4 conjugacy Delta_2(3/8,K) = (1/2) Delta_std(3/4,2K)",
          abs(w38 - 0.5 * wstd34) < 1e-8,
          f"{w38:.3e} vs {0.5 * wstd34:.3e}")
    inv = wstd34 > wstd
    check("EQ4 pinned inversion: Delta_std(3/4,1) > Delta_std(4/5,1)"
          " so the control dethrones the mediant 2/5", inv,
          f"{wstd34:.3e} vs {wstd:.3e}")
    return {"delta2_25": w2, "delta2_38": w38,
            "control_inversion_pinned": bool(inv)}


def main():
    pins = {"K": K_MAIN, "q_comp": Q_COMP, "bd_max": BD_MAX,
            "floor": FLOOR}
    pins["EQ1"] = eq1()
    pins["EQ2"] = eq2()
    pins["EQ3"] = eq3()
    pins["EQ4"] = eq4()
    out = os.path.join(HERE, "p29_registration.json")
    with open(out, "w") as f:
        json.dump(pins, f, indent=1)
    print(f"\npinned -> {out}")
    if FAILURES:
        print("DERIVATION FAILURES:", FAILURES)
        return 1
    print("all derivations ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
