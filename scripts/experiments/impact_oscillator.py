#!/usr/bin/env python3
"""The impact oscillator under the lens (Shaw & Holmes 1983):
    x'' + 2 zeta x' + x = cos(omega t)  for x < sigma;  at x = sigma: x' -> -r x'.
Flight between impacts is the exact damped-forced solution; impacts
are located by coarse stepping on the analytic flight plus bisection.
Demonstrations (all written to impact_results.json):
 A. bifurcation diagram: steady-state impact velocities vs clearance
    sigma at fixed omega, r - the (1,1) orbit, period doubling to
    (1,2), period adding.
 B. grazing: the maximal impact velocity near the grazing clearance
    sigma_g = A (linear-response amplitude) scales as sqrt(sigma_g -
    sigma) (Nordmark 1991).
 C. (m, n) census on an (omega, sigma) grid: impacts per forcing
    period in steady state, labelled as a reduced fraction - the
    count that survives where the anchors move.
 D. complete chatter: at low r an impact sequence accumulates with
    geometrically shrinking gaps (ratio -> r), infinitely many impacts
    in finite time (Budd & Dux 1994).
 E. Volterra strain on a glued ring: N linear springs glued with phase
    Phi relax to uniform strain Phi/N with energy N(1 - cos(Phi/N)) ->
    Phi^2/(2N).
"""
import json
import math
from fractions import Fraction
from multiprocessing import Pool

ZETA = 0.05


def flight(x0, v0, t0, omega, zeta=ZETA):
    """Exact solution x(t), v(t) for t >= t0 with x(t0)=x0, v(t0)=v0."""
    wd = math.sqrt(1 - zeta * zeta)
    X = 1 / math.sqrt((1 - omega ** 2) ** 2 + (2 * zeta * omega) ** 2)
    phi = math.atan2(2 * zeta * omega, 1 - omega ** 2)
    xp0 = X * math.cos(omega * t0 - phi); vp0 = -X * omega * math.sin(omega * t0 - phi)
    C1 = x0 - xp0
    C2 = (v0 - vp0 + zeta * C1) / wd
    def x(t):
        s = t - t0
        e = math.exp(-zeta * s)
        return e * (C1 * math.cos(wd * s) + C2 * math.sin(wd * s)) + X * math.cos(omega * t - phi)
    def v(t):
        s = t - t0
        e = math.exp(-zeta * s)
        h = e * ((-zeta * C1 + wd * C2) * math.cos(wd * s) + (-zeta * C2 - wd * C1) * math.sin(wd * s))
        return h - X * omega * math.sin(omega * t - phi)
    return x, v


def next_impact(x0, v0, t0, omega, sigma, tmax, h=0.02):
    x, v = flight(x0, v0, t0, omega)
    t = t0 + 1e-9
    if x(t) >= sigma:        # leaving the wall: step until clear
        while x(t) >= sigma and t < t0 + 5 * h:
            t += h / 10
    while t < tmax:
        t2 = t + h
        if x(t2) >= sigma:
            a, b = t, t2
            for _ in range(50):
                m = (a + b) / 2
                if x(m) >= sigma: b = m
                else: a = m
            return b, v(b)
        t = t2
    return None, None


def run(omega, sigma, r, n_periods=200, skip=120, x0=0.0, v0=0.0):
    T = 2 * math.pi / omega
    t, x, v = 0.0, x0, v0
    impacts = []
    tmax = n_periods * T
    while True:
        ti, vi = next_impact(x, v, t, omega, sigma, tmax)
        if ti is None:
            break
        impacts.append((ti, vi))
        t, x, v = ti, sigma, -r * vi
        if len(impacts) > 4000:
            break
    return [(ti, vi) for ti, vi in impacts if ti >= skip * T], impacts


def mn_label(impacts, omega, sigma):
    """(m impacts, n periods) in steady state from the impact-time pattern."""
    T = 2 * math.pi / omega
    if len(impacts) < 4:
        return "0/1"
    phases = [round((ti / T) % 1.0, 3) for ti, _ in impacts]
    # find the smallest n such that the phase sequence is n-periodic-ish in count
    ts = [ti for ti, _ in impacts]
    span = ts[-1] - ts[0]
    m_per_period = (len(ts) - 1) / (span / T) if span > 0 else 0
    return str(Fraction(m_per_period).limit_denominator(8))


