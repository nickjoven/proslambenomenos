#!/usr/bin/env python3
"""P-21 registered computation, route 2: blind numeric search for the
maximum probability of Hardy's nonlocality paradox.

Full 5-parameter space: Schmidt angle theta (psi = cos theta |00> +
sin theta |11>) plus four measurement angles alpha0, alpha1, beta0,
beta1 (the "+" outcome of angle t projects onto (cos t, sin t)).
Objective: p_Hardy - lambda * sum of squared constraint probabilities,
maximized by in-repo Nelder-Mead (stdlib only) from 200 seeded random
starts on the registered penalty schedule lambda = 1e3, 1e5, 1e7,
1e9, then polished with the constraints eliminated (envelope in k,
golden-section to 1e-12) as registered in p21_registration.json.

The registration (pinned max, Schmidt weights, tolerances, seed,
start count) was committed before this file existed; this script
reads the pins only to COMPARE against them at the end.

Outputs -> p21_results.json.
"""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p21_registration.json").read_text())

SEED = REG["optimizer"]["seed"]
STARTS = REG["optimizer"]["starts"]
LAMBDAS = REG["optimizer"]["lambda_schedule"]


# ------------------------------------------------------------ physics
def amp(c, s, ta, tb, ap, bp):
    """<alice(ta), bob(tb)|psi>; '+' of angle t is (cos t, sin t),
    '-' is (-sin t, cos t)."""
    ua = (math.cos(ta), math.sin(ta)) if ap else (-math.sin(ta), math.cos(ta))
    ub = (math.cos(tb), math.sin(tb)) if bp else (-math.sin(tb), math.cos(tb))
    return c * ua[0] * ub[0] + s * ua[1] * ub[1]


def hardy(x):
    """(p_Hardy, [P_Z1, P_Z2, P_Z3]) at x = (theta, a0, a1, b0, b1)."""
    th, a0, a1, b0, b1 = x
    c, s = math.cos(th), math.sin(th)
    z1 = amp(c, s, a0, b0, True, True) ** 2
    z2 = amp(c, s, a1, b0, True, False) ** 2
    z3 = amp(c, s, a0, b1, False, True) ** 2
    p = amp(c, s, a1, b1, True, True) ** 2
    return p, (z1, z2, z3)


def penalized(x, lam):
    p, (z1, z2, z3) = hardy(x)
    return p - lam * (z1 * z1 + z2 * z2 + z3 * z3)


def p_env(k):
    """Constraint-eliminated envelope (derivation layer EQ5)."""
    return k * k * (1 - k) ** 2 / ((1 + k * k) * (k * k - k + 1) ** 2)


# ------------------------------------------------- Nelder-Mead (ours)
def nelder_mead(f, x0, step, iters=500, ftol=1e-14, xtol=1e-11):
    """Maximize f. Classic coefficients (1, 2, 0.5, 0.5)."""
    n = len(x0)
    simplex = [list(x0)]
    for i in range(n):
        v = list(x0)
        v[i] += step
        simplex.append(v)
    fs = [f(v) for v in simplex]
    for _ in range(iters):
        order = sorted(range(n + 1), key=lambda i: -fs[i])
        simplex = [simplex[i] for i in order]
        fs = [fs[i] for i in order]
        if fs[0] - fs[-1] < ftol and max(
                abs(simplex[j][i] - simplex[0][i])
                for j in range(1, n + 1) for i in range(n)) < xtol:
            break
        cent = [sum(simplex[j][i] for j in range(n)) / n for i in range(n)]
        xr = [cent[i] + (cent[i] - simplex[-1][i]) for i in range(n)]
        fr = f(xr)
        if fr > fs[0]:
            xe = [cent[i] + 2 * (cent[i] - simplex[-1][i]) for i in range(n)]
            fe = f(xe)
            simplex[-1], fs[-1] = (xe, fe) if fe > fr else (xr, fr)
        elif fr > fs[-2]:
            simplex[-1], fs[-1] = xr, fr
        else:
            xc = [cent[i] + 0.5 * (simplex[-1][i] - cent[i]) for i in range(n)]
            fc = f(xc)
            if fc > fs[-1]:
                simplex[-1], fs[-1] = xc, fc
            else:
                for j in range(1, n + 1):
                    simplex[j] = [0.5 * (simplex[j][i] + simplex[0][i])
                                  for i in range(n)]
                    fs[j] = f(simplex[j])
    best = max(range(n + 1), key=lambda i: fs[i])
    return simplex[best], fs[best]


def golden_max(f, lo, hi, tol=1e-12):
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    x1, x2 = b - g * (b - a), a + g * (b - a)
    f1, f2 = f(x1), f(x2)
    while b - a > tol:
        if f1 < f2:
            a, x1, f1 = x1, x2, f2
            x2 = a + g * (b - a)
            f2 = f(x2)
        else:
            b, x2, f2 = x2, x1, f1
            x1 = b - g * (b - a)
            f1 = f(x1)
    x = 0.5 * (a + b)
    return x, f(x)


