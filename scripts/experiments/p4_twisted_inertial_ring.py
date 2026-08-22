#!/usr/bin/env python3
"""P-4 experiment: holonomy vs gate on a twisted inertial ring.

Ring of N second-order phase oscillators (Kuramoto with inertia):
    m th'' = -g th' + J [ sin(th_{i+1} - th_i + s_i) + sin(th_{i-1} - th_i - s_{i-1}) ]
plus an on-site substrate -K sin(th_i) on every non-bow site (the
bridge/nut analog: without it a free ring co-rotates with the bow and
never slips - first smoke run, 0 slips at every F_N),
with s_i = 0 on every bond except bond 0 (between site N-1 and site 0),
where s = pi (twisted) or 0 (control). Site B = N//2 is the bow node:
Coulomb stick-slip against a bow moving at constant velocity v_bow,
static threshold mu_s*F_N, dynamic friction mu_d*F_N (Kawano/Guettler
ingredient: conditionally reflecting contact). A phase kink launched at
a slip travels around the ring and returns after ~N/c, c = sqrt(J/m).

Variant --clamp (second run): no substrate; site 0 is clamped (the
bridge), so waves propagate freely and return after ~N/c. The pinned
variant's slip period was ~8 at every N - a local relaxation, not a
returning corner - so it is outside the Kawano regime by its own data.

Observable: slip-event period at the bow node in units of the ring
round-trip time. Period doubling (ratio ~2) is the f0/2 mechanism.
Sweep F_N at fixed v_bow; report the onset F_N of doubling for twisted
vs control and even vs odd N. Writes p4_results.json.
"""

import json
import math
import sys

TWO_PI = 2 * math.pi


def run(N, twisted, F_N, v_bow=0.3, m=1.0, g=0.05, J=1.0, K=1.0, mu_s=1.0, mu_d=0.5,
        clamp=False,
        dt=0.01, T=600.0, T_skip=300.0):
    s = [0.0] * N
    s[N - 1] = math.pi if twisted else 0.0      # bond (N-1 -> 0)
    B = N // 2
    # start near the bond-compatible uniform gradient so the twist is a
    # holonomy of the background, not a launched kink
    grad = (math.pi / N) if twisted else 0.0
    th = [grad * i for i in range(N)]
    w = [0.0] * N
    stuck = True
    slips = []
    steps = int(T / dt)
    c = math.sqrt(J / m)
    for k in range(steps):
        t = k * dt
        F = [0.0] * N
        for i in range(N):
            j = (i + 1) % N
            F[i] += J * math.sin(th[j] - th[i] + s[i])
            F[j] += J * math.sin(th[i] - th[j] - s[i])
        for i in range(N):
            if i == B or (clamp and i == 0):
                continue
            a = (F[i] - (0.0 if clamp else K) * math.sin(th[i]) - g * w[i]) / m
            w[i] += a * dt
            th[i] += w[i] * dt
        # bow node
        req = g * v_bow - F[B]                    # force needed to hold stick
        if stuck:
            if abs(req) > mu_s * F_N:
                stuck = False
                if t >= T_skip:
                    slips.append(t)
                w[B] = v_bow
            else:
                w[B] = v_bow
                th[B] += v_bow * dt
                continue
        if not stuck:
            rel = w[B] - v_bow
            fric = -mu_d * F_N * (1 if rel > 0 else -1) if abs(rel) > 1e-9 else 0.0
            a = (F[B] - g * w[B] + fric) / m
            w_new = w[B] + a * dt
            if (w_new - v_bow) * rel <= 0 and abs(req) <= mu_s * F_N:
                stuck = True
                w[B] = v_bow
            else:
                w[B] = w_new
            th[B] += w[B] * dt
    T_round = N / c
    if len(slips) < 3:
        regime = "stuck" if stuck else "sliding"
        return {"n_slips": len(slips), "ratio": None, "T_round": T_round,
                "regime": regime}
    gaps = [b - a for a, b in zip(slips, slips[1:])]
    gaps.sort()
    med = gaps[len(gaps) // 2]
    return {"n_slips": len(slips), "ratio": med / T_round, "T_round": T_round,
            "gap_min": gaps[0], "gap_max": gaps[-1], "regime": "stick-slip"}


def main():
    clamp = "--clamp" in sys.argv
    refine = "--refine" in sys.argv
    Ns = [int(x) for x in [a for a in sys.argv[1:] if not a.startswith("--")] or ["8", "9"]]
    F_grid = ([1.5 + 0.05 * k for k in range(13)] if refine
              else [0.6 + 0.1 * k for k in range(18)])
    T, T_skip = (1200.0, 400.0) if refine else (400.0, 200.0)
    out = {}
    for N in Ns:
        for twisted in (False, True):
            key = f"N={N} {'twisted' if twisted else 'control'}"
            rows = []
            for F_N in F_grid:
                r = run(N, twisted, F_N, T=T, T_skip=T_skip, clamp=clamp)
                r["gaps_n"] = r["n_slips"]
                rows.append({"F_N": round(F_N, 2), **r})
                rat = r["ratio"]
                print(f"{key:18s} F_N={F_N:4.2f} slips={r['n_slips']:4d} "
                      f"period/round={'%.3f' % rat if rat else '  - '} {r['regime']}", flush=True)
            out[key] = rows
    name = ("p4_results_refine.json" if refine else
            "p4_results_clamp.json" if clamp else "p4_results_pinned.json")
    with open("scripts/experiments/" + name, "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
