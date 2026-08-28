#!/usr/bin/env python3
"""P-31 experiment: the second bridge. Runs AFTER the registration
commit. Exact orbits at the landmark ladders, denominator
certificates at the registered rationals; clauses (a)-(e).

Results -> p31_results.json.
"""
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import p31_derive as D

CAP = 20000
DEN_CAP = 10 ** 6


def rational_orbit(t, cap=CAP, den_cap=DEN_CAP):
    """Exact multivalued BFS at rational t; returns
    ('closed', size) or ('diverges', max_denominator_seen)."""
    beta = 1 / t
    one = Fraction(1)
    seen = {1 - t, t}
    frontier = [1 - t, t]
    max_den = max(x.denominator for x in frontier)
    while frontier:
        if len(seen) > cap or max_den > den_cap:
            return "diverges", max_den
        nxt = []
        for x in frontier:
            kids = []
            if 0 <= x <= t:
                kids.append(beta * x)
            if 1 - t <= x <= one:
                kids.append(beta * x + 1 - beta)
            for k in kids:
                if k not in seen:
                    seen.add(k)
                    nxt.append(k)
                    if k.denominator > max_den:
                        max_den = k.denominator
        frontier = nxt
    return "closed", len(seen)


def main():
    out = {"clauses": {}}

    print("== (a) multinacci rungs")
    sizes = {}
    ok_a = True
    for n in range(2, 6):
        F = D.Field(D.multinacci_poly(n), 1, 2)
        closed, size = D.boundary_orbit(F, cap=CAP)
        sizes[f"t{n}"] = {"closed": closed, "size": size}
        print(f"  t_{n}: closed={closed} size={size}")
        if not closed:
            ok_a = False
    if sizes["t2"]["size"] != 4:
        ok_a = False
        print("  (a) golden size != 4")
    print(f"clause (a): {'ok' if ok_a else 'FAIL'}")
    out["multinacci"] = sizes
    out["clauses"]["a"] = ok_a

    print("== (b) doubling rungs")
    ok_b = True
    for n in (2, 3):
        F = D.Field(D.doubling_poly(n), Fraction(3, 2), 2)
        closed, size = D.boundary_orbit(F, cap=CAP)
        sizes[f"s{n}"] = {"closed": closed, "size": size}
        print(f"  s_{n}: closed={closed} size={size}")
        if not closed:
            ok_b = False
    print(f"clause (b): {'ok' if ok_b else 'FAIL'}")
    out["doubling"] = {k: sizes[k] for k in ("s2", "s3")}
    out["clauses"]["b"] = ok_b

    print("== (c) rational certificates")
    ok_c = True
    rats = {}
    for p, q in ((3, 5), (5, 9), (4, 7), (8, 13), (13, 21)):
        verdict, stat = rational_orbit(Fraction(p, q))
        rats[f"{p}/{q}"] = {"verdict": verdict, "stat": stat}
        print(f"  t = {p}/{q}: {verdict} (den/size {stat})")
        if verdict != "diverges":
            ok_c = False
    print(f"clause (c): {'ok' if ok_c else 'FAIL'}")
    out["rationals"] = rats
    out["clauses"]["c"] = ok_c

    print("== (d) the skeleton distinction")
    reg = json.load(open(os.path.join(HERE, "p31_registration.json")))
    gap = reg["EQ5"]["gap"]
    ok_d = (sizes["s2"]["closed"]
            and rats["4/7"]["verdict"] == "diverges"
            and 1e-3 < gap < 2e-3)
    print(f"  structure at s_2 (closed, size {sizes['s2']['size']}); "
          f"certified nothing at 4/7, {gap:.4e} away: "
          f"{'ok' if ok_d else 'FAIL'}")
    out["clauses"]["d"] = ok_d

    print("== (e) full table, no timeouts as evidence")
    ok_e = all(v["closed"] for v in sizes.values()) and \
        all(r["stat"] > DEN_CAP for r in rats.values())
    print(f"  closures exact, divergences certified by denominator "
          f"> 1e6: {'ok' if ok_e else 'FAIL'}")
    out["clauses"]["e"] = ok_e

    json.dump(out, open(os.path.join(HERE, "p31_results.json"), "w"),
              indent=1)
    print("results -> p31_results.json")
    print("clauses:", out["clauses"])
    return 0 if all(out["clauses"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
