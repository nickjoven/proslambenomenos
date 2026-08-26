#!/usr/bin/env python3
"""P-22 registered computation: seeded Euler-Maruyama runs of the
fundamental (sin theta) and two-photon (sin 2 theta) Adler equations,
scored against the quadrature pins in p22_registration.json under
the clause set of PREDICTIONS.md P-22 as amended by P-22a."""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p22_registration.json").read_text())
DT = REG["dt"]
BANDS = REG["bands"]


def run(theta0, delta, eps, D, T, k, seed):
    """Integrate dtheta = (delta - eps sin(k theta))dt + sqrt(2D)dW;
    return final theta and (for hop analysis) the well index track."""
    rng = random.Random(seed)
    g = rng.gauss
    s = math.sin
    n = int(T / DT)
    amp = math.sqrt(2 * D * DT)
    th = theta0
    for _ in range(n):
        th += (delta - eps * s(k * th)) * DT + (amp * g(0.0, 1.0) if D > 0 else 0.0)
    return th


def run_track(delta, eps, D, T, seed):
    """Two-photon run recording pi-well transitions and time averages
    of cos theta / cos 2 theta."""
    rng = random.Random(seed)
    g = rng.gauss
    s = math.sin
    c = math.cos
    n = int(T / DT)
    amp = math.sqrt(2 * D * DT)
    th = 0.0
    well = 0                      # committed well index (multiple of pi)
    hops = []                     # signed committed well steps
    c1 = c2 = 0.0
    for _ in range(n):
        th += (delta - eps * s(2 * th)) * DT + amp * g(0.0, 1.0)
        w = round(th / math.pi)
        # Schmitt trigger: commit only once inside the new well's core,
        # so barrier-top flicker is not counted as hopping
        if w != well and abs(th - math.pi * w) < math.pi / 4:
            hops.append(w - well)
            well = w
        c1 += c(th)
        c2 += c(2 * th)
    return hops, c1 / n, c2 / n


def main():
    out = {"clauses": {}, "detail": {}}
    seeds = REG["seeds"]

    # (a) deterministic tongue and beat, both scenarios
    eps = REG["det_eps"]
    T = 2000.0
    ok_a = True
    det = {}
    for k in (1, 2):
        for delta in REG["det_deltas"]:
            th_end = run(0.1, delta, eps, 0.0, T, k, seeds["det"])
            v = (th_end - 0.1) / T
            if delta < eps:
                good = abs(th_end - 0.1) < 2 * math.pi
            else:
                tgt = math.sqrt(delta**2 - eps**2)
                good = abs(v - tgt) < BANDS["beat_rel"] * tgt
            det[f"k{k}_d{delta}"] = v
            ok_a = ok_a and good
    out["clauses"]["a_tongue_beat"] = bool(ok_a)
    out["detail"]["det"] = det

    # (b) noisy mobility, amended band, M = 12 ensemble
    M, Tm = 12, REG["T_mob"]
    ok_b = True
    mob = {}
    for (delta, epsv, D) in REG["grid_mobility"]:
        key = f"{delta}_{epsv}_{D}"
        vs = []
        for m in range(M):
            th_end = run(0.0, delta, epsv, D, Tm, 1, seeds["mob"] + 1000 * m + hash(key) % 997)
            vs.append(th_end / Tm)
        v = sum(vs) / M
        sig = math.sqrt(2 * D / (Tm * M))
        pin = REG["v_pin"][key]
        band = max(0.04 * abs(pin), 3 * sig)
        good = abs(v - pin) < band
        mob[key] = {"v": v, "pin": pin, "band": band, "ok": bool(good)}
        ok_b = ok_b and good
    out["clauses"]["b_mobility"] = bool(ok_b)
    out["detail"]["mobility"] = mob

    # (c) locked variance, two-photon, delta = 0
    ok_c = True
    var = {}
    for D in REG["D_ladder_var"]:
        rng = random.Random(seeds["var"] + int(D * 1000))
        g = rng.gauss
        s = math.sin
        n = int(REG["T_var"] / DT)
        amp = math.sqrt(2 * D * DT)
        th = 0.0
        burn = int(50.0 / DT)
        acc = acc2 = 0.0
        cnt = 0
        for i in range(n):
            th += (0.0 - 1.0 * s(2 * th)) * DT + amp * g(0.0, 1.0)
            th -= math.pi * round(th / math.pi)     # fold into the current well
            if i >= burn:
                acc += th
                acc2 += th * th
                cnt += 1
        v_meas = acc2 / cnt - (acc / cnt) ** 2
        pin = REG["var_pin"][str(D)]
        good = abs(v_meas - pin) < BANDS["variance_rel"] * pin
        var[str(D)] = {"var": v_meas, "pin": pin, "ok": bool(good)}
        ok_c = ok_c and good
    out["clauses"]["c_variance"] = bool(ok_c)
    out["detail"]["variance"] = var

    # (d) pi-hops: rate vs MFPT pin, and hop-size purity
    ok_d = True
    hop = {}
    for D in REG["hop_D"]:
        hops, c1, c2 = run_track(0.0, 1.0, D, REG["T_hop"], seeds["hop"] + int(D * 1000))
        n_hops = len(hops)
        rate = n_hops / REG["T_hop"] / 2.0   # per direction convention: pin is 1/(2 MFPT)
        pin = REG["hop_rate_pin"][str(D)]
        band = BANDS["hop_rel"][str(D)] * pin
        pure = sum(1 for h in hops if abs(h) == 1) / max(n_hops, 1)
        good = abs(rate - pin) < band and pure >= BANDS["pi_hop_fraction_min"]
        hop[str(D)] = {"n": n_hops, "rate": rate, "pin": pin, "band": band,
                       "pi_fraction": pure, "ok": bool(good)}
        ok_d = ok_d and good
    out["clauses"]["d_pi_hops"] = bool(ok_d)
    out["detail"]["hops"] = hop

    # (e) the protected observable at (eps, D) = (1, 0.25)
    hops_e, c1, c2 = run_track(0.0, 1.0, 0.25, REG["T_hop"], seeds["hop"] + 77)
    ok_e = abs(c2) > BANDS["cos2_min"] and abs(c1) < BANDS["cos1_max"] and len(hops_e) > 50
    out["clauses"]["e_protected"] = bool(ok_e)
    out["detail"]["protected"] = {"cos1": c1, "cos2": c2, "n_hops": len(hops_e)}

    changes = ((not ok_b) or (not ok_a) or (not ok_e))
    out["changes_my_mind_fired"] = bool(changes)
    (HERE / "p22_results.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["clauses"].items():
        print(f"clause {k}: {'as registered' if v else 'NOT as registered'}")
    print(f"protected observable: <cos2theta> = {c2:.3f}, <cos theta> = {c1:.3f}, "
          f"{len(hops_e)} hops")
    print(f"changes-my-mind fired: {changes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
