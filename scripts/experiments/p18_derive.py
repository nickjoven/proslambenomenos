#!/usr/bin/env python3
"""P-18 derivation layer (pre-registration): the C2 retest of P-14's
fired k-resolved clause. Everything here is derived BEFORE the
registered eigensolves run; every "=" is checked by the stdlib CAS
(symb.py) or by exact closed form.

Setup. Same geometry as P-14 - x in [0, L], L = 1500, c: 1.0 down to
0.5 across [150, 1350] - but the ramp is now the QUINTIC smoothstep
    c(x) = 1 - 0.5 s(u),  u = (x - 150)/1200,  s = 6u^5 - 15u^4 + 10u^3,
which has s' = s'' = 0 at both ends: c is C2 everywhere. The same two
substrates share this c and differ in impedance:
    sramp    rho = 1/c^2, T = 1   =>  Z = 1/c
    szramp   rho = 1/c,   T = c   =>  Z = 1  (V = 0)
P-14's diagnosis blamed the C1 corners of the linear ramp (where c'
jumps, (sqrt Z)'' has distributional spikes) for the kink-localised
residual that killed clause d. If that diagnosis is right, removing
the corners must recover the zero-free-parameter first-order shifts.

Derived facts (each an EQ line):
  EQ1  general potential closed form: for Z = 1/c,
       V = c (c (c^{-1/2})')' / c^{-1/2} = c'^2/4 - c c''/2  (CAS, two
       concrete c's).
  EQ2  linear limit: c = 1 + bx has c'' = 0, so EQ1 gives V = b^2/4 -
       P-14's EQ2 recovered as the special case.
  EQ3  quintic endpoints: s(0) = 0, s(1) = 1, s' = s'' = 0 at both
       ends (exact CAS evaluation), so c' = c'' = 0 at the ramp edges
       and V vanishes THERE TOO: V is globally continuous, zero
       outside the ramp. No corners exist to blame.
  EQ4  szramp: Z = sqrt((1/c) c) = 1 identically for the quintic c.
  EQ5  the smoothness certificate: int_ramp V dtau =
       int_ramp c'^2/(4c) dx, because int (c c''/2)(dx/c) = [c'/2]
       vanishes at C2 edges. (For the linear ramp this boundary term
       is exactly the corner contribution that clause d ignored.)
  EQ6  the numbers: T_r = int dx/c (adaptive Simpson), T = 150 + T_r
       + 300; tau(x) by 4th-order cumulative Simpson; shift_k =
       (2/T) int_ramp V(x) sin^2(k pi tau(x)/T) dx/c(x) for k = 1..80
       by fine composite Simpson; Vbar_s = (1/T) int_ramp V dtau.
  EQ7  eigensolver validation: Sturm bisection reproduces the uniform
       chain's exact Dirichlet spectrum to 1e-12 (same tool as P-14).
  EQ8  Fourier decay: because V is continuous (only V' jumps at the
       edges), the oscillatory part |shift_k - Vbar_s| decays in k -
       the mean over k = 41..80 sits below the mean over k = 1..40.

Pinned outputs -> p18_registration.json: shift_k for k = 1..80,
Vbar_s, T, tolerances, grids, and the linear-control expectation.
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
DX = X1 - X0
C_MIN = 0.5

OUT, FAILED = [], []


def eq(n, ok, statement, detail):
    line = f"EQ {n} {'PASS' if ok else 'FAIL'}  {statement}  | {detail}"
    OUT.append(line)
    print(line)
    if not ok:
        FAILED.append(n)


# ---- the profile and its exact derivatives (checked below by CAS) ----
def s_of(u):
    return u * u * u * (10.0 + u * (-15.0 + 6.0 * u))


def sp_of(u):
    return 30.0 * u * u * (1.0 - u) * (1.0 - u)


def spp_of(u):
    return 60.0 * u * (1.0 - u) * (1.0 - 2.0 * u)


def c_of(x):
    if x <= X0:
        return 1.0
    if x >= X1:
        return C_MIN
    return 1.0 - 0.5 * s_of((x - X0) / DX)


def cp_of(x):
    if x <= X0 or x >= X1:
        return 0.0
    return -0.5 * sp_of((x - X0) / DX) / DX


def cpp_of(x):
    if x <= X0 or x >= X1:
        return 0.0
    return -0.5 * spp_of((x - X0) / DX) / (DX * DX)


def V_of(x):
    cp, cpp = cp_of(x), cpp_of(x)
    return 0.25 * cp * cp - 0.5 * c_of(x) * cpp


# EQ1: V = c(c (c^-1/2)')'/c^-1/2 = c'^2/4 - c c''/2, two concrete c's
t = Vr("t")
oks, worsts = [], []
for cE in (add(N(2), mul(N(0.3), sin(t))),
           add(N(1), powe(add(N(1), mul(N(0.2), t)), N(-0.5)))):
    w = powe(cE, N(-0.5))
    lhs = div(mul(cE, d(mul(cE, d(w, "t")), "t")), w)
    rhs = sub(mul(N(0.25), d(cE, "t"), d(cE, "t")),
              mul(N(0.5), cE, d(d(cE, "t"), "t")))
    ok, worst, nv = equal(lhs, rhs, {"t": (0.1, 3.0)})
    oks.append(ok)
    worsts.append(worst)
eq(1, all(oks), "Z = 1/c  =>  V = c(c(c^-1/2)')'/(c^-1/2) = c'^2/4 - c c''/2",
   f"two concrete c, worst rel delta {max(worsts):.2e}")

# EQ2: linear limit recovers P-14's constant b^2/4
x, b = Vr("x"), Vr("b")
cLin = add(N(1), mul(b, x))
rhsLin = sub(mul(N(0.25), d(cLin, "x"), d(cLin, "x")),
             mul(N(0.5), cLin, d(d(cLin, "x"), "x")))
ok, worst, nv = equal(rhsLin, mul(N(0.25), b, b),
                      {"x": (0.0, 1150.0), "b": (-4.1e-4, -1.1e-4)})
eq(2, ok, "linear c = 1+bx: c'' = 0  =>  V = b^2/4 (P-14 EQ2 as the special case)",
   f"worst rel delta {worst:.2e}")

# EQ3: quintic endpoint derivatives, exact CAS evaluation
u = Vr("u")
sE = add(mul(N(6), powe(u, N(5))), mul(N(-15), powe(u, N(4))),
         mul(N(10), powe(u, N(3))))
spE, sppE = d(sE, "u"), d(d(sE, "u"), "u")
from symb import ev  # noqa: E402
vals = [ev(e, {"u": uu}) for e in (sE, spE, sppE) for uu in (0.0, 1.0)]
targets = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
ok3 = all(abs(v - tgt) < 1e-14 for v, tgt in zip(vals, targets))
# and the coded derivatives match the CAS derivatives on the interior
okp, wp, _ = equal(spE, mul(N(30), u, u, sub(N(1), u), sub(N(1), u)), {"u": (0.0, 1.0)})
okpp, wpp, _ = equal(sppE, mul(N(60), u, sub(N(1), u), sub(N(1), mul(N(2), u))),
                     {"u": (0.0, 1.0)})
eq(3, ok3 and okp and okpp,
   "s(0)=0, s(1)=1, s'=s''=0 at both ends; coded s', s'' = CAS derivatives",
   f"endpoint vals {['%.1e' % v for v in vals]}; worst {max(wp, wpp):.2e}")

# EQ4: szramp Z = 1 identically for the quintic c
cQ = sub(N(1), mul(N(0.5), sE))
ZE = sqrt(mul(div(N(1), cQ), cQ))
ok, worst, nv = equal(ZE, N(1), {"u": (0.0, 1.0)})
eq(4, ok, "szramp: Z = sqrt((1/c) c) = 1  =>  V = 0", f"worst rel delta {worst:.2e}")

# EQ5: smoothness certificate - the boundary term vanishes
int_V_dtau = simpson(lambda xx: V_of(xx) / c_of(xx), X0, X1)
int_cp2 = simpson(lambda xx: cp_of(xx) ** 2 / (4.0 * c_of(xx)), X0, X1)
ok5 = abs(int_V_dtau - int_cp2) < 1e-9 * abs(int_cp2)
eq(5, ok5, "int_ramp V dtau = int_ramp c'^2/(4c) dx (C2 edges: [c'/2] = 0)",
   f"lhs {int_V_dtau:.9e}, rhs {int_cp2:.9e}, rel delta "
   f"{abs(int_V_dtau - int_cp2) / abs(int_cp2):.2e}")

# EQ6: the numbers - T, tau(x), the 80 pinned shifts
T_r = simpson(lambda xx: 1.0 / c_of(xx), X0, X1)
T_tot = X0 + T_r + (L - X1) / C_MIN
Vbar_s = int_V_dtau / T_tot

M = 24000                      # steps across the ramp (even)
h = DX / M
xs = [X0 + i * h for i in range(M + 1)]
tau = [X0]                     # tau(X0) = X0 (c = 1 to the left)
for i in range(M):
    xm = xs[i] + 0.5 * h
    inc = (h / 6.0) * (1.0 / c_of(xs[i]) + 4.0 / c_of(xm) + 1.0 / c_of(xs[i + 1]))
    tau.append(tau[-1] + inc)
ok_tau = abs(tau[-1] - (X0 + T_r)) < 1e-9 * T_r

Vs = [V_of(xx) for xx in xs]
invc = [1.0 / c_of(xx) for xx in xs]


def shift_of(kk):
    g = [Vs[i] * math.sin(kk * math.pi * tau[i] / T_tot) ** 2 * invc[i]
         for i in range(M + 1)]
    ssum = g[0] + g[M] + 4.0 * sum(g[1:M:2]) + 2.0 * sum(g[2:M - 1:2])
    return (2.0 / T_tot) * (h / 3.0) * ssum


shifts = {kk: shift_of(kk) for kk in range(1, 81)}
mean_hi = sum(shifts[kk] for kk in range(60, 81)) / 21
ok6 = ok_tau and abs(mean_hi - Vbar_s) < 0.05 * Vbar_s
eq(6, ok6, "T, tau(x), shift_k = (2/T) int V sin^2(k pi tau/T) dtau, k = 1..80",
   f"T_r = {T_r:.6f}, T = {T_tot:.6f}, Vbar_s = {Vbar_s:.6e}, "
   f"mean shift(k=60..80) = {mean_hi:.6e}, tau-integ rel err "
   f"{abs(tau[-1] - (X0 + T_r)) / T_r:.1e}")


# EQ7: Sturm bisection vs the uniform chain's exact spectrum
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


n7 = 200
eig = sturm_eigs([2.0] * n7, [-1.0] * (n7 - 1), 20, 0.0, 4.1)
exact = [4 * math.sin(kk * math.pi / (2 * (n7 + 1))) ** 2 for kk in range(1, 21)]
worst7 = max(abs(e - x_) / x_ for e, x_ in zip(eig, exact))
eq(7, worst7 < 1e-12, "Sturm bisection = (4/a^2) sin^2(k pi/(2(n+1))) on the uniform chain",
   f"worst rel dev {worst7:.2e} over k = 1..20, n = {n7}")

# EQ8: Fourier decay of the oscillatory part (V continuous, V' jumps)
osc = [abs(shifts[kk] - Vbar_s) for kk in range(1, 81)]
lo_mean = sum(osc[:40]) / 40
hi_mean = sum(osc[40:]) / 40
eq(8, hi_mean < lo_mean, "mean |shift_k - Vbar_s| over k = 41..80 < mean over k = 1..40",
   f"low-k mean {lo_mean:.3e}, high-k mean {hi_mean:.3e}, "
   f"max osc {max(osc):.3e} at k = {osc.index(max(osc)) + 1}")

pin = {"L": L, "X0": X0, "X1": X1, "C_MIN": C_MIN,
       "T_ramp": T_r, "T_total": T_tot, "Vbar_s": Vbar_s,
       "int_V_dtau": int_V_dtau,
       "shifts": {str(kk): shifts[kk] for kk in range(1, 81)},
       "grids": [1499, 2999], "k_window": [5, 60], "n_eigs": 80,
       "linear": {"B": -0.5 / 1200.0, "V0": (0.5 / 1200.0) ** 2 / 4.0,
                  "Vbar": 3.416182292891435e-08},
       "tolerances": {"weyl_rel": 2e-3, "not_isospectral_min": 1e-9,
                      "shift_rms_over_vbar": 0.3, "mean_rel": 0.03,
                      "control_rms_over_vbar_min": 2.0,
                      "improvement_factor_min": 5.0}}
(HERE / "p18_registration.json").write_text(json.dumps(pin, indent=1) + "\n")
(HERE / "p18_derive_out.txt").write_text("\n".join(OUT) + "\n")
print(f"\npinned: Vbar_s = {Vbar_s:.6e}, T = {T_tot:.6f}, 80 k-resolved shifts; "
      f"shift_1 = {shifts[1]:.6e}, max osc dev {max(osc):.3e}")
sys.exit(1 if FAILED else 0)
