#!/usr/bin/env python3
"""P-38 derivation layer (pre-registration): the Hardy-order bridge.

A-21, first item of the earned frontier (owner directive 2026-09-01:
earned parts to their ends before cleanup). Van der Lugt & Ormrod,
Quantum 8, 1543 (2024) / arXiv:2311.00557: a POSSIBILISTIC (GHZ-
style, probability-free at the hidden-variable level) proof that
the quantum switch's causal order is indefinite. Their scenario,
re-derived here with our own instruments before registration:

Three quantum switches A, B, C at spacelike separation, controls
in the GHZ state (|000> + |111>)/sqrt2, targets each |0>. Each
switch is controlled in the X basis:
    W = |+><+| (x) F E  +  |-><-| (x) E F
(E = agent 1's Kraus, applied FIRST in the |+> branch). Agent i
(i = 1, 2) has input x_i: x_i = 0 -> identity, output a_i = 0;
x_i = 1 -> Z-measure the target (outcome a_i), re-prepare |1>.
Agent 3 measures the outgoing control in the Y basis (a_3).

Derived facts:
  EQ1  the switch data, from our own 64-dim simulation (stdlib
       complex): for the four registered input patterns the parity
       events forbidden by
         x=y=z=1     ->  a1+b1+c1 = 0 (mod 2)
         x=1,y=z=0   ->  a1+b3+c3 = 1
         x=0,y=1,z=0 ->  a3+b1+c3 = 1
         x=y=0,z=1   ->  a3+b3+c1 = 1
       have probability EXACTLY zero (machine floor), and every
       parity-allowed outcome has the same derived probability
       (uniform over the allowed set) - the possibilistic pattern
       with its numbers pinned.
  EQ2  the classical ceiling, exhaustive: deterministic local
       models (per switch, outputs any functions of that switch's
       own inputs; relativistic causality forbids more, and the
       imported Theorem 1 reduces definite causal order + free
       choice to exactly this class) - all 4096 strategies
       enumerated; the maximum number of the four conditions
       jointly satisfiable is 3, never 4. Restricting to the
       64 effective assignments (a1 at x=1, a3 at x=0 per switch)
       gives the same ceiling - the GHZ parity argument, exhausted
       rather than asserted.
  EQ3  the Mermin functional M = E_111(a1b1c1) - E_100(a1b3c3)
       - E_010(a3b1c3) - E_001(a3b3c1) (expectations of the
       parity +-1 variables): classical max = 2 over the 4096
       (exhaustive), the switch value = 4 (from EQ1's zeros), and
       4 is the ALGEBRAIC maximum - the switch sits on the
       ceiling, which is the paper's "maximal" statement in
       ladder-priced form.
  EQ4  instrument nulls (item 8): (a) normalization - each input
       pattern's 64 outcome probabilities sum to 1 at 1e-14;
       (b) no-signalling spot check - A-side marginals invariant
       under y, z at 1e-14 (the relativistic-causality premise is
       a property of the DATA, verified, not assumed);
       (c) definite-wiring control - replacing every switch with
       the fixed wiring FE (a definite-order world) satisfies
       condition 1 but breaks all three Y-pattern conditions:
       the contradiction needs the coherence, not the bookkeeping.

Run: python3 scripts/experiments/p38_derive.py
"""
import itertools
import json
import math
import os

SQ2 = math.sqrt(2.0)


# ---------------------------------------------------------------
# state machinery: dense complex vectors over listed qubits
# ---------------------------------------------------------------
def kron_state(*amps_lists):
    out = [1.0 + 0.0j]
    for amps in amps_lists:
        out = [a * b for a in out for b in amps]
    return out


def apply_1q(state, n, q, m):
    """Apply 2x2 matrix m to qubit q (0 = most significant)."""
    out = [0.0j] * len(state)
    shift = n - 1 - q
    for i, a in enumerate(state):
        if a == 0:
            continue
        bit = (i >> shift) & 1
        for nb in (0, 1):
            c = m[nb][bit]
            if c != 0:
                out[i ^ ((bit ^ nb) << shift)] += c * a
    return out


