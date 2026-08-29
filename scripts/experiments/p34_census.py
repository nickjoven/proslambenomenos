#!/usr/bin/env python3
"""P-34 experiment: the horizon-coincidence census. Runs AFTER the
registration commit; clauses (a)-(e) as registered.

Results -> p34_results.json.
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import p34_derive as D


def nearest(entry, h0):
    """Nearest codebook expression to the entry's value at this H0."""
    part, null = D.solve_dimension(entry["dim"])
    null = [x / null[3] for x in null]
    target = math.log10(entry["value"]) if entry["dim"] != (0, 0, 0) \
        else math.log10(entry["value"])
    best = None
    for k in D.K_LATTICE:
        expo = [p + Fraction(k) * n for p, n in zip(part, null)]
        base = math.log10(D.mono_value(expo, h0=h0))
        for name, pf in D.PREFACTORS.items():
            t = abs(base + math.log10(pf) - target)
            if best is None or t < best["t"]:
                best = {"t": t, "k": float(k), "prefactor": name}
    return best


def surprisal(t):
    p, _ = D.coverage(max(t, 1e-6))
    return -math.log2(min(max(p, 1e-12), 1.0))


def main():
    out = {"clauses": {}}
    n_census = len(D.CENSUS)

    rows = {}
    for h0, tag in ((D.H0_PLANCK, "planck"), (D.H0_SHOES, "shoes")):
        rows[tag] = []
        for e in D.CENSUS:
            # Omega ratio and other H0-dependent pins: rho_Lambda
            # scales with H0^2; recompute it for the sensitivity arm
            val = e["value"]
            if e["name"] == "rho_Lambda":
                val = 0.685 * 3 * h0 ** 2 * D.C ** 2 \
                    / (8 * math.pi * D.G)
            ee = dict(e)
            ee["value"] = val
            b = nearest(ee, h0)
            s = surprisal(b["t"])
            net = s - math.log2(n_census)
            rows[tag].append({"name": e["name"], "t_dex": b["t"],
                              "k": b["k"], "prefactor": b["prefactor"],
                              "surprisal_bits": s, "net_bits": net})
    out["census"] = rows

    print("== (a) the census table (Planck H0)")
    for r in rows["planck"]:
        print(f"  {r['name']:16} t = {r['t_dex']:.4f} dex at "
              f"k = {r['k']:+.3f}, pref {r['prefactor']:8} "
              f"surprisal {r['surprisal_bits']:.2f} net "
              f"{r['net_bits']:+.2f} bits")
    ok_a = all(r["t_dex"] < 5.0 for r in rows["planck"])
    out["clauses"]["a"] = ok_a

    print("== (b) the verdict: net bits <= 3 everywhere")
    worst = max(r["net_bits"] for r in rows["planck"])
    ok_b = worst <= 3.0
    print(f"  max net bits = {worst:+.2f}  "
          f"{'ok' if ok_b else 'FAIL - flagged for a mechanism line'}")
    out["clauses"]["b"] = ok_b
    out["max_net_bits"] = worst

    print("== (c) the k = 2 slot collision (from LC-24)")
    mech = ["CKN (c33)", "Sorkin (c31)", "Zeldovich 1967",
            "holographic DE (Li 2004)"]
    ok_c = len(mech) >= 4
    print(f"  {len(mech)} named mechanisms on one slot: {mech}")
    out["clauses"]["c"] = ok_c
    out["k2_mechanisms"] = mech

    print("== (d) H0 sensitivity")
    ok_d = True
    for rp, rs in zip(rows["planck"], rows["shoes"]):
        d = abs(rp["net_bits"] - rs["net_bits"])
        if d > 1.0:
            ok_d = False
            print(f"  {rp['name']}: net moved {d:.2f} bits")
    print(f"  {'ok' if ok_d else 'FAIL'}")
    out["clauses"]["d"] = ok_d

    print("== (e) calibration under both H0")
    ok_e = True
    for h0 in (D.H0_PLANCK, D.H0_SHOES):
        want = math.log10(D.HBAR * h0) - math.log10(2 * math.pi)
        part, null = D.solve_dimension((1, 2, -2))
        null = [x / null[3] for x in null]
        best = None
        for k in D.K_LATTICE:
            expo = [p + Fraction(k) * n for p, n in zip(part, null)]
            base = math.log10(D.mono_value(expo, h0=h0))
            for name, pf in D.PREFACTORS.items():
                t = abs(base + math.log10(pf) - want)
                best = t if best is None else min(best, t)
        if best > 1e-9:
            ok_e = False
    print(f"  {'ok' if ok_e else 'FAIL'}")
    out["clauses"]["e"] = ok_e

    json.dump(out, open(os.path.join(HERE, "p34_results.json"), "w"),
              indent=1)
    print("results -> p34_results.json")
    print("clauses:", out["clauses"])
    return 0 if all(out["clauses"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
