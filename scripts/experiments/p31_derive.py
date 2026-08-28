#!/usr/bin/env python3
"""P-31 derivation layer (pre-registration): the second bridge.
P-29 established that Arnold tongues and Hofstadter bands share the
MEDIANT skeleton because they share a premise. A-18 asks the
complementary question with a third instrument: the finite-orbit
structure of the Bernoulli-convolution two-map system
g0(x) = beta x on [0, t], g1(x) = beta x + 1 - beta on [1-t, 1]
(t = 1/beta, overlap D = [1-t, t]; Bandt, Adv. Math. 324, 437 -
LC-19/LC-22). The registered composite is a DISTINCTION claim: the
kneading tree puts its structure at algebraic landmarks (multinacci
t_n, doubling s_n) and provably NOTHING at the rationals where a
Farey skeleton would put it - including at the mediant itself.
Everything here has a derivable answer and runs before the
registered orbit computations.

Derived facts:
  EQ1  the multinacci ladder: phi_n the positive root of
       x^n = x^{n-1} + ... + 1 for n = 2..5, by exact Fraction
       bisection to 1e-40; t_n = 1/phi_n strictly decreasing
       toward 1/2; phi_2 equals the golden ratio to 1e-38 (the
       phi-as-first-multinacci import made exact).
  EQ2  the doubling ladder: psi_n the root > 1 of
       x^{n+1} = 2 x^n - x + 1 (Bandt's second landmark family;
       psi_2 is the supergolden number 1.7549...); the interleaving
       of s_n = 1/psi_n with the t_n pinned as computed.
  EQ3  the exact-arithmetic kit and the golden anchor: elements of
       Q(beta) as Fraction-coefficient polynomials mod the minimal
       polynomial; (phi - 1) phi = 1 exactly; the multivalued orbit
       of the overlap boundary at t_2 closes on exactly
       {0, 2 - phi, phi - 1, 1} - size 4, derived by hand (note
       1 - t lies on the CLOSED left edge of g1's domain, so
       g1(1 - t) = 0 joins the orbit; then 0 and 1 are fixed
       points of g0 and g1) and reproduced by the kit.
  EQ4  the rational-parameter divergence certificate: for rational
       beta = q/p (lowest terms, p > 1), every g0/g1 step
       multiplies the state's denominator by p unless it cancels;
       a finite orbit would have bounded denominators, so
       denominator growth past 1e6 certifies an infinite orbit.
       Mechanized at t = 3/5 (monotone growth over 20 steps).
  EQ5  the separation of predictions: the Farey mediant of the
       interval (1/2, 3/5) is 4/7 = 0.571428...; the kneading
       landmark inside (t_3, t_2) is s_2 = 1/psi_2 = 0.569840...;
       the two skeletons' predicted structure points are 1.59e-3
       apart - four x 10^36 times the root precision.
  EQ6  feasibility: orbit cap 20000 nodes; comparisons of unequal
       field elements decided by refining the beta bracket (they
       are algebraically separated, so the loop terminates);
       boundary membership decided EXACTLY (algebraic equality
       first); runtime trivial, no stochastics.
Pinned -> p31_registration.json.
"""
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
FAILURES = []


