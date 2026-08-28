#!/usr/bin/env python3
"""Verification for the P-29 claim farey-bridge-mediant-mechanism,
by independent live reimplementation: tongue widths by the
ROTATION-NUMBER STAIRCASE (long iteration + bisection on the
plateau edges - a different route than the experiment's tangency
bisection), bandwidths by characteristic-polynomial bisection (no
eigh), and its own mediant arithmetic. Nothing read from results
files.

Checks: (1) the staircase route reproduces the exact rho = 0
tongue width K/pi within 2e-3 (its own accuracy anchor); (2) in
[1/3, 1/2] and [1/4, 1/3], the mediant beats every listed
competitor on BOTH instruments by both routes; (3) the derived
control inversion: under pure-second-harmonic forcing, 3/8 beats
the mediant 2/5 on the tongue side while the butterfly ordering
is unchanged.

--mutant harmonic-blind  runs the control with FIRST-harmonic
    forcing (the premise intact); the mediant keeps winning, the
    required inversion never appears, and check (3) kills it.
--mutant mediant-shift   uses the SECOND mediant (a+2c)/(b+2d) as
    the "mediant" (a numerator shift would land on the symmetric
    twin (q-p)/q, which ties by the p -> q-p symmetry; a bare
    denominator shift lands on unreduced fractions); the second
    mediant is interior but ties-or-loses against the competitor
    list, and check (2)'s strict inequality kills it.
"""
import math
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"harmonic-blind", "mediant-shift"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

K = 0.5


