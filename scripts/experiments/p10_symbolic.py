#!/usr/bin/env python3
"""P-10 step 1, run and committed BEFORE any Monte Carlo: the
Myrheim-Meyer order-to-dimension null, derived by direct integration.

Setting. N points sprinkled uniformly into the causal interval
(Alexandrov set) I(p,q) between p = (0, 0vec) and q = (1, 0vec) in
d-dimensional Minkowski space, signature (+,-,...,-). x precedes y iff
t_y - t_x > |vec y - vec x|. R = number of causally related UNORDERED
pairs; the null is f(d) = E[R] / C(N,2).

Geometry used (each piece checked below):
  - in coordinates (t, r), r = |vec x|, the interval is
    0 <= r <= m(t) = min(t, 1-t); its volume element is
    S_d r^(d-2) dr dt with S_d the area of the unit (d-2)-sphere
    (S_2 = 2, S_3 = 2*pi, S_4 = 4*pi);
  - for x in I, the future-related fraction is vol(I(x,q))/V =
    tau(x,q)^d, tau^2 = (1-t)^2 - r^2 (scaling + Lorentz invariance
    of the interval volume; total proper time 1); likewise the past.
    So g(x) := P(random point related to x) = tau(p,x)^d + tau(x,q)^d
    and f(d) = E[g] = 2 * I_J(d) / I_V(d), with
    I_V = int int r^(d-2) dr dt,  I_J = int int r^(d-2) tau(x,q)^d dr dt
    (the S_d factor cancels in every ratio).

Arithmetic: exact fractions.Fraction wherever the integrand is
polynomial (d = 1, 2, 4, and the elementary antiderivative pieces of
d = 3); deterministic composite-Simpson quadrature with
refinement-based error control elsewhere. No random numbers anywhere
in this file.

Variance of R, derived (not binomial): R = sum over pairs of
indicators X_ij; disjoint pairs are independent; pairs sharing a
point have Cov = E[g^2] - f^2 (conditional independence given the
shared point). Hence, for fixed N,
    Var(R) = C(N,2) f(1-f) + 6 C(N,3) (E[g^2] - f^2)
and the binomial first term alone UNDERESTIMATES the spread (the
correction is derived and tabulated below; it dominates for large N).

Mutant nulls, derived in advance:
  - d = 2, permute one lightcone coordinate across points: in
    lightcone coordinates the d = 2 sprinkle is an iid product
    measure on the unit square, so the permutation is a
    distributional symmetry: f stays 1/2 identically.
  - any d, permute the t coordinate across points (spatial parts
    kept): each pair becomes (t from the t-marginal, x from the
    spatial marginal), all four independent, so
    f_shuf(d) = P(|t1 - t2| > |x1 - x2|), computed by quadrature.
    At d = 2 the t- and x-marginals are the SAME triangle density,
    so |dt| and |dx| are iid and f_shuf(2) = 1/2 = f(2): the t-shuffle
    is ALSO ineffective at d = 2 (in the mean). At d = 3, 4 it lands
    at d* = f^-1(f_shuf) far from d.

Prints one line per checked equality:
    EQ k PASS/FAIL <description>: <lhs> = <rhs> (delta ...)
then the registered band table. Exit 0 iff every EQ passes.
"""
import math
import sys
from fractions import Fraction as Fr
from math import comb

FAILED = []


def eq(k, desc, lhs, rhs, tol=0.0):
    if isinstance(lhs, Fr) and isinstance(rhs, Fr):
        delta = abs(lhs - rhs)
        ok = delta == 0
        print(f"EQ {k} {'PASS' if ok else 'FAIL'} {desc}: {lhs} = {rhs} "
              f"(delta {float(delta):.3e})")
    else:
        lf, rf = float(lhs), float(rhs)
        delta = abs(lf - rf)
        ok = delta <= tol
        print(f"EQ {k} {'PASS' if ok else 'FAIL'} {desc}: {lf:.12g} = {rf:.12g} "
              f"(delta {delta:.3e}, tol {tol:.1e})")
    if not ok:
        FAILED.append(k)


# ----- exact bivariate polynomials over Q: dict {(i,j): c} = c t^i r^j -----

def bmul(A, B):
    out = {}
    for (i, j), a in A.items():
        for (k, l), b in B.items():
            out[(i + k, j + l)] = out.get((i + k, j + l), Fr(0)) + a * b
    return {k: v for k, v in out.items() if v != 0}


