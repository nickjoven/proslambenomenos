#!/usr/bin/env python3
"""P-21 derivation layer (pre-registration): Hardy's nonlocality
paradox and its maximum probability, derived BEFORE the blind search
runs. Every "=" below is checked by the stdlib CAS (symb.py), by
exhaustive enumeration, or by exact arithmetic in Q(sqrt 5) - no
floating point in the theorem-grade steps.

Setup. Real two-qubit Hilbert space (sufficient for Hardy's argument;
the state and all measurement vectors can be chosen real). State in
Schmidt form |psi> = c|00> + s|11>, c^2 + s^2 = 1, c, s > 0; write
k = c/s. Alice measures A0 or A1, Bob B0 or B1; the "+" outcome of a
setting with angle t projects onto (cos t, sin t), the "-" outcome
onto (-sin t, cos t). Hardy's three zero-constraints:

    Z1:  P(A0=+, B0=+) = 0
    Z2:  P(A1=+, B0=-) = 0
    Z3:  P(A0=-, B1=+) = 0

and the paradox event is p_Hardy = P(A1=+, B1=+). Any local
hidden-variable assignment obeying Z1-Z3 gives p_Hardy = 0 (EQ1,
exhaustive over all 16 deterministic assignments); quantum mechanics
does not.

Derived facts (each an EQ line):
  EQ1  LHV exhaustion: every deterministic assignment with A1=+ and
       B1=+ lands in a Z1/Z2/Z3 event - the paradox event has LHV
       probability zero under the constraints.
  EQ2  constraint elimination: with tan a0 = a, tan b0 = -k/a,
       tan a1 = -k^2/a, tan b1 = k a, the three amplitudes vanish
       identically (CAS, sampled box in (k, a), both signs of a).
  EQ3  the paradox probability in the reduced parametrization:
       p = k^2 (1-k^2)^2 / [(1+k^2)(1+k^4/a^2)(1+k^2 a^2)]  (CAS).
  EQ4  exact global minimization of the denominator (no calculus):
       (1+k^4/a^2)(1+k^2 a^2) - (1+k^3)^2 = k^2 (a - k/a)^2 >= 0,
       with equality iff a^2 = k  (CAS identity).
  EQ5  the envelope: p_env(k) = k^2(1-k^2)^2/[(1+k^2)(1+k^3)^2]
       = k^2 (1-k)^2 / [(1+k^2)(1-k+k^2)^2]  (CAS), and
       p_env(1/k) = p_env(k)  (CAS): the two Schmidt orderings tie.
  EQ6  stationarity: d/dk log p_env = 2 Q(k) / [k(1-k)(1+k^2)
       (k^2-k+1)] with Q(k) = k^5 - 2k^4 - 2k + 1  (CAS).
  EQ7  Q(k) = (k+1)(k^4 - 3k^3 + 3k^2 - 3k + 1)  (integer
       polynomial arithmetic; the k = -1 root is spurious for
       k = c/s > 0).
  EQ8  the palindromic quartic collapses in y = k + 1/k:
       k^4 - 3k^3 + 3k^2 - 3k + 1 = k^2 (y^2 - 3y + 1)  (CAS).
  EQ9  y* = (3+sqrt 5)/2 is a root of y^2 - 3y + 1 = 0, exactly, in
       Q(sqrt 5); y* = Phi^2 with Phi = (1+sqrt 5)/2 (also exact),
       and y* > 2 is the branch reached by real k > 0.
  EQ10 p_env in y-form: p_env = (y-2)/(y (y-1)^2)  (CAS).
  EQ11 the maximum, exactly in Q(sqrt 5):
       p* = (y*-2)/(y*(y*-1)^2) = (5 sqrt 5 - 11)/2 = phi^5,
       phi = (sqrt 5 - 1)/2  (exact field arithmetic: y*-2 = phi,
       y*-1 = Phi, p* = phi/Phi^4, and phi^5 computed as a literal
       fifth power - all as pairs of rationals).
  EQ12 the optimal Schmidt structure, exactly: c s = 1/y* = phi^2,
       so c^2 and s^2 are the roots of w^2 - w + phi^4 = 0 with
       discriminant 1 - 4 phi^4 = 6 sqrt 5 - 13  (exact), i.e.
       {c^2, s^2} = (1 -+ sqrt(6 sqrt 5 - 13))/2.
  EQ13 the maximally entangled slice: at k = 1 the reduced p is the
       zero function of a (CAS) - Hardy's paradox vanishes on the
       maximally entangled state.

Pinned outputs -> p21_registration.json: the maximum, the optimal
k*, theta*, Schmidt weights, the optimizer's start count, seed,
penalty schedule and tolerance bands - all BEFORE p21_hardy.py runs.
"""
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from symb import N, V, add, sub, mul, div, powe, sqrt, sin, cos, log, d, equal  # noqa: E402

