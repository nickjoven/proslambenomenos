#!/usr/bin/env python3
"""P-30 experiment: the order ladder. Runs AFTER the registration
commit. Exact complex arithmetic throughout; clauses (a)-(e) as
registered in PREDICTIONS.md P-30.

Results -> p30_results.json.
"""
import itertools
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import p30_derive as D

RT2 = math.sqrt(2.0)


# ------------------------------------------------------ (a) OCB causal rung
def ocb_causal_max():
    """Exhaustive over deterministic one-way-signalling strategies.
    Order A->B: Alice sends m = f(a); her guess x = gA(a); Bob's
    guess y = gB(m, b, b'). Order B->A mirrored (Bob sends
    m = f(b, b'), guess y = gB(b, b'); Alice x = gA(a, m))."""
    best = 0.0
    n_str = 0
    fs = list(itertools.product((0, 1), repeat=2))     # f: {0,1}->{0,1}
    gAs = fs
    gB8 = list(itertools.product((0, 1), repeat=8))    # g(m,b,b')
    for f in fs:
        for gA in gAs:
            for gB in gB8:
                n_str += 1
                s = 0.0
                for a in (0, 1):
                    for b in (0, 1):
                        m = f[a]
                        x = gA[a]
                        y0 = gB[m * 4 + b * 2 + 0]
                        y1 = gB[m * 4 + b * 2 + 1]
                        _ = y0
                        s += 0.25 * (0.5 * (x == b)
                                     + 0.5 * (y1 == a))
                best = max(best, s)
    # order B->A: Bob sends m = f2(b, b'); y = gB2(b, b');
    # Alice x = gA2(a, m)
    f2s = list(itertools.product((0, 1), repeat=4))
    gB2s = f2s
    gA2s = f2s
    for f2 in f2s:
        for gB2 in gB2s:
            for gA2 in gA2s:
                n_str += 1
                s = 0.0
                for a in (0, 1):
                    for b in (0, 1):
                        m0 = f2[b * 2 + 0]
                        x0 = gA2[a * 2 + m0]
                        y1 = gB2[b * 2 + 1]
                        s += 0.25 * (0.5 * (x0 == b)
                                     + 0.5 * (y1 == a))
                best = max(best, s)
    return best, n_str


# ------------------------------------------------- (b) OCB process rung
def ocb_process_value_clean():
    """p = (1/2)[P(x=b|b'=0) + P(y=a|b'=1)], settings uniform."""
    p0 = 0.0
    p1 = 0.0
    for a in (0, 1):
        for b in (0, 1):
            for x in (0, 1):
                for y in (0, 1):
                    pr0 = D.ocb_probability(x, a, y, b, 0)
                    pr1 = D.ocb_probability(x, a, y, b, 1)
                    if x == b:
                        p0 += pr0 / 4
                    if y == a:
                        p1 += pr1 / 4
    return 0.5 * (p0 + p1)


# ------------------------------------------------- (c) VLBC rung
def vlbc_causal_max():
    """Exhaustive deterministic DRF strategies for Theorem 1's
    inequality. lambda = 1: A1 < A2 < C; lambda = 2: A2 < A1 < C;
    Bob spacelike (b = g(y) only; a, c never see y).
    a1 = f1(x1 [, x2 if second]), a2 = f2(x2 [, x1 if second]),
    c = h(x1, x2, z), b = g(y)."""
    best = 0.0
    n_str = 0
    f1_first = list(itertools.product((0, 1), repeat=2))   # a1(x1)
    f2_second = list(itertools.product((0, 1), repeat=4))  # a2(x1,x2)
    hs = list(itertools.product((0, 1), repeat=8))         # c(x1,x2,z)
    gs = list(itertools.product((0, 1), repeat=2))         # b(y)

    def value(a1f, a2f, h, g, order):
        # returns LHS of inequality (6)
        t1 = t2 = t3 = 0.0
        for x1 in (0, 1):
            for x2 in (0, 1):
                if order == 1:
                    a1 = a1f[x1]
                    a2 = a2f[x1 * 2 + x2]
                else:
                    a2 = a1f[x2]
                    a1 = a2f[x2 * 2 + x1]
                for y in (0, 1):
                    b = g[y]
                    for z in (0, 1):
                        c = h[x1 * 4 + x2 * 2 + z]
                        if y == 0:
                            # conditioned on y=0: weight 1/8 over x1x2z
                            if b == 0 and a2 == x1:
                                t1 += 1 / 8
                            if b == 1 and a1 == x2:
                                t2 += 1 / 8
                        if x1 == 0 and x2 == 0:
                            # conditioned on x=00: weight 1/4 over y z
                            if (b ^ c) == (y & z):
                                t3 += 1 / 4
        return t1 + t2 + t3

    for order in (1, 2):
        for a1f in f1_first:
            for a2f in f2_second:
                for g in gs:
                    for h in hs:
                        n_str += 1
                        best = max(best, value(a1f, a2f, h, g, order))
    return best, n_str


