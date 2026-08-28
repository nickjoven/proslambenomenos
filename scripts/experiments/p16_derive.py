#!/usr/bin/env python3
"""P-16 derivation layer (pre-registration): the two spectral
dimensions of a causal set. Eichhorn-Mizera (CQG 31, 125007) compute
d_s from a random walk on the sprinkled causet's undirected Hasse
graph and find it INCREASES at small scales; Belenchia-Benincasa-
Marciano-Modesto (PRD 93, 044017) compute d_s from the regularised
nonlocal d'Alembertian's heat kernel and find universal reduction to
2. Both cannot be "the" spectral dimension. P-16 computes BOTH
definitions - the walk on our own sprinklings, the d'Alembertian by
quadrature of the paper's exact eq. (15) operator - and registers
the divergence, crowning no winner. Everything here runs before the
registered ensembles.

Derived facts:
  EQ1  K0 by two independent routes (integral representation vs
       series through the known K0(1)) to 1e-10.
  EQ2  the BBMM 2D operator g(z), z = k^2, rho = 1 (their eq. 15,
       constants a = -2, b = {4, -8, 4}): the IR limit g -> -z and
       the UV form g -> -2 + b1/z verified fit-free from the
       quadrature itself.
  EQ3  the regularised operator g_reg = a g/(a - g) (their eq. 5):
       IR g_reg -> -z, UV g_reg -> -(a^2/b1) z (their eq. 6) -
       verified from the same quadrature.
  EQ4  the exact log-derivative instrument for the heat kernel:
       d_s(s) = -2 s <g_reg>_P (the P-15 trick, derivative under
       the integral), cross-checked against finite differences of
       ln P; the pinned curve: d_s -> 2 in BOTH limits with a
       superdiffusive maximum between (BBMM Fig. 2 shape), and the
       UNregularised d = 2 identity d_s = 4 rho s (their eq. 14)
       reproduced - the anchor their own regularisation argument
       hangs on.
  EQ5  the link-count null for the walk side: in the unit causal
       square, E[links] = N(N-1) int (1-a)(1-b)(1-ab)^{N-2} da db
       (exact, no Poisson approximation) - the mean Hasse degree
       grows ~ 2 ln N: the EM nonlocality driver, pinned at the
       registered N ladder.
  EQ6  instrument anchors on the cycle graph C_n: continuous-time
       d_s(t) = 2t <lambda>_P and even-step discrete d_s both
       plateau at 1 inside the P-15 window (validates both walk
       instruments on a known spectrum).
  EQ7  the short-scale limits that frame the registered divergence:
       walk-side d_s(t) = 2t <lambda> -> 0 LINEARLY as t -> 0 on
       any finite graph (exact instrument statement); d'Alembertian
       d_s(s) -> 2 as s -> 0 (their eq. 12). Opposite directions -
       this is the disagreement, derived before it is measured.
Pinned -> p16_registration.json.
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


# ---------- EQ1: K0 two ways ----------
def k0(x, n=3000, tmax=None):
    """K0(x) = int_0^inf e^{-x cosh t} dt, truncated adaptively."""
    if tmax is None:
        tmax = math.acosh(max(40.0 / x, 2.0)) + 2.0
    h = tmax / n
    s = 0.5 * (math.exp(-x) + math.exp(-x * math.cosh(tmax)))
    for i in range(1, n):
        s += math.exp(-x * math.cosh(i * h))
    return s * h


K0_1_REF = 0.421024438240708333  # Abramowitz-Stegun 9.8, K0(1)
d1 = abs(k0(1.0) - K0_1_REF)
d2 = abs(k0(1.0, n=6000) - k0(1.0, n=3000))
eq(1, d1 < 1e-10 and d2 < 1e-12, "K0 quadrature vs reference and self-consistency",
   f"|K0(1) - ref| = {d1:.1e}, depth split {d2:.1e}")

# ---------- EQ2: the BBMM 2D operator, via the E1 closed form ----------
A2 = -2.0
B2 = [4.0, -8.0, 4.0]
SQPI4 = math.sqrt(math.pi) / 4.0
EULER_G = 0.5772156649015328606


def expint_e1_scaled(x):
    """f(x) = e^x E1(x), stable for all x > 0."""
    if x <= 1.0:
        s = -EULER_G - math.log(x)
        term, k = x, 1
        val = term
        while abs(term) > 1e-18 * (abs(val) + 1):
            k += 1
            term *= -x * (k - 1) / (k * k)
            val += term
        return math.exp(x) * (s + val)
    # Lentz continued fraction for e^x E1(x) = 1/(x+1- 1/(x+3- 4/(x+5- ...)))
    tiny = 1e-30
    f = tiny
    C, D = f, 0.0
    for k in range(0, 200):
        a = 1.0 if k == 0 else -k * k
        b = x + 2 * k + 1
        D = b + a * D
        D = tiny if D == 0 else D
        C = b + a / C
        C = tiny if C == 0 else C
        D = 1 / D
        delta = C * D
        f *= delta
        if abs(delta - 1) < 1e-15:
            break
    return f


def J0(c, a):
    """int_0^inf e^{-c u} K0(a sqrt(u)) du = (1/(2c)) e^x E1(x), x = a^2/(4c).
    The 1/2 prefactor is verified against direct quadrature in EQ2."""
    x = a * a / (4 * c)
    return expint_e1_scaled(x) / (2 * c)


def Jn(c, a, n):
    """(-d/dc)^n J0 by Richardson central differences (analytic in c)."""
    if n == 0:
        return J0(c, a)
    h = 1e-3 * c

    # 4th-order Richardson: D(h/2)*4/3 - D(h)/3
    def deriv(fun, cc):
        Dh = (fun(cc - h) - fun(cc + h)) / (2 * h)
        Dh2 = (fun(cc - h / 2) - fun(cc + h / 2)) / h
        return (4 * Dh2 - Dh) / 3.0
    if n == 1:
        return deriv(lambda cc: J0(cc, a), c)
    if n == 2:
        return deriv(lambda cc: Jn(cc, a, 1), c)
    raise ValueError(n)


def g2_bbmm15(z):
    """BBMM PRD 93, 044017 eq. (15) AS PRINTED, at rho = 1, via the E1
    closed form of its xi-integrals. Kept as the AUDIT object: this
    printed formula fails the paper's own IR limit by the exact
    constant 4/sqrt(pi) - 2 (see EQ2)."""
    a = math.sqrt(z)
    tot = 0.0
    for n in range(3):
        tot += B2[n] / math.factorial(n) * (SQPI4 ** n) * Jn(SQPI4, a, n)
    return A2 + tot


def g2(z):
    """the SOURCE operator, Aslanbeigi-Saravani-Sorkin JHEP 1406, 024
    eq. (5), d = 2 minimal, rho = 1, closed form:
        g(Z) = -Z e^{Z/2} E2(Z/2),  E2(x) = e^{-x} - x E1(x)
    so g(z) = -z (1 - x f(x)) with x = z/2, f = e^x E1(x).
    Exact limits: IR g -> -z (E2(0) = 1); UV g -> -2 + 8/z - 48/z^2."""
    x = 0.5 * z
    return -z * (1.0 - x * expint_e1_scaled(x))


def g2_quad(z, n=1400):
    """direct double-quadrature cross-check (moderate z only)."""
    sz = math.sqrt(z)
    xi_max = math.sqrt(80.0 / SQPI4)
    h = xi_max / n
    tot = 0.0
    for i in range(1, n + 1):
        xi = i * h
        w = math.exp(-SQPI4 * xi * xi) * k0(sz * xi, n=700)
        coeff = sum(B2[m] / math.factorial(m) * (SQPI4 * xi * xi) ** m for m in range(3))
        tot += w * coeff * xi
    return A2 + 2.0 * tot * h


# (i) the SOURCE closed form: IR and UV limits, exact asymptotics
irs = [(z, g2(z) / (-z)) for z in (1e-2, 1e-3, 1e-4)]
ok_ir = abs(irs[-1][1] - 1) < 5e-3
zu1, zu2 = 400.0, 900.0
b1_est1 = (g2(zu1) - A2) * zu1
b1_est2 = (g2(zu2) - A2) * zu2
ok_uv = abs(b1_est1 - (8 - 48 / zu1)) < 0.05 and abs(b1_est2 - (8 - 48 / zu2)) < 0.05
# (ii) THE AUDIT FINDING: BBMM eq. (15) as printed misses its own IR
# limit by exactly 4/sqrt(pi) - 2 = 0.25675... (psi-sum derivation:
# sum b_n psi(n+1) = -2 with these b_n, so g(0) = a + 1/c0). Verified
# numerically against the E1-closed-form implementation of eq. (15),
# which itself is cross-checked against direct double quadrature.
defect_derived = 4 / math.sqrt(math.pi) - 2
defect_measured = g2_bbmm15(1e-6)
xc1 = abs(g2_bbmm15(1.0) - g2_quad(1.0))
ok_defect = abs(defect_measured - defect_derived) < 1e-3 and xc1 < 5e-3
# (iii) the two agree in the UV (same physics there)
uv_agree = abs(g2_bbmm15(400.0) - g2(400.0)) < 5e-3
eq(2, ok_ir and ok_uv and ok_defect and uv_agree,
   "ASS eq. (5) closed form: IR -> -z, UV -> -2 + 8/z - 48/z^2 exact; "
   "BBMM printed eq. (15) fails its own IR limit by 4/sqrt(pi) - 2",
   f"IR ratios {['%.4f' % r for _, r in irs]}; b1(z) = {b1_est1:.4f}/{b1_est2:.4f} "
   f"vs 8 - 48/z; defect {defect_measured:.6f} vs derived {defect_derived:.6f}; "
   f"UV agreement {abs(g2_bbmm15(400.0) - g2(400.0)):.1e}")
B1_UV = 8.0


def greg(z):
    g = g2(z)
    return A2 * g / (A2 - g)


# ---------- EQ3: regularised limits ----------
r_ir = greg(1e-3) / (-1e-3)
slope_uv1 = greg(zu1) / (-(A2 * A2 / B1_UV) * zu1)
slope_uv2 = greg(zu2) / (-(A2 * A2 / B1_UV) * zu2)
eq(3, abs(r_ir - 1) < 0.02 and abs(slope_uv1 - 1) < 0.1 and abs(slope_uv2 - 1) < 0.1,
   "g_reg = a g/(a - g): IR -> -z, UV -> -(a^2/b1) z (their eq. 6)",
   f"IR ratio {r_ir:.4f}; UV ratios {slope_uv1:.3f}, {slope_uv2:.3f}")


# ---------- EQ4: the heat-kernel instrument and the pinned curve ----------
def ds_dalembertian(s, zgrid):
    num = den = 0.0
    for z, w, gz in zgrid:
        e = math.exp(s * gz)
        num += w * gz * e
        den += w * e
    return -2.0 * s * num / den


def make_zgrid(nz=220, zmax=2000.0):
    """log-spaced z grid with trapezoid weights and cached g_reg."""
    zs = [1e-4 * (zmax / 1e-4) ** (i / nz) for i in range(nz + 1)]
    grid = []
    for i, z in enumerate(zs):
        if i == 0:
            w = 0.5 * (zs[1] - zs[0])
        elif i == nz:
            w = 0.5 * (zs[nz] - zs[nz - 1])
        else:
            w = 0.5 * (zs[i + 1] - zs[i - 1])
        grid.append((z, w, greg(z)))
    return grid


ZG = make_zgrid()
# cross-check the exact log-derivative against finite differences
s0 = 2.0


def lnP(s):
    tot = 0.0
    m = max(s * gz for _, _, gz in ZG)
    for _, w, gz in ZG:
        tot += w * math.exp(s * gz - m)
    return m + math.log(tot)


fd = -2 * (lnP(s0 * 1.01) - lnP(s0 * 0.99)) / (math.log(1.01) - math.log(0.99))
inst = ds_dalembertian(s0, ZG)
ok4a = abs(fd - inst) < 5e-3
scurve = [0.02 * (1.35 ** i) for i in range(30)]
dvals = [(s, ds_dalembertian(s, ZG)) for s in scurve]
ds_small = ds_dalembertian(0.005, ZG)
ds_large = ds_dalembertian(300.0, ZG)
peak_s, peak_v = max(dvals, key=lambda t: t[1])
# the unregularised d = 2 identity d_s = 4 rho s (their eq. 14): a
# divergent-integral limit statement, so its check gets a deep cutoff
nzu, zmax_u = 400, 1.0e7
zs_u = [1e-4 * (zmax_u / 1e-4) ** (i / nzu) for i in range(nzu + 1)]
ZG_unreg = []
for i, z in enumerate(zs_u):
    if i == 0:
        w = 0.5 * (zs_u[1] - zs_u[0])
    elif i == nzu:
        w = 0.5 * (zs_u[nzu] - zs_u[nzu - 1])
    else:
        w = 0.5 * (zs_u[i + 1] - zs_u[i - 1])
    ZG_unreg.append((z, w, g2(z)))
lin1 = ds_dalembertian(2.0, ZG_unreg) / (4 * 2.0)
lin2 = ds_dalembertian(4.0, ZG_unreg) / (4 * 4.0)
ok4 = (ok4a and abs(ds_small - 2) < 0.1 and abs(ds_large - 2) < 0.15
       and peak_v > 2.1 and abs(lin1 - 1) < 0.05 and abs(lin2 - 1) < 0.05)
eq(4, ok4, "d_s(s) = -2s<g_reg>: UV -> 2, IR -> 2, max between; unregularised = 4 rho s",
   f"instr vs FD {abs(fd - inst):.1e}; ds(0.005) = {ds_small:.3f}, ds(300) = {ds_large:.3f}, "
   f"max {peak_v:.3f} at s = {peak_s:.2f}; 4rhos ratios {lin1:.3f}/{lin2:.3f}")

# ---------- EQ5: the link-count null ----------


def links_exact(N, n=400):
    h = 1.0 / n
    tot = 0.0
    for i in range(n):
        a = (i + 0.5) * h
        for j in range(n):
            b = (j + 0.5) * h
            tot += (1 - a) * (1 - b) * (1 - a * b) ** (N - 2)
    return N * (N - 1) * tot * h * h


NLADDER = [64, 128, 256]
Lpin = {str(N): links_exact(N) for N in NLADDER}
deg = {k: 2 * v / int(k) for k, v in Lpin.items()}
ok5 = deg["256"] > deg["128"] > deg["64"] and \
    abs(links_exact(128) - links_exact(128, n=800)) < 0.2
eq(5, ok5, "E[links] exact quadrature; mean Hasse degree grows ~ 2 ln N",
   "; ".join(f"N={k}: L = {v:.1f}, deg = {deg[k]:.2f}" for k, v in Lpin.items()))

# ---------- EQ6: cycle-graph instrument anchors ----------
n6 = 200
lams = [1 - math.cos(2 * math.pi * k / n6) for k in range(n6)]   # normalized cycle


def ds_walk_ct(t, lam):
    num = sum(x * math.exp(-t * x) for x in lam)
    den = sum(math.exp(-t * x) for x in lam)
    return 2 * t * num / den


lam1 = min(x for x in lams if x > 1e-12)
t_win = 0.5 / lam1
probe = [t_win * f for f in (0.05, 0.1, 0.2)]
ct_vals = [ds_walk_ct(t, lams) for t in probe]
ok6a = all(abs(v - 1) < 0.12 for v in ct_vals)
mus = [1 - x for x in lams]


def pbar(n):
    return sum(m ** n for m in mus) / n6


steps = [40, 80, 160]
dd = [(-2 * (math.log(pbar(2 * n + 2)) - math.log(pbar(2 * n))) /
      (math.log(2 * n + 2) - math.log(2 * n))) for n in steps]
ok6b = all(abs(v - 1) < 0.12 for v in dd)
eq(6, ok6a and ok6b, "cycle anchors: continuous-time and even-step walk d_s -> 1 in window",
   f"ct {['%.3f' % v for v in ct_vals]}, disc {['%.3f' % v for v in dd]}")

# ---------- EQ7: the framed divergence ----------
t_small = 1e-3
walk_small = ds_walk_ct(t_small, lams)
ok7 = walk_small < 0.01 and abs(ds_small - 2) < 0.1
eq(7, ok7, "short scale: walk d_s -> 0 linearly (exact on any finite graph); "
   "d'Alembertian d_s -> 2 (their eq. 12) - opposite directions, derived",
   f"walk ds(1e-3) = {walk_small:.2e}; dalembertian ds(0.005) = {ds_small:.3f}")

pin = {"N_ladder": NLADDER, "R_seeds": 3, "seed0": 160016,
       "links_pin": Lpin, "deg_pin": deg,
       "b1_uv": B1_UV, "dalembertian_curve": dvals,
       "dalembertian_peak": {"s": peak_s, "ds": peak_v},
       "unreg_slope_check": [lin1, lin2],
       "bands": {"links_sigma": 6.0, "anchor_tol": 0.12,
                 "superdiff_min": 2.15, "peak_growth_min": 0.10,
                 "instr_agree": 0.15, "dal_uv_tol": 0.1},
       "window_rule": "t in [t_lattice, 0.5/lambda_1], per P-15",
       "clauses": {
           "a": "link counts inside 6 sigma of the exact quadrature at every (N, seed)",
           "b": "walk superdiffusion: window peak d_s > 2.15 at every N >= 128, and mean peak grows from N = 64 to 256 by > 0.10 (the EM signature on our sprinklings)",
           "c": "instrument agreement: even-step and continuous-time walk d_s agree within 0.15 at the window centre",
           "d": "the divergence: at t -> lattice scale the walk d_s falls below 1 while the d'Alembertian curve stays within 0.1 of 2 as s -> 0, and the walk peak is N-dependent while the continuum curve is N-independent by construction - the two definitions cannot be identified at short scale"}}
(HERE / "p16_registration.json").write_text(json.dumps(pin, indent=1) + "\n")
(HERE / "p16_derive_out.txt").write_text("\n".join(OUT) + "\n")
print(f"\npinned: dalembertian max {peak_v:.3f} at s = {peak_s:.2f}; links {Lpin}; "
      f"walk anchors OK; ladder N = {NLADDER} x 3 seeds")
sys.exit(1 if FAILED else 0)
