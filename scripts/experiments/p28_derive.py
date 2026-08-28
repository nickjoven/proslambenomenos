#!/usr/bin/env python3
"""P-28 derivation layer (pre-registration): the gap integers of the
golden flux ladder. Every gap of Harper at rational flux p/q carries
a unique pair of integers (s, t) with r = s q + t p and |t| <= q/2
(the gap-labeling Diophantine equation; Satija's review writes the
irrational form N = s + t phi, with t the Chern number of Hall
conductivity via Streda). P-7 computed the ladder's spectra and
deliberately did NOT claim Chern content; A-12 converts that scope
into an earned claim. Everything here is exact integer/rational
arithmetic or an instrument anchor, and runs before the registered
spectral computation.

Derived facts:
  EQ1  existence and uniqueness of the label: for every ladder rung
       (p, q) = (F_{n-1}, F_n) and every gap index r in 1..q-1, a
       unique t with |t| < q/2 for odd q; for even q the single
       ambiguous case is r = q/2 (t = +-q/2 both solve) - exactly
       the central gap that P-7's parity rule shows is CLOSED. The
       number theory and the spectrum agree on which label cannot
       be assigned.
  EQ2  the Fibonacci congruence F_{n-1} F_j = (-1)^{j+1} F_{n-j}
       (mod F_n), verified exhaustively along the ladder, and its
       corollary THE MAP: the gap at r = F_j carries |t| = F_{n-j}
       (mirror r = q - F_j carries the same |t|, opposite sign).
       Corollaries pinned: t(r = F_{n-1}) = +1, t(r = F_{n-2}) =
       -1 (the principal pair), and t(r = 1) = +-F_{n-2} - the
       edge gap carries the LARGE Fibonacci Chern number.
  EQ3  instrument anchors: kernels.eig.eigh (first experiment-side
       consumer) agrees with the P-7 Jacobi route on the q = 13
       Bloch matrices at both Chambers corners to 1e-9; the q = 2
       central gap closes to 1e-13 (c25 Dirac interop).
  EQ4  the Streda slope is exact by unimodularity: consecutive
       rungs satisfy |p q' - p' q| = 1 (Farey neighbors,
       exhaustively), and for a gap with labels (s, t) present at
       both rungs, (r'/q' - r/q)/(p'/q' - p/q) = t exactly in
       rational arithmetic. What remains for the experiment is the
       SPECTRAL content: the gap's energy windows overlap and
       band-counting at the overlap midpoint returns r'
       independently.
  EQ5  feasibility (the P-22a pass): the width floor is 1e-9;
       hierarchy clauses use tiers |t| in {1, 2, 3}; the edge-gap
       clause is conditioned on resolution (|t| = F_{n-2} grows
       along the ladder, so its gap must eventually drop below any
       floor - the rung where it does is a measured output, with
       resolution required only through q = 13).
Pinned -> p28_registration.json.
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))

FAILURES = []

FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
# ladder rungs (p, q) = (F_{n-1}, F_n), n = 3..12 (1-indexed FIB)
LADDER = [(FIB[n - 2], FIB[n - 1], n) for n in range(3, 13)]
FLOOR = 1e-9


def check(name, ok, detail=""):
    print(f"  {name}: {'ok' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)
    return ok


def label(r, p, q):
    """The unique (s, t), r = s q + t p, |t| <= q/2; returns
    (s, t, ambiguous)."""
    pinv = pow(p, -1, q)
    t = (r * pinv) % q
    if t > q / 2:
        t -= q
    amb = (2 * abs(t) == q)
    s = (r - t * p) // q
    assert s * q + t * p == r
    return s, t, amb


# ----------------------------------------------------------------- EQ1
def eq1():
    print("EQ1 label existence/uniqueness along the ladder")
    for p, q, n in LADDER:
        ambs = []
        for r in range(1, q):
            s, t, amb = label(r, p, q)
            if amb:
                ambs.append(r)
        if q % 2 == 1:
            check(f"EQ1 q={q} odd: no ambiguous label", ambs == [],
                  repr(ambs))
        else:
            check(f"EQ1 q={q} even: ambiguity exactly at central "
                  f"r=q/2", ambs == [q // 2], repr(ambs))
    return {}


# ----------------------------------------------------------------- EQ2
def eq2():
    print("EQ2 the Fibonacci congruence and THE MAP")
    ok_all = True
    for p, q, n in LADDER:
        for j in range(2, n):
            lhs = (FIB[n - 2] * FIB[j - 1]) % q
            rhs = ((-1) ** (j + 1) * FIB[n - j - 1]) % q
            if lhs != rhs:
                ok_all = False
    check("EQ2 F_{n-1} F_j = (-1)^{j+1} F_{n-j} (mod F_n), all rungs",
          ok_all)
    # the map: r = F_j  ->  |t| = F_{n-j}; mirror same |t|, flip sign
    # (q = 2 excluded: its only gap is the ambiguous self-mirror
    # central, which the spectrum closes - the map is vacuous there)
    map_ok = True
    pins = {}
    for p, q, n in LADDER:
        if q == 2:
            continue
        rows = []
        for j in range(2, n):
            r = FIB[j - 1]
            if r >= q:
                continue
            s, t, _ = label(r, p, q)
            sm, tm, _ = label(q - r, p, q)
            want = FIB[n - j - 1]
            if abs(t) != want or tm != -t:
                map_ok = False
            rows.append({"j": j, "r": r, "t": t, "expected_abs":
                         want})
        pins[str(q)] = rows
    check("EQ2 map r=F_j -> |t|=F_{n-j} with sign-flipped mirrors",
          map_ok)
    # corollaries
    cor_ok = True
    for p, q, n in LADDER:
        if q < 3:
            continue
        _, t1, _ = label(p, p, q)
        _, t2, _ = label(q - p, p, q)
        _, te, _ = label(1, p, q)
        if t1 != 1 or t2 != -1 or abs(te) != FIB[n - 3]:
            cor_ok = False
    check("EQ2 corollaries: t(r=p)=+1, t(r=q-p)=-1, |t(r=1)|=F_{n-2}",
          cor_ok)
    return {"map": pins}


# ----------------------------------------------------------------- EQ3
def eq3():
    print("EQ3 instrument anchors (kernels.eigh vs P-7 Jacobi; c25)")
    from kernels.eig import eigh
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "p7f", os.path.join(HERE, "p7_flux.py"))
    p7f = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p7f)
    worst = 0.0
    for corner, k2 in ((+1.0, 0.0), (-1.0, math.pi / 13)):
        H = p7f.bloch(8, 13, corner, k2)
        ej, _ = p7f.jacobi_eigs([row[:] for row in H])
        ek = sorted(eigh([row[:] for row in H]))
        worst = max(worst, max(abs(a - b)
                               for a, b in zip(sorted(ej), ek)))
    check("EQ3 kernels.eigh vs Jacobi on q=13 Bloch corners", worst
          < 1e-9, f"worst {worst:.2e}")
    # q=2 central closure (c25 Dirac)
    e1 = sorted(eigh(p7f.bloch(1, 2, +1.0, 0.0)))
    e2 = sorted(eigh(p7f.bloch(1, 2, -1.0, math.pi / 2)))
    edges = sorted(e1 + e2)
    central = edges[2] - edges[1]
    check("EQ3 q=2 central gap closes (c25)", abs(central) < 1e-13,
          f"width {central:.2e}")
    return {"eigh_vs_jacobi_worst": worst, "q2_central": central}


# ----------------------------------------------------------------- EQ4
def eq4():
    print("EQ4 unimodularity and the exact Streda slope")
    uni_ok = True
    for (p1, q1, _), (p2, q2, _) in zip(LADDER, LADDER[1:]):
        if abs(p1 * q2 - p2 * q1) != 1:
            uni_ok = False
    check("EQ4 consecutive rungs are Farey neighbors (unimodular)",
          uni_ok)
    slope_ok = True
    for (p1, q1, _), (p2, q2, _) in zip(LADDER[2:], LADDER[3:]):
        for t in (1, -1, 2, -2, 3):
            for s in range(-3, 4):
                r1 = s * q1 + t * p1
                r2 = s * q2 + t * p2
                if not (0 < r1 < q1 and 0 < r2 < q2):
                    continue
                slope = (Fraction(r2, q2) - Fraction(r1, q1)) / \
                    (Fraction(p2, q2) - Fraction(p1, q1))
                if slope != t:
                    slope_ok = False
    check("EQ4 (dN/dalpha) = t exactly for shared labels (rationals)",
          slope_ok)
    return {}


# ----------------------------------------------------------------- EQ5
def eq5():
    print("EQ5 feasibility pins")
    print(f"  width floor {FLOOR}; hierarchy tiers |t| in {{1,2,3}}; "
          f"edge-gap resolution required through q = 13 "
          f"(|t| = 5), reported beyond")
    return {"floor": FLOOR, "hierarchy_tiers": [1, 2, 3],
            "edge_gap_required_through_q": 13}


def main():
    pins = {"ladder": [(p, q, n) for p, q, n in LADDER]}
    pins["EQ1"] = eq1()
    pins["EQ2"] = eq2()
    pins["EQ3"] = eq3()
    pins["EQ4"] = eq4()
    pins["EQ5"] = eq5()
    out = os.path.join(HERE, "p28_registration.json")
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
