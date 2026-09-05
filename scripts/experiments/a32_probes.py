#!/usr/bin/env python3
"""a32_probes.py - the smear-identity check of scripts/verify/p49_near_band.py
fed series that are NOT the smeared drive-locked fundamental, so its
tolerance can be shown to fail them (LAW-60; the LAW-59 numbers for the
noise probe were a scratch realisation with no script - L-18).
Runs the verifier's own N = 48 ring once (gamma 0.5, window [10, 50)),
then applies check (1)'s arithmetic, copied from the verifier, to:
  real        the neighbour's velocity (must pass)
  wrongsite   site b+2's velocity fed as the neighbour's
  noise       0.3 cos(3 theta_b) + N(0, 0.2), seed 1
  noise+trend the same plus a linear trend of amplitude 2
  locked      A_1 cos(theta_b), rotor-locked, no smear
  locked+dc   the same plus a DC offset of 3
Prints meas, pred, |diff|, tol, the slow bound and the verdict per probe
and writes a32_probes.json. Deterministic (the verifier's own seed).
"""
import cmath, json, math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "verify"))
import p49_near_band as V  # noqa: E402


def check1(v1, TH, DT):
    ref_b = [t[0] - t[1] for t in TH]; ref_r = [t[0] for t in TH]
    A1b, fund1 = V.fundamental(v1, ref_b)
    Om = (ref_r[-1] - ref_r[0]) / ((len(ref_r) - 1) * DT); T = len(v1) * DT
    x1 = [t[1] for t in TH]; m = sum(x1) / len(x1)
    pred = abs(sum(cmath.exp(-1j * (x - m)) for x in x1)) / len(x1)
    z_tot = V.lockin_phasor(v1, ref_r)
    per = max(1, int(round(2 * math.pi / Om / DT))); half = per // 2
    rem = [a - b for a, b in zip(v1, fund1)]
    slow1 = [sum(rem[max(0, k - half):min(len(rem), k + half + 1)]) / (min(len(rem), k + half + 1) - max(0, k - half)) for k in range(len(rem))]
    slow_rms = math.sqrt(sum(x * x for x in slow1) / len(slow1))
    ref_res = abs(sum(cmath.exp(-1j * r) for r in ref_r)) / len(ref_r)
    slow_bound = 2.0 * slow_rms * ref_res / A1b
    meas = 2.0 * abs(z_tot) / A1b
    tol = slow_bound + 2.0 / (Om * T)
    ok = abs(meas - pred) <= tol and slow_bound <= 0.05
    return {"meas": meas, "pred": pred, "diff": abs(meas - pred), "tol": tol, "slow_bound": slow_bound, "A1b": A1b, "ref_resultant": ref_res, "pass": ok}


def main():
    n = 48; f = V.own_fold(n, -math.pi) + 0.02
    ev, TH, Vv, cmin, cmax = V.run(n, 0.5, f, (10.0, 50.0))
    assert ev is not None
    v1 = [x[1] for x in Vv]; v2 = [x[2] for x in Vv]
    r = random.Random(1)
    A1 = V.fundamental(v1, [t[0] - t[1] for t in TH])[0]
    L = len(v1)
    probes = {
        "real": v1,
        "wrongsite": v2,
        "noise": [0.3 * math.cos(3 * t[0]) + r.gauss(0, 0.2) for t in TH],
        "noise+trend": [0.3 * math.cos(3 * t[0]) + r.gauss(0, 0.2) + 2.0 * (k / L - 0.5) for k, t in enumerate(TH)],
        "locked": [A1 * math.cos(t[0]) for t in TH],
        "locked+dc": [A1 * math.cos(t[0]) + 3.0 for t in TH],
    }
    out = {}
    for name, series in probes.items():
        res = check1(series, TH, V.DT); out[name] = res
        print("%-12s meas %.4f pred %.4f |d| %.4f tol %.4f slow_bound %.4f -> %s" % (name, res["meas"], res["pred"], res["diff"], res["tol"], res["slow_bound"], "PASS" if res["pass"] else "FAIL"))
    json.dump(out, open(os.path.join(HERE, "a32_probes.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
