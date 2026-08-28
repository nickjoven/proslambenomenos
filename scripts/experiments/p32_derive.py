#!/usr/bin/env python3
"""P-32 derivation layer (pre-registration): the drive-geometry
parity factorial. A-2's open debt: LC-3/LC-4 imported the Josephson
claim (Frolov 2006; Lazarides 2008: alternating 0-pi arrays give
half-integer Shapiro steps for EVEN junction number), P-9/R-6
established that E1's per-site-pinning ring shows NO parity - and
the reconciliation hypothesis (the drive type carries the
difference) was never tested. P-32 runs the 2 x 2 factorial on one
codebase: drive (per-site pinning vs uniform bias + AC) x geometry
(one pi seam vs alternating 0-pi bonds), N = 4..9. Everything here
has a derivable answer and runs before the registered cells.

Derived facts:
  EQ1  the frustration classes, pure arithmetic: with alternating
       offsets s_i = 1/2 on odd bonds, the net ring frustration is
       f(N) = (floor(N/2)/2) mod 1 and odd N forces an alternation
       DEFECT (two adjacent 0-bonds). The registered classes for
       N = 4..9: {4, 8} clean (f = 0, no defect), {5, 9} defect
       (f = 0), {6} half-frustrated (f = 1/2), {7} both. The naive
       even/odd reading of the imported claim REFINES to a mod-4
       + defect structure - derived before anything is measured.
  EQ2  instrument identities on the driven map: rho(I + 1) =
       rho(I) + 1 exactly (translation covariance) and
       rho(-I) = -rho(I) under theta -> -theta with a half-period
       drive shift (nu = 1/8: shift 4 steps) - both verified at
       1e-12 on a seam ring.
  EQ3  ground-state anchors (K = 0, no drive, damped relaxation):
       the seam ring relaxes to uniform strain 1/(2N) per bond
       (P-9's account, now verified for every N = 4..9 at 1e-8);
       the clean ALT ring (N = 4) relaxes to bond strains
       cancelling the offsets exactly; the half-frustrated ALT
       ring (N = 6) relaxes with total residual winding 1/2
       distributed over the ring.
  EQ4  the P-9 reproduction pins: the attractor-controlled widths
       from p9_results_attractor.json at K = 1.0 imported as
       bands (+- 5e-3) for clause (a) - same protocol, same
       instrument, so reproduction must be tight.
  EQ5  the declared validation cell (N = 4, seam, bias): plateau
       width stable under ITERS doubling within 10 percent; only
       stability inspected.
  EQ6  registered parameters: pinning cells K = 1.0, J = 0.6,
       target rho = 1/2, Omega scan [0.30, 0.80]; bias cells
       K = 0, J = 0.6, A = 0.9, nu = 1/8, targets rho = 1/8
       (integer step) and 1/16 (half step), I scans target
       +- 0.06; TOL 4e-4, ITERS 3200, TRANS 900 (E1's); width
       floor 1e-5; initial conditions: control in-phase, seam
       i/(2N), ALT its relaxed ground state.
Pinned -> p32_registration.json.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))

TWO_PI = 2 * math.pi
FAILURES = []
ITERS, TRANS = 3200, 900
TOL = 4e-4
NU = 1.0 / 8.0


def check(name, ok, detail=""):
    print(f"  {name}: {'ok' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)
    return ok


def offsets(geom, N):
    """Bond b sits between sites b and b+1 (mod N)."""
    if geom == "control":
        return [0.0] * N
    if geom == "seam":
        return [0.0] * (N - 1) + [0.5]
    if geom == "alt":
        return [0.5 if b % 2 == 1 else 0.0 for b in range(N)]
    raise ValueError(geom)


def init_theta(geom, N):
    if geom == "control":
        return [0.0] * N
    if geom == "seam":
        return [i / (2 * N) for i in range(N)]
    if geom == "alt":
        return relax(geom, N)
    raise ValueError(geom)


def rho(N, geom, K, J, I, A, theta0=None, iters=ITERS, trans=TRANS):
    """Mean advance per step of the driven pinned ring; theta in
    turns; drive A sin(2 pi nu t) uniform across sites."""
    s = offsets(geom, N)
    th = list(theta0) if theta0 is not None else init_theta(geom, N)
    total = 0.0
    for t in range(iters + trans):
        drv = (A / TWO_PI) * math.sin(TWO_PI * NU * t) if A else 0.0
        adv = []
        for i in range(N):
            up = (i + 1) % N
            dn = (i - 1) % N
            c = (J / TWO_PI) * (
                math.sin(TWO_PI * (th[up] - th[i] + s[i])) +
                math.sin(TWO_PI * (th[dn] - th[i] - s[dn])))
            pin = (K / TWO_PI) * math.sin(TWO_PI * th[i]) if K else 0.0
            adv.append(I + drv - pin + c)
        for i in range(N):
            th[i] += adv[i]
        if t >= trans:
            total += sum(adv) / N
    return total / iters


def relax(geom, N, iters=6000, lr=0.25):
    """Damped relaxation of the undriven, unpinned ring."""
    s = offsets(geom, N)
    th = [0.001 * i * (N - i) for i in range(N)]
    for _ in range(iters):
        for i in range(N):
            up = (i + 1) % N
            dn = (i - 1) % N
            g = (math.sin(TWO_PI * (th[up] - th[i] + s[i])) +
                 math.sin(TWO_PI * (th[dn] - th[i] - s[dn])))
            th[i] += lr * g / TWO_PI
    m = sum(th) / N
    return [x - m for x in th]


def eq1():
    print("EQ1 the frustration classes (pure arithmetic)")
    classes = {}
    for N in range(4, 10):
        f = ((N // 2) * 0.5) % 1.0
        defect = (N % 2 == 1)
        cls = ("clean" if f == 0 and not defect else
               "defect" if f == 0 else
               "half" if not defect else "both")
        classes[N] = {"f": f, "defect": defect, "class": cls}
        print(f"  N={N}: f={f}, defect={defect} -> {cls}")
    want = {4: "clean", 5: "defect", 6: "half", 7: "both",
            8: "clean", 9: "defect"}
    check("EQ1 classes {4,8}=clean {5,9}=defect {6}=half {7}=both",
          all(classes[n]["class"] == want[n] for n in want))
    return {str(n): classes[n] for n in classes}


def eq2():
    print("EQ2 instrument identities")
    r0 = rho(5, "seam", 0.0, 0.6, 0.031, 0.9)
    r1 = rho(5, "seam", 0.0, 0.6, 1.031, 0.9)
    check("EQ2 rho(I+1) = rho(I) + 1", abs(r1 - r0 - 1.0) < 1e-12,
          f"{r1 - r0 - 1.0:.2e}")
    # sign symmetry: theta -> -theta, I -> -I, drive shifted by a
    # half period (4 steps at nu = 1/8) flips the drive sign
    s = offsets("seam", 5)
    th = [-x for x in init_theta("seam", 5)]
    total = 0.0
    I = -0.031
    for t in range(ITERS + TRANS):
        drv = (0.9 / TWO_PI) * math.sin(TWO_PI * NU * (t + 4))
        adv = []
        for i in range(5):
            up = (i + 1) % 5
            dn = (i - 1) % 5
            c = (0.6 / TWO_PI) * (
                math.sin(TWO_PI * (th[up] - th[i] + s[i])) +
                math.sin(TWO_PI * (th[dn] - th[i] - s[dn])))
            adv.append(I + drv + c)
        for i in range(5):
            th[i] += adv[i]
        if t >= TRANS:
            total += sum(adv) / 5
    rneg = total / ITERS
    check("EQ2 rho(-I) = -rho(I) (half-period shift)",
          abs(rneg + r0) < 1e-12, f"{rneg + r0:.2e}")
    return {}


def eq3():
    print("EQ3 ground-state anchors")
    ok = True
    for N in range(4, 10):
        th = relax("seam", N)
        # strains delta_i = th[i+1] - th[i] + s_i should be uniform
        # 1/(2N) (mod sign convention) OR -1/(2N)
        s = offsets("seam", N)
        d = [(th[(i + 1) % N] - th[i] + s[i]) for i in range(N)]
        d = [x - round(x - d[0]) for x in d]  # align branches
        spread = max(d) - min(d)
        mean = sum(d) / N
        if spread > 1e-8 or not (abs(abs(mean) - 1 / (2 * N)) < 1e-8):
            ok = False
            print(f"  seam N={N}: mean {mean:.6f} spread {spread:.1e}")
    check("EQ3 seam relaxes to uniform strain 1/(2N), N=4..9", ok)
    th4 = relax("alt", 4)
    s4 = offsets("alt", 4)
    d4 = [math.sin(TWO_PI * (th4[(i + 1) % 4] - th4[i] + s4[i]))
          for i in range(4)]
    check("EQ3 clean ALT (N=4) cancels offsets (all bond sines 0)",
          max(abs(x) for x in d4) < 1e-6,
          f"max {max(abs(x) for x in d4):.1e}")
    th6 = relax("alt", 6)
    s6 = offsets("alt", 6)
    d6 = [th6[(i + 1) % 6] - th6[i] + s6[i] for i in range(6)]
    wind = sum(d6)
    check("EQ3 half-frustrated ALT (N=6) carries residual winding "
          "1/2 mod 1", abs((wind % 1.0) - 0.5) < 1e-6
          or abs((wind % 1.0) - 0.5) > 1 - 1e-6, f"wind {wind:.6f}")
    return {}


def eq4():
    print("EQ4 the P-9 reproduction pins (K = 1.0)")
    src = json.load(open(os.path.join(HERE,
                                      "p9_results_attractor.json")))
    pins = {}
    for row in src["rows"]:
        if row["K"] == 1.0:
            key = f"{row['N']}_{'tw' if row['twisted'] else 'ctl'}"
            pins[key] = row["width"]
    check("EQ4 twelve pinned widths loaded", len(pins) == 12,
          str(len(pins)))
    return pins


def eq5():
    print("EQ5 validation cell: width stability under ITERS doubling")

    def width(iters):
        lo, hi = NU / 2 - 0.06, NU / 2 + 0.06
        n = 120
        inside = [lo + (hi - lo) * k / n for k in range(n + 1)
                  if abs(rho(4, "seam", 0.0, 0.6,
                             lo + (hi - lo) * k / n, 0.9,
                             iters=iters) - NU / 2) < TOL]
        if not inside:
            return 0.0
        return inside[-1] - inside[0]
    w1 = width(ITERS)
    w2 = width(2 * ITERS)
    ok = (w1 == 0 and w2 == 0) or (w1 > 0
                                   and abs(w2 - w1) < 0.1 * max(w1, w2)
                                   + 2 * 0.12 / 120)
    check("EQ5 N=4 seam bias half-step stable under ITERS x2", ok,
          f"{w1:.5f} vs {w2:.5f}")
    return {"w_half_seam4": w1}


def main():
    pins = {}
    pins["EQ1"] = eq1()
    pins["EQ2"] = eq2()
    pins["EQ3"] = eq3()
    pins["EQ4"] = eq4()
    pins["EQ5"] = eq5()
    pins["params"] = {"K_pin": 1.0, "J": 0.6, "A": 0.9, "nu": NU,
                      "TOL": TOL, "ITERS": ITERS, "TRANS": TRANS,
                      "floor": 1e-5,
                      "targets_bias": [NU, NU / 2],
                      "scan_halfspan": 0.06,
                      "omega_scan_pin": [0.30, 0.80]}
    out = os.path.join(HERE, "p32_registration.json")
    with open(out, "w") as f:
        json.dump(pins, f, indent=1)
    print(f"\npinned -> {out}")
    if FAILURES:
        print("DERIVATION FAILURES:", FAILURES)
        return 1
    print("all derivations ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
