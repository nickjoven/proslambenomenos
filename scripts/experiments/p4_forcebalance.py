#!/usr/bin/env python3
"""P-4 diagnostic: why does the twisted clamped ring need a larger
normal force to enter stick-slip? Static check first: with site 0
clamped and the pi bond adjacent, the uniform gradient pi/N per bond
is force-balanced at every free node (sin(pi/N) on both sides), so the
holonomy adds NO static pre-load at the bow node. Dynamic check: run
the sliding regime and record, at each velocity-crossing (the only
moments re-stick is possible), the hold force |req| = |g v - F_B|;
re-stick needs |req| <= mu_s F_N. Compare distributions."""

import math
import sys
sys.path.insert(0, "scripts/experiments")

TWO_PI = 2 * math.pi


def crossings(N, twisted, F_N, v_bow=0.3, m=1.0, g=0.05, J=1.0, mu_d=0.5,
              dt=0.01, T=400.0, T_skip=200.0):
    s = [0.0] * N
    s[N - 1] = math.pi if twisted else 0.0
    B = N // 2
    grad = (math.pi / N) if twisted else 0.0
    th = [grad * i for i in range(N)]
    w = [0.0] * N
    w[B] = v_bow + 0.01          # start sliding
    reqs = []
    rels = []
    allreq = []
    for k in range(int(T / dt)):
        t = k * dt
        F = [0.0] * N
        for i in range(N):
            j = (i + 1) % N
            F[i] += J * math.sin(th[j] - th[i] + s[i])
            F[j] += J * math.sin(th[i] - th[j] - s[i])
        for i in range(1, N):
            if i == B:
                continue
            w[i] += (F[i] - g * w[i]) / m * dt
            th[i] += w[i] * dt
        rel = w[B] - v_bow
        fric = -mu_d * F_N * (1 if rel > 0 else -1)
        w_new = w[B] + (F[B] - g * w[B] + fric) / m * dt
        if t >= T_skip:
            rels.append(rel)
            allreq.append(abs(g * v_bow - F[B]))
        if (w_new - v_bow) * rel <= 0 and t >= T_skip:
            reqs.append(abs(g * v_bow - F[B]))
        w[B] = w_new
        th[B] += w[B] * dt
    return reqs, rels, allreq


for N in (8, 16):
    for tw in (False, True):
        r, rels, allreq = crossings(N, tw, 1.0)
        mrel = sum(rels) / len(rels)
        print(f"N={N:2d} {'twisted' if tw else 'control'}: crossings={len(r)} "
              f"mean(w_B - v)={mrel:+.3f} min rel={min(rels):+.3f} max rel={max(rels):+.3f} "
              f"min|req|={min(allreq):.3f} frac|req|<=1: {sum(x<=1 for x in allreq)/len(allreq):.2f}")
