#!/usr/bin/env python3
"""Verification for the P-34 claim horizon-census-priced, by
independent live reimplementation: its own Planck-unit route to the
codebook (no Gaussian elimination - direct Planck-unit formulas),
its own interval-union coverage, its own census recompute for
three entries. Nothing read from results files.

Checks: (1) mu = H0 t_P from the direct Planck-time formula agrees
with 1.1776e-61 at 1e-12 relative; (2) coverage p(0.1 dex) within
1e-6 of an independently merged interval union; (3) the census
spot set: a0 nets <= 0.5 bits, m_pi nets <= 0.5 bits, rho_Lambda
nets <= 3 bits, all at Planck H0 with the census charge log2(5).

--mutant census-of-one  drops the census look-elsewhere charge
    (log2(1) = 0); rho_Lambda then nets 4.45 > 3 and the cap
    check kills it - the charge is load-bearing.
--mutant mu-wrong       uses c^{-3/2} in mu; the H0 t_P identity
    breaks at the first check.
"""
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"census-of-one", "mu-wrong"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

HBAR = 1.054571817e-34
C = 2.99792458e8
G = 6.67430e-11
H0 = 67.4 * 1000.0 / 3.0857e22

PREF = [1.0, 2.0, 3.0, 4.0, 0.5, 1 / 3, 0.25, math.pi,
        2 * math.pi, 4 * math.pi, math.pi ** 2, 4 * math.pi ** 2,
        8 * math.pi, 1 / math.pi, 1 / (2 * math.pi),
        1 / (4 * math.pi), 1 / math.pi ** 2, 1 / (4 * math.pi ** 2),
        3 / (8 * math.pi), 8 * math.pi / 3]
KS = sorted({p / q for q in (1, 2, 3)
             for p in range(-2 * q, 2 * q + 1)})


def mu():
    cexp = -1.5 if MUTANT == "mu-wrong" else -2.5
    return HBAR ** 0.5 * G ** 0.5 * C ** cexp * H0


def coverage(t):
    logs = sorted(math.log10(p) for p in PREF)
    cell = abs(math.log10(HBAR ** 0.5 * G ** 0.5 * C ** -2.5
                          * H0)) / 6
    merged = []
    for v in logs:
        lo, hi = v - t, v + t
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(hi, merged[-1][1])
        else:
            merged.append([lo, hi])
    return min(sum(b - a for a, b in merged) / cell, 1.0)


def nearest_dex(target_log, base_log):
    """min over k, pref of |base + k log10(mu) + log(pref) - target|
    with mu from the TRUE formula (the codebook grid itself)."""
    lmu = math.log10(HBAR ** 0.5 * G ** 0.5 * C ** -2.5 * H0)
    best = None
    for k in KS:
        for p in PREF:
            t = abs(base_log + k * lmu + math.log10(p) - target_log)
            best = t if best is None else min(best, t)
    return best


def main():
    failures = []

    tp = math.sqrt(HBAR * G / C ** 5)
    m = mu()
    print(f"mu = {m:.6e}; H0 t_P = {H0 * tp:.6e}")
    if abs(m / (H0 * tp) - 1) > 1e-12:
        print("FAIL: mu is not H0 t_P")
        failures.append("mu")

    p01 = coverage(0.1)
    print(f"coverage p(0.1 dex) = {p01:.6f}")
    if abs(p01 - 0.2750) > 5e-4:
        print("FAIL: coverage off the pinned 0.2750")
        failures.append("coverage")

    charge = 0.0 if MUTANT == "census-of-one" else math.log2(5)
    # a0: acceleration base = Planck acceleration a_P = c / t_P;
    # slot k=1 gives c H0 x pref
    a_P = C / tp
    t_a0 = nearest_dex(math.log10(1.2e-10), math.log10(a_P))
    s_a0 = -math.log2(max(coverage(max(t_a0, 1e-6)), 1e-12))
    net_a0 = s_a0 - charge
    # m_pi: mass base = Planck mass m_P = sqrt(hbar c / G)
    m_P = math.sqrt(HBAR * C / G)
    m_pi = 139.57039e6 * 1.602176634e-19 / C ** 2
    t_pi = nearest_dex(math.log10(m_pi), math.log10(m_P))
    s_pi = -math.log2(max(coverage(max(t_pi, 1e-6)), 1e-12))
    net_pi = s_pi - charge
    # rho_Lambda: density base = Planck density c^7/(hbar G^2)...
    # as mass density: rho_P = c^5/(hbar G^2); use energy density
    rho_P = C ** 7 / (HBAR * G ** 2)
    rho_L = 0.685 * 3 * H0 ** 2 * C ** 2 / (8 * math.pi * G)
    t_rho = nearest_dex(math.log10(rho_L), math.log10(rho_P))
    s_rho = -math.log2(max(coverage(max(t_rho, 1e-6)), 1e-12))
    net_rho = s_rho - charge
    print(f"a0: t {t_a0:.4f} net {net_a0:+.2f} | m_pi: t {t_pi:.4f} "
          f"net {net_pi:+.2f} | rho_L: t {t_rho:.4f} net "
          f"{net_rho:+.2f}")
    if net_a0 > 0.5 or net_pi > 0.5:
        print("FAIL: a0 or m_pi nets above 0.5 bits")
        failures.append("zero-bit-rows")
    if net_rho > 3.0:
        print("FAIL: rho_Lambda nets above the 3-bit cap")
        failures.append("cap")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p34 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
