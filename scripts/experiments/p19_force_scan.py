#!/usr/bin/env python3
"""P-19 force-provenance scan: the RUNS forces in p19_alf_waveguide.py
are hardcoded, so this scan documents where they came from and what
they could and could not have biased. For each bow position beta the
bow force is swept over [0.60, 2.20] in steps of 0.05 with the
experiment's own simulate()/lock_stats(), and every run is classified
by its dominant-cluster period: an m=1 lock (period in [1.70, 2.10]
T0, >90 percent of intervals in the cluster, std < 0.02) or an m=2
lock (period in [2.60, 3.00] T0, same criteria).

What this establishes: each hardcoded force sits INSIDE a lock
plateau, not on an edge, and the lock period drifts by at most
0.016 T0 across an entire plateau - a factor ~4 below the 0.06 T0
separation from exact doubling and far below the beta-to-beta period
differences that carry the slope discriminator. Force selection
inside the plateaus therefore cannot move a lock onto 2.000 T0 or
flatten dP/dbeta; it only nudges eps within its stated bracket.

Deterministic, stdlib only. Output: p19_force_scan.json."""
import json
import math  # noqa: F401  (kept for parity with the experiment module)
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from p19_alf_waveguide import simulate, lock_stats, RUNS  # noqa: E402

F_LO, F_HI, F_STEP = 0.60, 2.20, 0.05
M_BANDS = {1: (1.70, 2.10), 2: (2.60, 3.00)}
HARD = {(beta, m): force for beta, force, m in RUNS}


def classify(mean, std, n_lock, n_all):
    if n_all == 0 or n_lock / n_all <= 0.9 or std >= 0.02:
        return None
    for m, (lo, hi) in M_BANDS.items():
        if lo <= mean <= hi:
            return m
    return None


def main():
    out = {"f_grid": [F_LO, F_HI, F_STEP], "betas": {}}
    ok = True
    for beta in sorted({b for b, _, _ in RUNS}):
        rows = []
        F = F_LO
        while F <= F_HI + 1e-9:
            st = lock_stats(simulate(beta, F))
            if st is None:
                rows.append({"F": round(F, 2), "m": None})
            else:
                mean, std, n_lock, n_all = st
                rows.append({"F": round(F, 2), "m": classify(mean, std, n_lock, n_all),
                             "P_T0": round(mean, 4), "std_T0": round(std, 4),
                             "n": [n_lock, n_all]})
            F += F_STEP
        entry = {"rows": rows}
        for m in (1, 2):
            plat = [r for r in rows if r["m"] == m]
            if plat:
                pers = [r["P_T0"] for r in plat]
                entry[f"m{m}_window_F"] = [plat[0]["F"], plat[-1]["F"]]
                entry[f"m{m}_period_drift_T0"] = round(max(pers) - min(pers), 4)
            hf = HARD.get((beta, m))
            if hf is not None:
                inside = bool(plat) and plat[0]["F"] <= hf <= plat[-1]["F"]
                entry[f"m{m}_hardcoded_F"] = hf
                entry[f"m{m}_hardcoded_inside_plateau"] = inside
                ok = ok and inside
                print(f"beta={beta:.2f} m={m}: plateau "
                      f"{[plat[0]['F'], plat[-1]['F']] if plat else None}, "
                      f"drift {entry.get(f'm{m}_period_drift_T0')}, "
                      f"hardcoded F={hf} inside={inside}")
        out["betas"][f"{beta:.2f}"] = entry
    out["all_hardcoded_inside_plateaus"] = bool(ok)
    (HERE / "p19_force_scan.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"all hardcoded forces inside plateaus: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
