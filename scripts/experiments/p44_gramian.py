#!/usr/bin/env python3
"""P-44 registered run: the Jin-v4 corroboration clauses
(PREDICTIONS.md P-44 fixed before this ran). Instruments:
p44_spotcheck.py / p44_ellipse.py - the fresh-context survey
agent's verification layer, committed as provenance and imported
here as functions. Lessons L-7/L-8/L-9 consulted.

Run: python3 scripts/experiments/p44_gramian.py
"""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p44_spotcheck import (core_checks, dag, double_layer, eye,  # noqa: E402
                           fro, inv, madd, make_instance, mm,
                           opnorm, smul)
from p44_ellipse import ellipse_run  # noqa: E402


def disk_mass(inst, N=2048):
    A1, gam = double_layer(inst, N)
    n = inst["n"]
    Mass = [[0j] * n for _ in range(n)]
    for k in range(N):
        Dk = madd(A1[k], dag(A1[k]))
        Mass = madd(Mass, smul(inst["Rdom"] / N, Dk))
    return fro(madd(Mass, smul(2, eye(n)), 1, -1))


def jordan_ramp():
    """The derive layer's pinned near-extremal family:
    B = [[eps, 1], [0, -eps]], Omega = disk of radius ~w(B),
    f = z / Rdom; the chain slack must stay positive and shrink
    toward 0 as |T| -> 2."""
    import cmath
    from p44_spotcheck import PQ, eigmax, eigmin, herm_part
    rows = []
    # the derive layer's pinned family (p44_spotcheck near-extremal
    # section): B = [[eps, 1], [0, -eps]], symmetric eigenvalue
    # split, numerical radius 1/2 + O(eps^2) - the first draft of
    # this runner used [[0,1],[0,eps]] (radius 1/2 + O(eps), too
    # slow an approach to 2) and fired clause (d); the fix restores
    # the registered instrument, recorded in R-43.
    for eps in (0.3, 0.1, 0.03, 0.01):
        B = [[eps + 0j, 1 + 0j], [0j, -eps + 0j]]
        S = [[1 + 0j, 1 + 0j], [0j, -2 * eps + 0j]]
        Si = inv(S)
        wB = 0.0
        for k in range(1440):
            th = 2 * math.pi * k / 1440
            M = herm_part(smul(cmath.exp(-1j * th), B))
            wB = max(wB, eigmax(M))
        Rdom = 1.0001 * wB
        lam = [(eps + 0j) / Rdom, (-eps + 0j) / Rdom]
        T = mm(S, mm([[lam[0], 0j], [0j, lam[1]]], Si))
        G = mm(dag(S), S)
        P, _ = PQ(G, lam, 0.5)
        sG = eigmax(G)
        s2 = eigmin(madd(smul(2, G), P, 1, -1)) / sG
        s1 = eigmin(madd(P, G, 1, -1)) / sG
        rows.append({"eps": eps, "normT": opnorm(T),
                     "slack_2G_P": s2, "slack_P_G": s1})
    return rows


def main():
    rng = random.Random(20260901)
    out = {}
    # clause (a): mass two, both domains
    inst = make_instance(rng, 4, cond_pow=1.2)
    out["disk_mass_defect"] = disk_mass(inst)
    ell = ellipse_run(seed=7)
    out["ellipse"] = {k: ell[k] for k in
                      ("mass_defect", "density_min", "reH_min",
                       "od_right_max", "od_wrong_min",
                       "big_min_rel", "comp_min_rel", "cancel_rel",
                       "chain_2G_P", "chain_P_G")}
    a = (out["disk_mass_defect"] <= 1e-13
         and ell["mass_defect"] <= 1e-13
         and ell["density_min"] >= -1e-12)
    # clause (b): Caratheodory + membership discrimination (ellipse)
    b = (ell["reH_min"] >= -1e-9 and ell["od_right_max"] <= 1e-9
         and ell["od_wrong_min"] >= 1e-2)
    # clause (c): the Gramian chain, 400 legitimate instances
    worst2, worst1, worstk, maxT = 9e9, 9e9, 9e9, 0.0
    for t in range(400):
        n = rng.choice((2, 3, 4, 5))
        inst2 = make_instance(rng, n,
                              cond_pow=rng.uniform(0.5, 3.0))
        r = core_checks(inst2)
        worst2 = min(worst2, r["min_2G_P"])
        worst1 = min(worst1, r["min_P_G"])
        worstk = min(worstk, r["min_k1"])
        maxT = max(maxT, r["normT"])
    out["hunt"] = {"trials": 400, "worst_2G_P": worst2,
                   "worst_P_G": worst1, "worst_k1": worstk,
                   "maxT": maxT}
    c = (worst2 >= -1e-9 and worst1 >= -1e-9 and worstk >= -1e-9
         and maxT <= 2.0 + 1e-9)
    # clause (d): extremal tightness
    ramp = jordan_ramp()
    out["ramp"] = ramp
    slacks = [r["slack_2G_P"] for r in ramp]
    d = (ramp[-1]["normT"] >= 1.999
         and all(s > 0 for s in slacks)
         and all(slacks[i + 1] < slacks[i]
                 for i in range(len(slacks) - 1))
         and slacks[-1] <= 1e-6)
    # clause (e): the Psi-cancellation
    e = ell["cancel_rel"] <= 1e-9 and ell["big_min_rel"] >= -1e-7
    out["clauses"] = {"a": a, "b": b, "c": c, "d": d, "e": e}
    with open(os.path.join(HERE, "p44_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("clauses:", out["clauses"])
    print("hunt:", out["hunt"])
    print("ramp:", [(r["eps"], round(r["normT"], 5),
                     f"{r['slack_2G_P']:.2e}") for r in ramp])


if __name__ == "__main__":
    main()
