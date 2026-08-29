#!/usr/bin/env python3
"""P-36 registered cells: bond-slip onset and channel on the free
pi ring. Protocol fixed in PREDICTIONS.md P-36 (detector and
channel clause derived in p36_channel.py) before this ran.

Detector: e_j(t) = raw covariant bond strain minus its initial
value; event when max_j |e_j| > 1.5 pi. Channel of the FIRST
event: W is sampled every unit after the event; the first lattice
departure of W classifies it - round(dW) = +-1 is a single
(W-changing) slip, no departure within the 120-unit watch is a
paired (W-neutral) slip; |round(dW)| >= 2 is recorded as "multi"
(fires clause (e), the derivation missed a branch). A later
cascade does not contaminate the first-event classification.
Everything else as P-35: independent runs per grid level, soft
ramp 200, hold 500, Euler-Cromer dt = 0.02, dt/2 validation cell.

Run: python3 scripts/experiments/p36_ring.py [--quick]
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p35_ring import fold_fc, ground_state, winding  # noqa: E402

TAU = 2 * math.pi


def covariant(th, A, j, N):
    return th[(j + 1) % N] - th[j] - A[j]


def run_level(N, twisted, sector, gamma, f_target, dt,
              t_ramp=200.0, t_meas=500.0):
    A, th = ground_state(N, twisted, sector)
    s0 = [covariant(th, A, j, N) for j in range(N)]
    w = [0.0] * N
    b = N // 2
    W0 = winding(th, A, N)
    n_ramp = int(t_ramp / dt)
    n_meas = int(t_meas / dt)
    sample_every = max(1, int(1.0 / dt))
    worst_sector = 0.0
    event_t = None
    dW_first = None
    for s in range(n_ramp + n_meas):
        f = f_target * min(1.0, (s + 1) / n_ramp)
        for j in range(N):
            Dr = th[(j + 1) % N] - th[j] - A[j]
            Dl = th[j] - th[j - 1] - A[j - 1]
            acc = (math.sin(Dr) - math.sin(Dl) - gamma * w[j]
                   + (f if j == b else 0.0))
            w[j] += dt * acc
        for j in range(N):
            th[j] += dt * w[j]
        if (s + 1) % sample_every:
            continue
        t_now = (s + 1) * dt
        if event_t is None:
            W = winding(th, A, N)
            off = (abs(W - (round(W - 0.5) + 0.5)) if twisted
                   else abs(W - round(W)))
            worst_sector = max(worst_sector, off)
            emax = max(abs(covariant(th, A, j, N) - s0[j])
                       for j in range(N))
            if emax > 1.5 * math.pi:
                event_t = t_now
        else:
            if dW_first is None:
                W = winding(th, A, N)
                if abs(W - W0) > 0.6:
                    dW_first = round(W - W0)
            if t_now >= event_t + 120.0:
                break
    result = {"event": event_t is not None, "event_t": event_t,
              "worst_sector_off": worst_sector}
    if event_t is not None:
        e = [covariant(th, A, j, N) - s0[j] for j in range(N)]
        slipped = [(j, round(e[j] / TAU)) for j in range(N)
                   if abs(e[j]) > 1.5 * math.pi]
        if dW_first is None:
            channel = "paired"
        elif abs(dW_first) == 1:
            channel = "single"
        else:
            channel = "multi"
        result.update({"dW_first": dW_first, "channel": channel,
                       "slipped_bonds": slipped[:8],
                       "n_slipped": len(slipped)})
    return result


def onset_scan(N, twisted, sector, gamma, dt=0.02):
    total = ((2 * sector - 1) * math.pi) if twisted else 0.0
    fold = fold_fc(N, total)
    onset, detail = None, None
    lev = 0
    while (fold - 0.10) + 0.005 * lev <= fold + 0.06 + 1e-9:
        f = (fold - 0.10) + 0.005 * lev
        r = run_level(N, twisted, sector, gamma, f, dt)
        if r["event"]:
            onset, detail = f, r
            break
        detail = r
        lev += 1
    return {"fold": fold, "onset": onset, "detail": detail}


def main():
    quick = "--quick" in sys.argv
    dt = 0.02
    Ns = [64] if quick else [64, 96, 128]
    cells = []
    for N in Ns:
        for tag, tw, sec in (("control", False, 0),
                             ("twist0", True, 0), ("twist1", True, 1)):
            cells.append((tag, N, tw, sec, 0.02))
    if not quick:
        for g in (0.01, 0.04):
            for tag, tw, sec in (("control", False, 0),
                                 ("twist0", True, 0),
                                 ("twist1", True, 1)):
                cells.append((tag, 64, tw, sec, g))
    out = {"cells": {}}
    for tag, N, tw, sec, g in cells:
        key = "%s_N%d_g%g" % (tag, N, g)
        r = onset_scan(N, tw, sec, g, dt)
        out["cells"][key] = r
        d = r["detail"]
        print(key, "fold %.4f onset %s" % (r["fold"], r["onset"]),
              "channel %s dW_first %s n_slipped %s sector_off %.1e"
              % (d.get("channel"), d.get("dW_first"),
                 d.get("n_slipped"), d["worst_sector_off"]), flush=True)
    v = onset_scan(64, False, 0, 0.02, dt / 2)
    out["validation_dt_half"] = {"onset": v["onset"], "fold": v["fold"],
                                 "channel": v["detail"].get("channel")}
    print("validation dt/2: onset", v["onset"],
          "channel", v["detail"].get("channel"))

    ev = {}
    for N in Ns:
        cc = out["cells"]["control_N%d_g0.02" % N]
        c0 = out["cells"]["twist0_N%d_g0.02" % N]
        c1 = out["cells"]["twist1_N%d_g0.02" % N]
        if None in (cc["onset"], c0["onset"], c1["onset"]):
            ev[str(N)] = {"incomplete": True}
            continue
        split = abs(c1["onset"] - c0["onset"])
        fr = c1["fold"] / cc["fold"]
        band = 2 * 0.005 / cc["fold"] + split / cc["fold"] + 1e-4
        ratio = 0.5 * (c0["onset"] + c1["onset"]) / cc["onset"]
        ev[str(N)] = {
            "ratio": ratio, "fold_ratio": fr, "band": band,
            "b_holds": abs(ratio - fr) <= band,
            "split": split, "c_holds": split <= 0.005 + 1e-9,
            "e_holds": (cc["detail"].get("channel") == "paired"
                        and c0["detail"].get("channel") == "single"
                        and c1["detail"].get("channel") == "single")}
    if not quick:
        gv = {}
        for g in (0.01, 0.04):
            cc = out["cells"]["control_N64_g%g" % g]
            c0 = out["cells"]["twist0_N64_g%g" % g]
            c1 = out["cells"]["twist1_N64_g%g" % g]
            if None in (cc["onset"], c0["onset"], c1["onset"]):
                gv[str(g)] = {"incomplete": True}
                continue
            split = abs(c1["onset"] - c0["onset"])
            fr = c1["fold"] / cc["fold"]
            band = 2 * 0.005 / cc["fold"] + split / cc["fold"] + 1e-4
            ratio = 0.5 * (c0["onset"] + c1["onset"]) / cc["onset"]
            gv[str(g)] = {"ratio": ratio, "fold_ratio": fr,
                          "band": band,
                          "d_holds": abs(ratio - fr) <= band}
        ev["gamma_variants"] = gv
    out["clauses"] = ev
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "p36_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(ev, indent=1))


if __name__ == "__main__":
    main()
