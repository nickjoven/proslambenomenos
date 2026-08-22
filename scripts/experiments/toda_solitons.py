#!/usr/bin/env python3
"""Solitons on an inertial nonlinear chain (Toda) against the linear
null. Units m = a = b = 1. Relative displacement r_n = u_{n+1} - u_n;
Toda force between neighbours f(r) = 1 - exp(-r) (linear null:
f(r) = r, same sound speed c = 1). Velocity-Verlet.

Three demonstrations:
 1. EXACT SOLITON: r_n(t) = -ln(1 + sinh^2(k) sech^2(k n - beta t)),
    beta = sinh k, speed v = sinh(k)/k > c = 1 (Toda 1967). Launched
    on the Toda chain it keeps its shape; the same profile on the
    linear chain disperses.
 2. EMERGENCE: a generic compression pulse on the Toda chain sheds a
    soliton (sharp, supersonic, shape-fixed) plus a dispersive tail;
    on the linear chain the whole pulse spreads (Schrodinger 1914,
    width ~ t^(1/3) Airy front).
 3. SPEED-AMPLITUDE LAW: measured soliton speed vs the amplitude
    parameter k against v/c = sinh(k)/k.
Writes toda_results.json with profiles and measurements."""
import json
import math
import sys

N = 600
DT = 0.02


def force(r, toda):
    return (1.0 - math.exp(-r)) if toda else r


def step(u, w, toda, dt):
    n = len(u)
    acc = [0.0] * n
    for i in range(n):
        rR = u[(i + 1) % n] - u[i]
        rL = u[i] - u[(i - 1) % n]
        acc[i] = force(rR, toda) - force(rL, toda)
    for i in range(n):
        w[i] += acc[i] * dt
        u[i] += w[i] * dt
    return u, w


def verlet(u, w, toda, T, dt=DT, record_at=()):
    # velocity-Verlet: half-kick, drift, half-kick
    n = len(u)
    def accel(u):
        a = [0.0] * n
        for i in range(1, n - 1):      # ends clamped (u_0 = u_{N-1} = 0): no periodic wrap
            a[i] = force(u[i + 1] - u[i], toda) - force(u[i] - u[i - 1], toda)
        return a
    a = accel(u)
    snaps = {}
    steps = int(round(T / dt))
    rec = set(int(round(t / dt)) for t in record_at)
    for k in range(steps + 1):
        if k in rec:
            snaps[round(k * dt, 6)] = [u[i + 1] - u[i] for i in range(n - 1)]
        if k == steps:
            break
        for i in range(n):
            w[i] += 0.5 * dt * a[i]
            u[i] += dt * w[i]
        a = accel(u)
        for i in range(n):
            w[i] += 0.5 * dt * a[i]
    return snaps


def sech2(x):
    return 0.0 if abs(x) > 350 else 1.0 / math.cosh(x) ** 2


def displacements(rfun):
    """u_n = sum_{m<n} r_m with u_0 = 0 (the left end, far from the pulse)."""
    u = [0.0] * N
    for n in range(1, N):
        u[n] = u[n - 1] + rfun(n - 1)
    return u


def soliton_ic(kap, x0):
    beta = math.sinh(kap)
    rt = lambda n, t: -math.log(1 + math.sinh(kap) ** 2 * sech2(kap * (n - x0) - beta * t))
    h = 1e-4
    u0 = displacements(lambda n: rt(n, 0.0))
    um = displacements(lambda n: rt(n, -h))
    w = [(a - b) / h for a, b in zip(u0, um)]      # exact velocity of the travelling profile
    r = [rt(n, 0.0) for n in range(N)]
    return u0, w, r


def pulse_ic(amp, width, x0):
    rt = lambda n, t: -amp * math.exp(-((n - x0 - t) / width) ** 2)   # right-moving at sound speed c = 1
    h = 1e-4
    u0 = displacements(lambda n: rt(n, 0.0))
    um = displacements(lambda n: rt(n, -h))
    w = [(a - b) / h for a, b in zip(u0, um)]
    r = [rt(n, 0.0) for n in range(N)]
    return u0, w, r


def peak_stats(r):
    i = min(range(len(r)), key=lambda n: r[n])
    pk = -r[i]
    # contiguous half-maximum width around the peak (not the global half-max set)
    lo = i
    while lo > 0 and -r[lo - 1] > pk / 2: lo -= 1
    hi = i
    while hi < len(r) - 1 and -r[hi + 1] > pk / 2: hi += 1
    return i, pk, hi - lo + 1


def main():
    out = {}
    # 1. exact soliton, kappa = 1.0, on Toda and on the linear null
    kap = 1.0
    for toda in (True, False):
        u, w, r0 = soliton_ic(kap, 120)
        snaps = verlet(u, w, toda, 120.0, record_at=(0, 40, 80, 120))
        stats = {t: peak_stats(r) for t, r in snaps.items()}
        out[f"exact_k1_{'toda' if toda else 'linear'}"] = {"snaps": {str(t): r for t, r in snaps.items()},
                                                           "stats": {str(t): s for t, s in stats.items()}}
        print(f"exact soliton k=1 on {'Toda' if toda else 'linear'}: " +
              "; ".join(f"t={t}: pos {s[0]} peak {s[1]:.4f} fwhm {s[2]}" for t, s in sorted(stats.items())), flush=True)
    # 2. emergence from a generic pulse
    for toda in (True, False):
        u, w, r0 = pulse_ic(1.2, 4.0, 120)
        snaps = verlet(u, w, toda, 160.0, record_at=(0, 40, 80, 120, 160))
        stats = {t: peak_stats(r) for t, r in snaps.items()}
        out[f"pulse_{'toda' if toda else 'linear'}"] = {"snaps": {str(t): r for t, r in snaps.items()},
                                                        "stats": {str(t): s for t, s in stats.items()}}
        print(f"pulse on {'Toda' if toda else 'linear'}: " +
              "; ".join(f"t={t}: pos {s[0]} peak {s[1]:.4f} fwhm {s[2]}" for t, s in sorted(stats.items())), flush=True)
    # 3. speed-amplitude law
    law = []
    for kap in (0.5, 0.8, 1.0, 1.3, 1.6):
        u, w, r0 = soliton_ic(kap, 100)
        snaps = verlet(u, w, True, 60.0, record_at=(0, 60))
        p0 = peak_stats(snaps[0.0])[0]; p1 = peak_stats(snaps[60.0])[0]
        v = (p1 - p0) / 60.0
        law.append({"kappa": kap, "v_measured": v, "v_theory": math.sinh(kap) / kap,
                    "amplitude": 2 * math.log(math.cosh(kap))})
        print(f"k={kap}: v = {v:.4f}, sinh(k)/k = {math.sinh(kap)/kap:.4f}, amplitude {2*math.log(math.cosh(kap)):.3f}", flush=True)
    out["law"] = law
    with open("scripts/experiments/toda_results.json", "w") as f:
        json.dump(out, f)


if __name__ == "__main__":
    main()
