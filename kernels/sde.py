#!/usr/bin/env python3
"""Stochastic-integrator kernels: the Euler-Maruyama Adler phase
integrator, the Schmitt-trigger committed-event detector, and the
escape-with-reset winding protocol. Extracted, not rewritten; every
function preserves the RNG call sequence and floating-point operation
order of its source, so ported callers keep identical numbers.

Admission (two-artifact rule):
  adler_em        scripts/experiments/p22_locking.py:18-29 (run),
                  scripts/verify/p22_locking_skeleton.py:41-50 (em)
  mod_pi_track    scripts/experiments/p22_locking.py:32-55 (run_track),
                  scripts/experiments/p23_protect.py:16-35 (member),
                  scripts/verify/p22_locking_skeleton.py:53-72 (em_avg)
  ring_escape     scripts/experiments/p24_memory.py:113-141 (rung 3),
                  scripts/verify/p24_memory_hierarchy.py:91-125 (escape_run)
  diffuse_ensemble
                  scripts/experiments/p24_memory.py:22-40 (rung 1),
                  scripts/verify/p24_memory_hierarchy.py:129-137

Selftest anchors (from the derive layers that earned them):
  - deterministic Adler beat: (theta(T) - theta(0))/T -> sqrt(delta^2
    - eps^2) outside the tongue (p22_derive.py EQ1: the contour
    integral equals 2 pi/sqrt(delta^2 - eps^2)); inside the tongue the
    phase locks.
  - two-photon bistability: two starts pi apart both lock and stay pi
    apart (p22_derive.py EQ2: two stable phases per 2 pi, pi apart).
  - rung-1 diffusion: ensemble <cos theta> at t follows e^{-Dt} inside
    its CLT band (p24_derive.py EQ1: cos is the generator's
    eigenfunction with eigenvalue -1).
  - escape-with-reset: the fresh p24 falsifier cell (N = 8, D = 0.20,
    seed 1234, T = 60) reproduces its committed-event count exactly.

stdlib only.
"""
import math
import random


def adler_em(theta0, delta, eps, D, T, k, seed, dt):
    """Euler-Maruyama for dtheta = (delta - eps sin(k theta)) dt +
    sqrt(2D) dW; returns the final phase. D = 0 runs the deterministic
    integrator with no RNG draws (p22_locking.py:18)."""
    rng = random.Random(seed)
    g = rng.gauss
    s = math.sin
    n = int(T / dt)
    amp = math.sqrt(2 * D * dt)
    th = theta0
    for _ in range(n):
        th += (delta - eps * s(k * th)) * dt + (amp * g(0.0, 1.0) if D > 0 else 0.0)
    return th


def mod_pi_track(eps, D, T, seed, dt, delta=0.0):
    """Two-photon (sin 2 theta) Euler-Maruyama run with the Schmitt
    trigger: a well change commits only once the phase sits inside the
    new well's core (|theta - pi w| < pi/4), so barrier-top flicker is
    not counted as hopping. Returns (signed committed hops list,
    <cos theta>, <cos 2 theta>) (p22_locking.py:32 run_track;
    p23_protect.py:16 member and the p22 falsifier's em_avg are the
    same loop with delta = 0)."""
    rng = random.Random(seed)
    g = rng.gauss
    s = math.sin
    c = math.cos
    n = int(T / dt)
    amp = math.sqrt(2 * D * dt)
    th = 0.0
    well = 0
    hops = []
    c1 = c2 = 0.0
    for _ in range(n):
        th += (delta - eps * s(2 * th)) * dt + amp * g(0.0, 1.0)
        w = round(th / math.pi)
        if w != well and abs(th - math.pi * w) < math.pi / 4:
            hops.append(w - well)
            well = w
        c1 += c(th)
        c2 += c(2 * th)
    return hops, c1 / n, c2 / n


def ring_escape(N, D, T, seed, dt, K=1.0, check_dt=0.05):
    """Overdamped Langevin on a ring of N phases with E = K sum(1 -
    cos dphi), started in the uniform w = 1 twist; the escape-with-
    reset protocol (P-24a): the winding is checked every check_dt, a
    departure from w = 1 must persist for two consecutive checks to
    commit (Schmitt trigger on the winding), and the cell is reset to
    the uniform twist after each committed event. Returns (committed
    events, single-step events)
    (scripts/verify/p24_memory_hierarchy.py:91 escape_run;
    scripts/experiments/p24_memory.py:113 is the same protocol)."""
    rng = random.Random(seed)
    g = rng.gauss
    amp = math.sqrt(2 * D * dt)
    phi = [2 * math.pi * i / N for i in range(N)]
    events = singles = 0
    pending = None
    check = max(1, int(check_dt / dt))
    n = int(T / dt)
    for step in range(n):
        grad = [0.0] * N
        for i in range(N):
            dr = phi[(i + 1) % N] - phi[i]
            dl = phi[i] - phi[(i - 1) % N]
            grad[i] = K * (math.sin(dr) - math.sin(dl))
        for i in range(N):
            phi[i] += grad[i] * dt + amp * g(0.0, 1.0)
        if step % check == 0:
            tot = 0.0
            for i in range(N):
                d = phi[(i + 1) % N] - phi[i]
                tot += (d + math.pi) % (2 * math.pi) - math.pi
            w = round(tot / (2 * math.pi))
            if w != 1:
                if pending == w:
                    events += 1
                    if abs(w - 1) == 1:
                        singles += 1
                    phi = [2 * math.pi * i / N for i in range(N)]
                    pending = None
                else:
                    pending = w
            else:
                pending = None
    return events, singles


