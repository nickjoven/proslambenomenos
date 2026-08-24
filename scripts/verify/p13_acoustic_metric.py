#!/usr/bin/env python3
"""Verification for the P-13 acoustic-metric claims, by independent
miniature reimplementation - nothing here reads the experiment's
stored results; every number is recomputed live on chains one third
the experiment's size with a different pulse and different profiles:

(i) chain-arrivals-read-acoustic-metric: front arrivals (first
    crossing of |u| >= 0.25 - a different observable from the
    experiment's peak time, so the reimplementation is independent
    in method as well as in code; the peak observable drifts and
    lobe-hops on short baselines) on a live 500-site ramp (c: 1.0 ->
    0.6 over sites 100..400) match the discrete eikonal sum of 1/c,
    RMS relative deviation < 2%, offset calibrated on a live uniform
    control.
(ii) junction-reflection-reads-impedance-not-metric: live junctions
    re-derive the impedance law ((Z1-Z2)/(Z1+Z2))^2, Z = sqrt(mJ):
    the c-matched junction (Z x4) reflects ~0.36, the Z-matched
    junction (c /4) stays under 0.05 (its small residual is the
    pulse's flux at the slow side's band edge - see the claim's
    scope line and p13_jz_diagnosis.py).
The symbolic layer (EQ1-EQ8) is re-run first; any EQ failure fails
the verification.

--mutant shuffled-profile   scores the live ramp arrivals against a
    block-shuffled profile's eikonal (same multiset of local delays,
    different arrangement) and must FAIL the 2% test.
--mutant c-ratio-reflection predicts junction reflection from the
    metric ratio ((c1-c2)/(c1+c2))^2 instead of the impedance ratio
    and must FAIL against the live junctions.
"""
import math
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "scripts" / "experiments"
sys.path.insert(0, str(EXP))

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"shuffled-profile", "c-ratio-reflection"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

N, TAU, DT = 500, 40.0, 0.05
TH = 0.25
CHK = [150, 200, 250, 300, 350, 400, 450]


def mini_c(x):
    if x <= 100:
        return 1.0
    if x >= 400:
        return 0.6
    return 1.0 - 0.4 * (x - 100) / 300.0


def integrate(m, J, t_end, checkpoints=(), e_marks=()):
    """Euler-Cromer mini chain, half-sine displacement drive at site 0.
    Returns (front arrival times: first crossing of |u| >= TH,
    energies at the requested (time, cut) marks)."""
    u = [0.0] * N
    v = [0.0] * N
    dtm = [DT / x for x in m]
    cross = {j: None for j in checkpoints}
    marks = {}
    for s in range(int(t_end / DT) + 1):
        t = s * DT
        u[0] = math.sin(math.pi * t / TAU) if t <= TAU else 0.0
        for i in range(1, N - 1):
            v[i] += dtm[i] * (J[i] * (u[i + 1] - u[i]) + J[i - 1] * (u[i - 1] - u[i]))
        for i in range(1, N - 1):
            u[i] += DT * v[i]
        for j in checkpoints:
            if cross[j] is None and abs(u[j]) >= TH:
                cross[j] = t
        for (tm, cut) in e_marks:
            if s == int(tm / DT):
                marks[(tm, cut)] = (sum(0.5 * m[i] * v[i] * v[i] for i in range(cut))
                                    + sum(0.5 * J[i] * (u[i + 1] - u[i]) ** 2 for i in range(cut - 1)))
    return cross, marks


def main():
    # 1. every "=" re-checked: the symbolic layer must be green
    r = subprocess.run([sys.executable, str(EXP / "p13_symbolic.py")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL: symbolic layer (EQ1-EQ8) not green")
        return 1

    # 2. arrivals read the metric: live mini control calibrates the
    #    offset, live mini ramp is scored against its eikonal
    ctrl, _ = integrate([1.0] * N, [1.0] * (N - 1), 500.0, checkpoints=CHK)
    nn = len(CHK)
    sx, sy = sum(CHK), sum(ctrl.values())
    sxx = sum(j * j for j in CHK)
    sxy = sum(j * ctrl[j] for j in CHK)
    slope = (nn * sxy - sx * sy) / (nn * sxx - sx * sx)
    t0 = (sy - slope * sx) / nn
    if abs(1.0 / slope - 1.0) > 0.005:
        print(f"FAIL: mini control speed {1.0 / slope:.4f} off c0 = 1 by > 0.5%")
        return 1

    delays = [1.0 / mini_c(i) for i in range(N - 1)]
    if MUTANT == "shuffled-profile":
        blocks = [delays[i:i + 50] for i in range(0, len(delays), 50)]
        random.Random(7).shuffle(blocks)
        delays = [x for b in blocks for x in b]
    eik = {}
    acc, k = 0.0, 0
    for j in CHK:
        while k < j:
            acc += delays[k]
            k += 1
        eik[j] = acc
    m_r = [1.0 / mini_c(i) ** 2 for i in range(N)]
    ramp, _ = integrate(m_r, [1.0] * (N - 1), 640.0, checkpoints=CHK)
    rms = math.sqrt(sum(((ramp[j] - (t0 + eik[j])) / (t0 + eik[j])) ** 2 for j in CHK) / nn)
    if rms >= 0.02:
        print(f"FAIL: live ramp arrival RMS {rms:.4f} >= 0.02 against the "
              f"{'shuffled substrate' if MUTANT else 'profile'}'s eikonal")
        return 1

    # 3. scattering reads the impedance: live junctions vs the law
    #    (or, under the mutant, vs the metric-ratio law)
    for tag, (m2, J2), tol in (("jc", (4.0, 4.0), 0.05), ("jz", (4.0, 0.25), 0.05)):
        m = [1.0 if i < 250 else m2 for i in range(N)]
        J = [1.0 if i < 249 else J2 for i in range(N - 1)]
        _, marks = integrate(m, J, 330.0, e_marks=((60.0, N), (330.0, 220)))
        rr = marks[(330.0, 220)] / marks[(60.0, N)]
        z1, z2 = 1.0, math.sqrt(m2 * J2)
        c1, c2 = 1.0, math.sqrt(J2 / m2)
        law = ((c1 - c2) / (c1 + c2)) ** 2 if MUTANT == "c-ratio-reflection" \
            else ((z1 - z2) / (z1 + z2)) ** 2
        if abs(rr - law) > tol:
            print(f"FAIL: {tag} live R {rr:.4f} vs "
                  f"{'metric-ratio' if MUTANT == 'c-ratio-reflection' else 'impedance'} "
                  f"law {law:.4f} (|diff| > {tol})")
            return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print(f"PASS: EQ layer green; live mini ramp RMS {rms:.4f} < 0.02 against "
          "its eikonal; live junctions follow the impedance law - arrivals "
          "read the metric, scattering reads the impedance")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
