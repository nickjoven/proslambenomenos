#!/usr/bin/env python3
"""P-47 derive layer: classical Kibble-Zurek on the free pi ring with
exact half-sector counting. Everything a registered clause depends
on is measured here first and written to p47_derive.json.

THE MODEL. The P-35/P-36 ring (N inertial phase oscillators, sine
bonds J = 1, one pi bond A_0 = pi on the twisted ring) with a
Langevin bath: v' = v + dt (sin D_j - sin D_{j-1} - gamma v)
+ sqrt(2 gamma T dt) xi, theta' = theta + dt v' (Euler-Cromer with
Maruyama noise, the P-36 update order). No load. Protocol: burn-in
at T_i, linear ramp T -> 0 over tau_Q, short settle at T = 0, read
the covariant winding W = sum_j wrap(D_j) / 2 pi.

THE COUNT IS EXACT (species-two zero). sum_j D_j = -sum_j A_j
identically on a ring, so sum_j wrap(D_j) = -sum A - 2 pi (number
of wraps): W sits on the integer lattice (control) or the
half-integer lattice (twisted) at EVERY state, thermal or not, no
threshold, no smear (L-1 does not apply because there is no
detector - the count is arithmetic). A defect count that is exact
by construction is what A-26 asked for.

THE SHARED DENSITY (exact at equilibrium). At temperature T the
bonds carry the weight exp(cos D / T) each, identical for the pi
bond because the energy 1 - cos D depends on the covariant strain
only. With S = sum_j wrap(D_j), the ring's closure selects
S = 2 pi n (control) or S = 2 pi (n - 1/2) (twisted) from ONE
density rho_N(S), the N-fold convolution of the single-bond wrapped
density - so P_c(W = n) ~ rho_N(2 pi n) and P_tw(W = n - 1/2)
~ rho_N(2 pi (n - 1/2)). The twist shifts the lattice and touches
nothing else. Two exact consequences: the moments (E_c, E_tw) =
(<W^2>_control, <W^2>_twisted) lie on a one-parameter curve
traced by T, and the fast-quench limit (read at T_i) has
E = N <u^2>_{T_i} / 4 pi^2 for both rings up to the O(e^{-N/xi})
closure correction. The slow limit is E_c -> 0, E_tw -> 1/4: the
half quantum the twisted ring cannot shed (W^2 >= 1/4 at every
sample, exactly).

THE QUENCH. The registered prediction is the shared-density
relation applied to the FROZEN distributions: both rings quenched
at the same tau_Q freeze at the same effective temperature (the
twist is invisible to the local physics that sets the freeze), so
the twisted E_tw is predicted from the control E_c through the
curve, with no free parameter. How E_c itself falls with tau_Q is
NOT derived here: the winding changes only by a bond wrapping
through pi, an activated event (barrier 2 J), so the freeze is set
by the phase-slip rate, not by the spin-wave correlation length
the textbook KZ argument uses; a power-law exponent would be a
guessed band (L-3). The ladder's local exponents are measured and
reported; the registered scaling clause is ordering only.

ANCHOR (L-9): before any quench, equilibrium sampling at fixed T
must reproduce rho_N's lattice moments for both rings.

Run: python3 scripts/experiments/p47_derive.py
"""
import json
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p35_ring import ground_state, winding  # noqa: E402

TAU = 2 * math.pi
EPS = 2.0 ** -52


# ---------- the shared density, by quadrature (stdlib) ----------

def bond_moments(T, n=1200):
    """<u^2> and the characteristic function phi(k) of the wrapped
    single-bond density ~ exp(cos u / T) on (-pi, pi]."""
    h = TAU / n
    Z = 0.0
    m2 = 0.0
    for i in range(n):
        u = -math.pi + (i + 0.5) * h
        w = math.exp((math.cos(u) - 1.0) / T)
        Z += w
        m2 += w * u * u
    return m2 / Z


def phi_bond(k, T, n=1200):
    h = TAU / n
    Z = 0.0
    c = 0.0
    for i in range(n):
        u = -math.pi + (i + 0.5) * h
        w = math.exp((math.cos(u) - 1.0) / T)
        Z += w
        c += w * math.cos(k * u)
    return c / Z


