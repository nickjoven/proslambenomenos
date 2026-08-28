#!/usr/bin/env python3
"""P-29 experiment: the Farey bridge. Runs AFTER the registration
commit. Tongue widths (tangency bisection) and Harper bandwidths
(two-corner eigh) for every mediant and competitor of every
registered interval; clauses (a)-(e) as registered.

Results -> p29_results.json.
"""
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import p29_derive as D

K = D.K_MAIN


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for k, i in enumerate(order):
            r[i] = k
        return r
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return num / (dx * dy)


def main():
    reg = json.load(open(os.path.join(HERE, "p29_registration.json")))
    intervals = reg["EQ1"]["intervals"]
    out = {"clauses": {}, "intervals": []}

    cacheT, cacheS = {}, {}

    def width(p, q):
        if (p, q) not in cacheT:
            cacheT[(p, q)] = D.tongue_width(p, q, K)
        return cacheT[(p, q)]

    def bw(p, q):
        if (p, q) not in cacheS:
            cacheS[(p, q)] = D.bandwidth_S(p, q)
        return cacheS[(p, q)]

    ok_a = ok_b = ok_e = True
    spears = []
    for iv in intervals:
        mp, mq = iv["mediant"]
        rows = [{"frac": f"{mp}/{mq}", "q": mq, "is_mediant": True,
                 "delta": width(mp, mq), "S": bw(mp, mq)}]
        for cp, cq in iv["competitors"]:
            rows.append({"frac": f"{cp}/{cq}", "q": cq,
                         "is_mediant": False,
                         "delta": width(cp, cq), "S": bw(cp, cq)})
        med = rows[0]
        for r in rows[1:]:
            if r["delta"] >= med["delta"]:
                ok_a = False
                print(f"  (a) [{iv['a']}/{iv['b']},{iv['c']}/"
                      f"{iv['d']}]: {r['frac']} tongue "
                      f"{r['delta']:.3e} >= mediant {med['delta']:.3e}")
            if r["S"] >= med["S"]:
                ok_b = False
                print(f"  (b) [{iv['a']}/{iv['b']},{iv['c']}/"
                      f"{iv['d']}]: {r['frac']} S {r['S']:.4f} >= "
                      f"mediant {med['S']:.4f}")
        for r in rows:
            if r["delta"] <= reg["floor"] or r["S"] <= 1e-6:
                ok_e = False
                print(f"  (e) floor: {r}")
        rho = None
        if len(rows) >= 5:
            rho = spearman([r["delta"] for r in rows],
                           [r["S"] for r in rows])
            spears.append(rho)
        out["intervals"].append(
            {"interval": f"{iv['a']}/{iv['b']}..{iv['c']}/{iv['d']}",
             "rows": rows, "spearman": rho})
        lab = f"[{iv['a']}/{iv['b']}, {iv['c']}/{iv['d']}]"
        print(f"{lab:16} mediant {med['frac']:6} "
              f"D {med['delta']:.3e} S {med['S']:.4f} "
              f"competitors {len(rows) - 1}"
              f"{'  spearman %.3f' % rho if rho is not None else ''}")

    print(f"clause (a) mediant widest tongue everywhere: "
          f"{'ok' if ok_a else 'FAIL'}")
    print(f"clause (b) mediant largest bandwidth everywhere: "
          f"{'ok' if ok_b else 'FAIL'}")
    ok_c = all(r >= 0.5 for r in spears)
    print(f"clause (c) Spearman >= 0.5 in all {len(spears)} "
          f"eligible intervals (min {min(spears):.3f}): "
          f"{'ok' if ok_c else 'FAIL'}")
    out["clauses"].update({"a": ok_a, "b": ok_b, "c": ok_c})
    out["spearman_min"] = min(spears)

    # (d) the control: second-harmonic forcing in [1/3, 1/2]
    d25 = D.tongue_width(2, 5, K, harmonic=2, span=0.08)
    d38 = D.tongue_width(3, 8, K, harmonic=2, span=0.05)
    s25, s38 = bw(2, 5), bw(3, 8)
    ok_d = (d38 > d25) and (s25 > s38)
    print(f"clause (d) control: Delta_2(3/8) {d38:.3e} > "
          f"Delta_2(2/5) {d25:.3e} (derived inversion) while "
          f"S(2/5) {s25:.4f} > S(3/8) {s38:.4f}: "
          f"{'ok' if ok_d else 'FAIL'}")
    out["clauses"]["d"] = ok_d
    out["control"] = {"delta2_38": d38, "delta2_25": d25,
                      "S_25": s25, "S_38": s38}

    print(f"clause (e) floors: {'ok' if ok_e else 'FAIL'}")
    out["clauses"]["e"] = ok_e

    # unscored context: pooled log-log width relation
    pts = sorted({(r["frac"], r["delta"], r["S"])
                  for ivv in out["intervals"] for r in ivv["rows"]})
    out["pooled"] = [{"frac": f, "delta": dl, "S": s}
                     for f, dl, s in pts]

    json.dump(out, open(os.path.join(HERE, "p29_results.json"), "w"),
              indent=1)
    print("results -> p29_results.json")
    print("clauses:", out["clauses"])
    return 0 if all(out["clauses"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