def badd(A, B):
    out = dict(A)
    for k, v in B.items():
        out[k] = out.get(k, Fr(0)) + v
    return {k: v for k, v in out.items() if v != 0}


def bpow(A, n):
    out = {(0, 0): Fr(1)}
    for _ in range(n):
        out = bmul(out, A)
    return out


def int_r_to_m(A, m_is_t):
    """int_0^m A(t,r) dr as a univariate poly {power: coeff} in t,
    with m = t (True) or m = 1-t (False)."""
    uni = {}
    for (i, j), a in A.items():
        c = a / (j + 1)                       # int r^j = m^(j+1)/(j+1)
        if m_is_t:
            uni[i + j + 1] = uni.get(i + j + 1, Fr(0)) + c
        else:                                  # t^i (1-t)^(j+1), expanded
            for kk in range(j + 2):
                uni[i + kk] = uni.get(i + kk, Fr(0)) \
                    + c * comb(j + 1, kk) * (Fr(-1) ** kk)
    return uni


def u_intdef(U, lo, hi):
    lo, hi = Fr(lo), Fr(hi)
    return sum(c * (hi ** (p + 1) - lo ** (p + 1)) / (p + 1)
               for p, c in U.items())


def exact_tr(A):
    """int_0^1 dt int_0^{min(t,1-t)} A(t,r) dr, exact."""
    return u_intdef(int_r_to_m(A, True), 0, Fr(1, 2)) \
        + u_intdef(int_r_to_m(A, False), Fr(1, 2), 1)


TP2 = {(2, 0): Fr(1), (0, 2): Fr(-1)}                     # tau(p,x)^2 = t^2 - r^2
TQ2 = {(0, 0): Fr(1), (1, 0): Fr(-2), (2, 0): Fr(1),      # tau(x,q)^2
       (0, 2): Fr(-1)}                                    # = (1-t)^2 - r^2
R0, R1, R2 = {(0, 0): Fr(1)}, {(0, 1): Fr(1)}, {(0, 2): Fr(1)}


# ----- deterministic quadrature (composite Simpson, refinement error) -----

def simpson_w(n):
    w = [2.0] * (n + 1)
    w[0] = w[-1] = 1.0
    for i in range(1, n, 2):
        w[i] = 4.0
    return w


def quad1(f, a, b, n):
    w = simpson_w(n)
    h = (b - a) / n
    return h / 3.0 * sum(wi * f(a + i * h) for i, wi in enumerate(w))


def quad1_ref(f, a, b, n=512):
    c, fine = quad1(f, a, b, n), quad1(f, a, b, 2 * n)
    return fine, abs(fine - c)


def quad2(h, nt, ns):
    """int_0^1 dt m(t) int_0^1 ds h(t, r = m(t) s); Simpson x Simpson."""
    wt, ws = simpson_w(nt), simpson_w(ns)
    tot = 0.0
    for it in range(nt + 1):
        t = it / nt
        m = t if t <= 0.5 else 1.0 - t
        if m == 0.0:
            continue
        row = 0.0
        for js in range(ns + 1):
            row += ws[js] * h(t, m * (js / ns))
        tot += wt[it] * m * row
    return tot / (3.0 * nt) / (3.0 * ns)


def quad2_ref(h, n=256):
    c, fine = quad2(h, n, n), quad2(h, 2 * n, 2 * n)
    return fine, abs(fine - c)


def clamp(x):
    return x if x > 0.0 else 0.0


# =====================  A. the closed form f(d)  =====================

print("# A. related-pair fraction f(d) by direct integration")

# EQ 1-3: interval volumes I_V (exact) vs quadrature and vs the
# closed form V_d = omega_{d-1} / (d 2^{d-1}), omega_k = unit-ball vol.
IV = {2: exact_tr(R0), 3: exact_tr(R1), 4: exact_tr(R2)}
S = {2: 2.0, 3: 2.0 * math.pi, 4: 4.0 * math.pi}


def ball_vol(k):
    return math.pi ** (k / 2) / math.gamma(k / 2 + 1)


k_eq = 1
for d in (2, 3, 4):
    Vd = ball_vol(d - 1) / (d * 2 ** (d - 1))
    eq(k_eq, f"d={d} interval volume S_d*I_V vs omega/(d 2^(d-1))",
       S[d] * float(IV[d]), Vd, tol=1e-12)
    k_eq += 1