def rho_N(S_values, N, T, kmax=None, nk=600):
    """rho_N(S) = (1/pi) int_0^inf phi(k)^N cos(k S) dk, Simpson."""
    if kmax is None:
        # phi(k)^N decays like exp(-N <u^2> k^2 / 2) for small k
        m2 = bond_moments(T)
        kmax = 12.0 / math.sqrt(max(N * m2, 1e-9))
        kmax = min(kmax, 40.0)
    h = kmax / nk
    phis = [phi_bond(i * h, T) ** N for i in range(nk + 1)]
    out = []
    for S in S_values:
        acc = 0.0
        for i in range(nk + 1):
            wgt = 1 if i in (0, nk) else (4 if i % 2 else 2)
            acc += wgt * phis[i] * math.cos(i * h * S)
        out.append(acc * h / 3.0 / math.pi)
    return out


def lattice_moments(N, T, nmax=None):
    """(E_c, E_tw, P_c, P_tw): second moments and distributions of W
    on the integer / half-integer lattices from rho_N at T."""
    if nmax is None:
        m2 = bond_moments(T)
        nmax = int(6 * math.sqrt(N * m2) / TAU) + 2
    Wc = [n for n in range(-nmax, nmax + 1)]
    Wt = [n - 0.5 for n in range(-nmax + 1, nmax + 1)]
    rc = rho_N([TAU * w for w in Wc], N, T)
    rt = rho_N([TAU * w for w in Wt], N, T)
    Zc, Zt = sum(rc), sum(rt)
    Pc = {w: r / Zc for w, r in zip(Wc, rc)}
    Pt = {w: r / Zt for w, r in zip(Wt, rt)}
    Ec = sum(w * w * p for w, p in Pc.items())
    Et = sum(w * w * p for w, p in Pt.items())
    return Ec, Et, Pc, Pt


def curve(N, Ts):
    return [(T,) + lattice_moments(N, T)[:2] for T in Ts]


def predict_tw_from_c(N, Ec_measured, Ts_curve):
    """Invert the control moment on the curve (monotone in T) by
    bisection and return the predicted twisted moment."""
    lo, hi = Ts_curve[0], Ts_curve[-1]
    for _ in range(22):
        mid = 0.5 * (lo + hi)
        Ec, Et, _, _ = lattice_moments(N, mid)
        if Ec < Ec_measured:
            lo = mid
        else:
            hi = mid
    T = 0.5 * (lo + hi)
    return T, lattice_moments(N, T)[1]


# ---------- the Langevin ring ----------

def quench_sample(N, twisted, gamma, T_i, tau_Q, dt, rng, t_burn=20.0,
                  t_settle=20.0, record_ramp_end=True):
    """One realization. Returns (W_final, W_ramp_end, lattice_off)."""
    A, th = ground_state(N, twisted, 0)
    # random phases + Maxwellian velocities at T_i
    th = [rng.uniform(-math.pi, math.pi) for _ in range(N)]
    v = [rng.gauss(0.0, math.sqrt(T_i)) for _ in range(N)]
    n_burn = int(round(t_burn / dt))
    n_ramp = int(round(tau_Q / dt))
    n_settle = int(round(t_settle / dt))
    sinD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
    W_ramp = None
    for s in range(n_burn + n_ramp + n_settle):
        if s < n_burn:
            T = T_i
        elif s < n_burn + n_ramp:
            T = T_i * (1.0 - (s - n_burn + 1) / n_ramp)
        else:
            T = 0.0
        sig = math.sqrt(2.0 * gamma * T * dt) if T > 0 else 0.0
        for j in range(N):
            a = sinD[j] - sinD[j - 1] - gamma * v[j]
            v[j] += dt * a + (sig * rng.gauss(0.0, 1.0) if sig else 0.0)
        for j in range(N):
            th[j] += dt * v[j]
        sinD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
        if s == n_burn + n_ramp - 1:
            W_ramp = winding(th, A, N)
    W = winding(th, A, N)
    off = abs(W - (round(W - 0.5) + 0.5)) if twisted else abs(W - round(W))
    return W, W_ramp, off


