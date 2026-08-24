#!/usr/bin/env python3
"""Verification for the P-13 acoustic-metric claims: on a mass-spring
chain, (i) pulse arrival times read the acoustic metric c(x) =
sqrt(J/m) - the discrete eikonal sum matches measured peak arrivals
(RMS relative deviation < 2%, checked against the committed
p13_results.json produced by scripts/experiments/p13_acoustic_chain.py);
(ii) the metric is not a complete summary of the substrate: energy
reflection at a junction follows the impedance law ((Z1-Z2)/(Z1+Z2))^2
with Z = sqrt(mJ), re-derived LIVE here on a miniature chain - the
c-matched junction (Z x4) reflects ~0.36 while the Z-matched junction
(c /4) reflects under 0.02.  The symbolic layer (EQ1-EQ8) is re-run
first; any EQ failure fails the verification.

--mutant shuffled-profile   scores the measured ramp/lens arrivals
    against a block-shuffled profile's eikonal (same multiset of local
    delays, different arrangement) and must FAIL the 2% test.
--mutant c-ratio-reflection predicts junction reflection from the
    metric ratio ((c1-c2)/(c1+c2))^2 instead of the impedance ratio
    and must FAIL against the live miniature junctions.
"""
import json
import math
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


def mini_junction(m2, J2, n=500, jn=250, tau=40.0, dt=0.05):
    """Live miniature junction chain (left medium m=J=1), returning
    measured energy reflection E_left(t=330)/E_in(t=60)."""
    m = [1.0 if i < jn else float(m2) for i in range(n)]
    J = [1.0 if i < jn - 1 else float(J2) for i in range(n - 1)]
    u = [0.0] * n
    v = [0.0] * n
    dtm = [dt / x for x in m]
    e_in = e_left = None
    for s in range(int(330.0 / dt) + 1):
        t = s * dt
        u[0] = math.sin(math.pi * t / tau) if t <= tau else 0.0
        for i in range(1, n - 1):
            v[i] += dtm[i] * (J[i] * (u[i + 1] - u[i]) + J[i - 1] * (u[i - 1] - u[i]))
        for i in range(1, n - 1):
            u[i] += dt * v[i]
        if s == int(60.0 / dt):
            e_in = (sum(0.5 * m[i] * v[i] * v[i] for i in range(n))
                    + sum(0.5 * J[i] * (u[i + 1] - u[i]) ** 2 for i in range(n - 1)))
        if s == int(330.0 / dt):
            e_left = (sum(0.5 * m[i] * v[i] * v[i] for i in range(jn - 30))
                      + sum(0.5 * J[i] * (u[i + 1] - u[i]) ** 2 for i in range(jn - 31)))
    return e_left / e_in


def main():
    import p13_profiles as P
    from p13_acoustic_chain import shuffled_eikonal, rms_rel, CHK

    # 1. the symbolic layer must be green (every "=" re-checked)
    r = subprocess.run([sys.executable, str(EXP / "p13_symbolic.py")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL: symbolic layer (EQ1-EQ8) not green")
        return 1

    res = json.loads((EXP / "p13_results.json").read_text())
    t0 = res["detail"]["dt"]["control_t0"]

    # 2. eikonal claim: measured arrivals vs the profile's own eikonal
    #    (or, under the mutant, a block-shuffled profile's eikonal)
    for name in ("ramp", "lens"):
        meas = {j: res["_arrivals"][name][str(j)] for j in CHK} if "_arrivals" in res else None
        if meas is None:
            rms = res["detail"]["dt"][f"{name}_rms"]
            ratio = res["detail"]["dt"][f"{name}_shuffle_ratio"]
            if MUTANT == "shuffled-profile":
                rms = rms * ratio          # the statistic against the shuffled eikonal
        else:
            m_a, J_a = P.profile(name)
            pred = (shuffled_eikonal(name) if MUTANT == "shuffled-profile"
                    else {j: P.eikonal(m_a, J_a, 0, j) for j in CHK})
            rms = rms_rel(meas, {j: t0 + pred[j] for j in CHK})
        if rms >= 0.02:
            print(f"FAIL: {name} arrival RMS {rms:.4f} >= 0.02 "
                  f"({'shuffled substrate' if MUTANT else 'registered eikonal'})")
            return 1

    # 3. scattering claim, live: impedance law vs (mutant) metric law
    for tag, (m2, J2) in (("jc", (4.0, 4.0)), ("jz", (4.0, 0.25))):
        z1, z2 = 1.0, math.sqrt(m2 * J2)
        c1, c2 = 1.0, math.sqrt(J2 / m2)
        law = ((c1 - c2) / (c1 + c2)) ** 2 if MUTANT == "c-ratio-reflection" \
            else ((z1 - z2) / (z1 + z2)) ** 2
        rr = mini_junction(m2, J2)
        if abs(rr - law) > 0.05:
            print(f"FAIL: {tag} measured R {rr:.4f} vs "
                  f"{'metric-ratio' if MUTANT == 'c-ratio-reflection' else 'impedance'} "
                  f"law {law:.4f} (|diff| > 0.05)")
            return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print("PASS: EQ layer green; ramp+lens arrivals within 2% of their "
          "eikonal; live junctions follow the impedance law (jc ~ 0.36, "
          "jz quiet) - the metric is read by arrivals and silent in scattering")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
