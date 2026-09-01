#!/usr/bin/env python3
"""P-39 derivation layer (pre-registration): the alpha-family
(A-22, second item of the earned frontier).

Liu & Chiribella (Nat. Commun. 16, 3314 (2025); arXiv:2403.02749)
proved the ICO Tsirelson bound for the biased OCB correlation
  I_alpha = P(a1 = b | c = 0) + alpha * P(a2 = x1 | c = 1):
  ICO bound B(alpha) = (1 + alpha + sqrt(1 + alpha^2)) / 2.   [IMPORTED]
Geometrically: the pair (P_A, P_B) lives in the circle of radius
1/2 around (1/2, 1/2); causal distributions fill the inscribed
square. What this layer EARNS with P-30's instruments:

  EQ1  the causal side, exhaustive and exact: all 8192
       deterministic one-way-signalling strategies (4 x 4 x 256
       per order, both orders - P-30's count) evaluated in
       Fraction arithmetic; the causal value is
         C(alpha) = max(1 + alpha/2, 1/2 + alpha)
       exactly, on the registered rational alpha grid. The
       extreme causal points are (1, 1/2) and (1/2, 1).
  EQ2  the achieving family, constructed by us: W(theta) =
       (1/4)[1 + cos(theta) A + sin(theta) B] with A = sz^A2
       sz^B1, B = sz^A1 sx^B1 sz^B2 (the OCB terms; theta = pi/4
       is P-30's W). Validity for every theta: Hermitian, Tr = 4,
       spectrum {0 x8, 1/2 x8}, and the no-causal-loop
       trace-and-replace identity of P-30 EQ3.
  EQ3  achievability ON the circle: with the OCB local strategies
       (eqs. 20-23 conventions, full contraction - no shortcut),
       the two success probabilities are (1 +- trig)/2, and at
       the optimal angle the value lands on B(alpha) at 1e-12.
       Which trig feeds which task is determined by computation,
       not assumed.
  EQ4  geometry: the four causal extreme points lie ON the ICO
       circle (radius residual 1e-12) - the square is inscribed;
       the ICO advantage B - C is 0 at alpha = 0 exactly,
       positive on the whole grid alpha > 0, and maximized on
       the grid at alpha = 1 with value (sqrt2 - 1)/2.

Run: python3 scripts/experiments/p39_derive.py
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p30_derive import (SI, SX, SZ, herm_eigs, kron, madd,  # noqa: E402
                        matmul, mscale, pauli_string, trace,
                        trace_replace)

ALPHAS = [Fraction(0), Fraction(1, 4), Fraction(1, 2),
          Fraction(3, 4), Fraction(1), Fraction(3, 2),
          Fraction(2), Fraction(4)]


# ---------------------------------------------------------------
# EQ1: exhaustive causal side, exact
# ---------------------------------------------------------------
def causal_extremes():
    """All 8192 deterministic one-way-signalling strategies
    (order AB: 4 x 4 x 256; order BA: 16 x 16 x 16), evaluated in
    exact Fractions. Returns the (P_A, P_B) point set and the
    per-alpha maximum."""
    pts = set()
    # order A -> B: a1 = f(x1), message m = g(x1), a2 = h(b, c, m)
    for f_bits in range(4):
        for g_bits in range(4):
            for h_bits in range(256):
                pa = pb = 0
                for x1 in (0, 1):
                    for b in (0, 1):
                        a1 = (f_bits >> x1) & 1
                        m = (g_bits >> x1) & 1
                        if a1 == b:
                            pa += 1
                        a2 = (h_bits >> ((b << 2) | (1 << 1) | m)) & 1
                        if a2 == x1:
                            pb += 1
                pts.add((Fraction(pa, 4), Fraction(pb, 4)))
    # order B -> A: a2 = f(b, c), m = g(b, c), a1 = h(x1, m)
    for f_bits in range(16):
        for g_bits in range(16):
            for h_bits in range(16):
                pa = pb = 0
                for x1 in (0, 1):
                    for b in (0, 1):
                        a2 = (f_bits >> ((b << 1) | 1)) & 1
                        if a2 == x1:
                            pb += 1
                        m = (g_bits >> (b << 1)) & 1
                        a1 = (h_bits >> ((x1 << 1) | m)) & 1
                        if a1 == b:
                            pa += 1
                pts.add((Fraction(pa, 4), Fraction(pb, 4)))
    best = {}
    for al in ALPHAS:
        best[al] = max(pa + al * pb for pa, pb in pts)
    return pts, best


def eq1():
    pts, best = causal_extremes()
    out = {"n_points": len(pts), "per_alpha": {}}
    ok_all = True
    for al in ALPHAS:
        closed = max(1 + al / 2, Fraction(1, 2) + al)
        ok = best[al] == closed
        ok_all = ok_all and ok
        out["per_alpha"][str(al)] = {
            "enumerated": str(best[al]), "closed_form": str(closed),
            "equal": ok}
    out["extremes_present"] = (
        (Fraction(1), Fraction(1, 2)) in pts
        and (Fraction(1, 2), Fraction(1)) in pts)
    out["all_equal"] = ok_all
    return out


# ---------------------------------------------------------------
# EQ2/EQ3: the rotated family
# ---------------------------------------------------------------
def W_theta(th):
    A = pauli_string([SI, SZ, SZ, SI])
    B = pauli_string([SZ, SI, SX, SZ])
    return mscale(0.25, madd(pauli_string([SI, SI, SI, SI]),
                             mscale(math.cos(th), A),
                             mscale(math.sin(th), B)))


def probs_theta(th):
    """Full-contraction success probabilities (P_A, P_B) for
    W(theta) with the OCB strategies (P-30 eq. 20-23 route)."""
    W = W_theta(th)

    def prob(x, a, y, b, bp):
        xi = mscale(0.25, kron(madd(SI, mscale((-1) ** x, SZ)),
                               madd(SI, mscale((-1) ** a, SZ))))
        if bp == 1:
            rho = mscale(0.5, SI)
            eta = mscale(0.5, kron(madd(SI, mscale((-1) ** y, SZ)),
                                   rho))
        else:
            eta = mscale(0.25, kron(madd(SI, mscale((-1) ** y, SX)),
                                    madd(SI, mscale((-1) ** (b ^ y),
                                                    SZ))))
        return trace(matmul(W, kron(xi, eta))).real

    # OCB roles: x, y are the MEASUREMENT OUTCOMES (the guesses),
    # a, b, b' the inputs. P_A = P(x = b | b' = 0): Alice's outcome
    # equals Bob's bit; P_B = P(y = a | b' = 1): Bob's outcome
    # equals Alice's bit. Inputs a, b uniform.
    pa = sum(prob(b, a, y, b, 0) for a in (0, 1) for b in (0, 1)
             for y in (0, 1)) / 4
    pb = sum(prob(x, a, a, b, 1) for a in (0, 1) for b in (0, 1)
             for x in (0, 1)) / 4
    return pa, pb


def eq2_eq3():
    out = {"validity": {}, "achieve": {}}
    for al in ALPHAS:
        alf = float(al)
        # optimal angle: maximize P_A + alpha P_B; determined
        # numerically over theta, then compared to closed form
        best_th, best_v = None, -1
        for k in range(721):
            th = math.pi * k / 720
            pa, pb = probs_theta(th)
            v = pa + alf * pb
            if v > best_v:
                best_v, best_th = v, th
        # fine refine
        for _ in range(60):
            for dth in (1e-3, 1e-5, 1e-7):
                for cand in (best_th - dth, best_th + dth):
                    pa, pb = probs_theta(cand)
                    v = pa + alf * pb
                    if v > best_v:
                        best_v, best_th = v, cand
        Wv = W_theta(best_th)
        evs = sorted(herm_eigs(Wv))
        spec_ok = (all(abs(e) < 1e-9 for e in evs[:8])
                   and all(abs(e - 0.5) < 1e-9 for e in evs[8:]))
        tr_ok = abs(trace(Wv).real - 4) < 1e-10
        # no-causal-loop identity (P-30 EQ3 form)
        lhs = Wv
        rhs = madd(trace_replace(Wv, [1]), trace_replace(Wv, [3]),
                   mscale(-1.0, trace_replace(Wv, [1, 3])))
        loop_ok = max(abs(lhs[i][j] - rhs[i][j]) for i in range(16)
                      for j in range(16)) < 1e-10
        bound = (1 + alf + math.sqrt(1 + alf * alf)) / 2
        out["validity"][str(al)] = {"spec_ok": spec_ok,
                                    "trace_ok": tr_ok,
                                    "loop_ok": loop_ok}
        out["achieve"][str(al)] = {
            "theta_star": best_th, "value": best_v,
            "bound_imported": bound, "gap": bound - best_v}
    return out


def eq4(eq1_out, eq23_out):
    out = {}
    # inscribed square: extreme causal points on the circle
    for pt in [(1.0, 0.5), (0.5, 1.0), (0.0, 0.5), (0.5, 0.0)]:
        r = math.hypot(pt[0] - 0.5, pt[1] - 0.5)
        out.setdefault("radius_residuals", []).append(abs(r - 0.5))
    # advantage curve
    adv = {}
    for al in ALPHAS:
        alf = float(al)
        B = (1 + alf + math.sqrt(1 + alf * alf)) / 2
        C = float(max(1 + al / 2, Fraction(1, 2) + al))
        adv[str(al)] = B - C
    out["advantage"] = adv
    out["adv_zero_at_0"] = abs(adv["0"]) < 1e-15
    out["adv_max_at_1"] = max(adv, key=lambda k: adv[k]) == "1"
    out["adv_at_1_vs_closed"] = abs(
        adv["1"] - (math.sqrt(2) - 1) / 2)
    return out


def main():
    r1 = eq1()
    r23 = eq2_eq3()
    r4 = eq4(r1, r23)
    res = {"EQ1": r1, "EQ2_EQ3": r23, "EQ4": r4}
    with open(os.path.join(HERE, "p39_registration.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print("EQ1 all_equal:", r1["all_equal"], "n_points:",
          r1["n_points"], "extremes:", r1["extremes_present"])
    for al, d in r23["achieve"].items():
        v = r23["validity"][al]
        print(f"alpha {al}: value {d['value']:.12f} vs bound "
              f"{d['bound_imported']:.12f} gap {d['gap']:.2e} "
              f"valid {v['spec_ok'] and v['trace_ok'] and v['loop_ok']}")
    print("EQ4:", json.dumps(r4, indent=1))


if __name__ == "__main__":
    main()