OUT, FAILED = [], []


def eq(n, ok, statement, detail):
    line = f"EQ {n} {'PASS' if ok else 'FAIL'}  {statement}  | {detail}"
    OUT.append(line)
    print(line)
    if not ok:
        FAILED.append(n)


# ----------------------------------------------------------------- EQ1
# LHV exhaustion. A deterministic local assignment fixes outcomes
# (A0, A1, B0, B1) in {+1, -1}^4. Under Z1-Z3 the hidden-variable
# measure gives zero weight to any assignment realizing a forbidden
# event; check that EVERY assignment with A1 = B1 = +1 realizes one.
bad = []
for m in range(16):
    A0, A1, B0, B1 = ((m >> i) & 1 for i in range(4))  # 1 = "+"
    if not (A1 and B1):
        continue
    forbidden = (A1 and not B0) or ((not A0) and B1) or (A0 and B0)
    if not forbidden:
        bad.append((A0, A1, B0, B1))
eq(1, not bad, "every deterministic assignment with A1=+, B1=+ hits a "
   "Z1/Z2/Z3 event => LHV p_Hardy = 0",
   f"16 assignments enumerated; counterexamples: {bad!r}")

# ------------------------------------------------------- CAS building
# Trig of an angle with tangent t: cos = (1+t^2)^(-1/2), sin = t cos.
k, a = V("k"), V("a")


def cs_of_tan(t):
    c_ = powe(add(N(1), mul(t, t)), N(-0.5))
    return c_, mul(t, c_)


def amp(ta, tb, csch, ssch, alice_plus=True, bob_plus=True):
    """Amplitude <alice, bob|psi> for outcome vectors: '+' of tangent t
    is (cos, sin); '-' is (-sin, cos)."""
    ca, sa = cs_of_tan(ta)
    cb, sb = cs_of_tan(tb)
    ua = (ca, sa) if alice_plus else (mul(N(-1), sa), ca)
    ub = (cb, sb) if bob_plus else (mul(N(-1), sb), cb)
    return add(mul(csch, ua[0], ub[0]), mul(ssch, ua[1], ub[1]))


# Schmidt coefficients via k: c = k/sqrt(1+k^2), s = 1/sqrt(1+k^2).
den = powe(add(N(1), mul(k, k)), N(-0.5))
c_sch = mul(k, den)
s_sch = den

t_a0 = a
t_b0 = div(mul(N(-1), k), a)
t_a1 = div(mul(N(-1), k, k), a)
t_b1 = mul(k, a)

# ----------------------------------------------------------------- EQ2
BOXP = {"k": (0.15, 0.9), "a": (0.2, 2.5)}
BOXM = {"k": (0.15, 0.9), "a": (-2.5, -0.2)}
worst2 = 0.0
ok2 = True
for name, e in (("Z1", amp(t_a0, t_b0, c_sch, s_sch, True, True)),
                ("Z2", amp(t_a1, t_b0, c_sch, s_sch, True, False)),
                ("Z3", amp(t_a0, t_b1, c_sch, s_sch, False, True))):
    for box in (BOXP, BOXM):
        ok_, w_, nv = equal(e, N(0), box)
        ok2 = ok2 and ok_
        worst2 = max(worst2, w_)