# ----------------------------------------------------------- the search
def main():
    rng = random.Random(SEED)
    per_start = []
    best_x, best_val = None, -1.0
    for _ in range(STARTS):
        x = [rng.uniform(0.02, math.pi / 2 - 0.02)] + \
            [rng.uniform(-math.pi / 2, math.pi / 2) for _ in range(4)]
        for lam in LAMBDAS:
            x, _ = nelder_mead(lambda v: penalized(v, lam), x, step=0.25
                               if lam == LAMBDAS[0] else 0.02)
        p, zs = hardy(x)
        per_start.append({"p": p, "viol": max(zs)})
        if p - LAMBDAS[-1] * sum(z * z for z in zs) > best_val:
            best_val = p - LAMBDAS[-1] * sum(z * z for z in zs)
            best_x = x

    p_pen, zs_pen = hardy(best_x)
    th = best_x[0] % math.pi
    c, s = abs(math.cos(th)), abs(math.sin(th))
    k_raw = c / s if s > 0 else float("inf")
    k_canon = min(k_raw, 1 / k_raw)

    # registered polish: constraints eliminated, golden-section in k
    k_star, p_star = golden_max(p_env, 1e-3, 0.999)
    c2 = k_star ** 2 / (1 + k_star ** 2)
    s2 = 1 / (1 + k_star ** 2)
    w_min, w_max = min(c2, s2), max(c2, s2)

    # registered maximally-entangled slice: k = 1, tangents
    # (a, -1/a, -1/a, a), c = s = 1/sqrt2, over the registered grid + polish
    def p_slice(la):
        aa = 10.0 ** la
        c1 = s1 = 1 / math.sqrt(2)
        return amp(c1, s1, math.atan(-1 / aa), math.atan(aa), True, True) ** 2

    grid = [(-3 + 6 * i / 999) for i in range(1000)]
    la_best = max(grid, key=p_slice)
    xs, me_max = nelder_mead(lambda v: p_slice(v[0]), [la_best], step=0.05)
    me_max = max(me_max, max(p_slice(g) for g in grid))

    pinned = REG["pinned_max"]
    dev = p_star - pinned
    dev_pen = p_pen - pinned
    w_dev = max(abs(w_min - REG["schmidt"]["weight_min"]),
                abs(w_max - REG["schmidt"]["weight_max"]))
    # basin diagnostic (not a registered clause): a start "found the
    # global basin" if its final penalized-stage p sits within 1e-3 of
    # the pinned maximum - the penalty method leaves a positive
    # infeasibility offset of order C^2/(4 lambda), so p at the
    # penalized optimum sits slightly ABOVE the constrained maximum.
    near = sum(1 for r in per_start if abs(r["p"] - pinned) < 1e-3)

    clauses = {
        "a_polished_max_within_1e-9": abs(dev) <= 1e-9,
        "b_schmidt_weights_within_1e-6": w_dev <= 1e-6,
        "c_me_slice_below_1e-12": me_max <= 1e-12,
        "mind_change_exceedance": dev > 1e-9,
        "mind_change_search_floor": p_star < pinned - 1e-6,
    }

    res = {
        "prediction": "P-21",
        "seed": SEED,
        "starts": STARTS,
        "lambda_schedule": LAMBDAS,
        "best_penalized": {
            "x": best_x,
            "p": p_pen,
            "constraint_probs": list(zs_pen),
            "k_canonical": k_canon,
            "dev_from_pinned": dev_pen,
        },
        "polished": {
            "k": k_star,
            "p": p_star,
            "dev_from_pinned": dev,
            "weight_min": w_min,
            "weight_max": w_max,
            "weight_dev_from_pinned": w_dev,
        },
        "me_slice_max": me_max,
        "starts_within_1e-3_of_pinned": near,
        "pinned_max": pinned,
        "clauses": clauses,
    }
    (HERE / "p21_results.json").write_text(json.dumps(res, indent=1) + "\n")

    print(f"pinned maximum        {pinned:.15f}")
    print(f"best penalized p      {p_pen:.15f}  (dev {dev_pen:+.3e}; "
          f"worst constraint prob {max(zs_pen):.3e})")
    print(f"polished maximum      {p_star:.15f}  (dev {dev:+.3e})")
    print(f"polished k            {k_star:.15f}  (pinned {REG['k_star']:.15f})")
    print(f"Schmidt weights       {w_min:.12f} / {w_max:.12f}  "
          f"(dev {w_dev:.3e})")
    print(f"ME slice maximum      {me_max:.3e}")
    print(f"starts near pinned    {near}/{STARTS}")
    for name, ok in clauses.items():
        print(f"clause {name}: {ok}")
    ok = (clauses["a_polished_max_within_1e-9"]
          and clauses["b_schmidt_weights_within_1e-6"]
          and clauses["c_me_slice_below_1e-12"]
          and not clauses["mind_change_exceedance"]
          and not clauses["mind_change_search_floor"])
    print("all registered clauses as expected" if ok
          else "REGISTERED CLAUSE FAILED - record, do not rescue")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
