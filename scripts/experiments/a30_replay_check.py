#!/usr/bin/env python3
"""a30_replay_check.py - the 2026-09-05 audit of R-48e, made reproducible.

Reruns a30_replay's real run and its two linear replays (from rest, A;
from the event state, B) at gamma 0.5 and reads window [30, 80] three
ways R-48e did not: (1) by linearity of least squares the drive-locked
phasor of B equals A's plus the projection of the FREE motion (B - A,
the undriven decay from the event state) on the carrier - reported per
site with its slow part, and the carrier cos(ref_b)'s own slow
component (running mean over one rotor period); (2) the b-1 side read
against its OWN bond phase theta_b - theta_{b-1} (reconstructed from
the recorded velocities and the event state) beside the b+1 phase
a30_replay used for both sides; (3) the excess under two Omega
estimators, the endpoint slope of ref_b (a30_replay) and the rotor's
own phase advance (P-49). Writes a30_replay_check.json. Derive layer.
"""
import json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from a30_replay import run_real, run_linear, N, B  # noqa: E402
from p35_ring import fold_fc  # noqa: E402
from p49_derive import decompose  # noqa: E402
from p46_derive import evanescent  # noqa: E402


def fund_phasor(series, ref):
    c = [math.cos(r) for r in ref]; s_ = [math.sin(r) for r in ref]
    cc = sum(x * x for x in c); ss = sum(x * x for x in s_); cs = sum(x * y for x, y in zip(c, s_))
    yc = sum(x * y for x, y in zip(series, c)); ys = sum(x * y for x, y in zip(series, s_))
    det = cc * ss - cs * cs
    return complex((yc * ss - ys * cs) / det, (ys * cc - yc * cs) / det)


def main():
    t0 = time.time(); dt = 0.001; g = 0.5; f = fold_fc(N, -math.pi) + 0.005
    real = run_real(g, f, dt, 90.0)
    c0 = math.cos(math.pi / N); th_e, v_e = real["state"]; th_gs = real["th_gs"]
    order = [(B + 1 + m) % N for m in range(N - 1)]
    disp = [th_e[j] - th_gs[j] for j in order]; md = sum(disp) / len(disp)
    init = ([d - md for d in disp], [v_e[j] for j in order])
    VA = run_linear(g, dt, real["F"], c0, None); VB = run_linear(g, dt, real["F"], c0, init)
    lo, hi = int(30 / dt), int(80 / dt); REF = real["REF"][lo:hi]
    th_p1 = [th_e[B + 1]]
    for row in real["V"]:
        th_p1.append(th_p1[-1] + dt * row[0])
    th_b = [th_p1[k] + real["REF"][k] for k in range(len(real["REF"]))]
    th_m1 = [th_e[B - 1]]
    for row in real["V"]:
        th_m1.append(th_m1[-1] + dt * row[1])
    REFm = [th_b[k] - th_m1[k] for k in range(lo, hi)]
    Om_ref = (REF[-1] - REF[0]) / ((hi - lo - 1) * dt)
    Om_rot = (th_b[hi - 1] - th_b[lo]) / ((hi - lo - 1) * dt)
    per = max(1, int(round(2 * math.pi / Om_ref / dt))); half = per // 2
    out = {"gamma": g, "window": [30.0, 80.0], "c0": c0, "Omega_ref_slope": Om_ref, "Omega_rotor_phase": Om_rot, "sites": {}, "excess": {}}
    for col, name in ((0, "plus1"), (2, "plus2")):
        a = [r[col] for r in VA[lo:hi]]; b = [r[col] for r in VB[lo:hi]]
        zA, zB = fund_phasor(a, REF), fund_phasor(b, REF)
        free = [y - x for x, y in zip(a, b)]; zF = fund_phasor(free, REF)
        dec = decompose(free, REF, per)
        out["sites"][name] = {"A_abs": abs(zA), "B_abs": abs(zB), "free_abs": abs(zF), "additivity": abs(zA + zF - zB),
                              "free_along_A": (zF * zA.conjugate()).real / abs(zA),
                              "free_slow_part_proj": abs(fund_phasor(dec["slow"], REF)),
                              "free_rest_proj": abs(fund_phasor(dec["rest"], REF))}
    c = [math.cos(r) for r in REF]
    sl = [sum(c[max(0, k - half):min(len(c), k + half + 1)]) / (min(len(c), k + half + 1) - max(0, k - half)) for k in range(len(c))]
    out["carrier_cos_slow_rms"] = math.sqrt(sum(x * x for x in sl) / len(sl))
    for Om, lab in ((Om_ref, "ref_slope"), (Om_rot, "rotor_phase")):
        wtop = max(abs(evanescent(Om, cc_, g, dt)[0]) for cc_ in (0.9214, 1.0))
        out["excess"][lab] = {"w_top": wtop}
        for V, vn in ((real["V"], "real"), (VA, "linear_rest"), (VB, "linear_event_state")):
            a1 = abs(fund_phasor([r[0] for r in V[lo:hi]], REF)); a2 = abs(fund_phasor([r[2] for r in V[lo:hi]], REF))
            m1 = abs(fund_phasor([r[1] for r in V[lo:hi]], REF)); m2 = abs(fund_phasor([r[3] for r in V[lo:hi]], REF))
            o1 = abs(fund_phasor([r[1] for r in V[lo:hi]], REFm)); o2 = abs(fund_phasor([r[3] for r in V[lo:hi]], REFm))
            out["excess"][lab][vn] = {"plus_side": a2 / a1 / wtop - 1, "minus_side_b_plus1_phase": m2 / m1 / wtop - 1, "minus_side_own_phase": o2 / o1 / wtop - 1}
    out["seconds"] = time.time() - t0
    json.dump(out, open(os.path.join(HERE, "a30_replay_check.json"), "w"), indent=1)
    for k, v in out["sites"].items():
        print(k, {kk: ("%.4e" % vv) for kk, vv in v.items()})
    print("carrier slow rms %.4f; Omega %.4f / %.4f" % (out["carrier_cos_slow_rms"], Om_ref, Om_rot))
    for lab, d in out["excess"].items():
        for vn in ("real", "linear_rest", "linear_event_state"):
            e = d[vn]; print("%-11s %-18s +%.2f%% / -(b+1 phase) %+.2f%% / -(own) %+.2f%%" % (lab, vn, 100 * e["plus_side"], 100 * e["minus_side_b_plus1_phase"], 100 * e["minus_side_own_phase"]))


if __name__ == "__main__":
    main()