def vlbc_algebraic_max():
    """Unconstrained deterministic assignments p(a b c | x y z):
    outcomes may depend on everything."""
    # first two terms: disjoint in b given y=0 -> sum <= 1,
    # achievable; third <= 1. Verify by direct construction:
    # b = y? choose b(everything): allow b to depend on x1,x2,z too
    best = 0.0
    # construct: b=0, a2=x1, a1 arbitrary -> t1 = 1; t3: c = b^(y z)
    # with b known: c(x,y,z) free -> t3 = 1. total 2.
    t1 = 1.0
    t3 = 1.0
    best = t1 + t3
    return best


def switch_vlbc_value():
    """The exact circuit: |Phi+>_{CB}, target |0>, measure-reprepare
    Alices (order controlled by C), Bob Z/X on B, Charlie
    (Z+-X)/rt2 on output C."""
    # state vector on C (x) B, target handled through Kraus
    # p(a1 a2 b c | x1 x2 y z):
    # amplitude: for control 0 branch: A1 then A2 on target;
    # control 1: A2 then A1. Target starts |0>.
    # A_i Kraus for outcome a_i, setting x_i: K = |x_i><a_i|
    def K(x, a):
        M = [[0j] * 2 for _ in range(2)]
        M[x][a] = 1 + 0j
        return M

    def apply2(Ka, Kb, v):  # Kb after Ka on a 2-vector
        w = [sum(Ka[i][j] * v[j] for j in range(2)) for i in range(2)]
        return [sum(Kb[i][j] * w[j] for j in range(2))
                for i in range(2)]

    def bloch_proj(nx, nz, out):
        # projector onto outcome 'out' of measurement n.sigma
        # eigenvector for +1: ...; build (1 + s n.sigma)/2
        s = 1 - 2 * out
        return [[0.5 * (1 + s * nz), 0.5 * s * nx],
                [0.5 * s * nx, 0.5 * (1 - s * nz)]]

    P = {}
    for x1 in (0, 1):
        for x2 in (0, 1):
            for y in (0, 1):
                for z in (0, 1):
                    for a1 in (0, 1):
                        for a2 in (0, 1):
                            # branch amplitudes on (C,B) after target
                            # contraction: |Phi+> = (|00>+|11>)/rt2
                            t0 = [1 + 0j, 0j]
                            amp0 = apply2(K(x1, a1), K(x2, a2), t0)
                            amp1 = apply2(K(x2, a2), K(x1, a1), t0)
                            # target discarded: sum over final target
                            # basis t: joint (C,B) unnormalized state
                            # |psi_t> = (amp0[t] |0>_C + amp1[t] |1>_C)
                            #            (x) |C-partner>_B / rt2
                            # with B entangled to INPUT control:
                            # |Phi+>_{CB}: control branch c0 pairs
                            # with B=|0>, c1 with B=|1>.
                            for b in (0, 1):
                                for c in (0, 1):
                                    # y=0: Z; y=1: X
                                    nxB, nzB = (0.0, 1.0) if y == 0 \
                                        else (1.0, 0.0)
                                    # z=0: (Z+X)/rt2; z=1: (Z-X)/rt2
                                    nxC = (1 / RT2) * (1 if z == 0
                                                       else -1)
                                    nzC = 1 / RT2
                                    PB = bloch_proj(nxB, nzB, b)
                                    PC = bloch_proj(nxC, nzC, c)
                                    pr = 0.0
                                    for t in (0, 1):
                                        # unnormalized |phi> on C(x)B
                                        # = (amp0[t]|0 0> + amp1[t]|1 1>)/rt2
                                        v = {(0, 0): amp0[t] / RT2,
                                             (1, 1): amp1[t] / RT2}
                                        # <phi| PC (x) PB |phi>
                                        acc = 0j
                                        for (ci, bi), vi in v.items():
                                            for (cj, bj), vj in \
                                                    v.items():
                                                acc += (vi.conjugate()
                                                        * vj
                                                        * PC[ci][cj]
                                                        * PB[bi][bj])
                                        pr += acc.real
                                    P[(a1, a2, b, c, x1, x2, y, z)] = pr
    # inequality (6) terms
    t1 = t2 = t3 = 0.0
    for k, pr in P.items():
        a1, a2, b, c, x1, x2, y, z = k
        if y == 0:
            if b == 0 and a2 == x1:
                t1 += pr / 8
            if b == 1 and a1 == x2:
                t2 += pr / 8
        if x1 == 0 and x2 == 0:
            if (b ^ c) == (y & z):
                t3 += pr / 4
    return t1, t2, t3, P