def diffuse_ensemble(M, D, T, dt, seed):
    """M untended phases dtheta = sqrt(2D) dW from theta = 0, one
    shared RNG, member loop inside the step loop (the rung-1 pattern,
    scripts/verify/p24_memory_hierarchy.py:129). Returns the list of
    final phases."""
    rng = random.Random(seed)
    th = [0.0] * M
    for _ in range(int(T / dt)):
        amp = math.sqrt(2 * D * dt)
        for i in range(M):
            th[i] += amp * rng.gauss(0.0, 1.0)
    return th


# ---------------------------------------------------------------- selftest
def _selftest():
    ok = True

    # anchor 1: deterministic beat outside the tongue (p22_derive EQ1)
    T = 1200.0
    v = (adler_em(0.1, 1.5, 1.0, 0.0, T, 1, 1, 0.002) - 0.1) / T
    tgt = math.sqrt(1.25)
    band = 1e-3 * tgt + 1.5 * 2 * math.pi / T
    good = abs(v - tgt) < band
    ok &= good
    print(f"beat at (1.5, 1.0): {v:.5f} vs sqrt(1.25) = {tgt:.5f} "
          f"{'ok' if good else 'FAIL'}")

    # ... and locking inside the tongue (p22_derive EQ4's D -> 0 limit)
    th_end = adler_em(0.1, 0.3, 0.5, 0.0, 400.0, 1, 3, 0.002)
    good = abs(th_end - 0.1) < 2 * math.pi
    ok &= good
    print(f"lock at (0.3, 0.5): drift {abs(th_end - 0.1):.3f} < 2 pi "
          f"{'ok' if good else 'FAIL'}")

    # anchor 2: two-photon bistability, pi apart (p22_derive EQ2)
    a_end = adler_em(0.2, 0.4, 1.0, 0.0, 60.0, 2, 2, 0.002)
    b_end = adler_em(0.2 + math.pi, 0.4, 1.0, 0.0, 60.0, 2, 2, 0.002)
    sep = (b_end - a_end) % (2 * math.pi)
    good = abs(sep - math.pi) < 0.05
    ok &= good
    print(f"two-photon separation: {sep:.5f} vs pi {'ok' if good else 'FAIL'}")

    # anchor 3: rung-1 decay on e^{-Dt} (p24_derive EQ1)
    D, M, t_end = 0.5, 800, 1.5
    th = diffuse_ensemble(M, D, t_end, 0.002, 99)
    C = sum(math.cos(x) for x in th) / M
    pred = math.exp(-D * t_end)
    band = 5 * math.sqrt(0.5 * (1 - math.exp(-2 * D * t_end)) / M)
    good = abs(C - pred) < band
    ok &= good
    print(f"rung-1 <cos theta>: {C:.4f} vs e^-Dt = {pred:.4f} "
          f"(band {band:.4f}) {'ok' if good else 'FAIL'}")

    # anchor 4: Schmitt trigger + Bessel equilibrium in brief
    # (p23_derive EQ1: <cos 2 theta> = I1/I0(eps/2D) = 0.63472 at
    # kappa = 5/3; a short run just checks sign and hop commitment)
    hops, c1, c2 = mod_pi_track(1.0, 0.3, 500.0, 500, 0.002)
    good = c2 > 0.4 and abs(c1) < 0.6 and len(hops) >= 1 and \
        all(abs(h) == 1 for h in hops)
    ok &= good
    print(f"mod-pi track: <cos2> = {c2:.3f}, <cos1> = {c1:+.3f}, "
          f"{len(hops)} committed hops, all size pi {'ok' if good else 'FAIL'}")

    # anchor 5: escape-with-reset determinism on the p24 falsifier's
    # fresh cell (N = 8, D = 0.20, seed 1234), short window
    ev, singles = ring_escape(8, 0.20, 60.0, 1234, 0.005)
    good = (ev, singles) == (4, 4)
    ok &= good
    print(f"ring escape (N=8, D=0.2, T=60, seed 1234): "
          f"{ev} events / {singles} single {'ok' if good else 'FAIL'}")

    print("sde selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
