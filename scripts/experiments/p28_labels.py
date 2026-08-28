#!/usr/bin/env python3
"""P-28 experiment: the gap integers of the golden ladder.

Runs AFTER the registration commit. Spectra by kernels.eig.eigh at
the two P-7 Chambers corners; every open gap assigned its
Diophantine label; clauses (a)-(e) as registered in PREDICTIONS.md
P-28 against pins in p28_registration.json.

Results -> p28_results.json.
"""
import importlib.util
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from kernels.eig import eigh                       # noqa: E402
import p28_derive as D                             # noqa: E402

spec = importlib.util.spec_from_file_location(
    "p7f", os.path.join(HERE, "p7_flux.py"))
p7f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p7f)

FIB = D.FIB
FLOOR = D.FLOOR


def spectrum(p, q):
    """Union of the two Chambers-corner spectra (P-7 convention);
    returns sorted edges."""
    e1 = eigh(p7f.bloch(p, q, +1.0, 0.0))
    e2 = eigh(p7f.bloch(p, q, -1.0, math.pi / q))
    return sorted(list(e1) + list(e2))


def gaps_of(p, q):
    edges = spectrum(p, q)
    bands = [(edges[2 * i], edges[2 * i + 1])
             for i in range(len(edges) // 2)]
    out = []
    for r in range(1, q):
        lo = bands[r - 1][1]
        hi = bands[r][0]
        w = hi - lo
        row = {"r": r, "lo": lo, "hi": hi, "width": w,
               "open": w > FLOOR}
        if 2 * ((r * pow(p, -1, q)) % q) != q:
            s, t, _ = D.label(r, p, q)
            row["s"] = s
            row["t"] = t
        else:
            row["t"] = None  # ambiguous central
        out.append(row)
    return out, edges


def main():
    out = {"clauses": {}, "rungs": {}}
    ladder = [(p, q, n) for p, q, n in D.LADDER if q >= 3]
    allgaps = {}
    for p, q, n in ladder:
        g, edges = gaps_of(p, q)
        allgaps[q] = (p, q, n, g, edges)
        out["rungs"][str(q)] = {
            "p": p, "n": n,
            "open_gaps": sum(1 for x in g if x["open"]),
            "gaps": [{k: x[k] for k in ("r", "width", "t")}
                     for x in g if x["open"] or x["t"] is None]}

    # (a) two widest open gaps at r = F_{n-1}, F_{n-2}, t = +1/-1
    ok_a = True
    for p, q, n in ladder:
        if q < 5:
            continue
        g = [x for x in allgaps[q][3] if x["open"]]
        top2 = sorted(g, key=lambda x: -x["width"])[:2]
        got = {(x["r"], x["t"]) for x in top2}
        want = {(FIB[n - 2], 1), (FIB[n - 3], -1)}
        if got != want:
            ok_a = False
            print(f"  (a) q={q}: widest {sorted(got)} vs "
                  f"want {sorted(want)}")
    print(f"clause (a) principal pair t=+1/-1 at r=F_(n-1),F_(n-2): "
          f"{'ok' if ok_a else 'FAIL'}")
    out["clauses"]["a"] = ok_a

    # (b) hierarchy: median width decreasing over |t| = 1, 2, 3
    ok_b = True
    hier = {}
    for p, q, n in ladder:
        if q < 13:
            continue
        meds = []
        for tier in (1, 2, 3):
            ws = sorted(x["width"] for x in allgaps[q][3]
                        if x["open"] and x["t"] is not None
                        and abs(x["t"]) == tier)
            meds.append(ws[len(ws) // 2] if ws else None)
        hier[str(q)] = meds
        if any(m is None for m in meds) or not (
                meds[0] > meds[1] > meds[2]):
            ok_b = False
            print(f"  (b) q={q}: tier medians {meds}")
    print(f"clause (b) hierarchy over tiers 1>2>3: "
          f"{'ok' if ok_b else 'FAIL'}")
    out["clauses"]["b"] = ok_b
    out["hierarchy_medians"] = hier

    # (c) Fibonacci map on open Fibonacci-position gaps; edge gap
    ok_c = True
    edge_resolved_through = None
    for p, q, n in ladder:
        for j in range(2, n):
            r = FIB[j - 1]
            if r >= q:
                continue
            for rr, sign in ((r, 1), (q - r, -1)):
                x = allgaps[q][3][rr - 1]
                if not x["open"] or x["t"] is None:
                    continue
                if abs(x["t"]) != FIB[n - j - 1]:
                    ok_c = False
                    print(f"  (c) q={q} r={rr}: t={x['t']} vs "
                          f"|t|={FIB[n - j - 1]}")
        e = allgaps[q][3][0]
        if e["open"]:
            edge_resolved_through = q
            if abs(e["t"]) != FIB[n - 3]:
                ok_c = False
                print(f"  (c) q={q} edge gap t={e['t']} vs F_(n-2)="
                      f"{FIB[n - 3]}")
        elif q <= 13:
            ok_c = False
            print(f"  (c) q={q}: edge gap unresolved below floor "
                  f"(required through 13); width {e['width']:.2e}")
    print(f"clause (c) Fibonacci map + edge gap: "
          f"{'ok' if ok_c else 'FAIL'} (edge resolved through "
          f"q={edge_resolved_through})")
    out["clauses"]["c"] = ok_c
    out["edge_resolved_through_q"] = edge_resolved_through

    # (d) Streda by independent band counting across rung pairs
    ok_d = True
    streda = []
    pairs = [(a, b) for a, b in zip(ladder, ladder[1:])
             if a[1] >= 8]
    for (p1, q1, n1), (p2, q2, n2) in pairs:
        for t in (1, -1, 2):
            g1 = [x for x in allgaps[q1][3]
                  if x["open"] and x["t"] == t]
            g2 = [x for x in allgaps[q2][3]
                  if x["open"] and x["t"] == t]
            # match by energy overlap
            found = False
            for x1 in g1:
                for x2 in g2:
                    lo = max(x1["lo"], x2["lo"])
                    hi = min(x1["hi"], x2["hi"])
                    if hi <= lo:
                        continue
                    found = True
                    mid = 0.5 * (lo + hi)
                    edges2 = allgaps[q2][4]
                    cnt = sum(1 for e in edges2 if e < mid)
                    r2 = cnt // 2
                    slope = (Fraction(r2, q2) - Fraction(x1["r"], q1)) \
                        / (Fraction(p2, q2) - Fraction(p1, q1))
                    row = {"pair": f"{p1}/{q1}->{p2}/{q2}", "t": t,
                           "r1": x1["r"], "r2_counted": r2,
                           "slope": [slope.numerator,
                                     slope.denominator]}
                    streda.append(row)
                    if slope != t:
                        ok_d = False
                        print(f"  (d) {row}")
            if not found:
                ok_d = False
                print(f"  (d) {p1}/{q1}->{p2}/{q2} t={t}: no "
                      f"overlapping open gap pair")
    print(f"clause (d) Streda slopes exact from band counting: "
          f"{'ok' if ok_d else 'FAIL'} ({len(streda)} pairs)")
    out["clauses"]["d"] = ok_d
    out["streda"] = streda

    # (e) even-q central closure
    ok_e = True
    centrals = {}
    for q in (8, 34, 144):
        x = allgaps[q][3][q // 2 - 1]
        centrals[str(q)] = x["width"]
        if not abs(x["width"]) < 1e-12:
            ok_e = False
    print(f"clause (e) even-q central closure: "
          f"{'ok' if ok_e else 'FAIL'} {centrals}")
    out["clauses"]["e"] = ok_e
    out["central_widths"] = centrals

    # unscored context: t=+1 gap width along the ladder (P-7 ln-phi)
    w1 = {}
    for p, q, n in ladder:
        if q < 5:
            continue
        x = allgaps[q][3][FIB[n - 2] - 1]
        w1[str(q)] = x["width"]
    out["t1_width_ladder"] = w1

    json.dump(out, open(os.path.join(HERE, "p28_results.json"), "w"),
              indent=1)
    print("results -> p28_results.json")
    print("clauses:", out["clauses"])
    return 0 if all(out["clauses"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
