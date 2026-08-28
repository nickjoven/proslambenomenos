#!/usr/bin/env python3
"""Quadrature kernels: the log-domain constant-flux FPE mobility, the
double-well MFPT double quadrature, log-spaced trapezoid grids, and
Richardson central differentiation. Extracted, not rewritten.

Admission (two-artifact rule):
  mobility_quad   scripts/experiments/p22_derive.py:109-147 (EQ4),
                  scripts/verify/p22_locking_skeleton.py:82-96
  mfpt_double_well
                  scripts/experiments/p22_derive.py:193-221 (EQ6),
                  scripts/experiments/p24_derive.py:88-108 and
                  scripts/experiments/p24_plots.py:22-40 carry the
                  same double-quadrature pattern on their own grids
  log_trapezoid   scripts/experiments/p16_derive.py:233-246
                  (make_zgrid), scripts/verify/p16_two_dimensions.py:164-169
  richardson_deriv
                  scripts/experiments/p16_derive.py:129-143 (Jn);
                  the central-difference derivative pattern also lands
                  in p10_mm_dimension.py:60-65 and the p24 falsifier's
                  saddle check

Selftest anchors (from the derive layers that earned them):
  - mobility_quad reproduces its four exact limits (p22_derive.py EQ4):
    v = delta at eps = 0; v -> delta as D -> inf; v ->
    sqrt(delta^2 - eps^2) as D -> 0 outside the tongue; v -> 0 inside;
    plus the grid-convergence split.
  - mfpt_double_well: Kramers asymptote (eps/pi) e^{-eps/D} within a
    factor 2 at D = eps/5 (p22_derive.py EQ6).
  - log_trapezoid integrates z e^{-z} over a wide log range to the
    Gamma(2) = 1 value within trapezoid error.
  - richardson_deriv: d/dc of e^{-c} at c = 1 to ~1e-11 (4th-order).

stdlib only; floating-point operation order preserved from the sources
(the sliding-window maximum is a max over the same window either way,
so the deque route and the slice route agree bit for bit).
"""
import math
from collections import deque


def mobility_quad(delta, eps, D, n=None):
    """Stationary constant-flux FPE mobility for dtheta = (delta -
    eps sin theta) dt + sqrt(2D) dW, log-domain throughout:
    v = 2 pi D (1 - e^{-2 pi delta/D}) / int_0^{2pi} e^{-U(x)/D}
        [int_x^{x+2pi} e^{U(y)/D} dy] dx, U = -delta th - eps cos th.
    Resolution adapts to the integrand sharpness ~ 1/D; a sliding
    monotonic-deque window max keeps it O(n) (p22_derive.py:109;
    the p22 falsifier's mobility_quad is the n = 1600 slice form of
    the same sums)."""
    if delta == 0:
        return 0.0
    if n is None:
        n = max(1600, min(int(120 / D), 24000))
    h = 2 * math.pi / n
    Us = [(-delta * (i * h) - eps * math.cos(i * h)) / D for i in range(2 * n + 1)]
    dq = deque()
    wmax = [0.0] * (n + 1)
    for j in range(2 * n + 1):
        while dq and Us[dq[-1]] <= Us[j]:
            dq.pop()
        dq.append(j)
        i = j - n
        if i >= 0:
            while dq[0] < i:
                dq.popleft()
            wmax[i] = Us[dq[0]]
    log_terms = [0.0] * (n + 1)
    for i in range(n + 1):
        m = wmax[i]
        s = 0.5 * (math.exp(Us[i] - m) + math.exp(Us[i + n] - m))
        s += sum(math.exp(Us[i + j] - m) for j in range(1, n))
        log_terms[i] = -Us[i] + m + math.log(s * h)
    tmax = max(log_terms)
    tot = 0.5 * (math.exp(log_terms[0] - tmax) + math.exp(log_terms[-1] - tmax))
    tot += sum(math.exp(t - tmax) for t in log_terms[1:-1])
    log_norm = tmax + math.log(tot * h)
    return 2 * math.pi * D * (-math.expm1(-2 * math.pi * delta / D)) * math.exp(-log_norm)


def mfpt_double_well(eps, D, n=3000):
    """Exact mean first-passage time from the well bottom (theta = 0)
    to the adjacent barrier top (pi/2) for U = -(eps/2) cos 2 theta,
    reflecting at -pi/2, by the double quadrature
    T = (1/D) int_0^{pi/2} dx e^{U(x)/D} int_{-pi/2}^x e^{-U(y)/D} dy
    (p22_derive.py:193, EQ6). Hop rate per direction = 1/(2 T)."""
    def U(t):
        return -(eps / 2) * math.cos(2 * t) / D
    nx = n
    hx = (math.pi / 2) / nx
    ny = 2 * n
    hy = math.pi / ny
    ys = [-math.pi / 2 + j * hy for j in range(ny + 1)]
    emu = [math.exp(-U(y)) for y in ys]
    cum = [0.0]
    for j in range(ny):
        cum.append(cum[-1] + 0.5 * (emu[j] + emu[j + 1]) * hy)

    def inner(xv):
        j = (xv + math.pi / 2) / hy
        j0 = min(int(j), ny - 1)
        fr = j - j0
        return cum[j0] + fr * (cum[j0 + 1] - cum[j0])

    tot = 0.0
    for i in range(nx + 1):
        xv = i * hx
        w = 0.5 if i in (0, nx) else 1.0
        tot += w * math.exp(U(xv)) * inner(xv)
    return tot * hx / D