def equilibrium_samples(N, twisted, gamma, T, dt, rng, t_therm=60.0,
                        t_gap=10.0, M=100):
    """Anchor: thermalize at T, then read W every t_gap."""
    A, th = ground_state(N, twisted, 0)
    th = [rng.uniform(-math.pi, math.pi) for _ in range(N)]
    v = [rng.gauss(0.0, math.sqrt(T)) for _ in range(N)]
    sinD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
    sig = math.sqrt(2.0 * gamma * T * dt)
    n_therm = int(round(t_therm / dt))
    n_gap = int(round(t_gap / dt))
    Ws = []
    s = 0
    while len(Ws) < M:
        for j in range(N):
            a = sinD[j] - sinD[j - 1] - gamma * v[j]
            v[j] += dt * a + sig * rng.gauss(0.0, 1.0)
        for j in range(N):
            th[j] += dt * v[j]
        sinD = [math.sin(th[(j + 1) % N] - th[j] - A[j]) for j in range(N)]
        s += 1
        if s >= n_therm and (s - n_therm) % n_gap == 0:
            Ws.append(winding(th, A, N))
    return Ws


def stats(Ws):
    M = len(Ws)
    m2 = sum(w * w for w in Ws) / M
    m4 = sum(w ** 4 for w in Ws) / M
    se = math.sqrt(max(m4 - m2 * m2, 0.0) / M)
    hist = {}
    for w in Ws:
        key = round(w * 2) / 2
        hist[key] = hist.get(key, 0) + 1
    p0 = sum(1 for w in Ws if abs(w) < 0.75) / M   # W = 0 or W = +-1/2
    return {"M": M, "E": m2, "SE": se, "p_inner": p0,
            "hist": {str(k): v for k, v in sorted(hist.items())}}


def model_se(P, M):
    """SE of the sample mean of W^2 under the predicted lattice
    distribution P (used where the sample variance is degenerate,
    e.g. every twisted sample at +-1/2)."""
    e2 = sum(w * w * p for w, p in P.items())
    e4 = sum(w ** 4 * p for w, p in P.items())
    return math.sqrt(max(e4 - e2 * e2, 0.0) / M)


def inner_prob(P):
    return sum(p for w, p in P.items() if abs(w) < 0.75)