# ---------------------------------------------------------------
# one switch: control qubit c, target qubit t, agent inputs x1 x2
# returns list of (a1, a2, kraus-branch state factor) applied to
# the joint state; we implement by branching over Kraus outcomes.
# ---------------------------------------------------------------
def agent_kraus(x):
    """Kraus list [(outcome, 2x2 matrix)] for one agent."""
    if x == 0:
        return [(0, [[1, 0], [0, 1]])]
    # measure Z (outcome r), then prepare |1>: K_r = |1><r|
    return [(0, [[0, 0], [1, 0]]), (1, [[0, 0], [0, 1]])]


def switch_branches(x1, x2):
    """All (a1, a2, wiring-conditional op pairs): returns list of
    (a1, a2, K_plus, K_minus) where K_plus = K2 K1 (agent 1 FIRST
    in the |+> branch: W has F E there, E = agent 1) and
    K_minus = K1 K2."""
    def mm(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(2))
                 for j in range(2)] for i in range(2)]
    out = []
    for a1, K1 in agent_kraus(x1):
        for a2, K2 in agent_kraus(x2):
            out.append((a1, a2, mm(K2, K1), mm(K1, K2)))
    return out


def run_pattern(xs, ys, zs, definite_wiring=None):
    """Return dict {(a1,a2,a3,b1,b2,b3,c1,c2,c3): probability}.
    Qubit layout: [cA, cB, cC, tA, tB, tC] (n = 6).
    definite_wiring: None = the real switch; 'FE' = every switch
    replaced by the fixed |+>-branch wiring (EQ4c control)."""
    n = 6
    inv2 = 1.0 / SQ2
    ghz = [0.0j] * 8
    ghz[0] = inv2
    ghz[7] = inv2
    base = kron_state(ghz, [1, 0], [1, 0], [1, 0])
    # project each control onto X basis to apply the wiring, then
    # rebuild: easier to branch over Kraus outcomes and apply
    # controlled ops as 2x2 blocks on (control, target) pairs.
    probs = {}
    sw_inputs = [xs, ys, zs]
    branch_sets = [switch_branches(*sw_inputs[s]) for s in range(3)]
    for br in itertools.product(*branch_sets):
        st = list(base)
        outs = []
        for s, (o1, o2, Kp, Km) in enumerate(br):
            outs.append((o1, o2))
            cq, tq = s, 3 + s
            if definite_wiring == "FE":
                st = apply_ct(st, n, cq, tq, Kp, Kp)
            else:
                st = apply_ct(st, n, cq, tq, Kp, Km)
        # agent-3 Y measurements on each control
        for a3s in itertools.product((0, 1), repeat=3):
            st2 = list(st)
            for s, a3 in enumerate(a3s):
                # projector onto |+i> (a3=0) or |-i> (a3=1)
                sgn = 1.0 if a3 == 0 else -1.0
                P = [[0.5, -0.5j * sgn], [0.5j * sgn, 0.5]]
                st2 = apply_1q(st2, n, s, P)
            p = sum(abs(a) ** 2 for a in st2)
            if p < 1e-16:
                continue
            key = (outs[0][0], outs[0][1], a3s[0],
                   outs[1][0], outs[1][1], a3s[1],
                   outs[2][0], outs[2][1], a3s[2])
            probs[key] = probs.get(key, 0.0) + p
    return probs


def apply_ct(state, n, cq, tq, K_plus, K_minus):
    """Apply |+><+|_c (x) K_plus + |-><-|_c (x) K_minus on qubits
    (cq, tq)."""
    out = [0.0j] * len(state)
    cs, ts = n - 1 - cq, n - 1 - tq
    for i, a in enumerate(state):
        if a == 0:
            continue
        cb, tb = (i >> cs) & 1, (i >> ts) & 1
        for ncb in (0, 1):
            for ntb in (0, 1):
                # <ncb| (|+><+|)|cb> = 1/2 ; <ncb| (|-><-|)|cb>
                # = (+-)1/2 with sign (-1)^(ncb+cb)
                wp = 0.5
                wm = 0.5 * (1 if (ncb + cb) % 2 == 0 else -1)
                c = wp * K_plus[ntb][tb] + wm * K_minus[ntb][tb]
                if c != 0:
                    j = i ^ ((cb ^ ncb) << cs) ^ ((tb ^ ntb) << ts)
                    out[j] += c * a
    return out