q, err = quad2_ref(lambda t, r: r)
eq(4, "d=3 I_V exact vs Simpson quadrature", float(IV[3]), q,
   tol=max(4 * err, 1e-9))

# EQ 5: d=1 (no spatial direction): p_ord = int_0^1 (1-t) dt = 1/2.
IJ1 = u_intdef({0: Fr(1), 1: Fr(-1)}, 0, 1)
eq(5, "d=1 ordered-pair integral int(1-t)dt", IJ1, Fr(1, 2))
f_exact = {1: 2 * IJ1}                       # f(1) = 1: every pair related

# EQ 6: d=2, lightcone coordinates u,v iid uniform on the unit square:
# p_ord = int int (1-u)(1-v) du dv = 1/4 (independent derivation).
one_minus = {0: Fr(1), 1: Fr(-1)}
p_ord_uv = u_intdef(one_minus, 0, 1) ** 2
eq(6, "d=2 p_ord in lightcone coords", p_ord_uv, Fr(1, 4))

# EQ 7: same number from (t,r) coordinates: I_J(2)/I_V(2).
IJ = {2: exact_tr(bmul(R0, TQ2))}
eq(7, "d=2 p_ord (t,r) vs lightcone parameterisations",
   IJ[2] / IV[2], p_ord_uv)
f_exact[2] = 2 * IJ[2] / IV[2]

# d=3: I_J(3) = int int r ((1-t)^2 - r^2)^(3/2) dr dt. Inner
# antiderivative: -((1-t)^2 - r^2)^(5/2) / 5. With m = min(t,1-t):
#   inner = ((1-t)^5 - ((1-t)^2 - m^2)^(5/2)) / 5
#   t <= 1/2: (1-t)^2 - t^2 = 1 - 2t;  t >= 1/2: the bracket is 0.
# So I_J(3) = (1/5) [ int_0^1 (1-t)^5 dt - int_0^{1/2} (1-2t)^(5/2) dt ]
#           = (1/5) [ 1/6 - 1/7 ] = 1/210
# using int_0^{1/2} (1-2t)^(p/2) dt = [-(1-2t)^((p+2)/2) / (p+2)] = 1/(p+2).
one_minus_t5 = {kk: Fr(comb(5, kk) * (-1) ** kk) for kk in range(6)}
IJ[3] = (u_intdef(one_minus_t5, 0, 1) - Fr(1, 5 + 2)) / 5
eq(8, "d=3 I_J exact pieces", IJ[3], Fr(1, 210))
q, err = quad2_ref(lambda t, r: r * clamp((1 - t) ** 2 - r * r) ** 1.5)
eq(9, "d=3 I_J exact vs Simpson quadrature", float(IJ[3]), q,
   tol=max(4 * err, 1e-9))
f_exact[3] = 2 * IJ[3] / IV[3]

# d=4: fully polynomial.
IJ[4] = exact_tr(bmul(R2, bpow(TQ2, 2)))
q, err = quad2_ref(lambda t, r: r * r * ((1 - t) ** 2 - r * r) ** 2)
eq(10, "d=4 I_J exact vs Simpson quadrature", float(IJ[4]), q,
   tol=max(4 * err, 1e-9))
f_exact[4] = 2 * IJ[4] / IV[4]

print(f"# derived: f(1) = {f_exact[1]}, f(2) = {f_exact[2]}, "
      f"f(3) = {f_exact[3]}, f(4) = {f_exact[4]}")

# EQ 11-14: against the literature Gamma form
# G(d) = Gamma(d+1) Gamma(d/2) / (4 Gamma(3d/2))  (Myrheim 1978, Meyer
# 1988). The integrals show G(d) is the ORDERED-pair probability: the
# related-pair fraction is f(d) = 2 G(d). (At d=2: G = 1/4, f = 1/2;
# the factor 2 is convention, not a discrepancy - both conventions
# appear in the literature; E[R]/C(N,2) with R counting unordered
# related pairs is unambiguously 2 G(d).)


def gamma_form(d):
    return math.exp(math.lgamma(d + 1) + math.lgamma(d / 2)
                    - math.lgamma(1.5 * d)) / 4.0


for d in (1, 2, 3, 4):
    eq(10 + d, f"d={d} related fraction f vs 2x Gamma form",
       float(f_exact[d]), 2 * gamma_form(d), tol=1e-12)


