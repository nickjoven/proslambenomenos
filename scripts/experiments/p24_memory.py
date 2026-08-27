#!/usr/bin/env python3
"""P-24 registered computation: seeded simulations of the three
memory rungs, scored against p24_registration.json."""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p24_registration.json").read_text())
K = REG["K"]


def main():
    out = {"clauses": {}, "detail": {}}

    # ---- (a) rung 1: free phase diffusion ----
    r1 = REG["rung1"]
    D, M = r1["D"], r1["M"]
    dt = REG["dt"]["r1"]
    rng = random.Random(REG["seeds"]["r1"])
    thetas = [0.0] * M
    tgrid = r1["t_grid"]
    amp = math.sqrt(2 * D * dt)
    tcur = 0.0
    ok_a = True
    r1rows = {}
    for tg in tgrid:
        steps = int(round((tg - tcur) / dt))
        for _ in range(steps):
            for i in range(M):
                thetas[i] += amp * rng.gauss(0.0, 1.0)
        tcur = tg
        C = sum(math.cos(x) for x in thetas) / M
        pred = math.exp(-D * tg)
        band = 4 * math.sqrt(max(0.5 * (1 - math.exp(-2 * D * tg)), 1e-9) / M)
        good = abs(C - pred) < band
        r1rows[str(tg)] = {"C": C, "pred": pred, "band": band, "ok": bool(good)}
        ok_a = ok_a and good
    out["clauses"]["a_rung1"] = bool(ok_a)
    out["detail"]["rung1"] = r1rows

    # ---- (b) rung 2: locked bit telegraph ----
    eps = REG["eps2"]
    dt2 = REG["dt"]["r2"]
    T2 = REG["T2"]
    ok_b = True
    r2rows = {}
    rates = {}
    for Dv in REG["D2_ladder"]:
        rng = random.Random(REG["seeds"]["r2"] + int(Dv * 1000))
        g = rng.gauss
        s = math.sin
        n = int(T2 / dt2)
        amp = math.sqrt(2 * Dv * dt2)
        th = 0.0
        well = 0
        hops = 0
        for _ in range(n):
            th += (-eps * s(2 * th)) * dt2 + amp * g(0.0, 1.0)
            w = round(th / math.pi)
            if w != well and abs(th - math.pi * w) < math.pi / 4:
                hops += 1
                well = w
        tau_pin = REG["tau2_pin"][str(Dv)]
        n_pred = T2 / (2 * tau_pin)          # committed hops both directions? one per MFPT*2
        # committed-hop count expectation: total transitions = T2 / (2*T_MFPT) per
        # direction x 2 = T2/T_MFPT? convention fixed by P-22: rate/direction =
        # 1/(2 MFPT); total committed = T2/(2 MFPT) * 2 = T2/MFPT
        n_pred = T2 / tau_pin
        band = 3 * math.sqrt(n_pred)
        good = abs(hops - n_pred) < band
        rates[str(Dv)] = hops / T2
        r2rows[str(Dv)] = {"hops": hops, "pred": n_pred, "band": band, "ok": bool(good)}
        ok_b = ok_b and good
    # Arrhenius: barrier from two-point slope vs CAS barrier eps
    D1, D2v = REG["D2_ladder"]
    slope = (math.log(rates[str(D2v)]) - math.log(rates[str(D1)])) / (1 / D1 - 1 / D2v)
    pin_slope = (math.log(1 / REG["tau2_pin"][str(D2v)]) -
                 math.log(1 / REG["tau2_pin"][str(D1)])) / (1 / D1 - 1 / D2v)
    n1, n2c = r2rows[str(D1)]["hops"], r2rows[str(D2v)]["hops"]
    slope_band = (2 * (1 / math.sqrt(n1) + 1 / math.sqrt(n2c))) / abs(1 / D1 - 1 / D2v)
    good_sl = abs(slope - pin_slope) < slope_band
    r2rows["arrhenius"] = {"slope": slope, "pin_slope": pin_slope,
                           "cas_barrier": eps, "band": slope_band, "ok": bool(good_sl)}
    ok_b = ok_b and good_sl
    out["clauses"]["b_rung2"] = bool(ok_b)
    out["detail"]["rung2"] = r2rows

    # ---- (c) rung 3: winding on rings ----
    dt3 = REG["dt"]["r3"]
    ok_c = True
    r3rows = {}
    meas_rate = {}
    for (Nn, Dv) in REG["cells3"]:
        key = f"{Nn}_{Dv}"
        T3 = REG["T3"][key]
        rng = random.Random(REG["seeds"]["r3"] + Nn * 100 + int(Dv * 1000))
        g = rng.gauss
        amp = math.sqrt(2 * Dv * dt3)
        n_total = int(T3 / dt3)

        def winding(ph):
            tot = 0.0
            for i in range(Nn):
                d = ph[(i + 1) % Nn] - ph[i]
                d = (d + math.pi) % (2 * math.pi) - math.pi
                tot += d
            return round(tot / (2 * math.pi))

        # escape-from-w=1 with reset (P-24a protocol)
        phi = [2 * math.pi * i / Nn for i in range(Nn)]
        events = 0
        sizes_ok = 0
        time_in_run = 0.0
        pending = None                     # first off-w=1 sighting, must persist
        check_every = max(1, int(0.05 / dt3))
        for step in range(n_total):
            grad = [0.0] * Nn
            for i in range(Nn):
                dr = phi[(i + 1) % Nn] - phi[i]
                dl = phi[i] - phi[(i - 1) % Nn]
                grad[i] = K * (math.sin(dr) - math.sin(dl))
            for i in range(Nn):
                phi[i] += grad[i] * dt3 + amp * g(0.0, 1.0)
            time_in_run += dt3
            if step % check_every == 0:
                w = winding(phi)
                if w != 1:
                    if pending == w:       # sustained on two checks: committed
                        events += 1
                        if abs(w - 1) == 1:
                            sizes_ok += 1
                        phi = [2 * math.pi * i / Nn for i in range(Nn)]
                        pending = None
                    else:
                        pending = w
                else:
                    pending = None
        r_meas = events / T3
        meas_rate[key] = r_meas
        pin = REG["rate_pin"][key]
        nat = abs(math.log(max(r_meas, 1e-12)) - math.log(pin))
        band = 2 / math.sqrt(max(events, 1)) + REG["bands"]["abs_nat"]
        purity = sizes_ok / max(events, 1)
        good = nat < band and purity >= REG["bands"]["slip_purity"]
        r3rows[key] = {"events": events, "rate": r_meas, "langer": pin,
                       "nat_dev": nat, "band": band, "purity": purity,
                       "ok": bool(good)}
        ok_c = ok_c and good
    # ratio clauses
    for (a, b) in ((("16_0.16"), ("8_0.16")), (("32_0.3"), ("16_0.3"))):
        dln_meas = math.log(meas_rate[a]) - math.log(meas_rate[b])
        dln_pin = math.log(REG["rate_pin"][a]) - math.log(REG["rate_pin"][b])
        na, nb = r3rows[a]["events"], r3rows[b]["events"]
        band = 2 * (1 / math.sqrt(na) + 1 / math.sqrt(nb)) + REG["bands"]["ratio_nat"]
        good = abs(dln_meas - dln_pin) < band
        r3rows[f"ratio_{a}_over_{b}"] = {"dln_meas": dln_meas, "dln_pin": dln_pin,
                                          "band": band, "ok": bool(good)}
        ok_c = ok_c and good
    out["clauses"]["c_rung3"] = bool(ok_c)
    out["detail"]["rung3"] = r3rows

    # ---- (d) the order clause per P-24a: N = 16 vs N = 8 at D = 0.16 ----
    tau8 = 1.0 / meas_rate["8_0.16"]
    tau16 = 1.0 / meas_rate["16_0.16"]
    derived_ratio = REG["rate_pin"]["8_0.16"] / REG["rate_pin"]["16_0.16"]
    good_d = tau16 > tau8
    out["clauses"]["d_order"] = bool(good_d)
    out["detail"]["order"] = {"tau8": tau8, "tau16": tau16,
                              "measured_ratio": tau16 / tau8,
                              "derived_ratio": derived_ratio,
                              "derived_tau32_over_tau8_D016":
                              REG["crossover_check"]["tau32_over_tau8_D016"],
                              "derived_tau32_over_tau8_D06":
                              REG["crossover_check"]["tau32_over_tau8_D06"]}

    changes = not (ok_a and ok_b and ok_c and good_d)
    out["changes_my_mind_fired"] = bool(changes)
    (HERE / "p24_results.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["clauses"].items():
        print(f"clause {k}: {'as registered' if v else 'NOT as registered'}")
    print(f"changes-my-mind fired: {changes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