def job_bif(args):
    omega, r, sigma = args
    ss, _ = run(omega, sigma, r)
    return {"sigma": sigma, "v": [abs(vi) for _, vi in ss][-40:], "label": mn_label(ss, omega, sigma)}


def job_grid(args):
    omega, sigma, r = args
    ss, _ = run(omega, sigma, r, n_periods=120, skip=80)
    return {"omega": omega, "sigma": sigma, "label": mn_label(ss, omega, sigma)}


if __name__ == "__main__":
    out = {}
    omega, r = 2.8, 0.8
    A = 1 / math.sqrt((1 - omega ** 2) ** 2 + (2 * ZETA * omega) ** 2)
    out["A"] = A
    # A. bifurcation in sigma
    sigmas = [A * (1 - 0.9 * k / 160) for k in range(161)]   # from grazing downward
    with Pool(14) as p:
        bif = p.map(job_bif, [(omega, r, s) for s in sigmas], chunksize=4)
    out["bifurcation"] = bif
    # B. grazing: the square-root singularity of the impact map. Start on
    # the non-impacting periodic orbit (amplitude A) and lower the wall to
    # A - d: the FIRST impact velocity is v = A omega sin(theta) with
    # cos(theta) = 1 - d/A, i.e. v^2 = 2 A omega^2 d to leading order -
    # infinite slope dv/dd at d = 0. Measured by the exact flight.
    graz = []
    phi = math.atan2(2 * ZETA * omega, 1 - omega ** 2)
    for d in (0.0005, 0.001, 0.002, 0.004, 0.008, 0.016, 0.032):
        t0 = (phi + math.pi) / omega          # start at the trough of x_ss
        x0, v0 = -A, 0.0
        ti, vi = next_impact(x0, v0, t0, omega, A - d, t0 + 2 * math.pi / omega, h=0.005)
        graz.append({"d": d, "v_first": abs(vi) if vi is not None else None, "v2_over_d": (vi * vi / d) if vi is not None else None,
                     "theory_2Aw2": 2 * A * omega ** 2})
    out["grazing"] = graz
    # C. (m,n) census
    grid = [(w, s, r) for w in [1.5 + 0.1 * i for i in range(26)] for s in [0.05 + 0.05 * j for j in range(16)]]
    with Pool(14) as p:
        cen = p.map(job_grid, grid, chunksize=8)
    out["census"] = cen
    # D. complete chatter: slow forcing (omega = 0.5) presses the mass into
    # the wall for part of each cycle; with r = 0.5 the impacts accumulate
    # with gap ratio -> r (geometric), infinitely many in finite time.
    ss, allimp = run(0.5, 0.3, 0.5, n_periods=3, skip=0)
    gaps = [b - a for (a, _), (b, _) in zip(allimp, allimp[1:])]
    out["chatter"] = {"times": [t for t, _ in allimp[:80]], "gaps": gaps[:79], "r": 0.5}
    # E. Volterra strain
    volt = [{"N": N, "strain": math.pi / N, "energy": N * (1 - math.cos(math.pi / N)), "asymptote": math.pi ** 2 / (2 * N)} for N in (4, 8, 16, 32, 64, 128)]
    out["volterra"] = volt
    json.dump(out, open("scripts/experiments/impact_results.json", "w"))
    labels = {}
    for b in bif: labels.setdefault(b["label"], 0); labels[b["label"]] += 1
    print("A. bifurcation labels along sigma:", labels)
    print("B. grazing: " + ", ".join(f"d={g['d']}: v={g['v_first']:.4f} v^2/d={g['v2_over_d']:.2f}" for g in graz if g['v_first']) + f"  (2 A w^2 = {2*A*omega**2:.2f})")
    cl = {}
    for c in cen: cl[c["label"]] = cl.get(c["label"], 0) + 1
    print("C. census labels:", dict(sorted(cl.items(), key=lambda kv: -kv[1])[:8]))
    g = out["chatter"]["gaps"]
    small = [(i, x) for i, x in enumerate(g) if x < 0.5]
    print("D. chatter: impacts", len(allimp), "; gap ratios in the accumulating run:",
          [round(g[i + 1] / g[i], 3) for i, _ in small[:10] if i + 1 < len(g)])
    print("E. Volterra:", [(v["N"], round(v["energy"], 4), round(v["asymptote"], 4)) for v in volt])