def F(d):
    """Related-pair fraction as a function of continuous d (Gamma
    form, anchored to the direct integrals at d = 1..4 by EQ 11-14)."""
    return 2.0 * gamma_form(d)


def dF(d, h=1e-6):
    return (F(d + h) - F(d - h)) / (2 * h)


def d2F(d, h=1e-4):
    return (F(d + h) - 2 * F(d) + F(d - h)) / (h * h)


# EQ 15: F is strictly decreasing on the inversion domain.
grid = [1.0 + 0.05 * i for i in range(int((16 - 1) / 0.05) + 1)]
mono = all(F(a) > F(b) for a, b in zip(grid, grid[1:]))
eq(15, "F strictly decreasing on [1,16] (0.05 grid)",
   1.0 if mono else 0.0, 1.0, tol=0.0)


def invert(fv, lo=1.0, hi=24.0):
    """Bisection solve F(d) = fv; F decreasing (EQ 15)."""
    if fv >= F(lo):
        return lo
    if fv <= F(hi):
        return hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if F(mid) > fv:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


for i, d in enumerate((2, 3, 4)):
    eq(16 + i, f"inversion round-trip F^-1(f({d}))",
       invert(float(f_exact[d])), float(d), tol=1e-9)

# =====================  B. variance of R, derived  =====================

print("# B. pair-variance of R: E[g^2] with g = tau_p^d + tau_q^d")

# EQ 19: d=2, E[g^2] two ways. Lightcone: g = uv + (1-u)(1-v);
# E[g^2] = E[u^2]E[v^2] + 2 E[u(1-u)] E[v(1-v)] + E[(1-u)^2]E[(1-v)^2].
u2 = u_intdef({2: Fr(1)}, 0, 1)
u1mu = u_intdef({1: Fr(1), 2: Fr(-1)}, 0, 1)
om2 = u_intdef({0: Fr(1), 1: Fr(-2), 2: Fr(1)}, 0, 1)
Eg2_uv = u2 * u2 + 2 * u1mu * u1mu + om2 * om2
G2 = badd(TP2, TQ2)
Eg2 = {2: exact_tr(bmul(R0, bpow(G2, 2))) / IV[2]}
eq(19, "d=2 E[g^2] (t,r) vs lightcone parameterisations",
   Eg2[2], Eg2_uv)
print(f"# derived: E[g^2](2) = {Eg2[2]}")

# d=4: fully polynomial, plus quadrature cross-check.
G4 = badd(bpow(TP2, 2), bpow(TQ2, 2))
Eg2[4] = exact_tr(bmul(R2, bpow(G4, 2))) / IV[4]


def g4(t, r):
    a = clamp(t * t - r * r) ** 2
    b = clamp((1 - t) ** 2 - r * r) ** 2
    return r * r * (a + b) ** 2


q, err = quad2_ref(g4)
eq(20, "d=4 E[g^2] exact vs Simpson quadrature",
   float(Eg2[4]), q / float(IV[4]), tol=max(4 * err, 1e-9))
print(f"# derived: E[g^2](4) = {Eg2[4]}")

# d=3: (a^3+b^3)^2 = a^6 + b^6 (polynomial) + 2 (ab)^3 with a,b the
# proper times; the cross term needs (a^2 b^2)^(3/2) -> quadrature.
poly_part = exact_tr(bmul(R1, badd(bpow(TP2, 3), bpow(TQ2, 3))))


def g3cross(t, r):
    return r * 2.0 * (clamp(t * t - r * r)
                      * clamp((1 - t) ** 2 - r * r)) ** 1.5


qc, errc = quad2_ref(g3cross)
Eg2[3] = (float(poly_part) + qc) / float(IV[3])
qc2, errc2 = quad2_ref(lambda t, r: r * ((clamp(t * t - r * r) ** 1.5
                                          + clamp((1 - t) ** 2 - r * r) ** 1.5) ** 2))
eq(21, "d=3 E[g^2] poly+cross vs single quadrature",
   Eg2[3], qc2 / float(IV[3]), tol=max(4 * (errc + errc2), 1e-8))
print(f"# derived: E[g^2](3) = {Eg2[3]:.10f}  "
      f"(polynomial part {poly_part} / I_V, cross term by quadrature, "
      f"refinement error {errc:.1e})")

K2 = {d: float(Eg2[d]) - float(f_exact[d]) ** 2 for d in (2, 3, 4)}

# =====================  C. mutant nulls, derived  =====================

print("# C. mutant nulls")