def main():
    t0 = time.time()
    out = {}
    N = 32
    gamma = 1.0
    T_i = 2.0
    dt = 0.05
    # the curve for N = 32 and N = 64
    Ts = [2.0, 1.5, 1.0, 0.7, 0.5, 0.35, 0.25, 0.18, 0.12, 0.08, 0.05, 0.03]
    for n in (32, 64):
        cv = curve(n, Ts)
        out["curve_N%d" % n] = [{"T": T, "E_c": Ec, "E_tw": Et} for T, Ec, Et in cv]
        u2 = bond_moments(T_i)
        out["fast_null_N%d" % n] = {"T_i": T_i, "u2": u2, "E_iid": n * u2 / TAU ** 2,
                                    "E_c_curve": cv[0][1], "E_tw_curve": cv[0][2]}
        print("N %d: fast null iid %.4f, curve at T_i: E_c %.4f E_tw %.4f; slow end T=%.2f: E_c %.4f E_tw %.4f"
              % (n, n * u2 / TAU ** 2, cv[0][1], cv[0][2], Ts[-1], cv[-1][1], cv[-1][2]), flush=True)

    # anchor: equilibrium sampling at T = 0.5 and 0.25, both rings
    rng = random.Random(20260902)
    anc = {}
    # the gap between samples must exceed the slip time: at T = 0.5
    # the ring slips ~0.6 times per unit, at 0.35 ~0.1 (activated,
    # barrier 2 J), so gaps of 20 and 60 units decorrelate W; below
    # T ~ 0.3 equilibrium sampling by dynamics is out of reach on any
    # affordable window - which is the freeze physics itself
    for T, gap in ((0.5, 20.0), (0.35, 60.0)):
        Ec, Et, Pc, Pt = lattice_moments(N, T)
        rec = {"T": T, "gap": gap, "E_c_pred": Ec, "E_tw_pred": Et,
               "p_inner_pred": {"control": inner_prob(Pc), "twisted": inner_prob(Pt)}}
        for tw in (False, True):
            Ws = equilibrium_samples(N, tw, gamma, T, dt, rng, t_gap=gap, M=120)
            st = stats(Ws)
            key = "twisted" if tw else "control"
            pred = Et if tw else Ec
            rec[key] = st
            rec[key]["pred"] = pred
            rec[key]["SE_model"] = model_se(Pt if tw else Pc, st["M"])
            rec[key]["z"] = (st["E"] - pred) / rec[key]["SE_model"]
            print("anchor T %.2f %s: E %.4f (model SE %.4f) vs pred %.4f (z %.2f); p_inner %.3f vs %.3f; hist %s"
                  % (T, key, st["E"], rec[key]["SE_model"], pred, rec[key]["z"],
                     st["p_inner"], rec["p_inner_pred"][key], st["hist"]), flush=True)
        anc[str(T)] = rec
    out["anchor"] = anc

    # the quench ladder at N = 32
    ladder = [0.0, 5.0, 20.0, 80.0, 320.0]
    M = 60
    lad = {}
    for tau in ladder:
        rec = {"tau_Q": tau}
        t1 = time.time()
        for tw in (False, True):
            Ws, Wr, offs = [], [], []
            for m in range(M):
                W, W_ramp, off = quench_sample(N, tw, gamma, T_i, tau, dt, rng)
                Ws.append(W)
                Wr.append(W_ramp if W_ramp is not None else W)
                offs.append(off)
            st = stats(Ws)
            st["E_ramp_end"] = stats(Wr)["E"]
            st["changed_in_settle"] = sum(1 for a, b in zip(Ws, Wr) if abs(a - b) > 0.25)
            st["worst_lattice_off"] = max(offs)
            rec["twisted" if tw else "control"] = st
        Ec = rec["control"]["E"]
        Teff, Et_pred = predict_tw_from_c(N, Ec, Ts[::-1])
        _, _, Pc_eff, Pt_eff = lattice_moments(N, Teff)
        rec["T_eff_from_control"] = Teff
        rec["E_tw_pred_from_control"] = Et_pred
        rec["p_inner_tw_pred"] = inner_prob(Pt_eff)
        # band: the twisted model SE combined with the control SE
        # propagated through the curve (finite difference)
        Ec_up = Ec + rec["control"]["SE"]
        _, Et_up = predict_tw_from_c(N, Ec_up, Ts[::-1])
        rec["SE_tw_combined"] = math.sqrt(model_se(Pt_eff, M) ** 2 + (Et_up - Et_pred) ** 2)
        rec["z_tw"] = (rec["twisted"]["E"] - Et_pred) / rec["SE_tw_combined"]
        rec["seconds"] = time.time() - t1
        print("tau_Q %g: control E %.3f+-%.3f twisted E %.3f+-%.3f; T_eff %.3f pred_tw %.3f (z %.2f); "
              "lattice off %.1e/%.1e; settle changes %d/%d (%.0f s)"
              % (tau, Ec, rec["control"]["SE"], rec["twisted"]["E"], rec["twisted"]["SE"],
                 Teff, Et_pred, rec["z_tw"], rec["control"]["worst_lattice_off"],
                 rec["twisted"]["worst_lattice_off"], rec["control"]["changed_in_settle"],
                 rec["twisted"]["changed_in_settle"], rec["seconds"]), flush=True)
        lad[str(tau)] = rec
    out["ladder_N32"] = lad
    # local exponents
    keys = [k for k in ladder if k > 0]
    ex = []
    for a, b in zip(keys, keys[1:]):
        Ea, Eb = lad[str(a)]["control"]["E"], lad[str(b)]["control"]["E"]
        ex.append({"from": a, "to": b, "exponent": -math.log(Eb / Ea) / math.log(b / a)})
    out["local_exponents_control"] = ex
    print("local exponents", [(e["from"], e["to"], round(e["exponent"], 3)) for e in ex])

    # dt validation at one rung: dt and dt/4, 120 realizations each
    # (a first M = 60 dt/2 cell read 1.03 vs 0.45 and sent the layer
    # after a discretization effect; the powered cell shows none)
    t1 = time.time()
    dtv = {}
    for d in (dt, dt / 4):
        r2 = random.Random(11)
        Ws = [quench_sample(N, False, gamma, T_i, 20.0, d, r2)[0] for _ in range(120)]
        dtv[str(d)] = stats(Ws)
    a, b = dtv[str(dt)], dtv[str(dt / 4)]
    dtv["z"] = (a["E"] - b["E"]) / math.sqrt(a["SE"] ** 2 + b["SE"] ** 2)
    out["dt_check_tau20_control"] = dtv
    print("dt check at tau_Q 20 control: dt %.4f E %.3f +- %.3f vs dt %.4f E %.3f +- %.3f (z %.2f) (%.0f s)"
          % (dt, a["E"], a["SE"], dt / 4, b["E"], b["SE"], dtv["z"], time.time() - t1))
    out["seconds"] = time.time() - t0
    with open(os.path.join(HERE, "p47_derive.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote p47_derive.json in %.0f s" % out["seconds"])


if __name__ == "__main__":
    main()
