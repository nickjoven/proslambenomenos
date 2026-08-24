"""symb: a small symbolic layer (stdlib only) so that every "=" sign
in the P-13 material is accompanied by a computation that runs in CI.

Expressions are nested tuples: ('num', x), ('var', name), and the
operators add / mul / pow / sin / cos / exp / log built by the helper
constructors below. Two operations carry the load:

  d(e, x)              symbolic differentiation - exact rewrite rules,
                       no floating arithmetic in the rewrite itself.
  equal(a, b, box)     identity check by evaluation at random points
                       drawn from the stated box (the standard
                       polynomial-identity-testing move): an identity
                       false on a set of positive measure fails with
                       overwhelming probability. Equality is asserted
                       only over the sampled box, and that scope is
                       part of every EQ line that uses it.

There is deliberately no simplifier: algebraic rewriting is where CAS
bugs live, and none is needed to *check* an identity.
"""
import math
import random


def N(x):
    return ("num", float(x))


def V(name):
    return ("var", name)


def _fold(op, xs):
    e = xs[0]
    for x in xs[1:]:
        e = (op, e, x)
    return e


def add(*xs):
    return _fold("add", list(xs))


def mul(*xs):
    return _fold("mul", list(xs))


def sub(a, b):
    return add(a, mul(N(-1), b))


def div(a, b):
    return mul(a, powe(b, N(-1)))


def powe(a, b):
    return ("pow", a, b)


def sqrt(a):
    return powe(a, N(0.5))


def sin(a):
    return ("sin", a)


def cos(a):
    return ("cos", a)


def exp(a):
    return ("exp", a)


def log(a):
    return ("log", a)


def ev(e, env):
    """Evaluate an expression tree in the environment env: {name: float}.
    Raises ValueError/OverflowError/ZeroDivisionError on domain faults;
    equal() treats those as a discarded sample, not a verdict."""
    op = e[0]
    if op == "num":
        return e[1]
    if op == "var":
        return env[e[1]]
    if op == "add":
        return ev(e[1], env) + ev(e[2], env)
    if op == "mul":
        return ev(e[1], env) * ev(e[2], env)
    if op == "pow":
        base, expo = ev(e[1], env), ev(e[2], env)
        if base < 0 and expo != int(expo):
            raise ValueError("fractional power of negative base")
        if base == 0 and expo < 0:
            raise ZeroDivisionError
        return base ** expo
    if op == "sin":
        return math.sin(ev(e[1], env))
    if op == "cos":
        return math.cos(ev(e[1], env))
    if op == "exp":
        return math.exp(ev(e[1], env))
    if op == "log":
        v = ev(e[1], env)
        if v <= 0:
            raise ValueError("log of non-positive value")
        return math.log(v)
    raise ValueError(f"unknown op {op!r}")


def d(e, x):
    """Symbolic derivative of e with respect to the variable name x."""
    op = e[0]
    if op == "num":
        return N(0)
    if op == "var":
        return N(1) if e[1] == x else N(0)
    if op == "add":
        return add(d(e[1], x), d(e[2], x))
    if op == "mul":
        a, b = e[1], e[2]
        return add(mul(d(a, x), b), mul(a, d(b, x)))
    if op == "pow":
        a, b = e[1], e[2]
        if b[0] == "num":                      # a^c: c a^(c-1) a'
            return mul(b, powe(a, N(b[1] - 1)), d(a, x))
        # general a^b = exp(b log a)
        return mul(powe(a, b), add(mul(d(b, x), log(a)), mul(b, div(d(a, x), a))))
    if op == "sin":
        return mul(cos(e[1]), d(e[1], x))
    if op == "cos":
        return mul(N(-1), sin(e[1]), d(e[1], x))
    if op == "exp":
        return mul(exp(e[1]), d(e[1], x))
    if op == "log":
        return div(d(e[1], x), e[1])
    raise ValueError(f"unknown op {op!r}")


def equal(a, b, box, trials=300, tol=1e-9, seed=13):
    """True iff a == b at >= trials/2 valid sample points of box
    (box: {var: (lo, hi)}) within relative tolerance tol. Returns
    (ok, worst_delta, n_valid)."""
    rng = random.Random(seed)
    worst, valid = 0.0, 0
    for _ in range(trials):
        env = {v: rng.uniform(lo, hi) for v, (lo, hi) in box.items()}
        try:
            ya, yb = ev(a, env), ev(b, env)
        except (ValueError, OverflowError, ZeroDivisionError):
            continue
        valid += 1
        delta = abs(ya - yb) / max(1.0, abs(ya), abs(yb))
        worst = max(worst, delta)
        if delta > tol:
            return False, delta, valid
    return valid >= trials // 2, worst, valid


def simpson(f, a, b, tol=1e-12, depth=0):
    """Adaptive Simpson quadrature (stdlib), for the eikonal integrals."""
    c = 0.5 * (a + b)
    fa, fb, fc = f(a), f(b), f(c)

    def _rec(a, b, fa, fb, fc, whole, depth):
        c = 0.5 * (a + b)
        lm, rm = 0.5 * (a + c), 0.5 * (c + b)
        flm, frm = f(lm), f(rm)
        left = (c - a) / 6 * (fa + 4 * flm + fc)
        right = (b - c) / 6 * (fc + 4 * frm + fb)
        if depth > 50 or abs(left + right - whole) < 15 * tol:
            return left + right + (left + right - whole) / 15
        return (_rec(a, c, fa, fc, flm, left, depth + 1)
                + _rec(c, b, fc, fb, frm, right, depth + 1))

    whole = (b - a) / 6 * (fa + 4 * fc + fb)
    return _rec(a, b, fa, fb, fc, whole, 0)
