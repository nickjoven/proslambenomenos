#!/usr/bin/env python3
"""P-14 derivation layer (pre-registration): the commutator kernel is
spectrally audible - everything here is derived BEFORE the registered
eigensolves run, and every "=" is checked by the stdlib CAS (symb.py)
or by exact closed form.

Setup. Continuum substrate on x in [0, L], L = 1500, with the P-13
speed profile c(x): 1.0 for x <= 150, linear down to 0.5 at x = 1350,
then 0.5. Two substrates share this c (the metric) and differ in
impedance Z:
    ramp    rho = 1/c^2, T = 1      => Z = 1/c   (Z varies x2)
    zramp   rho = 1/c,   T = c      => Z = 1     (Z constant)
In travel-time coordinates tau (dtau = dx/c) the wave equation
becomes Schrodinger form with potential V = (d^2/dtau^2 sqrt(Z)) /
sqrt(Z): the metric is gauged away entirely; V is pure impedance.

Derived facts (each an EQ line):
  EQ1  log-derivative identity  d/dtau(w'/w) = w''/w - (w'/w)^2.
  EQ2  for c = 1 + b x and Z = 1/c:  V = c (c (sqrt(Z))')' / sqrt(Z)
       = b^2/4, a CONSTANT on the ramp (CAS, sampled box).
  EQ3  zramp: Z = sqrt((1/c) * c) = 1 identically  =>  V = 0.
  EQ4  the numbers: b = -0.5/1200; V0 = b^2/4; ramp travel time
       T_r = ln(1+b*1200)/b; total T = 150 + T_r + 300.
  EQ5  antiderivative check for the first-order shifts:
       d/dtau [tau/2 - (T/(4 k pi)) sin(2 k pi tau / T)]
       = sin^2(k pi tau / T)  (CAS), giving the exact k-resolved
       prediction  shift_k = (2 V0 / T) * S(tau1, tau2, k)  with
       S the closed-form integral over the ramp's tau-interval.
  EQ6  eigensolver validation: Sturm-sequence bisection on the
       symmetrized tridiagonal reproduces the uniform chain's exact
       Dirichlet spectrum (4/a^2) sin^2(k pi / (2(n+1))) to 1e-12.
  EQ7  commutator isometry: the weighted-Dirac seminorm distance
       end-to-end (sum of local slowness) agrees between ramp and
       zramp within O(1/n) and converges to the continuum T.

Pinned outputs -> p14_registration.json: shift_k for k = 1..80,
V0, Vbar, T, tolerances, grid sizes.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from symb import N, V as Vr, add, sub, mul, div, powe, sqrt, sin, cos, exp, log, d, equal, simpson  # noqa: E402

L = 1500.0
X0, X1 = 150.0, 1350.0
C_MIN = 0.5
B = (C_MIN - 1.0) / (X1 - X0)          # -0.5/1200

OUT, FAILED = [], []


def eq(n, ok, statement, detail):
    line = f"EQ {n} {'PASS' if ok else 'FAIL'}  {statement}  | {detail}"
    OUT.append(line)
    print(line)
    if not ok:
        FAILED.append(n)


def c_of(x):
    if x <= X0:
        return 1.0
    if x >= X1:
        return C_MIN
    return 1.0 + B * (x - X0)


# EQ1: log-derivative identity for two concrete w(tau)
t = Vr("t")
for i, w in enumerate((exp(mul(N(0.3), sin(t))),
                       add(N(2), powe(add(N(1), mul(N(0.2), t)), N(-0.5))))):
    lhs = d(div(d(w, "t"), w), "t")
    rhs = sub(div(d(d(w, "t"), "t"), w), powe(div(d(w, "t"), w), N(2)))
    ok, worst, nv = equal(lhs, rhs, {"t": (0.1, 3.0)})
    if i == 0:
        ok1, w1 = ok, worst
    else:
        eq(1, ok1 and ok, "d/dtau(w'/w) = w''/w - (w'/w)^2",
           f"two concrete w, worst rel delta {max(w1, worst):.2e}")

# EQ2: ramp potential is the constant b^2/4
x, b = Vr("x"), Vr("b")
cE = add(N(1), mul(b, x))
w = powe(cE, N(-0.5))                    # sqrt(Z) = c^(-1/2)
VE = div(mul(cE, d(mul(cE, d(w, "x")), "x")), w)
ok, worst, nv = equal(VE, mul(N(0.25), b, b),
                      {"x": (0.0, 1150.0), "b": (-4.1e-4, -1.1e-4)})
eq(2, ok, "c = 1+bx, Z = 1/c  =>  V = c(c sqrtZ')'/sqrtZ = b^2/4 (constant)",
   f"worst rel delta {worst:.2e} over the sampled (x, b) box")

# EQ3: zramp Z = 1 identically
ZE = sqrt(mul(div(N(1), cE), cE))
ok, worst, nv = equal(ZE, N(1), {"x": (0.0, 1150.0), "b": (-4.1e-4, -1.1e-4)})
eq(3, ok, "zramp: Z = sqrt((1/c) c) = 1  =>  V = 0", f"worst rel delta {worst:.2e}")

# EQ4: the numbers
V0 = B * B / 4.0
T_r = math.log(1.0 + B * (X1 - X0)) / B
T_r_quad = simpson(lambda xx: 1.0 / c_of(xx), X0, X1)
T_tot = X0 + T_r + (L - X1) / C_MIN
ok4 = abs(T_r - T_r_quad) < 1e-7 * T_r
eq(4, ok4, "V0 = b^2/4; T_r = ln(1+b Dx)/b; T = 150 + T_r + 300",
   f"V0 = {V0:.6e}; T_r = {T_r:.6f} (quad {T_r_quad:.6f}); T = {T_tot:.6f}")

# EQ5: antiderivative for the shift integral, then the shifts
k = Vr("k")
F = sub(mul(N(0.5), t), mul(div(N(T_tot), mul(N(4 * math.pi), k)),
                            sin(div(mul(N(2 * math.pi), k, t), N(T_tot)))))
ok, worst, nv = equal(d(F, "t"), powe(sin(div(mul(N(math.pi), k, t), N(T_tot))), N(2)),
                      {"t": (1.0, T_tot - 1.0), "k": (1.0, 80.0)})
tau1, tau2 = X0, X0 + T_r


def Sint(kk):
    def prim(tt):
        return 0.5 * tt - (T_tot / (4 * math.pi * kk)) * math.sin(2 * math.pi * kk * tt / T_tot)
    return prim(tau2) - prim(tau1)


shifts = {kk: (2.0 * V0 / T_tot) * Sint(kk) for kk in range(1, 81)}
Vbar = V0 * T_r / T_tot
ok5 = ok and abs(sum(shifts[kk] for kk in range(60, 81)) / 21 - Vbar) < 0.05 * Vbar
eq(5, ok5, "shift_k = (2 V0/T) int_ramp sin^2(k pi tau/T) dtau, -> Vbar = V0 T_r/T",
   f"antiderivative worst {worst:.2e}; Vbar = {Vbar:.6e}; "
   f"mean shift(k=60..80) = {sum(shifts[kk] for kk in range(60, 81))/21:.6e}")


# EQ6: Sturm bisection vs the uniform chain's exact spectrum
def sturm_count(diag, off, lam):
    cnt = 0
    q = diag[0] - lam
    if q < 0:
        cnt += 1
    for i in range(1, len(diag)):
        e2 = off[i - 1] * off[i - 1]
        q = diag[i] - lam - (e2 / q if q != 0 else e2 / 1e-300)
        if q < 0:
            cnt += 1
    return cnt


def sturm_eigs(diag, off, kmax, lo, hi, iters=100):
    out = []
    for kk in range(1, kmax + 1):
        a_, b_ = lo, hi
        for _ in range(iters):
            mid = 0.5 * (a_ + b_)
            if sturm_count(diag, off, mid) >= kk:
                b_ = mid
            else:
                a_ = mid
        out.append(0.5 * (a_ + b_))
    return out


n6 = 200
a6 = 1.0
diag = [2.0] * n6
off = [-1.0] * (n6 - 1)
eig = sturm_eigs(diag, off, 20, 0.0, 4.1)
exact = [4 * math.sin(kk * math.pi / (2 * (n6 + 1))) ** 2 for kk in range(1, 21)]
worst6 = max(abs(e - x_) / x_ for e, x_ in zip(eig, exact))
eq(6, worst6 < 1e-12, "Sturm bisection = (4/a^2) sin^2(k pi/(2(n+1))) on the uniform chain",
   f"worst rel dev {worst6:.2e} over k = 1..20, n = {n6}")


# EQ7: commutator-isometry - end-to-end seminorm distance per profile
def chain(profile, n):
    a = L / (n + 1)
    if profile == "ramp":
        rho = lambda xx: 1.0 / c_of(xx) ** 2   # noqa: E731
        Tt = lambda xx: 1.0                    # noqa: E731
    else:
        rho = lambda xx: 1.0 / c_of(xx)        # noqa: E731
        Tt = lambda xx: c_of(xx)               # noqa: E731
    m = [a * rho(i * a) for i in range(1, n + 1)]
    J = [Tt((i + 0.5) * a) / a for i in range(0, n + 1)]
    return a, m, J


def t_disc(profile, n):
    a, m, J = chain(profile, n)
    tot = 0.0
    for i in range(n + 1):
        mbar = a * (1.0 / c_of(max(i, 0.5) * a) ** (2 if profile == "ramp" else 1))
        c_e = math.sqrt(J[i] * a * a / mbar)
        tot += a / c_e
    return tot


rows7, ok7 = [], True
prev = None
for n7 in (1499, 2999):
    tr, tz = t_disc("ramp", n7), t_disc("zramp", n7)
    dev = abs(tr - tz) / T_tot
    conv = max(abs(tr - T_tot), abs(tz - T_tot)) / T_tot
    ok7 = ok7 and dev < 5e-3 and conv < 5e-3
    if prev is not None:
        ok7 = ok7 and dev < prev
    prev = dev
    rows7.append(f"n={n7}: T_ramp {tr:.4f}, T_zramp {tz:.4f}, "
                 f"rel split {dev:.2e}, rel dev from continuum {conv:.2e}")
eq(7, ok7, "seminorm end-to-end distance: ramp = zramp within O(1/n), both -> T",
   "; ".join(rows7))

pin = {"L": L, "B": B, "V0": V0, "T_ramp": T_r, "T_total": T_tot, "Vbar": Vbar,
       "tau_ramp": [tau1, tau2],
       "shifts": {str(kk): shifts[kk] for kk in range(1, 81)},
       "grids": [1499, 2999], "k_window": [5, 60], "n_eigs": 80,
       "tolerances": {"weyl_rel": 2e-3, "not_isospectral_min": 1e-9,
                      "shift_rms_over_vbar": 0.3, "t_disc_split_rel": 5e-3}}
(HERE / "p14_registration.json").write_text(json.dumps(pin, indent=1) + "\n")
(HERE / "p14_derive_out.txt").write_text("\n".join(OUT) + "\n")
print(f"\npinned: V0 = {V0:.6e}, Vbar = {Vbar:.6e}, T = {T_tot:.6f}, "
      f"80 k-resolved shifts")
sys.exit(1 if FAILED else 0)