def log_trapezoid(zmin, zmax, nz):
    """Log-spaced grid with trapezoid weights: [(z_i, w_i)] with
    z_i = zmin (zmax/zmin)^{i/nz} (p16_derive.py:233 make_zgrid; the
    p16 falsifier builds the same weights inline)."""
    zs = [zmin * (zmax / zmin) ** (i / nz) for i in range(nz + 1)]
    grid = []
    for i, z in enumerate(zs):
        if i == 0:
            w = 0.5 * (zs[1] - zs[0])
        elif i == nz:
            w = 0.5 * (zs[nz] - zs[nz - 1])
        else:
            w = 0.5 * (zs[i + 1] - zs[i - 1])
        grid.append((z, w))
    return grid


def richardson_deriv(fun, c, h=None):
    """4th-order Richardson central difference of fun at c, the
    (-d/dc) convention of its source: returns (fun(c-h) - fun(c+h))
    combined over h and h/2, i.e. -fun'(c) to O(h^4)
    (p16_derive.py:129, Jn's deriv)."""
    if h is None:
        h = 1e-3 * c
    Dh = (fun(c - h) - fun(c + h)) / (2 * h)
    Dh2 = (fun(c - h / 2) - fun(c + h / 2)) / h
    return (4 * Dh2 - Dh) / 3.0


# ---------------------------------------------------------------- selftest
def _selftest():
    ok = True

    # anchor 1: the four exact mobility limits (p22_derive.py EQ4)
    v0 = mobility_quad(0.7, 0.0, 0.4)
    g1 = abs(v0 - 0.7) < 1e-5
    vD = mobility_quad(0.7, 1.0, 60.0)
    g2 = abs(vD - 0.7) < 5e-3
    vdet = mobility_quad(1.5, 1.0, 0.02, n=2400)   # n trimmed for the
    g3 = abs(vdet - math.sqrt(1.25)) < 5e-3 * math.sqrt(1.25)  # ~5 s budget
    vin = mobility_quad(0.5, 1.0, 0.05, n=1600)
    g4 = abs(vin) < 1e-4
    vg1, vg2 = mobility_quad(0.9, 1.0, 0.25, n=800), mobility_quad(0.9, 1.0, 0.25, n=1600)
    g5 = abs(vg1 - vg2) < 1e-4 * abs(vg2)
    ok &= g1 and g2 and g3 and g4 and g5
    print(f"mobility limits: eps=0 {v0:.6f}; D=60 {vD:.4f}; D->0 out "
          f"{vdet:.5f} vs {math.sqrt(1.25):.5f}; D->0 in {vin:.1e}; "
          f"grid split {abs(vg1 - vg2) / abs(vg2):.1e} "
          f"{'ok' if g1 and g2 and g3 and g4 and g5 else 'FAIL'}")

    # anchor 2: MFPT vs the Kramers asymptote (p22_derive.py EQ6)
    r = 1.0 / (2 * mfpt_double_well(1.0, 0.2))
    kram = (1.0 / math.pi) * math.exp(-1.0 / 0.2)
    good = 0.5 < r / kram < 2.0
    ok &= good
    print(f"mfpt hop rate D=0.2: {r:.5f} vs Kramers {kram:.5f} "
          f"(ratio {r / kram:.3f}) {'ok' if good else 'FAIL'}")

    # anchor 3: log-trapezoid integrates z e^{-z} to Gamma(2) = 1
    grid = log_trapezoid(1e-6, 60.0, 800)
    tot = sum(w * z * math.exp(-z) for z, w in grid)
    good = abs(tot - 1.0) < 1e-4
    ok &= good
    print(f"log_trapezoid int z e^-z dz = {tot:.7f} vs 1 "
          f"{'ok' if good else 'FAIL'}")

    # anchor 4: Richardson derivative, (-d/dc) e^{-c} at c = 1 is e^{-1}
    d = richardson_deriv(lambda c: math.exp(-c), 1.0)
    good = abs(d - math.exp(-1.0)) < 1e-11
    ok &= good
    print(f"richardson (-d/dc) e^-c at 1: dev {abs(d - math.exp(-1)):.1e} "
          f"{'ok' if good else 'FAIL'}")

    print("quad selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
