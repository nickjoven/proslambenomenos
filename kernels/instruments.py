#!/usr/bin/env python3
"""Spectral-dimension and telegraph instruments: continuous-time
d_s(t) = 2t <lambda>_P, the even-step discrete d_s, the heat-kernel
d_s over a quadrature grid, and the committed-telegraph
autocorrelation. Extracted, not rewritten.

Admission (two-artifact rule):
  ds_continuous   scripts/experiments/p16_walk.py:96-99 (ds_ct),
                  scripts/verify/p16_two_dimensions.py:140-143;
                  the same instrument with a max-shift lands in
                  p15_derive.py:63-68 (ds_exact) and p16_derive.py:317
  ds_exact        scripts/experiments/p15_derive.py:63-68 (the
                  shifted, overflow-safe form of the same sum)
  ds_discrete     scripts/experiments/p16_walk.py:102-107 (ds_disc),
                  scripts/experiments/p16_derive.py:331-338 (EQ6's
                  even-step check)
  ds_heat_grid    scripts/experiments/p16_derive.py:224-230
                  (ds_dalembertian), scripts/verify/
                  p16_two_dimensions.py:171-174 (ds_dal)
  telegraph_autocorr
                  scripts/experiments/p24_derive.py:24-26 (EQ2:
                  C(t) = e^{-2 r t} from the 2x2 generator);
                  the committed-hop counting that measures r is
                  kernels/sde.py mod_pi_track (p22/p23/p24 lineage)

Selftest anchors:
  - cycle anchors (p16_derive.py EQ6): on C_200 both walk instruments
    plateau at 1 inside the P-15 window [t_lat, 0.5/lambda_1].
  - the exact Z curve (p15_derive.py EQ2): C_4096 continuous-time d_s
    equals 2t(2 - 2 I1/I0(2t)) to 1e-9 at the pinned t values.
  - short-scale exactness (p16_derive.py EQ7): d_s(t) -> 0 linearly
    on any finite graph; d_s(t)/(2 t mean lambda) -> 1 as t -> 0.
  - telegraph_autocorr: e^{-2rt} halves ln C per 1/(2r).

stdlib only; floating-point operation order preserved from the
verify-script sources.
"""
import math


def ds_continuous(t, lams):
    """d_s(t) = 2t <lambda>_P over an explicit spectrum, unshifted
    (scripts/verify/p16_two_dimensions.py:140 ds_ct; p16_walk.py:96)."""
    num = sum(x * math.exp(-t * x) for x in lams)
    den = sum(math.exp(-t * x) for x in lams)
    return 2 * t * num / den


def ds_exact(spec, t):
    """The same instrument with the max-shift that keeps huge spectra
    in range (p15_derive.py:63)."""
    mx = min(l * t for l in spec)
    num = sum(l * math.exp(-(l * t - mx)) for l in spec)
    den = sum(math.exp(-(l * t - mx)) for l in spec)
    return 2 * t * num / den


def ds_discrete(lams, N, n):
    """Even-step discrete d_s from the lazy-walk return probability
    pbar(n) = (1/N) sum (1 - lambda)^n, log-slope between n and n+2
    (p16_walk.py:102 ds_disc)."""
    mus = [1 - x for x in lams]

    def pbar(m):
        return sum(mu ** m for mu in mus) / N
    return -2 * (math.log(pbar(n + 2)) - math.log(pbar(n))) / \
        (math.log(n + 2) - math.log(n))


def ds_heat_grid(s, grid):
    """Heat-kernel d_s(s) = -2s <g>_P over a quadrature grid of
    (z, w, g(z)) triples (scripts/verify/p16_two_dimensions.py:171
    ds_dal; p16_derive.py:224 ds_dalembertian)."""
    num = sum(w * g * math.exp(s * g) for _, w, g in grid)
    den = sum(w * math.exp(s * g) for _, w, g in grid)
    return -2 * s * num / den


def telegraph_autocorr(rate, t):
    """Autocorrelation of the committed two-state telegraph with
    per-direction hop rate `rate`: C(t) = e^{-2 rate t}
    (p24_derive.py EQ2, the 2x2 generator's nonzero eigenvalue)."""
    return math.exp(-2 * rate * t)


def cycle_spectrum(n, S=(1,)):
    """Circulant Laplacian eigenvalues for symmetric offsets S
    (p15_derive.py:57)."""
    return [sum(2 * (1 - math.cos(2 * math.pi * k * s / n)) for s in S)
            for k in range(n)]


# ---------------------------------------------------------------- selftest
def _selftest():
    from kernels.specfun import bessel_ratio_p15
    ok = True

    # anchor 1: cycle anchors (p16_derive.py EQ6) - both instruments
    # plateau at 1 inside the window
    n6 = 200
    lams = [1 - math.cos(2 * math.pi * k / n6) for k in range(n6)]
    lam1 = min(x for x in lams if x > 1e-12)
    t_win = 0.5 / lam1
    ct_vals = [ds_continuous(t_win * f, lams) for f in (0.05, 0.1, 0.2)]
    g1 = all(abs(v - 1) < 0.12 for v in ct_vals)
    dd = [ds_discrete(lams, n6, n) for n in (40, 80, 160)]
    g2 = all(abs(v - 1) < 0.12 for v in dd)
    ok &= g1 and g2
    print(f"C_200 window plateau: ct {['%.3f' % v for v in ct_vals]}, "
          f"disc {['%.3f' % v for v in dd]} {'ok' if g1 and g2 else 'FAIL'}")

    # anchor 2: the exact Z curve (p15_derive.py EQ2)
    spec2 = cycle_spectrum(4096)
    worst = 0.0
    for t in (5.0, 10.0, 20.0, 40.0, 60.0):
        r = bessel_ratio_p15(2 * t)
        worst = max(worst, abs(ds_exact(spec2, t) - 2 * t * (2 - 2 * r)))
    good = worst < 1e-9
    ok &= good
    print(f"C_4096 vs Z curve 2t(2 - 2 I1/I0): worst dev {worst:.2e} "
          f"{'ok' if good else 'FAIL'}")

    # anchor 3: short-scale linearity (p16_derive.py EQ7)
    t = 1e-4
    v = ds_continuous(t, lams)
    lin = v / (2 * t * (sum(lams) / len(lams)))
    good = v < 0.01 and abs(lin - 1) < 1e-3
    ok &= good
    print(f"short scale: d_s(1e-4) = {v:.2e}, linear ratio {lin:.6f} "
          f"{'ok' if good else 'FAIL'}")

    # anchor 4: heat-kernel instrument vs finite differences on a toy
    # grid (the p16_derive EQ4 cross-check pattern, small grid)
    grid = [(z, 0.1, -z / (1 + z)) for z in [0.1 * i for i in range(1, 60)]]
    s0 = 2.0

    def lnP(s):
        return math.log(sum(w * math.exp(s * g) for _, w, g in grid))
    fd = -2 * (lnP(s0 * 1.001) - lnP(s0 * 0.999)) / (math.log(1.001) - math.log(0.999))
    inst = ds_heat_grid(s0, grid)
    good = abs(fd - inst) < 1e-4
    ok &= good
    print(f"heat-grid instrument vs FD: dev {abs(fd - inst):.1e} "
          f"{'ok' if good else 'FAIL'}")

    # anchor 5: telegraph decay identity
    r = 0.37
    good = abs(math.log(telegraph_autocorr(r, 1.0)) + 2 * r) < 1e-15
    ok &= good
    print(f"telegraph ln C(1) = -2r {'ok' if good else 'FAIL'}")

    print("instruments selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
        sys.exit(_selftest())
    print(__doc__)
