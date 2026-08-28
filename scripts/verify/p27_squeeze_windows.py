#!/usr/bin/env python3
"""Verification for the P-27 claim classical-gravity-squeeze-windows,
by independent live reimplementation: its own constants, its own
route to dimensional consistency (random rescaling of the base
units - both sides of each squeeze must scale by the identical
factor, a check that never touches the derive layer's dimension
vectors), its own bound arithmetic from the raw pinned inputs, and
its own window verdicts. Only the machine-parsed janse_table1.json
is shared - data, not code.

Checks: (1) unit-scaling invariance of eqs. (44)/(46)/(47); (2) the
six OSSW bounds recomputed from stated inputs land within 0.5
(lower) / 3.0 (upper) orders of the printed values; (3) verdicts:
continuous window negative under every rule, discrete positive at
8+ orders under the direct-on-Earth rule in BOTH arithmetics, and
exactly the three registered Asenbaum sign flips between printed
and recomputed bounds.

--mutant lambda-flip   puts the decoherence rate in the numerator
    of the lower bounds; the unit-scaling check kills it.
--mutant flip-blind    computes verdicts from printed bounds only
    and asserts sign stability; the three registered Asenbaum
    flips kill it.
"""
import json
import math
import random
import sys
from pathlib import Path

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"lambda-flip", "flip-blind"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

DATA = Path(__file__).resolve().parents[1] / "experiments" \
    / "janse_table1.json"
G = 6.674e-11
FOM_CAV = 1e14
AMU = 1.66054e-27

# raw pinned inputs (OSSW Section V, dT attested by Janse)
P = {"N": 1e26, "sa": 1e-7, "T": 100.0, "rN": 1e-15, "mN": 1e-26,
     "Vb": 6.371e6 ** 2 * 1e4, "Ml": 1e-24, "lam": 10.0,
     "Vl": 1e-25, "Rl": 1e-9}
PRINTED = {"cont": (1e-41, 1e-24), "disc": (1e-1, 1e-25),
           "nonloc": (1e-9, 1e-40)}


def bounds(p, g):
    core = p["sa"] ** 2 * p["N"] * p["T"]
    lam_pow = +1 if MUTANT == "lambda-flip" else -1
    lam = p["lam"] ** lam_pow
    return {
        "cont": (core * p["rN"] ** 4 / (p["Vb"] * g ** 2),
                 p["Ml"] ** 2 / p["Vl"] * lam),
        "disc": (core * p["rN"] ** 4 / (p["mN"] * g ** 2),
                 p["Ml"] * lam),
        "nonloc": (core * p["rN"] ** 3 / g ** 2,
                   p["Ml"] ** 2 / p["Rl"] * lam),
    }


DIMS = {"N": (0, 0, 0), "sa": (0, 1, -2), "T": (0, 0, 1),
        "rN": (0, 1, 0), "mN": (1, 0, 0), "Vb": (0, 3, 0),
        "Ml": (1, 0, 0), "lam": (0, 0, -1), "Vl": (0, 3, 0),
        "Rl": (0, 1, 0)}
G_DIM = (-1, 3, -2)


def main():
    failures = []

    # (1) unit-scaling invariance: rescale base units, both sides of
    # each squeeze must scale by the identical factor
    rng = random.Random(27)
    for trial in range(20):
        f = [rng.uniform(0.2, 5.0) for _ in range(3)]  # kg, m, s

        def scaled(v, d):
            return v * f[0] ** d[0] * f[1] ** d[1] * f[2] ** d[2]
        p2 = {k: scaled(v, DIMS[k]) for k, v in P.items()}
        g2 = scaled(G, G_DIM)
        b1 = bounds(P, G)
        b2 = bounds(p2, g2)
        for cls in b1:
            r_up = b2[cls][0] / b1[cls][0]
            r_lo = b2[cls][1] / b1[cls][1]
            if abs(r_up / r_lo - 1) > 1e-9:
                print(f"FAIL: units - {cls} sides scale by "
                      f"{r_up:.4g} vs {r_lo:.4g} under base rescale")
                failures.append("units")
                break
        if failures:
            break
    if not failures:
        print("unit-scaling invariance: ok (20 random rescalings)")

    # (2) six bounds vs printed
    b = bounds(P, G)
    for cls, (pu, pl) in PRINTED.items():
        du = math.log10(pu / b[cls][0])
        dl = math.log10(pl / b[cls][1])
        if abs(du) > 3.0 or abs(dl) > 0.5:
            print(f"FAIL: {cls} bounds off printed "
                  f"(upper delta {du:+.2f}, lower delta {dl:+.2f})")
            failures.append(f"bounds-{cls}")
        else:
            print(f"{cls}: upper delta {du:+.2f}, lower {dl:+.2f} ok")

    # (3) verdicts
    tab = json.load(open(DATA))["rows"]
    gisler = [r for r in tab if r["ref"].startswith("Gisler")][0]["FOM"]
    asen = [r for r in tab if r["ref"].startswith("Asenbaum")][0]["FOM"]
    fein_low_disc = 25000 * AMU / 133.0

    def win(cls, fom, arith, lower):
        up = (PRINTED[cls][0] if arith == "printed"
              else b[cls][0]) * fom / FOM_CAV
        return math.log10(up / lower)

    conts = [win("cont", f, a, PRINTED["cont"][1])
             for f in (FOM_CAV, gisler, asen)
             for a in ("printed", "recomputed")]
    if not all(w < 0 for w in conts):
        print("FAIL: a continuous window came out positive")
        failures.append("cont")
    dg = [win("disc", gisler, a, PRINTED["disc"][1])
          for a in ("printed", "recomputed")]
    if not all(w >= 8.0 for w in dg):
        print(f"FAIL: discrete Gisler window below 8 orders: {dg}")
        failures.append("disc-gisler")
    else:
        print(f"discrete/Gisler windows {dg[0]:+.2f} (printed), "
              f"{dg[1]:+.2f} (recomputed): ok")
    # the three registered flips
    flip_cells = [
        ("disc", asen, PRINTED["disc"][1]),
        ("disc", asen, fein_low_disc),
        ("nonloc", asen, 1e-35),
    ]
    if MUTANT == "flip-blind":
        flips = 0  # printed-only arithmetic sees no flip by construction
    else:
        flips = sum(1 for cls, fom, lo in flip_cells
                    if (win(cls, fom, "printed", lo) < 0)
                    != (win(cls, fom, "recomputed", lo) < 0))
    if flips != 3:
        print(f"FAIL: expected the three registered Asenbaum sign "
              f"flips, found {flips}")
        failures.append("flips")
    else:
        print("the three registered Asenbaum sign flips reproduce: ok")

    if MUTANT is not None:
        if failures:
            print(f"mutant {MUTANT} broke the verification as it must")
            return 1
        print(f"mutant {MUTANT} did not break the verification")
        return 0
    if failures:
        return 1
    print("p27 verification ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: exception {e!r}")
        sys.exit(1)