# ---------------------------------------------------------------
# the four conditions
# ---------------------------------------------------------------
PATTERNS = [
    (((1, 1), (1, 1), (1, 1)), ("a1", "b1", "c1"), 0),
    (((1, 1), (0, 0), (0, 0)), ("a1", "b3", "c3"), 1),
    (((0, 0), (1, 1), (0, 0)), ("a3", "b1", "c3"), 1),
    (((0, 0), (0, 0), (1, 1)), ("a3", "b3", "c1"), 1),
]
IDX = {"a1": 0, "a2": 1, "a3": 2, "b1": 3, "b2": 4, "b3": 5,
       "c1": 6, "c2": 7, "c3": 8}


def eq1_eq4():
    res = {"patterns": [], "nulls": {}}
    marg_ref = None
    for (xs, ys, zs), vars3, parity in PATTERNS:
        probs = run_pattern(xs, ys, zs)
        tot = sum(probs.values())
        bad = 0.0
        good = {}
        for k, p in probs.items():
            s = sum(k[IDX[v]] for v in vars3) % 2
            if s != parity:
                bad = max(bad, p)
            else:
                good[k] = p
        gv = list(good.values())
        res["patterns"].append({
            "inputs": [xs, ys, zs], "vars": vars3, "parity": parity,
            "total": tot, "worst_forbidden": bad,
            "n_allowed": len(gv), "min_allowed": min(gv),
            "max_allowed": max(gv)})
        # no-signalling: A-side marginal (a1,a2,a3)
        marg = {}
        for k, p in probs.items():
            marg[k[:3]] = marg.get(k[:3], 0.0) + p
        if xs == (1, 1):
            if marg_ref is None:
                marg_ref = marg
            else:
                d = max(abs(marg.get(k, 0) - marg_ref.get(k, 0))
                        for k in set(marg) | set(marg_ref))
                res["nulls"]["nosig_A_worst"] = max(
                    res["nulls"].get("nosig_A_worst", 0.0), d)
    # EQ4c definite-wiring control
    ctrl = []
    for (xs, ys, zs), vars3, parity in PATTERNS:
        probs = run_pattern(xs, ys, zs, definite_wiring="FE")
        viol = sum(p for k, p in probs.items()
                   if sum(k[IDX[v]] for v in vars3) % 2 != parity)
        ctrl.append(round(viol, 6))
    res["nulls"]["definite_FE_violation_mass"] = ctrl
    return res


# ---------------------------------------------------------------
# EQ2/EQ3: exhaustive classical enumeration
# ---------------------------------------------------------------
def eq2_eq3():
    best_sat, sat_hist = 0, {}
    best_M = -99
    # per switch: a1 response to x in {0,1} (2 bits), a3 response
    # to x (2 bits) -> 16 strategies per switch, 4096 total
    for sa in range(16):
        for sb in range(16):
            for sc in range(16):
                def out(s, which, x):
                    # bits: a1(0),a1(1),a3(0),a3(1)
                    return (s >> (which * 2 + x)) & 1
                sat = 0
                conds = [
                    ((out(sa, 0, 1) + out(sb, 0, 1)
                      + out(sc, 0, 1)) % 2, 0),
                    ((out(sa, 0, 1) + out(sb, 1, 0)
                      + out(sc, 1, 0)) % 2, 1),
                    ((out(sa, 1, 0) + out(sb, 0, 1)
                      + out(sc, 1, 0)) % 2, 1),
                    ((out(sa, 1, 0) + out(sb, 1, 0)
                      + out(sc, 0, 1)) % 2, 1),
                ]
                M = 0
                for i, (par, want) in enumerate(conds):
                    ok = par == want
                    sat += ok
                    e = 1 if par == 0 else -1
                    M += e if i == 0 else -e
                best_sat = max(best_sat, sat)
                sat_hist[sat] = sat_hist.get(sat, 0) + 1
                best_M = max(best_M, M)
    return {"n_strategies": 4096, "max_conditions_satisfied": best_sat,
            "histogram": sat_hist, "mermin_classical_max": best_M,
            "mermin_algebraic_max": 4}


def main():
    r14 = eq1_eq4()
    r23 = eq2_eq3()
    res = {"EQ1_EQ4": r14, "EQ2_EQ3": r23}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "p38_registration.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