# EQ 22: d=2 lightcone shuffle. u and v are independent, so permuting
# the v list across points leaves the pair law iid-uniform-product:
# f_lc = 2 P(u1<u2) P(v1<v2) = 2 * (1/2)*(1/2) = 1/2 = f(2).
Pu = u_intdef(one_minus, 0, 1)               # P(u1 < u2) = int (1-u) du
eq(22, "d=2 lightcone-shuffle fraction 2*P(u<)P(v<) vs f(2)",
   2 * Pu * Pu, f_exact[2])

# t-shuffle: marginals of the interval.
# time marginal: p_t(t) = d 2^(d-1) m(t)^(d-1)  (cross-section volume,
#   normalised: int m^(d-1) dt = 2^(1-d)/d);  exact CDF piecewise:
#   P_t(t) = 2^(d-1) t^d (t<=1/2),  1 - 2^(d-1)(1-t)^d (t>1/2).
# spatial radial marginal (D = d-1 spatial dims): available t-range at
#   radius r is 1-2r, so p_r(r) = 2^D D(D+1) r^(D-1)(1-2r) on [0,1/2].

# EQ 23: at d=2 the time marginal 4*min(t,1-t) equals the spatial
# marginal density 2(1-2|x|) shifted by 1/2: with s = t - 1/2,
# p_t(1/2+s) = 2 - 4|s| = p_x(s). Hence |t1-t2| and |x1-x2| are iid
# and f_shuf(2) = P(A > B) = 1/2 exactly.
pt_right = {0: Fr(4), 1: Fr(-4)}     # 4(1-t) for t>1/2 -> in s: 2-4s
pt_in_s = {0: Fr(2), 1: Fr(-4)}      # substitute t = 1/2 + s, s>0
px_in_s = {0: Fr(2), 1: Fr(-4)}      # 2(1-2s), s = |x| > 0
eq(23, "d=2 time marginal == spatial marginal (as polys in |s|)",
   Fr(sum(abs(pt_in_s[k] - px_in_s[k]) for k in pt_in_s)), Fr(0))
# consistency of the shift: 4(1-(1/2+s)) == 2-4s
eq(24, "d=2 marginal shift algebra", u_intdef(pt_right, Fr(1, 2), 1),
   u_intdef({0: Fr(2), 1: Fr(-4)}, 0, Fr(1, 2)))


def Pt_cdf(d, t):
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    if t <= 0.5:
        return 2 ** (d - 1) * t ** d
    return 1.0 - 2 ** (d - 1) * (1 - t) ** d


def pt_pdf(d, t):
    m = t if t <= 0.5 else 1.0 - t
    return d * 2 ** (d - 1) * m ** (d - 1)


def make_cdf_A(d, na=1600, ns=1024):
    """CDF of A = |t1 - t2|, t iid from the time marginal; the inner
    CDF is exact, the outer integral is Simpson."""
    def cdf(a, n):
        if a <= 0.0:
            return 0.0
        if a >= 1.0:
            return 1.0
        return quad1(lambda t: pt_pdf(d, t)
                     * (Pt_cdf(d, min(t + a, 1.0))
                        - Pt_cdf(d, max(t - a, 0.0))), 0.0, 1.0, n)
    tab = [cdf(i / na, ns) for i in range(na + 1)]
    errchk = max(abs(cdf(a, 2 * ns) - cdf(a, ns)) for a in (0.1, 0.3, 0.6))

    def interp(x):
        if x <= 0.0:
            return 0.0
        if x >= 1.0:
            return 1.0
        u = x * na
        i = int(u)
        if i >= na:
            return 1.0
        w = u - i
        return tab[i] * (1 - w) + tab[i + 1] * w
    return interp, errchk


def pr_pdf(d, r):
    D = d - 1
    return (2 ** D) * D * (D + 1) * r ** (D - 1) * (1 - 2 * r)