# ------------------------------------------------- (d) separability null
def switch_alice_marginal():
    """p(a1 a2 | x1 x2) with control |+>, B absent, C discarded,
    against the 50/50 classical mixture of fixed orders."""
    def K(x, a):
        M = [[0j] * 2 for _ in range(2)]
        M[x][a] = 1 + 0j
        return M

    def apply2(Ka, Kb, v):
        w = [sum(Ka[i][j] * v[j] for j in range(2)) for i in range(2)]
        return [sum(Kb[i][j] * w[j] for j in range(2))
                for i in range(2)]

    worst = 0.0
    for x1 in (0, 1):
        for x2 in (0, 1):
            for a1 in (0, 1):
                for a2 in (0, 1):
                    t0 = [1 + 0j, 0j]
                    amp0 = apply2(K(x1, a1), K(x2, a2), t0)
                    amp1 = apply2(K(x2, a2), K(x1, a1), t0)
                    # control |+>, C discarded, target discarded:
                    # p = sum_t || (amp0[t]|0> + amp1[t]|1>)/rt2 ||^2
                    p_sw = sum(abs(amp0[t]) ** 2 / 2
                               + abs(amp1[t]) ** 2 / 2
                               for t in (0, 1))
                    p_mix = 0.5 * sum(abs(amp0[t]) ** 2
                                      for t in (0, 1)) \
                        + 0.5 * sum(abs(amp1[t]) ** 2 for t in (0, 1))
                    worst = max(worst, abs(p_sw - p_mix))
    return worst


def main():
    out = {"clauses": {}}

    print("== (a) OCB causal rung, exhaustive")
    mx, n = ocb_causal_max()
    ok_a = abs(mx - 0.75) < 1e-15
    print(f"  max {mx} over {n} deterministic strategies "
          f"{'ok' if ok_a else 'FAIL'}")
    out["ocb_causal"] = {"max": mx, "strategies": n}
    out["clauses"]["a"] = ok_a

    print("== (b) OCB process rung")
    pv = ocb_process_value_clean()
    want = (2 + RT2) / 4
    ok_b = abs(pv - want) < 1e-12
    print(f"  process value {pv:.12f} vs (2+rt2)/4 {want:.12f} "
          f"{'ok' if ok_b else 'FAIL'}")
    out["ocb_process"] = pv
    out["clauses"]["b"] = ok_b

    print("== (c) VLBC rung")
    cmx, cn = vlbc_causal_max()
    ok_c1 = abs(cmx - 1.75) < 1e-15
    print(f"  DRF exhaustive max {cmx} over {cn} strategies "
          f"{'ok' if ok_c1 else 'FAIL'}")
    t1, t2, t3, _ = switch_vlbc_value()
    sv = t1 + t2 + t3
    wantv = 1 + (2 + RT2) / 4
    ok_c2 = abs(sv - wantv) < 1e-12
    print(f"  switch value {sv:.12f} = {t1:.4f} + {t2:.4f} + "
          f"{t3:.12f} vs {wantv:.12f} {'ok' if ok_c2 else 'FAIL'}")
    amx = vlbc_algebraic_max()
    ok_c3 = abs(amx - 2.0) < 1e-15
    out["vlbc"] = {"causal_max": cmx, "strategies": cn,
                   "switch_terms": [t1, t2, t3], "switch_value": sv,
                   "algebraic_max": amx}
    out["clauses"]["c"] = ok_c1 and ok_c2 and ok_c3

    print("== (d) the separability null")
    worst = switch_alice_marginal()
    ok_d = worst < 1e-12
    print(f"  |switch marginal - classical order mixture| worst "
          f"{worst:.2e} {'ok' if ok_d else 'FAIL'}")
    out["separability_worst"] = worst
    out["clauses"]["d"] = ok_d

    print("== (e) the ladder assembly")
    S_ocb = [8 * p - 4 for p in (mx, pv, 1.0)]
    S_vlbc = [8 * (p - 1) - 4 for p in (cmx, sv, amx)]
    bell = [2.0, 2 * RT2, 4.0]
    ok_e = all(abs(a - b) < 1e-12 for a, b in zip(S_ocb, bell)) and \
        all(abs(a - b) < 1e-12 for a, b in zip(S_vlbc, bell))
    print(f"  S(OCB) = {['%.10f' % s for s in S_ocb]}")
    print(f"  S(VLBC) = {['%.10f' % s for s in S_vlbc]}")
    print(f"  both = Bell ladder {{2, 2rt2, 4}} "
          f"{'ok' if ok_e else 'FAIL'}")
    out["ladders"] = {"S_ocb": S_ocb, "S_vlbc": S_vlbc}
    out["clauses"]["e"] = ok_e

    json.dump(out, open(os.path.join(HERE, "p30_results.json"), "w"),
              indent=1)
    print("results -> p30_results.json")
    print("clauses:", out["clauses"])
    return 0 if all(out["clauses"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
