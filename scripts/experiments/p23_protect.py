#!/usr/bin/env python3
"""P-23 registered computation: fresh-seeded ensembles of the
two-photon locked phase at delta = 0, scored against the derived
Bessel-ratio pins in p23_registration.json."""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = json.loads((HERE / "p23_registration.json").read_text())
DT = REG["dt"]


def member(epsv, D, T, seed):
    rng = random.Random(seed)
    g = rng.gauss
    s = math.sin
    c = math.cos
    n = int(T / DT)
    amp = math.sqrt(2 * D * DT)
    th = 0.0
    well = 0
    hops = 0
    c1 = c2 = 0.0
    for _ in range(n):
        th += (-epsv * s(2 * th)) * DT + amp * g(0.0, 1.0)
        w = round(th / math.pi)
        if w != well and abs(th - math.pi * w) < math.pi / 4:
            hops += 1
            well = w
        c1 += c(th)
        c2 += c(2 * th)
    return c1 / n, c2 / n, hops


def main():
    out = {"clauses": {}, "detail": {}}
    M = REG["M"]
    all_ok = True
    for (epsv, D, T) in REG["cells"]:
        key = str(D)
        pin = REG["cos2_pin"][key]
        c1s, c2s, hoplist = [], [], []
        for m in range(M):
            c1, c2, hops = member(epsv, D, T, REG["seed0"] + 100 * m + int(D * 1e4))
            c1s.append(c1)
            c2s.append(c2)
            hoplist.append(hops)
        mean2 = sum(c2s) / M
        sem2 = math.sqrt(sum((x - mean2) ** 2 for x in c2s) / (M - 1) / M)
        mean1 = sum(c1s) / M
        sem1 = math.sqrt(sum((x - mean1) ** 2 for x in c1s) / (M - 1) / M)
        ok = (abs(mean2 - pin) < 4 * sem2 and sem2 < 0.01
              and abs(mean1) < 4 * sem1
              and min(hoplist) >= REG["hop_min_per_member"])
        out["detail"][key] = {"mean_cos2": mean2, "sem2": sem2, "pin": pin,
                              "mean_cos1": mean1, "sem1": sem1,
                              "hops": hoplist, "ok": bool(ok)}
        all_ok = all_ok and ok
        print(f"D={key}: <cos2> = {mean2:.5f} +/- {sem2:.5f} vs pin {pin:.5f} "
              f"({abs(mean2 - pin) / sem2:.2f} SEM); <cos1> = {mean1:+.5f} "
              f"+/- {sem1:.5f}; hops min {min(hoplist)}  {'ok' if ok else 'FAIL'}")
    out["clauses"]["protection"] = bool(all_ok)
    out["changes_my_mind_fired"] = bool(not all_ok)
    (HERE / "p23_results.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"changes-my-mind fired: {not all_ok}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