def rho_N(Omega, K_, q=1, harmonic=1, N=20000, burn=2000):
    """Rotation number with the transient discarded and the count
    an exact multiple of q, so a locked p/q orbit returns p/q to
    machine precision instead of p/q + O(transient/N)."""
    w = 2 * math.pi * harmonic
    c = K_ / (2 * math.pi)
    th = 0.1234
    for _ in range(burn):
        th = th + Omega + c * math.sin(w * th)
    n_eff = q * max(1, N // q)
    th0 = th
    for _ in range(n_eff):
        th = th + Omega + c * math.sin(w * th)
    return (th - th0) / n_eff


def staircase_width(p, q, K_, harmonic=1):
    """Plateau edges by bisection on rho_N vs p/q."""
    rho = p / q
    span = K_ / (2 * math.pi) + 1e-3
    tol = 0.25 / 20000

    def locked(Om):
        return abs(rho_N(Om, K_, q=q, harmonic=harmonic) - rho) < tol
    # seed by bisection on the monotone staircase: g = rho_N - p/q
    # changes sign across the window, and once the bracket is
    # narrower than the window the midpoint sits inside it - this
    # finds arbitrarily narrow windows a coarse scan would miss
    a, b = rho - span, rho + span
    seed = None
    for _ in range(52):
        m = 0.5 * (a + b)
        r = rho_N(m, K_, q=q, harmonic=harmonic)
        if abs(r - rho) < tol:
            seed = m
            break
        if r < rho:
            a = m
        else:
            b = m
    if seed is None:
        return 0.0

    def edge(direction):
        lo, hi = seed, rho + direction * span
        for _ in range(44):
            m = 0.5 * (lo + hi)
            if locked(m):
                lo = m
            else:
                hi = m
        return 0.5 * (lo + hi)
    return edge(+1) - edge(-1)


def charpoly_edges(p, q):
    """Union spectrum of the two Chambers corners via the
    tridiagonal-plus-corner characteristic polynomial (as in the
    P-28 falsifier, independently written)."""
    out = []
    # k2 nudged off the exact corners by 2.7e-5: degenerate corner
    # roots give the sign-scan nothing to cross (a double root
    # touches zero), and the band-edge bias is O(delta^2) - far
    # below the O(0.1) ordering margins these checks use
    for corner, k2 in ((+1.0, 2.7e-5), (-1.0, math.pi / q + 2.7e-5)):
        diag = [2 * math.cos(2 * math.pi * p * (n + 1) / q + k2)
                for n in range(q)]

        def cp(x):
            if q == 1:
                return diag[0] + 2 * corner - x
            f = [1.0, diag[0] - x]
            for i in range(1, q):
                f.append((diag[i] - x) * f[-1] - f[-2])
            g = [1.0, diag[1] - x]
            for i in range(2, q - 1):
                g.append((diag[i] - x) * g[-1] - g[-2])
            gi = g[q - 2] if q > 2 else 1.0
            return f[q] - corner * corner * gi - 2 * corner * (-1) ** q
        m = max(6000, 700 * q)
        xs = [-4.5 + 9.0 * i / m for i in range(m + 1)]
        vals = [cp(x) for x in xs]
        roots = []
        for i in range(m):
            if vals[i] * vals[i + 1] < 0:
                a, b = xs[i], xs[i + 1]
                fa = vals[i]
                for _ in range(60):
                    c0 = 0.5 * (a + b)
                    fc = cp(c0)
                    if fa * fc <= 0:
                        b = c0
                    else:
                        a, fa = c0, fc
                roots.append(0.5 * (a + b))
        out += roots
    return sorted(out)


def bandwidth_S(p, q):
    if q == 1:
        return 8.0
    e = charpoly_edges(p, q)
    assert len(e) == 2 * q, f"roots {len(e)} != {2 * q} at {p}/{q}"
    return sum(e[2 * i + 1] - e[2 * i] for i in range(q))


def main():
    failures = []

    # (1) staircase accuracy anchor: rho = 0 width = K/pi
    w0 = staircase_width(0, 1, K)
    want = K / math.pi
    print(f"staircase rho=0 width {w0:.6f} vs K/pi {want:.6f}")
    if abs(w0 - want) > 2e-3:
        print("FAIL: staircase route misses the exact anchor")
        failures.append("anchor")

    # (2) mediant beats competitors on both instruments
    tests = [((1, 3, 1, 2), (2, 5), [(3, 8), (3, 7), (4, 9)]),
             ((1, 4, 1, 3), (2, 7), [(3, 10), (3, 11)])]
    for (a, b, c, d), med, comps in tests:
        mp, mq = med
        if MUTANT == "mediant-shift":
            mp, mq = a + 2 * c, b + 2 * d
        wm = staircase_width(mp, mq, K)
        sm = bandwidth_S(mp, mq)
        for cp_, cq in comps:
            wc = staircase_width(cp_, cq, K)
            sc = bandwidth_S(cp_, cq)
            if not (wm > wc):
                print(f"FAIL: [{a}/{b},{c}/{d}] tongue: mediant "
                      f"{mp}/{mq} {wm:.3e} !> {cp_}/{cq} {wc:.3e}")
                failures.append("tongue-order")
            if not (sm > sc):
                print(f"FAIL: [{a}/{b},{c}/{d}] bandwidth: mediant "
                      f"{mp}/{mq} {sm:.4f} !> {cp_}/{cq} {sc:.4f}")
                failures.append("band-order")
        if not failures:
            print(f"[{a}/{b},{c}/{d}]: mediant {mp}/{mq} tops both "
                  f"instruments (D {wm:.3e}, S {sm:.4f})")

    # (3) the control inversion
    harm = 1 if MUTANT == "harmonic-blind" else 2
    d38 = staircase_width(3, 8, K, harmonic=harm)
    d25 = staircase_width(2, 5, K, harmonic=harm)
    s25, s38 = bandwidth_S(2, 5), bandwidth_S(3, 8)
    print(f"control (harmonic {harm}): D(3/8) {d38:.3e}, D(2/5) "
          f"{d25:.3e}; S(2/5) {s25:.4f}, S(3/8) {s38:.4f}")
    if not (d38 > d25):
        print("FAIL: the derived control inversion (3/8 over 2/5) "
              "did not appear")
        failures.append("control")
    if not (s25 > s38):
        print("FAIL: butterfly ordering changed - it must not")
        failures.append("control-band")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p29 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
