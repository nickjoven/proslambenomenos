#!/usr/bin/env python3
"""POST-HOC DIAGNOSIS (labelled as such; rescues nothing). The
registered clause (c) expected jz reflection < 0.01 from the
monochromatic lattice value R(k = 0.05) = 0.0014; the chain measured
0.036. Hypothesis: the half-sine pulse is not monochromatic - its
flux above the slow medium's band edge omega_c = 2*sqrt(J2/m2) = 0.5
is TOTALLY reflected no matter how well the impedance is matched,
and its near-edge flux reflects strongly. This script computes the
prediction with no free parameters:

  1. record the incident waveform u(t) at one site of a uniform chain
     (same drive, same dt as the experiment);
  2. DFT it (own O(N L) transform, stdlib);
  3. weight each frequency by its energy flux w = omega^2 vg1 |U|^2;
  4. reflect each component with the exact lattice solve
     junction_solve(1, 1, 4, 0.25, k1(omega)) - and R = 1 above the
     band edge;
  5. compare  R_pred = sum(w R) / sum(w)  to the measured 0.036.

If R_pred disagrees with the measurement, the hypothesis is wrong and
the number below says so; nothing here is tuned.
"""
import cmath
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from p13_profiles import junction_solve  # noqa: E402

DT, TAU = 0.05, 60.0
N, REC, T_END = 700, 350, 690.0          # end reflection reaches REC at t ~ 698


def incident_waveform():
    u = [0.0] * N
    v = [0.0] * N
    trace = []
    for s in range(int(T_END / DT) + 1):
        t = s * DT
        u[0] = math.sin(math.pi * t / TAU) if t <= TAU else 0.0
        for i in range(1, N - 1):
            v[i] += DT * ((u[i + 1] - u[i]) + (u[i - 1] - u[i]))
        for i in range(1, N - 1):
            u[i] += DT * v[i]
        trace.append(u[REC])
    return trace


def main():
    trace = incident_waveform()
    T = len(trace) * DT
    m2, J2 = 4.0, 0.25
    w_edge = 2 * math.sqrt(J2 / m2)                     # band edge of the slow side
    L = 600                                             # omega up to 2 pi L / T ~ 5.5
    num = den = flux_above = 0.0
    rows = []
    for el in range(1, L + 1):
        om = 2 * math.pi * el / T
        if om >= 2.0:                                   # left band edge: no propagation
            break
        U = sum(x * cmath.exp(-1j * om * i * DT) for i, x in enumerate(trace)) * DT
        k1 = 2 * math.asin(om / 2)
        vg1 = math.cos(k1 / 2)
        w = om * om * vg1 * abs(U) ** 2
        if om >= w_edge:
            R = 1.0
        else:
            R, _ = junction_solve(1.0, 1.0, m2, J2, k1)
        num += w * R
        den += w
        if om >= w_edge:
            flux_above += w
        if el <= 12 or (om < w_edge < om + 2 * math.pi / T):
            rows.append((om, abs(U), R))
    R_pred = num / den
    measured = json.loads((HERE / "p13_results.json").read_text())["detail"]["dt"]["jz_R"]
    print(f"band edge of slow medium: omega_c = {w_edge}")
    print(f"flux fraction above band edge: {flux_above / den:.4f}")
    print(f"R_pred (flux-weighted exact lattice solve, no free parameters): {R_pred:.4f}")
    print(f"R_measured (experiment): {measured:.4f}")
    print(f"ratio pred/measured: {R_pred / measured:.3f}")
    out = {"omega_c": w_edge, "flux_above_edge": flux_above / den,
           "R_pred": R_pred, "R_measured": measured,
           "sample_rows_omega_U_R": [[round(a, 4), round(b, 5), round(c, 6)] for a, b, c in rows]}
    (HERE / "p13_jz_diagnosis.json").write_text(json.dumps(out, indent=1) + "\n")
    agree = abs(R_pred - measured) / measured < 0.25
    print("hypothesis " + ("SUPPORTED (within 25%)" if agree else "NOT SUPPORTED - diagnosis stays open"))
    return 0 if agree else 1


if __name__ == "__main__":
    sys.exit(main())