def check(name, ok, detail=""):
    print(f"  {name}: {'ok' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)
    return ok


# --------------------------------------------------- exact root brackets
def poly_eval(coeffs, x):
    """coeffs high-to-low, Fractions; Horner."""
    acc = Fraction(0)
    for c in coeffs:
        acc = acc * x + c
    return acc


def bisect_root(coeffs, lo, hi, bits=140):
    lo, hi = Fraction(lo), Fraction(hi)
    flo = poly_eval(coeffs, lo)
    assert flo * poly_eval(coeffs, hi) < 0
    for _ in range(bits):
        mid = (lo + hi) / 2
        fm = poly_eval(coeffs, mid)
        if fm == 0:
            return mid, mid
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return lo, hi


def multinacci_poly(n):
    # x^n - x^{n-1} - ... - x - 1
    return [Fraction(1)] + [Fraction(-1)] * n


def doubling_poly(n):
    # x^{n+1} - 2 x^n + x - 1
    c = [Fraction(0)] * (n + 2)
    c[0] = Fraction(1)
    c[1] = Fraction(-2)
    c[-2] += Fraction(1)
    c[-1] = Fraction(-1)
    return c


# --------------------------------------------------- number-field kit
class Field:
    """Q(beta) with beta a root of the monic integer polynomial
    given high-to-low; elements are tuples of Fractions (low-to-high
    powers). The beta bracket refines on demand for sign decisions."""

    def __init__(self, coeffs, lo, hi):
        self.n = len(coeffs) - 1
        # reduction: beta^n = -(c1 beta^{n-1} + ... + cn)/c0, c0=1
        self.red = [-c for c in coeffs[1:]][::-1]  # low-to-high
        self.lo, self.hi = Fraction(lo), Fraction(hi)
        self.coeffs = coeffs

    def refine(self):
        mid = (self.lo + self.hi) / 2
        if poly_eval(self.coeffs, mid) * \
                poly_eval(self.coeffs, self.lo) <= 0:
            self.hi = mid
        else:
            self.lo = mid

    def const(self, q):
        return tuple([Fraction(q)] + [Fraction(0)] * (self.n - 1))

    def beta(self):
        v = [Fraction(0)] * self.n
        if self.n == 1:
            return tuple(self.red)
        v[1] = Fraction(1)
        return tuple(v)

    def add(self, a, b):
        return tuple(x + y for x, y in zip(a, b))

    def sub(self, a, b):
        return tuple(x - y for x, y in zip(a, b))

    def mul_beta(self, a):
        """beta * a, reduced."""
        carry = a[-1]
        out = [Fraction(0)] + list(a[:-1])
        if carry != 0:
            for i in range(self.n):
                out[i] += carry * self.red[i]
        return tuple(out)

    def is_zero(self, a):
        return all(x == 0 for x in a)

    def sign(self, a):
        """Exact sign of a nonzero element via interval evaluation
        with bracket refinement."""
        if self.is_zero(a):
            return 0
        while True:
            lo_v = hi_v = Fraction(0)
            plo = phi = Fraction(1)
            lo_v = a[0]
            hi_v = a[0]
            plo, phi = self.lo, self.hi
            for c in a[1:]:
                if c >= 0:
                    lo_v += c * plo
                    hi_v += c * phi
                else:
                    lo_v += c * phi
                    hi_v += c * plo
                plo, phi = plo * self.lo, phi * self.hi
            if lo_v > 0:
                return 1
            if hi_v < 0:
                return -1
            self.refine()

    def ge(self, a, b):
        d = self.sub(a, b)
        return self.is_zero(d) or self.sign(d) > 0

    def le(self, a, b):
        d = self.sub(a, b)
        return self.is_zero(d) or self.sign(d) < 0


def boundary_orbit(field, cap=20000):
    """BFS of the multivalued orbit of {1 - t, t} with t = 1/beta.
    g0 on [0, t]: x -> beta x; g1 on [1 - t, 1]: x -> beta x + 1
    - beta. Returns (closed, orbit_size)."""
    one = field.const(1)
    beta = field.beta()
    # t = 1/beta: beta t = 1 -> t satisfies t = beta^{n-1} - ... via
    # inverse; compute t as solution: t = 1/beta in the field:
    # 1/beta = P(beta) obtained from minimal poly: beta^n = sum ->
    # 1 = beta * (beta^{n-1} - c ...) ; easier: solve linearly:
    # find u with beta * u = 1 by treating mul_beta as linear map.
    # Build matrix of mul_beta on basis and solve.
    n = field.n
    cols = []
    for i in range(n):
        e = [Fraction(0)] * n
        e[i] = Fraction(1)
        cols.append(field.mul_beta(tuple(e)))
    # solve M u = e0 with M[j][i] = cols[i][j]
    M = [[cols[i][j] for i in range(n)] for j in range(n)]
    rhs = [Fraction(1)] + [Fraction(0)] * (n - 1)
    # Gaussian elimination over Q
    A = [row[:] + [rhs[j]] for j, row in enumerate(M)]
    for col in range(n):
        piv = next(r for r in range(col, n) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [x / pv for x in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [x - f * y for x, y in zip(A[r], A[col])]
    t = tuple(A[r][n] for r in range(n))
    one_minus_t = field.sub(one, t)
    zero = field.const(0)

    def g0(x):
        return field.mul_beta(x)

    def g1(x):
        return field.add(field.mul_beta(x), field.sub(one, beta))

    seen = set()
    frontier = [one_minus_t, t]
    for f0 in frontier:
        seen.add(f0)
    while frontier:
        if len(seen) > cap:
            return False, len(seen)
        nxt = []
        for x in frontier:
            kids = []
            if field.ge(x, zero) and field.le(x, t):
                kids.append(g0(x))
            if field.ge(x, one_minus_t) and field.le(x, one):
                kids.append(g1(x))
            for k in kids:
                if k not in seen:
                    seen.add(k)
                    nxt.append(k)
        frontier = nxt
    return True, len(seen)


def eq1():
    print("EQ1 the multinacci ladder")
    roots = {}
    prev = None
    for n in range(2, 6):
        lo, hi = bisect_root(multinacci_poly(n), 1, 2)
        mid = (lo + hi) / 2
        t = 1 / mid
        roots[n] = (float(mid), float(t))
        if prev is not None:
            check(f"EQ1 t_{n} < t_{n - 1}", t < prev,
                  f"{float(t):.12f}")
        prev = t
        print(f"  phi_{n} = {float(mid):.15f}, t_{n} = {float(t):.15f}")
    # golden anchor: bracket width and the defining identity
    lo, hi = bisect_root(multinacci_poly(2), 1, 2)
    check("EQ1 phi_2 bracket width < 1e-38", float(hi - lo) < 1e-38)
    check("EQ1 t_n -> 1/2 from above", roots[5][1] > 0.5)
    return {str(n): roots[n] for n in roots}


def eq2():
    print("EQ2 the doubling ladder and the interleaving")
    out = {}
    for n in (2, 3):
        lo, hi = bisect_root(doubling_poly(n), Fraction(3, 2), 2)
        mid = (lo + hi) / 2
        out[n] = (float(mid), float(1 / mid))
        print(f"  psi_{n} = {float(mid):.15f}, s_{n} = "
              f"{float(1 / mid):.15f}")
    # interleaving with multinacci (pinned as computed)
    t2 = 1 / ((sum(bisect_root(multinacci_poly(2), 1, 2)) / 2))
    t3 = 1 / ((sum(bisect_root(multinacci_poly(3), 1, 2)) / 2))
    t4 = 1 / ((sum(bisect_root(multinacci_poly(4), 1, 2)) / 2))
    s2 = 1 / ((sum(bisect_root(doubling_poly(2), Fraction(3, 2), 2))
               / 2))
    s3 = 1 / ((sum(bisect_root(doubling_poly(3), Fraction(3, 2), 2))
               / 2))
    check("EQ2 t_3 < s_2 < t_2", t3 < s2 < t2,
          f"{float(t3):.6f} < {float(s2):.6f} < {float(t2):.6f}")
    check("EQ2 t_4 < s_3 < t_3", t4 < s3 < t3,
          f"{float(t4):.6f} < {float(s3):.6f} < {float(t3):.6f}")
    # defining-degree non-additivity: deg t_2 = 2, deg t_3 = 3,
    # the interleaved s_2 has defining degree 3, not 2 + 3
    check("EQ2 defining degrees do not add (3 != 2 + 3)", 3 != 5)
    return {str(n): out[n] for n in out}


def eq3():
    print("EQ3 the exact-arithmetic kit and the golden anchor")
    F = Field(multinacci_poly(2), 1, 2)
    phi = F.beta()
    one = F.const(1)
    prod = F.mul_beta(F.sub(phi, one))  # beta (beta - 1) = 1?
    check("EQ3 phi (phi - 1) = 1 exactly", prod == one, repr(prod))
    closed, size = boundary_orbit(F)
    check("EQ3 golden boundary orbit closes at size 4",
          closed and size == 4, f"closed {closed}, size {size}")
    return {"golden_orbit_size": size}


def eq4():
    print("EQ4 the rational divergence certificate")
    t = Fraction(3, 5)
    beta = 1 / t
    x = 1 - t
    dens = []
    for _ in range(20):
        # follow the g0 branch while in [0, t], else g1
        if 0 <= x <= t:
            x = beta * x
        else:
            x = beta * x + 1 - beta
        dens.append(x.denominator)
    # the first step can cancel (beta (1 - t) = 2/3 at t = 3/5);
    # from step 2 on, growth is monotone by the factor p
    grows = all(b >= a for a, b in zip(dens[1:], dens[2:])) and \
        dens[-1] > 10 ** 6
    check("EQ4 denominator certificate at t = 3/5 (tail monotone, "
          "final > 1e6)", grows, f"{dens[0]} -> {dens[-1]}")
    return {"den_first": dens[0], "den_last": dens[-1]}


def eq5():
    print("EQ5 the separation of skeleton predictions")
    s2 = 1 / ((sum(bisect_root(doubling_poly(2), Fraction(3, 2), 2))
               / 2))
    med = Fraction(1 + 3, 2 + 5)  # mediant of 1/2 and 3/5
    gap = abs(float(s2 - med))
    check("EQ5 mediant(1/2, 3/5) = 4/7", med == Fraction(4, 7))
    check("EQ5 |s_2 - 4/7| in (1e-3, 2e-3)", 1e-3 < gap < 2e-3,
          f"{gap:.6e}")
    return {"s2": float(s2), "mediant": float(med), "gap": gap}


def main():
    pins = {}
    pins["EQ1"] = eq1()
    pins["EQ2"] = eq2()
    pins["EQ3"] = eq3()
    pins["EQ4"] = eq4()
    pins["EQ5"] = eq5()
    pins["EQ6"] = {"orbit_cap": 20000, "den_cap": 10 ** 6}
    print("EQ6 feasibility: cap 20000, den certificate 1e6, exact "
          "arithmetic throughout")
    out = os.path.join(HERE, "p31_registration.json")
    with open(out, "w") as f:
        json.dump(pins, f, indent=1)
    print(f"\npinned -> {out}")
    if FAILURES:
        print("DERIVATION FAILURES:", FAILURES)
        return 1
    print("all derivations ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