eq(2, ok2, "tan a0 = a, tan b0 = -k/a, tan a1 = -k^2/a, tan b1 = k a "
   "kill all three Hardy amplitudes identically",
   f"Z1, Z2, Z3 on both sign boxes; worst |amp| {worst2:.2e}")

# ----------------------------------------------------------------- EQ3
p_full = powe(amp(t_a1, t_b1, c_sch, s_sch, True, True), N(2))
one_mk2 = sub(N(1), mul(k, k))
p_red = div(mul(k, k, one_mk2, one_mk2),
            mul(add(N(1), mul(k, k)),
                add(N(1), div(powe(k, N(4)), mul(a, a))),
                add(N(1), mul(k, k, a, a))))
ok3a, w3a, _ = equal(p_full, p_red, BOXP)
ok3b, w3b, _ = equal(p_full, p_red, BOXM)
eq(3, ok3a and ok3b, "p_Hardy = k^2 (1-k^2)^2 / [(1+k^2)(1+k^4/a^2)(1+k^2 a^2)]",
   f"worst rel delta {max(w3a, w3b):.2e} over both boxes")

# ----------------------------------------------------------------- EQ4
D = mul(add(N(1), div(powe(k, N(4)), mul(a, a))), add(N(1), mul(k, k, a, a)))
gap = sub(D, powe(add(N(1), powe(k, N(3))), N(2)))
sqterm = mul(k, k, powe(sub(a, div(k, a)), N(2)))
ok4, w4, _ = equal(gap, sqterm, BOXP)
eq(4, ok4, "(1+k^4/a^2)(1+k^2 a^2) - (1+k^3)^2 = k^2 (a-k/a)^2 "
   ">= 0, equality iff a^2 = k (exact minimization, no calculus)",
   f"worst rel delta {w4:.2e}")

# ----------------------------------------------------------------- EQ5
p_env = div(mul(k, k, one_mk2, one_mk2),
            mul(add(N(1), mul(k, k)), powe(add(N(1), powe(k, N(3))), N(2))))
one_mk = sub(N(1), k)
p_env2 = div(mul(k, k, one_mk, one_mk),
             mul(add(N(1), mul(k, k)),
                 powe(add(N(1), mul(N(-1), k), mul(k, k)), N(2))))
BOXK = {"k": (0.1, 0.9)}
ok5a, w5a, _ = equal(p_env, p_env2, BOXK)
kinv = div(N(1), k)
one_mki = sub(N(1), kinv)
p_env2_inv = div(mul(kinv, kinv, one_mki, one_mki),
                 mul(add(N(1), mul(kinv, kinv)),
                     powe(add(N(1), mul(N(-1), kinv), mul(kinv, kinv)), N(2))))
ok5b, w5b, _ = equal(p_env2, p_env2_inv, BOXK)
eq(5, ok5a and ok5b, "p_env(k) = k^2(1-k)^2/[(1+k^2)(1-k+k^2)^2]; "
   "p_env(1/k) = p_env(k)",
   f"worst rel delta {max(w5a, w5b):.2e}")

# ----------------------------------------------------------------- EQ6
Q = add(powe(k, N(5)), mul(N(-2), powe(k, N(4))), mul(N(-2), k), N(1))
dlog = d(log(p_env2), "k")
rhs = div(mul(N(2), Q),
          mul(k, one_mk, add(N(1), mul(k, k)),
              add(mul(k, k), mul(N(-1), k), N(1))))
ok6, w6, _ = equal(dlog, rhs, BOXK)
eq(6, ok6, "d/dk log p_env = 2 Q(k) / [k(1-k)(1+k^2)(k^2-k+1)], "
   "Q = k^5 - 2k^4 - 2k + 1",
   f"worst rel delta {w6:.2e}")

# ----------------------------------------------------------------- EQ7
# integer polynomial product (k+1)(k^4-3k^3+3k^2-3k+1), low->high coeffs
quart = [1, -3, 3, -3, 1][::-1]          # 1 - 3k + 3k^2 - 3k^3 + k^4
lin = [1, 1]                             # 1 + k
prod = [0] * 6
for i, ci in enumerate(lin):
    for j, cj in enumerate(quart):
        prod[i + j] += ci * cj
