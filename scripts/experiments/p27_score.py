#!/usr/bin/env python3
"""P-27 experiment: the classical-gravity squeeze window table.

Runs AFTER the registration commit. For each kernel class and each
inclusion rule, the surviving window log10(upper/lower) with every
bound traced to a pinned row and rule. Also the sign-stability
check of the changes-my-mind clause: no verdict may flip when a
printed OSSW bound is replaced by its recomputed value.

Results -> p27_results.json.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import p27_derive as D

FOM_CAV = D.FOM_CAV


def window_table():
    reg = json.load(open(os.path.join(HERE, "p27_registration.json")))
    tab = D.load_table()
    rows = {r["ref"].split()[0].strip("’"): r for r in tab["rows"]}
    gisler = [r for r in tab["rows"] if r["ref"].startswith("Gisler")][0]
    asen = [r for r in tab["rows"] if r["ref"].startswith("Asenbaum")][0]
    armano = [r for r in tab["rows"] if r["ref"].startswith("Armano")][0]

    printed = D.PRINTED
    rec = reg["EQ2"]["recomputed"]

    def upper(cls, fom, base="printed"):
        src = printed if base == "printed" else rec
        return src[f"{cls}_upper"] * fom / FOM_CAV

    def windows(base):
        src = printed if base == "printed" else rec
        out = []
        for cls in ("cont", "disc", "nonloc"):
            lowers = {"ossw": src[f"{cls}_lower"]}
            if cls == "nonloc":
                lowers["janse_e35"] = 1e-35
                lowers["fein"] = reg["EQ4"]["fein_nonloc_lower"]
            if cls == "disc":
                lowers["fein"] = reg["EQ4"]["fein_disc_lower"]
            for rule, fom, note in (
                    ("ossw-2022 (Cavendish)", FOM_CAV, "absolute"),
                    ("direct-on-Earth best (Gisler)", gisler["FOM"],
                     "absolute"),
                    ("+ LISA Pathfinder (Armano)", armano["FOM"],
                     "QUESTIONED differential"),
                    ("+ atom interferometry (Asenbaum)", asen["FOM"],
                     "QUESTIONED differential/relative")):
                up = upper(cls, fom, base)
                for lname, lo in lowers.items():
                    w = math.log10(up / lo)
                    out.append({"class": cls, "rule": rule,
                                "note": note, "lower_convention": lname,
                                "upper": up, "lower": lo,
                                "window_orders": w,
                                "verdict": "excluded" if w < 0
                                else "survives"})
        return out

    return windows("printed"), windows("recomputed"), reg


def main():
    wp, wr, reg = window_table()
    out = {"clauses": {}, "windows_printed": wp,
           "windows_recomputed": wr,
           "closure": reg["EQ5"]}

    print("== window table (printed OSSW bounds, FOM-rescaled) ==")
    print(f"{'class':7} {'rule':34} {'lower':10} "
          f"{'window':>8} verdict")
    for w in wp:
        print(f"{w['class']:7} {w['rule']:34} "
              f"{w['lower_convention']:10} "
              f"{w['window_orders']:+8.1f} {w['verdict']}"
              f"{'  [' + w['note'] + ']' if 'QUEST' in w['note'] else ''}")

    def pick(ws, cls, rule_start, lower="ossw"):
        return [w for w in ws if w["class"] == cls
                and w["rule"].startswith(rule_start)
                and w["lower_convention"] == lower][0]

    # clause (b): continuous negative everywhere
    ok_b = all(w["window_orders"] < 0 for w in wp
               if w["class"] == "cont")
    print(f"clause (b) continuous excluded under every rule: "
          f"{'ok' if ok_b else 'FAIL'}")
    out["clauses"]["b"] = ok_b

    # clause (c): discrete ~9-10 orders at Gisler; negative at Asenbaum
    d_g = pick(wp, "disc", "direct")["window_orders"]
    d_a = pick(wp, "disc", "+ atom")["window_orders"]
    ok_c = (8.5 <= d_g <= 10.5) and d_a < 0
    print(f"clause (c) discrete: Gisler {d_g:+.2f} (band [8.5, "
          f"10.5]), Asenbaum {d_a:+.2f} (< 0): "
          f"{'ok' if ok_c else 'FAIL'}")
    out["clauses"]["c"] = ok_c

    # clause (d): nonlocal positive under every rule; Janse-convention
    # Asenbaum gap within 1.5 orders of their stated "one order"
    nl_all_pos = all(w["window_orders"] > 0 for w in wp
                     if w["class"] == "nonloc")
    nl_a_janse = pick(wp, "nonloc", "+ atom", "janse_e35")[
        "window_orders"]
    ok_d = nl_all_pos and abs(nl_a_janse - 1.0) <= 1.5
    print(f"clause (d) nonlocal all positive: {nl_all_pos}; "
          f"Asenbaum gap (Janse convention) {nl_a_janse:+.2f} vs "
          f"their 'one order': {'ok' if ok_d else 'FAIL'}")
    out["clauses"]["d"] = ok_d

    # clause (e): closure FOMs as pinned
    cl = reg["EQ5"]
    ok_e = (abs(math.log10(cl["disc_close"] / 1e-10)) < 0.1
            and abs(math.log10(cl["nonloc_close_ossw"] / 1e-17)) < 0.1
            and abs(math.log10(cl["nonloc_close_janse"] / 1e-12)) < 0.1)
    print(f"clause (e) closure FOMs stand: {'ok' if ok_e else 'FAIL'}")
    out["clauses"]["e"] = ok_e

    # changes-my-mind: sign stability printed vs recomputed
    flips = []
    for a, b in zip(wp, wr):
        if (a["window_orders"] < 0) != (b["window_orders"] < 0):
            flips.append((a["class"], a["rule"], a["lower_convention"],
                          a["window_orders"], b["window_orders"]))
    ok_sign = len(flips) == 0
    print(f"sign stability printed vs recomputed: "
          f"{'ok - no verdict flips' if ok_sign else 'FAIL: ' + repr(flips)}")
    out["clauses"]["sign_stability"] = ok_sign
    out["flips"] = flips

    # clause (a) is the derive layer itself
    rc = D.main()
    out["clauses"]["a"] = (rc == 0)

    json.dump(out, open(os.path.join(HERE, "p27_results.json"), "w"),
              indent=1)
    print("results -> p27_results.json")
    print("clauses:", out["clauses"])
    return 0 if all(out["clauses"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
