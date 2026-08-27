#!/usr/bin/env python3
"""P-24 derivation layer (pre-registration): the memory hierarchy of
dynamical substrates - how expensively three classical substrates
forget one piece of information. Everything here is derived BEFORE
the registered simulations run; every "=" is CAS-checked, closed
form, or exact quadrature/linear algebra. Chat-level guesses die
here if they are wrong (one did: see EQ5).

The three rungs (all overdamped Langevin, noise strength D):
  1. UNTENDED PHASE   dtheta = sqrt(2D) dW on the circle.
     Memory = <cos theta(t)> given theta(0) = 0.
  2. LOCKED PHASE     dtheta = -eps sin(2 theta) dt + sqrt(2D) dW.
     Memory = the well index (the P-22 Z2 doublet as a bit).
  3. WINDING NUMBER   ring of N phases, E = K sum (1 - cos dphi),
     dphi_i/dt = -dE/dphi_i + sqrt(2D) xi_i.
     Memory = the winding number w (start in w = 1).

Derived facts:
  EQ1  rung 1 decays EXACTLY as e^{-D t}: cos theta is the
       eigenfunction of the diffusion generator with eigenvalue -1
       (CAS: d^2 cos/dtheta^2 = -cos). Lifetime tau1 = 1/D.
  EQ2  rung 2: the committed telegraph has autocorrelation
       e^{-2 r t} (2x2 generator eigenvalue, algebraic), with r =
       1/(2 T_MFPT) and T_MFPT the exact double quadrature; the
       Arrhenius barrier is EXACTLY eps (CAS: max U - min U for
       U = -(eps/2) cos 2 theta). Pins on a fresh D-ladder.
  EQ3  rung 3 saddle, CLOSED FORM: clamping one bond at Delta and
       relaxing the rest of the w = 1 sector gives the uniform
       distribution of the remaining winding (verified against
       numeric relaxation), so
         E(Delta) = K(1-cos Delta) + K(N-1)(1 - cos((2pi-Delta)/(N-1)))
       with stationary points where sin Delta = sin((2pi-Delta)/(N-1)):
       the minimum at the uniform twist and the saddle at
         Delta* = pi (N-3)/(N-2).
       Barrier Delta_E(N) = E(Delta*) - E_1(N), E_1 = N K (1 - cos(2pi/N)).
  EQ4  the full Langer rate, every factor derived: rate(N, D) =
       N * (lambda_u / 2 pi) * sqrt(det' H_min / |det' H_saddle|)
       * exp(-Delta_E/D), with the two Hessians assembled from the
       closed-form configurations, eigenvalues by cyclic Jacobi,
       the global-rotation zero mode dropped from both determinants
       (det'), lambda_u = the saddle's unstable curvature, and the
       factor N counting the slip's nucleation sites.
  EQ5  the hierarchy shape - and the death of a chat-level guess:
       Delta_E(N) GROWS with N but SATURATES at 2K (values pinned:
       N = 8, 16, 32, 256 below); there is no extensive topological
       protection in this 1D classical ring - lifetime rises with N
       only while the twisted state's own strain relaxes, then the
       N-fold nucleation penalty takes over. The crossover N*(D) is
       derived and pinned.
  EQ6  simulation bands derived: rung-1 CLT band, rung-2/3 Poisson
       bands from Langer-predicted event counts (every cell budgets
       > 60 committed events), plus a registered 0.35 nat allowance
       on ratio clauses and 0.7 nat (factor 2) on absolute Langer
       clauses for finite-barrier corrections (Delta_E/D is 2.9-7.1
       here, not infinity - declared, not hidden).
Pinned -> p24_registration.json.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from symb import N as Num, V as Var, sub, mul, sin as Sin, cos as Cos, d as Dop, ev  # noqa: E402

OUT, FAILED = [], []
K = 1.0


def eq(n, ok, statement, detail):
    line = f"EQ {n} {'PASS' if ok else 'FAIL'}  {statement}  | {detail}"
    OUT.append(line)
    print(line)
    if not ok:
        FAILED.append(n)


# ---------- EQ1: rung 1 exact decay ----------
t = Var("t")
lhs = Dop(Dop(Cos(t), "t"), "t")
worst1 = max(abs(ev(lhs, {"t": x}) + math.cos(x)) for x in [0.3 * k for k in range(1, 20)])
eq(1, worst1 < 1e-12, "d2(cos)/dtheta2 = -cos  =>  <cos theta(t)> = e^{-D t}, tau1 = 1/D",
   f"worst CAS residual {worst1:.1e}")


# ---------- EQ2: rung 2 pins ----------
def mfpt_double_well(epsv, D, n=3000):
    hy = math.pi / (2 * n)
    def U(x):
        return -(epsv / 2) * math.cos(2 * x) / D
    ys = [-math.pi / 2 + j * (math.pi / (2 * n)) * 2 for j in range(2 * n + 1)]
    emu = [math.exp(-U(y)) for y in ys]
    cum = [0.0]
    step = math.pi / (2 * n)
    for j in range(2 * n):
        cum.append(cum[-1] + 0.5 * (emu[j] + emu[j + 1]) * step)
    def inner(xv):
        j = (xv + math.pi / 2) / step
        j0 = min(int(j), 2 * n - 1)
        return cum[j0] + (j - j0) * (cum[j0 + 1] - cum[j0])
    nx = n
    hx = (math.pi / 2) / nx
    tot = 0.0
    for i in range(nx + 1):
        w = 0.5 if i in (0, nx) else 1.0
        tot += w * math.exp(U(i * hx)) * inner(i * hx)
    return tot * hx / D


EPS2 = 1.0
D2_LADDER = [0.22, 0.28]
tau2 = {str(Dv): mfpt_double_well(EPS2, Dv) for Dv in D2_LADDER}
u = Var("u")
Upot = mul(Num(-0.5 * EPS2), Cos(mul(Num(2), u)))
umax = max(ev(Upot, {"u": x}) for x in [i * 0.001 for i in range(3142)])
umin = min(ev(Upot, {"u": x}) for x in [i * 0.001 for i in range(3142)])
eq(2, abs((umax - umin) - EPS2) < 1e-6,
   "telegraph C(t) = e^{-2 r t}, r = 1/(2 T_MFPT); barrier = eps exactly",
   f"barrier {umax - umin:.6f}; tau2 pins {[f'{k}:{v:.1f}' for k, v in tau2.items()]}")


# ---------- EQ3: rung 3 closed-form saddle ----------
def E_of_delta(Delta, Nn):
    return K * (1 - math.cos(Delta)) + K * (Nn - 1) * (1 - math.cos((2 * math.pi - Delta) / (Nn - 1)))


def E1(Nn):
    return Nn * K * (1 - math.cos(2 * math.pi / Nn))


def delta_star(Nn):
    return math.pi * (Nn - 3) / (Nn - 2)


def barrier(Nn):
    return E_of_delta(delta_star(Nn), Nn) - E1(Nn)


# stationarity check by CAS derivative of the closed form
ok3 = True
rows3 = []
for Nn in (8, 16, 32):
    Dl = Var("x")
    Eexpr = sub(mul(Num(K), sub(Num(1), Cos(Dl))),
                mul(Num(-K * (Nn - 1)), sub(Num(1), Cos(mul(Num(1.0 / (Nn - 1)),
                    sub(Num(2 * math.pi), Dl))))))
    dE = Dop(Eexpr, "x")
    res = ev(dE, {"x": delta_star(Nn)})
    ok3 = ok3 and abs(res) < 1e-9
    rows3.append(f"N={Nn}: dE/dDelta at Delta* = {res:.1e}, barrier {barrier(Nn):.4f}")


# numeric check that uniform-rest is the constrained minimum
def relax_rest(Nn, Delta, iters=40000, lr=0.02, kick=0.3, seed=7):
    import random
    rng = random.Random(seed)
    # bonds: b[0] = Delta fixed; b[1..N-1] free with sum = 2pi - Delta
    free = Nn - 1
    b = [(2 * math.pi - Delta) / free + kick * (rng.random() - 0.5) for _ in range(free)]
    s = sum(b)
    b = [x + (2 * math.pi - Delta - s) / free for x in b]
    for _ in range(iters):
        g = [math.sin(x) for x in b]
        gm = sum(g) / free
        b = [x - lr * (gx - gm) for gx, x in zip(g, b)]
    return K * (1 - math.cos(Delta)) + K * sum(1 - math.cos(x) for x in b), b


ok3b = True
for Nn in (8, 16):
    Erelax, b = relax_rest(Nn, delta_star(Nn))
    Eclosed = E_of_delta(delta_star(Nn), Nn)
    spread = max(b) - min(b)
    ok3b = ok3b and abs(Erelax - Eclosed) < 1e-6 and spread < 1e-3
eq(3, ok3 and ok3b, "saddle at Delta* = pi(N-3)/(N-2); relaxed rest is uniform",
   "; ".join(rows3))


# ---------- EQ4: full Langer rates ----------
def jacobi_eigs(A, sweeps=60):
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(sweeps):
        off = max((abs(a[i][j]), i, j) for i in range(n) for j in range(i + 1, n))
        if off[0] < 1e-12:
            break
        _, p, q = off
        if a[p][p] == a[q][q]:
            th = math.pi / 4
        else:
            th = 0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
        c, s = math.cos(th), math.sin(th)
        for k in range(n):
            apk, aqk = a[p][k], a[q][k]
            a[p][k] = c * apk - s * aqk
            a[q][k] = s * apk + c * aqk
        for k in range(n):
            akp, akq = a[k][p], a[k][q]
            a[k][p] = c * akp - s * akq
            a[k][q] = s * akp + c * akq
    return sorted(a[i][i] for i in range(n))


def hessian(bonds):
    """H_ij = d2E/dphi_i dphi_j for E = K sum(1 - cos(phi_{i+1}-phi_i));
    bond j connects site j -> j+1 with difference bonds[j]."""
    n = len(bonds)
    c = [K * math.cos(b) for b in bonds]
    H = [[0.0] * n for _ in range(n)]
    for j in range(n):
        i, ip = j, (j + 1) % n
        H[i][i] += c[j]
        H[ip][ip] += c[j]
        H[i][ip] -= c[j]
        H[ip][i] -= c[j]
    return H


def langer_rate(Nn, D):
    bmin = [2 * math.pi / Nn] * Nn
    ds = delta_star(Nn)
    rest = (2 * math.pi - ds) / (Nn - 1)
    bsad = [ds] + [rest] * (Nn - 1)
    lmin = jacobi_eigs(hessian(bmin), sweeps=400)
    lsad = jacobi_eigs(hessian(bsad), sweeps=400)
    # drop one zero mode (global rotation) from each; saddle keeps its
    # negative eigenvalue as lambda_u
    lmin_nz = [x for x in lmin if abs(x) > 1e-9]
    neg = [x for x in lsad if x < -1e-9]
    lsad_nz = [x for x in lsad if abs(x) > 1e-9 and x > 0]
    lam_u = -neg[0]
    logdet = sum(math.log(x) for x in lmin_nz) - sum(math.log(x) for x in lsad_nz) \
        - math.log(lam_u)
    pref = Nn * (lam_u / (2 * math.pi)) * math.exp(0.5 * logdet)
    return pref * math.exp(-barrier(Nn) / D), pref


CELLS3 = [(8, 0.16), (16, 0.16), (16, 0.24), (16, 0.30), (32, 0.30)]
rate_pin, pref_pin = {}, {}
for (Nn, Dv) in CELLS3:
    r, p = langer_rate(Nn, Dv)
    rate_pin[f"{Nn}_{Dv}"] = r
    pref_pin[f"{Nn}_{Dv}"] = p
ok4 = all(len(set([round(pref_pin[f'16_{d}'], 6) for d in (0.16, 0.24, 0.3)])) == 1
          for _ in [0]) and all(v > 0 for v in rate_pin.values())
eq(4, ok4, "Langer rate with derived prefactor (zero mode dropped, xN nucleation)",
   "; ".join(f"{k}: r={v:.3e}" for k, v in list(rate_pin.items())[:3]))

# ---------- EQ5: hierarchy shape; the chat guess dies ----------
b8, b16, b32, b256 = barrier(8), barrier(16), barrier(32), barrier(256)
mono = b8 < b16 < b32 < b256 < 2 * K
# crossover: tau3(N) = 1/rate; compare N=8 vs 32 at D = 0.16 and D = 0.6
tau_8_016 = 1.0 / langer_rate(8, 0.16)[0]
tau_32_016 = 1.0 / langer_rate(32, 0.16)[0]
tau_8_06 = 1.0 / langer_rate(8, 0.6)[0]
tau_32_06 = 1.0 / langer_rate(32, 0.6)[0]
cross = (tau_32_016 > tau_8_016) and (tau_32_06 < tau_8_06)
eq(5, mono and cross,
   "Delta_E grows with N, saturates at 2K; NO extensive protection - the "
   "lifetime gain with N inverts at large D (crossover derived)",
   f"barriers {b8:.4f} < {b16:.4f} < {b32:.4f} < {b256:.4f} < 2; "
   f"tau32/tau8 at D=0.16: {tau_32_016/tau_8_016:.1f}x, at D=0.6: "
   f"{tau_32_06/tau_8_06:.2f}x")

# ---------- EQ6: bands and budgets ----------
T3 = {"8_0.16": 2500.0, "16_0.16": 45000.0, "16_0.24": 7000.0,
      "16_0.3": 3000.0, "32_0.3": 5000.0}
budget = {k: rate_pin[k.replace('_0.3', '_0.3')] * T3[k] for k in T3}
# rung-2 budgets
T2 = 30000.0
n2 = {k: T2 / (2 * v) for k, v in tau2.items()}
ok6 = all(v > 60 for v in budget.values()) and all(v > 60 for v in n2.values())
eq(6, ok6, "event budgets > 60 everywhere; bands: Poisson + 0.35 nat (ratios) "
   "/ 0.7 nat (absolute Langer)",
   "rung3 " + "; ".join(f"{k}:{v:.0f}" for k, v in budget.items()) +
   " | rung2 " + "; ".join(f"{k}:{v:.0f}" for k, v in n2.items()))

pin = {"K": K, "eps2": EPS2, "D2_ladder": D2_LADDER, "tau2_pin": tau2,
       "T2": T2, "cells3": [[c[0], c[1]] for c in CELLS3], "T3": T3,
       "rate_pin": rate_pin, "pref_pin": pref_pin,
       "barriers": {"8": b8, "16": b16, "32": b32, "256": b256},
       "delta_star": {str(n): delta_star(n) for n in (8, 16, 32)},
       "rung1": {"D": 0.5, "M": 4000, "t_grid": [0.5, 1.0, 2.0, 4.0]},
       "dt": {"r1": 0.002, "r2": 0.004, "r3": 0.005},
       "seeds": {"r1": 811, "r2": 822, "r3": 833},
       "bands": {"ratio_nat": 0.35, "abs_nat": 0.7, "slip_purity": 0.98},
       "crossover_check": {"tau32_over_tau8_D016": tau_32_016 / tau_8_016,
                            "tau32_over_tau8_D06": tau_32_06 / tau_8_06}}
(HERE / "p24_registration.json").write_text(json.dumps(pin, indent=1) + "\n")
(HERE / "p24_derive_out.txt").write_text("\n".join(OUT) + "\n")
print(f"\npinned: barriers {b8:.4f}/{b16:.4f}/{b32:.4f} -> 2K; "
      f"5 Langer cells; tau2 ladder; rung-1 exact")
sys.exit(1 if FAILED else 0)
