#!/usr/bin/env python3
"""P-49 registered runner: the late-window instrument near and in the
band, the decay of the transient excess, and the smear identity.
Clauses and cells fixed in PREDICTIONS.md P-49 before this ran; the
definitions (the recording, the drive-locked decomposition, the
floors, the describing-function band, the smear identity) imported
from p49_derive.py, whose two passes are pinned in p49_derive.json
and not rerun here.

Cells (twisted sector 0, N = 64, f = fold + 0.005, ramp 200, dt =
0.001, kappa = 1):
  late windows [300, 380] after the event at gamma 0.35 / 0.5
  (above the band) and 0.8 / 1.0 (at and in the band);
  the decay ladder at gamma 0.5: windows [30,80] [80,130] [130,180]
  [180,230] [230,280] [300,350].

Run: python3 scripts/experiments/p49_near_band.py
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import fold_fc  # noqa: E402
from p49_derive import N, cell_readout  # noqa: E402

LATE = (0.35, 0.5, 0.8, 1.0)
DECAY = (30.0, 80.0, 130.0, 180.0, 230.0, 300.0)


def main():
    t0 = time.time()
    fold = fold_fc(N, -math.pi)
    f = fold + 0.005
    dt = 0.001
    out = {"N": N, "fold": fold, "f": f, "dt": dt, "late": {}, "decay": []}
    a_ok = b_ok = d_ok = True
    for g in LATE:
        c = cell_readout(g, f, dt, (300.0, 380.0))
        out["late"]["gamma_%g" % g] = c
        a_ok &= c["ratio21_in_band"]
        if g in (0.35, 0.5):
            b_ok &= c["A1_in_band"]
        d_ok &= c["smear"]["holds"]
        print("late gamma %g: event %.1f Omega %.3f | (a) ratio21 %.4e band [%.4e, %.4e] floor %.1e in %s (%+.2f%%) | (b) A1 %.4e band [%.4e, %.4e] in %s (%+.2f%%)%s | (d) smear %.4f vs %.4f tol %.4f %s | ratio32 %.4e (%.0f s)"
              % (g, c["event_t"], c["Omega"], c["ratio21"], *c["w_band"], c["self_floor_ratio"], c["ratio21_in_band"], 100 * c["ratio21_over_top"],
                 c["A1"], *c["A1_band"], c["A1_in_band"], 100 * c["A1_rel_to_top"], "" if g in (0.35, 0.5) else " [reported]",
                 c["smear"]["measured"], c["smear"]["predicted"], c["smear"]["tolerance"], c["smear"]["holds"], c["ratio32"], time.time() - t0), flush=True)
    excess, x1 = [], []
    for w0 in DECAY:
        c = cell_readout(0.5, f, dt, (w0, w0 + 50.0))
        out["decay"].append(c)
        excess.append(c["ratio21_over_top"])
        x1.append(c["x1_rms"])
        d_ok &= c["smear"]["holds"]
        print("decay [%g, %g]: x1 rms %.3f | excess %+.2f%% (floor %.2f%%) | A1 %+.2f%% | smear %.4f vs %.4f tol %.4f %s"
              % (w0, w0 + 50, c["x1_rms"], 100 * c["ratio21_over_top"], 100 * c["self_floor_ratio"] / max(c["w_band"]), 100 * c["A1_rel_to_top"],
                 c["smear"]["measured"], c["smear"]["predicted"], c["smear"]["tolerance"], c["smear"]["holds"]), flush=True)
    last = out["decay"][-1]
    c_ok = (all(excess[i + 1] <= excess[i] for i in range(len(excess) - 1))
            and all(x1[i + 1] <= x1[i] for i in range(len(x1) - 1))
            and last["ratio21_in_band"])
    out["clauses"] = {"a_holds": a_ok, "b_holds": b_ok, "c_holds": c_ok, "d_holds": d_ok}
    out["seconds_total"] = time.time() - t0
    with open(os.path.join(HERE, "p49_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out["clauses"]), "in %.0f s" % out["seconds_total"])


if __name__ == "__main__":
    main()
