#!/usr/bin/env python3
"""a30_replay.py - A-30: is the transient offset-2 excess linear?

The real run (the A-34 runner: twisted ring, sector 0, N = 64, f =
fold + 0.005, dt = 0.001, gamma 0.5) records, from the event, the two
rotor bond forces on the neighbours (F_+ = -sin D_b on b+1, F_- =
+sin D_{b-1} on b-1), the drive phase ref_b = theta_b - theta_{b+1},
and the velocities at b+-1, b+-2. Then a purely LINEAR open chain of
the other 63 sites (bond stiffness c0 = cos(pi/N), the twisted ground
state's; damping gamma) is driven at its two ends by the recorded
forces, (A) from rest and (B) from the ring's true state at the event
(displacements from the ground state and velocities), and read with
the same lock-in against the same recorded ref_b. By superposition a
linear chain's drive-locked response is the linear response whatever
its initial state, so: excess in (B) but not (A) would be an artefact
of the reference (the slow motion sits in ref_b); excess in neither
is the ring bonds' nonlinearity; excess in (A) is the drive's own
spectrum through the chain. Window [30, 80] (P-48's, the 27 percent),
and [300, 380] as the quiet control. Derive layer; no registration.
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import fold_fc, ground_state  # noqa: E402
from p46_derive import evanescent  # noqa: E402
from p49_derive import decompose  # noqa: E402

N = 64
B = N // 2
WINDOWS = [(30.0, 80.0), (300.0, 380.0)]


def run_real(gamma, f, dt, t_end):
    A, th = ground_state(N, True, 0)
    th_gs = list(th)
    v = [0.0] * N
    D0 = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
    sinD = [math.sin(x) for x in D0]
    n_ramp = int(round(200.0 / dt)); per_unit = int(round(1.0 / dt))
    event = None; n_total = int(round(1500.0 / dt))
    F, REF, V, C = [], [], [], []
    state = None
    s = 0
    while s < n_total:
        fnow = f * min(1.0, (s + 1) / n_ramp)
        for j in range(N):
            v[j] += dt * (sinD[j] - sinD[j - 1] - gamma * v[j] + (fnow if j == B else 0.0))
        for j in range(N):
            th[j] += dt * v[j]
        sinD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
        s += 1
        if event is None:
            if s % per_unit == 0:
                D = [th[(j + 1) % N] - th[j] - A[j] for j in range(N)]
                if max(abs(D[j] - D0[j]) for j in range(N)) > 1.5 * math.pi:
                    event = s; n_total = s + int(round(t_end / dt)) + 1
                    state = (list(th), list(v))
            continue
        # forces on b+1 from bond b, on b-1 from bond b-1 (the rotor's bonds)
        F.append((-sinD[B], sinD[B - 1]))
        REF.append(th[B] - th[B + 1])
        V.append([v[B + 1], v[B - 1], v[B + 2], v[B - 2]])
        if s % per_unit == 0:
            cs = [math.cos(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)
                  if min(abs(j - B), N - abs(j - B)) >= 1 and j != B - 1]
            C.append((min(cs), max(cs)))
    return {"event_t": event * dt, "F": F, "REF": REF, "V": V, "C": C, "state": state, "th_gs": th_gs}


def run_linear(gamma, dt, F, c0, init=None):
    """Open chain of M = N - 1 sites: index m = 0 is b+1, m = M-1 is b-1
    (going the long way round). Linear bonds c0 between consecutive m;
    end forces from F."""
    M = N - 1
    if init is None:
        u = [0.0] * M; w = [0.0] * M
    else:
        u, w = list(init[0]), list(init[1])
    V = []
    for (fp, fm) in F:
        acc = [0.0] * M
        for m in range(M):
            a = -gamma * w[m]
            if m + 1 < M:
                a += c0 * (u[m + 1] - u[m])
            if m - 1 >= 0:
                a -= c0 * (u[m] - u[m - 1])
            if m == 0:
                a += fp
            if m == M - 1:
                a += fm
            acc[m] = a
        for m in range(M):
            w[m] += dt * acc[m]
        for m in range(M):
            u[m] += dt * w[m]
        V.append([w[0], w[M - 1], w[1], w[M - 2]])
    return V


def readout(V, REF, dt, lo, hi, gamma, c_lo, c_hi):
    ref = REF[lo:hi]
    Om = (ref[-1] - ref[0]) / ((hi - lo - 1) * dt)
    Om = -Om if Om < 0 else Om
    per = max(1, int(round(2 * math.pi / Om / dt)))
    amps = {}
    for name, col in (("p1", 0), ("m1", 1), ("p2", 2), ("m2", 3)):
        dec = decompose([row[col] for row in V[lo:hi]], ref, per)
        amps[name] = dec["amp"]
    ws = [abs(evanescent(Om, c, gamma, dt)[0]) for c in (c_lo, c_hi)]
    r_plus = amps["p2"] / amps["p1"]; r_minus = amps["m2"] / amps["m1"]
    return {"Omega": Om, "A": amps, "w_band": [min(ws), max(ws)],
            "ratio21_plus": r_plus, "ratio21_minus": r_minus,
            "excess_plus": r_plus / max(ws) - 1.0, "excess_minus": r_minus / max(ws) - 1.0}


def main():
    dt = 0.001; gamma = 0.5
    f = fold_fc(N, -math.pi) + 0.005
    t0 = time.time(); lines = []
    def log(s):
        print(s, flush=True); lines.append(s)
    real = run_real(gamma, f, dt, 380.0)
    log("real run: event %.1f (%.0f s)" % (real["event_t"], time.time() - t0))
    c0 = math.cos(math.pi / N)
    th_e, v_e = real["state"]; th_gs = real["th_gs"]
    # linear-chain initial state from the ring's state at the event:
    # displacements from the ground state along m = 0 (b+1) .. M-1 (b-1),
    # with the common drift (mean displacement) removed
    order = [(B + 1 + m) % N for m in range(N - 1)]
    disp = [th_e[j] - th_gs[j] for j in order]
    mean_d = sum(disp) / len(disp)
    init = ([d - mean_d for d in disp], [v_e[j] for j in order])
    t1 = time.time()
    VA = run_linear(gamma, dt, real["F"], c0, None)
    log("linear from rest (%.0f s)" % (time.time() - t1)); t1 = time.time()
    VB = run_linear(gamma, dt, real["F"], c0, init)
    log("linear from the event state (%.0f s)" % (time.time() - t1))
    out = {"gamma": gamma, "f": f, "dt": dt, "c0": c0, "event_t": real["event_t"], "windows": {}}
    for (a, b_) in WINDOWS:
        lo, hi = int(round(a / dt)), int(round(b_ / dt))
        if hi > len(real["V"]):
            continue
        ci = real["C"][int(a):int(b_)]
        c_lo, c_hi = min(c[0] for c in ci), max(c[1] for c in ci)
        res = {"c_range_real": [c_lo, c_hi]}
        res["real"] = readout(real["V"], real["REF"], dt, lo, hi, gamma, c_lo, c_hi)
        res["linear_rest"] = readout(VA, real["REF"], dt, lo, hi, gamma, c0, c0)
        res["linear_event_state"] = readout(VB, real["REF"], dt, lo, hi, gamma, c0, c0)
        out["windows"]["%g_%g" % (a, b_)] = res
        for k in ("real", "linear_rest", "linear_event_state"):
            r = res[k]
            log("  win [%3.0f,%3.0f] %-18s Omega %.4f A1 %.4e A2 %.4e ratio21 %.4e (side -: %.4e) band top %.4e excess %+.2f%% (side -: %+.2f%%)"
                % (a, b_, k, r["Omega"], r["A"]["p1"], r["A"]["p2"], r["ratio21_plus"], r["ratio21_minus"], r["w_band"][1], 100 * r["excess_plus"], 100 * r["excess_minus"]))
    out["seconds_total"] = time.time() - t0
    log("total %.0f s" % out["seconds_total"])
    json.dump(out, open(os.path.join(HERE, "a30_replay.json"), "w"), indent=1)
    open(os.path.join(HERE, "a30_replay.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