ok7 = prod == [1, -2, 0, 0, -2, 1]
eq(7, ok7, "Q(k) = (k+1)(k^4 - 3k^3 + 3k^2 - 3k + 1) (integer coeffs); "
   "k = -1 spurious for k = c/s > 0",
   f"product coeffs low->high {prod}")

# ----------------------------------------------------------------- EQ8
y = add(k, div(N(1), k))
quartE = add(powe(k, N(4)), mul(N(-3), powe(k, N(3))),
             mul(N(3), powe(k, N(2))), mul(N(-3), k), N(1))
collapsed = mul(k, k, add(mul(y, y), mul(N(-3), y), N(1)))
ok8, w8, _ = equal(quartE, collapsed, BOXK)
eq(8, ok8, "k^4 - 3k^3 + 3k^2 - 3k + 1 = k^2 (y^2 - 3y + 1), y = k + 1/k",
   f"worst rel delta {w8:.2e}")

# --------------------------------------------- exact Q(sqrt5) numbers


class Q5:
    """Exact arithmetic in Q(sqrt 5): x = a + b sqrt 5, a, b rational."""

    def __init__(self, aa, bb=0):
        self.a, self.b = Fraction(aa), Fraction(bb)

    def __add__(self, o):
        return Q5(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        return Q5(self.a - o.a, self.b - o.b)

    def __mul__(self, o):
        return Q5(self.a * o.a + 5 * self.b * o.b,
                  self.a * o.b + self.b * o.a)

    def inv(self):
        n = self.a * self.a - 5 * self.b * self.b
        return Q5(self.a / n, -self.b / n)

    def __eq__(self, o):
        return self.a == o.a and self.b == o.b

    def __float__(self):
        return float(self.a) + float(self.b) * math.sqrt(5)

    def __repr__(self):
        return f"({self.a}) + ({self.b})*sqrt5"


half = Fraction(1, 2)
ystar = Q5(3 * half, half)                 # (3 + sqrt5)/2
Phi = Q5(half, half)                       # (1 + sqrt5)/2
phi = Q5(-half, half)                      # (sqrt5 - 1)/2
one, two, three = Q5(1), Q5(2), Q5(3)

# ----------------------------------------------------------------- EQ9
ok9 = (ystar * ystar - three * ystar + one == Q5(0)) and (Phi * Phi == ystar) \
    and float(ystar) > 2
eq(9, ok9, "y* = (3+sqrt5)/2 solves y^2 - 3y + 1 = 0; y* = Phi^2; y* > 2",
   f"y* = {float(ystar):.15f}")

# ---------------------------------------------------------------- EQ10
p_env_y = div(sub(y, N(2)), mul(y, powe(sub(y, N(1)), N(2))))
ok10, w10, _ = equal(p_env2, p_env_y, BOXK)
eq(10, ok10, "p_env = (y-2)/(y (y-1)^2) in y = k + 1/k",
   f"worst rel delta {w10:.2e}")

# ---------------------------------------------------------------- EQ11
pstar = (ystar - two) * (ystar * (ystar - one) * (ystar - one)).inv()
phi5 = phi * phi * phi * phi * phi
target = Q5(-11 * half, 5 * half)          # (5 sqrt5 - 11)/2
ok11 = (pstar == phi5 == target) and (ystar - two == phi) \
    and (ystar - one == Phi) \
    and (pstar == phi * (Phi * Phi * Phi * Phi).inv())
eq(11, ok11, "p* = (y*-2)/(y*(y*-1)^2) = phi/Phi^4 = phi^5 = "
   "(5 sqrt5 - 11)/2, exact in Q(sqrt5)",
   f"p* = {pstar!r} = {float(pstar):.17f}")

# ---------------------------------------------------------------- EQ12
cs = ystar.inv()
phi2 = phi * phi
disc = one - Q5(4) * phi2 * phi2
ok12 = (cs == phi2) and (disc == Q5(-13, 6))
c2 = (1 - math.sqrt(float(disc))) / 2
s2 = (1 + math.sqrt(float(disc))) / 2
kstar = math.sqrt(c2 / s2)
theta_star = math.atan2(math.sqrt(s2), math.sqrt(c2))
eq(12, ok12, "optimal state: c s = 1/y* = phi^2 exactly; c^2, s^2 = "
   "(1 -+ sqrt(6 sqrt5 - 13))/2 (disc = 1 - 4 phi^4 = 6 sqrt5 - 13)",
   f"c^2 = {c2:.15f}, s^2 = {s2:.15f}, k* = {kstar:.15f}")

# ---------------------------------------------------------------- EQ13
# at k = 1 the reduced tangents are a, -1/a, -1/a, a and c = s = 1/sqrt2;
# the paradox probability is amp(tan a1 = -1/a, tan b1 = a)^2:
p_par_k1 = powe(amp(mul(N(-1), div(N(1), a)), a, div(N(1), sqrt(N(2))),
                    div(N(1), sqrt(N(2))), True, True), N(2))
ok13a, w13a, _ = equal(p_par_k1, N(0), {"a": (0.2, 2.5)})
ok13b, w13b, _ = equal(p_par_k1, N(0), {"a": (-2.5, -0.2)})
eq(13, ok13a and ok13b, "k = 1 (maximally entangled): the constrained "
   "paradox probability is the zero function of a",
   f"worst |p| {max(w13a, w13b):.2e}")

# --------------------------------------------------- pinned registration
pmax = float(pstar)
sanity = kstar ** 2 * (1 - kstar) ** 2 / ((1 + kstar ** 2) * (kstar ** 2 - kstar + 1) ** 2)
print(f"float sanity: p_env(k*) = {sanity:.17f} vs p* = {pmax:.17f} "
      f"(delta {abs(sanity - pmax):.2e})")

reg = {
    "prediction": "P-21",
    "pinned_max_exact": "(5*sqrt(5)-11)/2 = phi^5, phi = (sqrt(5)-1)/2",
    "pinned_max": pmax,
    "phi": float(phi),
    "y_star": float(ystar),
    "k_star": kstar,
    "theta_star": theta_star,
    "schmidt": {
        "convention": "psi = c|00> + s|11>, k = c/s <= 1 canonical "
                      "(the k <-> 1/k mirror ties, EQ5)",
        "c2": c2,
        "s2": s2,
        "cs": float(cs),
        "weight_min": c2,
        "weight_max": s2,
    },
    "closed_form": "p_env(k) = k^2 (1-k)^2 / ((1+k^2) (1-k+k^2)^2)",
    "stationarity": "k^5 - 2k^4 - 2k + 1 = 0 -> (k+1)(k^4-3k^3+3k^2-3k+1) "
                    "= 0 -> y = k+1/k: y^2 - 3y + 1 = 0 -> y* = (3+sqrt5)/2",
    "optimizer": {
        "starts": 200,
        "seed": 20260826,
        "dims": 5,
        "parameters": "theta (Schmidt angle), alpha0, alpha1, beta0, beta1",
        "penalty": "p_Hardy - lambda * sum_i P_i^2 over the three "
                   "zero-constraint probabilities",
        "lambda_schedule": [1e3, 1e5, 1e7, 1e9],
        "polish": "constraint-eliminated envelope p_env(k), "
                  "golden-section in k to 1e-12",
        "me_slice": "constraint-eliminated p(k=1, a): 1000-point grid in "
                    "log10 a in [-3, 3] plus Nelder-Mead polish in a",
    },
    "tolerances": {
        "max_abs_dev_from_pinned": 1e-9,
        "schmidt_weight_dev": 1e-6,
        "me_slice_ceiling": 1e-12,
        "search_floor_below_pinned": 1e-6,
    },
}

if not FAILED:
    (HERE / "p21_registration.json").write_text(json.dumps(reg, indent=1) + "\n")
    print("wrote p21_registration.json")
else:
    print(f"NOT writing registration: EQ failures {FAILED}")

print(f"derivation layer: {len(OUT)} EQ lines, {len(FAILED)} failures")
sys.exit(1 if FAILED else 0)
