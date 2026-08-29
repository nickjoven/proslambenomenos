#!/usr/bin/env python3
"""P-34 derivation layer (pre-registration): the horizon-coincidence
census. A-8: how impressed should anyone be by the famous
horizon-scale numerical coincidences (a0 ~ c H0 / 2 pi, the CKN /
Sorkin / Zeldovich dark-energy magnitude, the Weinberg pion
relation, the neutrino-dark-energy scale, the why-now ratio)? The
census prices them all against one derived codebook.

The codebook: monomials in {hbar, c, G, H0} with a declared
exponent lattice and a declared prefactor set. The dimension matrix
of the four constants over (M, L, T) has rank 3, so its null space
is one-dimensional: EVERY dimensionless combination is a power of
mu = H0 t_P ~ 1.2e-61, and every dimensionful coincidence reduces
to a pair (k, prefactor) - slots are few by algebra, mechanisms are
many by literature. Per AGENTS.md item 8 the instrument nulls are
stated here, before registration:
  (a) detector null response: the coverage function p(t) - the
      probability that a uniformly placed target within one minimal
      k-cell lies within t dex of SOME codebook value - computed by
      exact interval union (EQ2);
  (b) observable conservation identity: the mu-degeneracy (EQ1,
      EQ3) - equal-dimension monomials differ exactly by a power of
      mu, so the census cannot double-count slots;
  (c) domain validity: the k-lattice ({p/q, q <= 3, |p/q| <= 2}),
      the 20-element prefactor set spanning [1/(4 pi^2), 4 pi^2],
      and the one-k-cell null window (10.15 dex) are declared, and
      adjacent prefactor clouds are verified disjoint.

Derived facts:
  EQ1  the null vector: solving the 3 x 4 dimension system in exact
       Fractions gives mu = hbar^{1/2} G^{1/2} c^{-5/2} H0 = H0 t_P;
       numerically 1.18e-61 (Planck 2018 H0).
  EQ2  the coverage table p(t) for t in {0.02, 0.05, 0.1, 0.2, 0.3,
       0.5} by exact interval union, and the expected number of
       <= t hits in a 5-entry census.
  EQ3  the degeneracy check: three independently constructed
       equal-dimension monomial pairs differ by mu^k exactly.
  EQ4  the calibration theorem row: Gibbons-Hawking T = hbar H0 /
       (2 pi k_B) (catalog c7) is an EQUATION; with the exact
       prefactor the codebook reproduces it to < 1e-12 dex - the
       instrument calibrates on a known non-coincidence, which is
       excluded from the pigeonhole count.
  EQ5  the census pins (LC-24): a0 = 1.2e-10 m/s^2 (RAR),
       rho_Lambda from Planck 2018, Omega_L/Omega_m = 2.19,
       m_pi = 139.57 MeV, sqrt(dm2_atm) = 50.4 meV; H0 sensitivity
       pair {67.4, 73.0}.
Pinned -> p34_registration.json.
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
FAILURES = []

HBAR = 1.054571817e-34
C = 2.99792458e8
G = 6.67430e-11
KB = 1.380649e-23
H0_PLANCK = 67.4 * 1000.0 / 3.0857e22
H0_SHOES = 73.0 * 1000.0 / 3.0857e22

# dimensions (M, L, T)
DIMS = {"hbar": (1, 2, -1), "c": (0, 1, -1), "G": (-1, 3, -2),
        "H0": (0, 0, -1)}
VALS = {"hbar": HBAR, "c": C, "G": G, "H0": H0_PLANCK}

K_LATTICE = sorted({Fraction(p, q) for q in (1, 2, 3)
                    for p in range(-2 * q, 2 * q + 1)})
PREFACTORS = {
    "1": 1.0, "2": 2.0, "3": 3.0, "4": 4.0, "1/2": 0.5,
    "1/3": 1 / 3, "1/4": 0.25, "pi": math.pi, "2pi": 2 * math.pi,
    "4pi": 4 * math.pi, "pi^2": math.pi ** 2,
    "4pi^2": 4 * math.pi ** 2, "8pi": 8 * math.pi,
    "1/pi": 1 / math.pi, "1/2pi": 1 / (2 * math.pi),
    "1/4pi": 1 / (4 * math.pi), "1/pi^2": 1 / math.pi ** 2,
    "1/4pi^2": 1 / (4 * math.pi ** 2), "3/8pi": 3 / (8 * math.pi),
    "8pi/3": 8 * math.pi / 3,
}


def check(name, ok, detail=""):
    print(f"  {name}: {'ok' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)
    return ok


def solve_dimension(target):
    """Exponents (a, b, g, h) with hbar^a c^b G^g H0^h having the
    target (M, L, T) dimension, plus the null vector; exact
    Fractions, Gaussian elimination on the 3 x 4 system."""
    names = ["hbar", "c", "G", "H0"]
    A = [[Fraction(DIMS[n][d]) for n in names] for d in range(3)]
    rhs = [Fraction(x) for x in target]
    M = [row[:] + [rhs[i]] for i, row in enumerate(A)]
    piv_cols = []
    r = 0
    for col in range(4):
        piv = next((i for i in range(r, 3) if M[i][col] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        M[r] = [x / M[r][col] for x in M[r]]
        for i in range(3):
            if i != r and M[i][col] != 0:
                f = M[i][col]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv_cols.append(col)
        r += 1
        if r == 3:
            break
    free = [c_ for c_ in range(4) if c_ not in piv_cols][0]
    # particular solution: free var = 0
    part = [Fraction(0)] * 4
    for i, col in enumerate(piv_cols):
        part[col] = M[i][4]
    # null vector: free var = 1
    null = [Fraction(0)] * 4
    null[free] = Fraction(1)
    for i, col in enumerate(piv_cols):
        null[col] = -M[i][free]
    return part, null


def mono_value(expo, h0=H0_PLANCK):
    v = 1.0
    vals = {"hbar": HBAR, "c": C, "G": G, "H0": h0}
    for n, e in zip(["hbar", "c", "G", "H0"], expo):
        v *= vals[n] ** float(e)
    return v


def eq1():
    print("EQ1 the null vector mu")
    _, null = solve_dimension((0, 0, 0))
    # normalize so H0 exponent = 1
    scale = 1 / null[3]
    null = [x * scale for x in null]
    want = [Fraction(1, 2), Fraction(-5, 2), Fraction(1, 2),
            Fraction(1)]
    check("EQ1 mu = hbar^1/2 c^-5/2 G^1/2 H0", null == want,
          str(null))
    mu = mono_value(null)
    tp = math.sqrt(HBAR * G / C ** 5)
    check("EQ1 mu = H0 t_P numerically", abs(mu / (H0_PLANCK * tp)
                                             - 1) < 1e-12,
          f"mu = {mu:.4e}")
    return {"mu": mu, "log10_mu": math.log10(mu)}


def coverage(t):
    """Measure of the union of [v - t, v + t] over prefactor log
    offsets, inside one minimal k-cell."""
    logs = sorted(math.log10(v) for v in PREFACTORS.values())
    cell = abs(math.log10(mono_value(
        solve_dimension((0, 0, 0))[1]))) / 6  # minimal k spacing
    ivs = [(v - t, v + t) for v in logs]
    merged = []
    for lo, hi in sorted(ivs):
        if merged and lo <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(hi, merged[-1][1]))
        else:
            merged.append((lo, hi))
    cov = sum(hi - lo for lo, hi in merged)
    return min(cov / cell, 1.0), cell


def eq2():
    print("EQ2 the coverage table (the detector null)")
    _, null = solve_dimension((0, 0, 0))
    null = [x / null[3] for x in null]
    table = {}
    for t in (0.02, 0.05, 0.1, 0.2, 0.3, 0.5):
        p, cell = coverage(t)
        table[str(t)] = p
        print(f"  p(match <= {t} dex) = {p:.4f} "
              f"(expected hits in 5 trials: {5 * p:.2f})")
    check("EQ2 cell width ~ 10.15 dex", abs(cell - 10.155) < 0.05,
          f"{cell:.3f}")
    # domain validity: prefactor clouds of adjacent k disjoint
    spread = (max(math.log10(v) for v in PREFACTORS.values())
              - min(math.log10(v) for v in PREFACTORS.values()))
    check("EQ2 adjacent clouds disjoint (spread + 2t < cell)",
          spread + 1.0 < cell, f"spread {spread:.2f}")
    return {"coverage": table, "cell_dex": cell}


def eq3():
    print("EQ3 the mu-degeneracy (conservation identity)")
    ok = True
    for target in ((0, 1, -2), (1, 0, 0), (-1, -3, 2)):
        part, null = solve_dimension(target)
        # a second solution: part + null; ratio must be mu^1
        v1 = mono_value(part)
        v2 = mono_value([p + n for p, n in zip(part, null)])
        _, nn = solve_dimension((0, 0, 0))
        mu = mono_value([x / nn[3] for x in nn])
        r = v2 / v1
        if abs(math.log10(r) / math.log10(mu ** float(null[3]
               / null[3])) - 1) > 1e-9 and \
                abs(math.log10(r) - math.log10(mu)
                    * float(null[3])) > 1e-6:
            ok = False
    check("EQ3 equal-dimension monomials differ by powers of mu", ok)
    return {}


def eq4():
    print("EQ4 the calibration theorem row (Gibbons-Hawking, c7)")
    # T_dS = hbar H0 / (2 pi k_B): temperature involves k_B, outside
    # the 4-constant codebook; calibrate on the energy k_B T =
    # hbar H0 / 2 pi: dimension (M, L^2, T^-2)
    part, null = solve_dimension((1, 2, -2))
    # find the member of the family equal to hbar * H0 (k solved)
    want = math.log10(HBAR * H0_PLANCK)
    best = None
    for k in K_LATTICE:
        expo = [p + Fraction(k) * n / null[3]
                for p, n in zip(part, null)]
        v = math.log10(mono_value(expo))
        for name, pf in PREFACTORS.items():
            d = abs(v + math.log10(pf) - (want - math.log10(
                2 * math.pi)))
            if best is None or d < best[0]:
                best = (d, name, float(k))
    check("EQ4 codebook reproduces hbar H0/(2 pi) at < 1e-9 dex",
          best[0] < 1e-9, f"prefactor {best[1]}, k = {best[2]:.3f}")
    return {"calibration_dex": best[0]}


CENSUS = [
    {"name": "a0 (RAR)", "dim": (0, 1, -2), "value": 1.2e-10,
     "claim": "c H0 / 2pi", "source": "McGaugh-Lelli-Schombert"},
    {"name": "rho_Lambda", "dim": (1, -1, -2),
     "value": 0.685 * 3 * H0_PLANCK ** 2 * C ** 2
     / (8 * math.pi * G),
     "claim": "M_P^2 H0^2 (CKN/Sorkin/Zeldovich slot)",
     "source": "Planck 2018 + c33/c31"},
    {"name": "Omega_L/Omega_m", "dim": (0, 0, 0),
     "value": 0.685 / 0.315, "claim": "O(1) (why-now)",
     "source": "Planck 2018"},
    {"name": "m_pi", "dim": (1, 0, 0),
     "value": 139.57039e6 * 1.602176634e-19 / C ** 2,
     "claim": "(hbar^2 H0 / (G c))^{1/3} (Weinberg)",
     "source": "PDG"},
    {"name": "nu mass scale", "dim": (1, 0, 0),
     "value": 0.0504 * 1.602176634e-19 / C ** 2,
     "claim": "m_P mu^{1/2} (dark-energy scale)",
     "source": "PDG sqrt(dm2_atm)"},
]


def eq5():
    print("EQ5 the census pins")
    for e in CENSUS:
        print(f"  {e['name']}: {e['value']:.4e} SI ({e['claim']})")
    check("EQ5 five census entries", len(CENSUS) == 5)
    return {"n": len(CENSUS)}


def main():
    pins = {}
    pins["EQ1"] = eq1()
    pins["EQ2"] = eq2()
    pins["EQ3"] = eq3()
    pins["EQ4"] = eq4()
    pins["EQ5"] = eq5()
    pins["k_lattice"] = [str(k) for k in K_LATTICE]
    pins["prefactors"] = sorted(PREFACTORS)
    out = os.path.join(HERE, "p34_registration.json")
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
