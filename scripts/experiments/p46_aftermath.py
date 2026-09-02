#!/usr/bin/env python3
"""P-46 registered runner: the slip aftermath in the derived current.
Clauses and cells fixed in PREDICTIONS.md P-46 before this ran;
definitions (the momentum bookkeeping, the lock-in, the cycle-
windowed torque, the evanescent closed forms) imported from
p46_derive.py; the pinned torque coefficient read from
p46_derive.json (the N = 32 validation cells, never rerun here).

Cells (twist0, N = 64, f = fold + 0.005, soft ramp 200, dt = 0.001,
run to the P-36 event plus the aftermath):
  gamma 0.02  aftermath 400, lock-in window [300, 400], offset 1;
              wavebench frames of the site-energy excess, the
              current and the velocity for Delta in [0, 120]
  gamma 0.04  aftermath 400, window [300, 400], offsets 1 and 2,
              cycle torque read unregistered
  gamma 0.1   aftermath 200, window [100, 200], offsets 1 and 2,
              cycle torque read unregistered

Run: python3 scripts/experiments/p46_aftermath.py [--quick]
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import fold_fc  # noqa: E402
from p46_derive import evanescent, integrate_aftermath  # noqa: E402
from wavebench import wave_page  # noqa: E402

CELLS = [
    {"gamma": 0.02, "after": 400.0, "windows": [(300.0, 400.0)],
     "offsets_registered": (1,), "torque": False, "record": True},
    {"gamma": 0.04, "after": 400.0, "windows": [(300.0, 400.0)],
     "offsets_registered": (1, 2), "torque": True, "record": False},
    {"gamma": 0.1, "after": 200.0, "windows": [(100.0, 200.0)],
     "offsets_registered": (1, 2), "torque": True, "record": False},
]


def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    N = 64
    fold = fold_fc(N, -math.pi)
    f = fold + 0.005
    dt = 0.01 if quick else 0.001
    pins = json.load(open(os.path.join(HERE, "p46_derive.json")))
    Kpins = {}
    for g, r in pins["validation_N32"].items():
        for w in r["windows"]:
            cy = w.get("cycle", {})
            if cy.get("turns", 0) > 0 and "K" in cy and w["window"][0] >= 100.0 \
                    and (g != "0.04" or w["window"][0] >= 300.0):
                Kpins[g] = {"K": cy["K"], "K_floor": cy["K_floor"]}
    out = {"N": N, "f": f, "fold": fold, "dt": dt, "K_pins": Kpins, "cells": {}}
    verdict = {"a": True, "b2": True, "c": True}
    for cell in CELLS:
        g = cell["gamma"]
        t1 = time.time()
        rec = ({"from": 0.0, "to": 120.0, "dtf": 0.5} if cell["record"] else None)
        r = integrate_aftermath(N, True, 0, g, f, dt, windows=cell["windows"],
                                after_event=cell["after"], offsets=(1, 2, 3),
                                record=rec)
        key = "gamma_%g" % g
        res = {"gamma": g, "event_t": r["event_t"], "seconds": time.time() - t1,
               "worst_recursion_ratio": r["worst_recursion_ratio"],
               "worst_ring_identity_ratio": r["worst_ring_identity_ratio"],
               "E_b_split": r["E_b_split"]}
        # (a)
        a_ok = (r["worst_recursion_ratio"] <= 1.0
                and r["worst_ring_identity_ratio"] <= 1.0)
        res["a_holds"] = a_ok
        verdict["a"] &= a_ok
        # (b2) drift transfer
        sm = {int(round(d)): (P, Pr, vb) for d, P, Pr, vb in r["samples"]
              if abs(d - round(d)) < 1e-9}
        Pr10, Om10 = sm[10][1], sm[10][2]
        checks = {}
        b2_ok = True
        late = {0.02: 300, 0.04: 300, 0.1: 200}[g]
        for D in (int(round(1 / g)), int(round(2 / g)), int(round(3 / g)), late):
            if D in sm:
                pred = Pr10 * math.exp(-g * (D - 10))
                dev = sm[D][1] - pred
                bound = 4.0 / Om10
                checks[str(D)] = {"P_ring": sm[D][1], "pred": pred, "dev": dev,
                                  "bound": bound, "holds": abs(dev) <= bound,
                                  "P": sm[D][0], "v_b": sm[D][2]}
                b2_ok &= abs(dev) <= bound
        res["drift"] = {"P_ring_event": sm[0][1], "P_ring_10": Pr10,
                        "omega_10": Om10, "drift_pre": f / (N * g),
                        "one_percent_of_event_share": 0.01 * sm[0][1],
                        "checks": checks, "b2_holds": b2_ok}
        verdict["b2"] &= b2_ok
        # rotor spin-up readout (unregistered): v_b vs P - P_ring pred
        res["spin_up"] = {str(D): {"v_b_sample": sm[D][2],
                                   "terminal_f_over_gamma": f / g,
                                   "fraction": sm[D][2] / (f / g)}
                          for D in (40, 100, 200) if D in sm}
        # (c) evanescence, (b1) torque
        wins = []
        for w in r["windows"]:
            if w.get("empty"):
                continue
            om_lo = min(w["cycle"].get("omega_start", w["omega_bar"]),
                        w["cycle"].get("omega_end", w["omega_bar"]))
            om_hi = max(w["cycle"].get("omega_start", w["omega_bar"]),
                        w["cycle"].get("omega_end", w["omega_bar"]))
            A1s, ws = [], []
            for om in (om_lo, w["omega_bar"], om_hi):
                for c in (w["cmin"], w["cmax"]):
                    wv, A1 = evanescent(om, c, g, dt)
                    A1s.append(A1)
                    ws.append(abs(wv))
            A = w["A"]
            floor = w["lockin_floor"]
            f1 = floor + w["self_floor"]["1"]
            f2 = floor + w["self_floor"]["2"]
            c1 = {"A1": A["1"], "band": [min(A1s), max(A1s)], "floor": f1,
                  "holds": min(A1s) - f1 <= A["1"] <= max(A1s) + f1}
            wr = {"window": w["window"], "omega_bar": w["omega_bar"],
                  "omega_range": [om_lo, om_hi], "c_range": [w["cmin"], w["cmax"]],
                  "wave_amp": w["wave_amp"], "lockin_floor": floor,
                  "self_floor": w["self_floor"],
                  "A": A, "offset1": c1}
            c_ok = c1["holds"]
            if 2 in cell["offsets_registered"]:
                pred2 = [A["1"] * x for x in ws]
                c2 = {"A2": A["2"], "band": [min(pred2), max(pred2)], "floor": f2,
                      "ratio21": A["2"] / A["1"], "w_abs_band": [min(ws), max(ws)],
                      "holds": min(pred2) - f2 <= A["2"] <= max(pred2) + f2}
                wr["offset2"] = c2
                c_ok &= c2["holds"]
            wr["offset3_unregistered"] = {"A3": A["3"], "pred": A["1"] * (sum(ws) / len(ws)) ** 2,
                                          "floor_over_pred": floor / (A["1"] * (sum(ws) / len(ws)) ** 2)}
            wr["c_holds"] = c_ok
            verdict["c"] &= c_ok
            if cell["torque"]:
                cy = w["cycle"]
                om = 0.5 * (cy["omega_start"] + cy["omega_end"])
                K = cy["mean"] * om ** 3 / g
                Kfl = (cy["chirp_floor"] + cy["step_floor"]) * om ** 3 / g
                # UNREGISTERED reading: the derive layer could not pin
                # a coefficient (K = -0.92 at gamma 0.1 vs +1.9 at 0.04,
                # both above their floors), so the DC torque is reported
                # against the 1-percent-held-drift scale only
                t1c = {"turns": cy["turns"], "mean": cy["mean"], "K": K,
                       "K_floor": Kfl, "pins": Kpins,
                       "held_drift_torque_1pct": 0.01 * g * sm[0][1],
                       "measured_over_1pct": abs(cy["mean"]) / (0.01 * g * sm[0][1])}
                wr["torque_unregistered"] = t1c
            wins.append(wr)
        res["windows"] = wins
        out["cells"][key] = res
        print(key, "event %.1f" % r["event_t"], "a", a_ok, "b2", b2_ok,
              "devs", {k: "%.1e" % v["dev"] for k, v in checks.items()},
              "spin-up", {k: "%.3f" % v["fraction"] for k, v in res["spin_up"].items()},
              "(%.0f s)" % res["seconds"], flush=True)
        for wr in wins:
            print("   window", wr["window"], "Omega %.2f" % wr["omega_bar"],
                  "A1 %.4e band [%.4e, %.4e] floor %.1e holds %s"
                  % (wr["A"]["1"], wr["offset1"]["band"][0], wr["offset1"]["band"][1],
                     wr["lockin_floor"], wr["offset1"]["holds"]))
            if "offset2" in wr:
                print("      A2 %.3e band [%.3e, %.3e] holds %s; A3 %.2e (floor/pred %.1f)"
                      % (wr["A"]["2"], wr["offset2"]["band"][0], wr["offset2"]["band"][1],
                         wr["offset2"]["holds"], wr["A"]["3"],
                         wr["offset3_unregistered"]["floor_over_pred"]))
            if "torque_unregistered" in wr:
                tq = wr["torque_unregistered"]
                print("      torque (unregistered): %d turns mean %.3e K %.3f +- %.3f; "
                      "|T|/1pct-drift-torque %.1e"
                      % (tq["turns"], tq["mean"], tq["K"], tq["K_floor"],
                         tq["measured_over_1pct"]))
        print("   E_b split", json.dumps({k: {a: round(b, 1) for a, b in d.items()}
                                          for k, d in r["E_b_split"].items()}))
        if cell["record"]:
            fr = r["frames"]
            html = wave_page(
                title="One Slip, By the Current",
                subtitle=("The P-36 twisted ring (N = 64, sector +½) one grid level "
                          "above its fold, γ = 0.02: the aftermath of the top-bond slip "
                          "read in the P-45 site energy and bond current. Three fields, "
                          "Δ = 0 at the P-36 event: site-energy excess hⱼ − hⱼ(pre), "
                          "bond current Jⱼ = −½ sin(Dⱼ)(vⱼ + vⱼ₊₁), "
                          "and velocity vⱼ. The loaded site is the rotor at the centre; "
                          "what the ring keeps is the released strain wave and the loss "
                          "of its rigid drift. Recomputed from the registered equations "
                          "(P-46); the page is a recording, not a claim."),
                series=[{"name": "site-energy excess hⱼ − hⱼ(pre), clipped",
                         "frames": [[max(-3.0, min(3.0, x)) for x in fr_] for fr_ in fr["h"]],
                         "color": "#d2a24c"},
                        {"name": "bond current Jⱼ, clipped",
                         "frames": [[max(-3.0, min(3.0, x)) for x in fr_] for fr_ in fr["J"]],
                         "color": "#4c8fd2"},
                        {"name": "velocity vⱼ, clipped",
                         "frames": [[max(-3.0, min(3.0, x)) for x in fr_] for fr_ in fr["v"]],
                         "color": "#7a5cc4"}],
                t0=0.0, dtf=0.5, vmin=-3.0, vmax=3.0,
                events=[{"t": 0.0, "label": "slip"},
                        {"t": 1.0 / g, "label": "1/γ"},
                        {"t": N / 2.0, "label": "N/2"}],
                note=("Values are clipped to ±3 for display: the rotor site's excess "
                      "reaches ~1500 and its bonds' currents ~50; the ring's fields sit "
                      "within ±1. Engine: scripts/experiments/wavebench.py. "
                      "Data: scripts/experiments/p46_results.json."))
            with open(os.path.join(HERE, "p46_waves.html"), "w") as fh:
                fh.write(html)
            res["frames_recorded"] = len(fr["h"])
    out["clauses"] = {"a_holds": verdict["a"], "b_holds": verdict["b2"],
                      "c_holds": verdict["c"]}
    out["seconds_total"] = time.time() - t0
    name = "p46_results%s.json" % ("_quick" if quick else "")
    with open(os.path.join(HERE, name), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out["clauses"]), "in %.0f s" % out["seconds_total"])


if __name__ == "__main__":
    main()