def f_shuffled(d, cdfA, nr, nang):
    """P(|t1-t2| > |x1-x2|) with all four coordinates independent,
    drawn from the interval's marginals (the t-shuffled null)."""
    wr = simpson_w(nr)
    hr = 0.5 / nr
    rs = [i * hr for i in range(nr + 1)]
    ps = [pr_pdf(d, r) for r in rs]
    tot = 0.0
    if d == 2:
        for i, r1 in enumerate(rs):
            for j, r2 in enumerate(rs):
                # signs of x are +-, independent, prob 1/2 each branch
                v = 0.5 * (1.0 - cdfA(abs(r1 - r2))) \
                    + 0.5 * (1.0 - cdfA(r1 + r2))
                tot += wr[i] * wr[j] * ps[i] * ps[j] * v
        return tot * (hr / 3.0) ** 2
    wa = simpson_w(nang)
    if d == 3:                       # angle phi uniform on [0, 2pi)
        ha = math.pi / nang          # integrate [0,pi], weight 1/pi
        angs = [math.cos(k * ha) for k in range(nang + 1)]
        wgt = 1.0 / math.pi
    else:                            # d = 4: cos(theta) uniform on [-1,1]
        ha = 2.0 / nang
        angs = [-1.0 + k * ha for k in range(nang + 1)]
        wgt = 0.5
    for i, r1 in enumerate(rs):
        for j, r2 in enumerate(rs):
            pij = ps[i] * ps[j] * wr[i] * wr[j]
            if pij == 0.0:
                continue
            row = 0.0
            for k, c in enumerate(angs):
                B = math.sqrt(clamp(r1 * r1 + r2 * r2 - 2 * r1 * r2 * c))
                row += wa[k] * (1.0 - cdfA(B))
            tot += pij * row
    return tot * (hr / 3.0) ** 2 * (ha / 3.0) * wgt


F_SHUF = {}
k_eq = 25
for d in (2, 3, 4):
    cdfA, cerr = make_cdf_A(d)
    coarse = f_shuffled(d, cdfA, 48, 48)
    fine = f_shuffled(d, cdfA, 80, 80)
    F_SHUF[d] = fine
    tol = max(6 * (abs(fine - coarse) + cerr), 2e-4)
    if d == 2:
        eq(k_eq, "d=2 t-shuffle fraction (quadrature) vs derived 1/2",
           fine, 0.5, tol=max(tol, 2e-3))
    else:
        eq(k_eq, f"d={d} t-shuffle fraction refinement (coarse vs fine)",
           coarse, fine, tol=tol)
    k_eq += 1

DSTAR = {d: invert(F_SHUF[d]) for d in (3, 4)}
print(f"# derived t-shuffled nulls: f_shuf(2) = {F_SHUF[2]:.6f} (= f(2): "
      f"mutant ineffective at d=2 by EQ 22-25), "
      f"f_shuf(3) = {F_SHUF[3]:.6f} -> d* = {DSTAR[3]:.4f}, "
      f"f_shuf(4) = {F_SHUF[4]:.6f} -> d* = {DSTAR[4]:.4f}")

# =====================  D. registered band table  =====================

print("# D. registered bands: |mean_M d_hat - d| <= band, with")
print("#    sigma_f^2 = [C(N,2) f(1-f) + 6 C(N,3) k2] / C(N,2)^2,")
print("#    k2 = E[g^2]-f^2; sigma_d = sigma_f/|F'(d)|;")
print("#    bias = -F'' sigma_f^2 / (2 F'^3)  (delta method);")
print("#    band = |bias| + 4 sigma_d / sqrt(M).")
N_GRID = [128, 256, 512, 1024, 2048, 4096, 8192]
M_SCHED = {128: 40, 256: 40, 512: 40, 1024: 40, 2048: 24, 4096: 16, 8192: 12}
print("# BAND d N M f sigma_f sigma_d bias band binom_underest_factor")
for d in (2, 3, 4):
    fd = float(f_exact[d])
    fp, fpp = dF(d), d2F(d)
    for N in N_GRID:
        C2 = N * (N - 1) // 2
        C3 = N * (N - 1) * (N - 2) // 6
        var_f = (C2 * fd * (1 - fd) + 6 * C3 * K2[d]) / C2 ** 2
        s_f = math.sqrt(var_f)
        s_bin = math.sqrt(fd * (1 - fd) / C2)
        s_d = s_f / abs(fp)
        bias = -fpp * var_f / (2 * fp ** 3)
        M = M_SCHED[N]
        band = abs(bias) + 4 * s_d / math.sqrt(M)
        print(f"BAND {d} {N} {M} {fd:.10f} {s_f:.6e} {s_d:.6e} "
              f"{bias:+.3e} {band:.6f} {s_f / s_bin:.2f}")

print(f"# EQ summary: {('ALL PASS' if not FAILED else 'FAILED: ' + str(FAILED))}")
sys.exit(0 if not FAILED else 1)
