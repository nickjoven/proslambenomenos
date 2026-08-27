#!/usr/bin/env python3
"""Verification for the P-24 claim memory-hierarchy-of-substrates, by
independent live reimplementation: its own closed-form barrier, its
own Hessians and Jacobi eigensolver for the Langer prefactor, its own
Langevin integrator on a FRESH cell (N = 8, D = 0.20) the experiment
never ran, and a fresh rung-1 ensemble - nothing read from results
files.

Checks: (1) rung 1: ensemble <cos theta> at t = 1.5, D = 0.5 inside
its CLT band around e^{-Dt}; (2) the closed-form saddle identity
dE/dDelta = 0 at Delta* = pi(N-3)/(N-2); (3) rung 3 escape rate at
the fresh cell inside 2/sqrt(N_ev) + 0.7 nat of this file's own
Langer rate, with single-step purity >= 0.95; (4) the barrier
saturation: Delta_E(64) < 2K.

--mutant extensive-protection  asserts Delta_E scales extensively,
    Delta_E(64)/Delta_E(8) >= 8; the closed form gives about 4.2 and
    saturates, so FAIL.
--mutant barrier-free          asserts the escape rate is
    D-independent (|Delta ln rate| < 0.2 between D = 0.2 and 0.3);
    the derived difference is about 0.77 nat, so FAIL.
"""
import math
import random
import sys

MUTANT = None
if "--mutant" in sys.argv:
    i = sys.argv.index("--mutant")
    MUTANT = sys.argv[i + 1] if i + 1 < len(sys.argv) else "?"
KNOWN = {"extensive-protection", "barrier-free"}
if MUTANT is not None and MUTANT not in KNOWN:
    print(f"usage error: unknown mutant {MUTANT!r}; known: {sorted(KNOWN)}")
    sys.exit(2)

K = 1.0


def E_delta(Delta, N):
    return K * (1 - math.cos(Delta)) + K * (N - 1) * (1 - math.cos((2 * math.pi - Delta) / (N - 1)))


def barrier(N):
    ds = math.pi * (N - 3) / (N - 2)
    return E_delta(ds, N) - N * K * (1 - math.cos(2 * math.pi / N))


def jacobi(A, sweeps=400):
    n = len(A)
    a = [r[:] for r in A]
    for _ in range(sweeps):
        off = max((abs(a[i][j]), i, j) for i in range(n) for j in range(i + 1, n))
        if off[0] < 1e-12:
            break
        _, p, q = off
        th = math.pi / 4 if a[p][p] == a[q][q] else \
            0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
        c, s = math.cos(th), math.sin(th)
        for k in range(n):
            apk, aqk = a[p][k], a[q][k]
            a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
        for k in range(n):
            akp, akq = a[k][p], a[k][q]
            a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
    return sorted(a[i][i] for i in range(n))


def hessian(bonds):
    n = len(bonds)
    c = [K * math.cos(b) for b in bonds]
    H = [[0.0] * n for _ in range(n)]
    for j in range(n):
        i, ip = j, (j + 1) % n
        H[i][i] += c[j]
        H[ip][ip] += c[j]
        H[i][ip] -= c[j]
        H[ip][i] -= c[j]
    return H


def langer_rate(N, D):
    ds = math.pi * (N - 3) / (N - 2)
    lmin = jacobi(hessian([2 * math.pi / N] * N))
    lsad = jacobi(hessian([ds] + [(2 * math.pi - ds) / (N - 1)] * (N - 1)))
    lam_u = -[x for x in lsad if x < -1e-9][0]
    logdet = sum(math.log(x) for x in lmin if abs(x) > 1e-9) \
        - sum(math.log(x) for x in lsad if x > 1e-9) - math.log(lam_u)
    return N * (lam_u / (2 * math.pi)) * math.exp(0.5 * logdet) * math.exp(-barrier(N) / D)


def escape_run(N, D, T, seed, dt=0.005):
    rng = random.Random(seed)
    g = rng.gauss
    amp = math.sqrt(2 * D * dt)
    phi = [2 * math.pi * i / N for i in range(N)]
    events = singles = 0
    pending = None
    check = max(1, int(0.05 / dt))
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


def main():
    # (1) rung 1 fresh ensemble
    D, M, t_end, dt = 0.5, 800, 1.5, 0.002
    rng = random.Random(99)
    th = [0.0] * M
    for _ in range(int(t_end / dt)):
        amp = math.sqrt(2 * D * dt)
        for i in range(M):
            th[i] += amp * rng.gauss(0.0, 1.0)
    C = sum(math.cos(x) for x in th) / M
    pred = math.exp(-D * t_end)
    band = 5 * math.sqrt(0.5 * (1 - math.exp(-2 * D * t_end)) / M)
    if abs(C - pred) > band:
        print(f"FAIL: rung-1 memory {C:.4f} off e^-Dt = {pred:.4f} beyond {band:.4f}")
        return 1

    # (2) saddle stationarity of the closed form
    for N in (8, 16):
        ds = math.pi * (N - 3) / (N - 2)
        h = 1e-6
        dE = (E_delta(ds + h, N) - E_delta(ds - h, N)) / (2 * h)
        if abs(dE) > 1e-6:
            print(f"FAIL: dE/dDelta at Delta*(N={N}) is {dE:.2e}, not zero")
            return 1

    # (4) saturation / extensive-protection mutant
    if MUTANT == "extensive-protection":
        if barrier(64) / barrier(8) < 8:
            print(f"FAIL: Delta_E(64)/Delta_E(8) = {barrier(64) / barrier(8):.2f} - "
                  "the barrier saturates at 2K; there is no extensive protection")
            return 1
    elif not (barrier(64) < 2 * K):
        print(f"FAIL: Delta_E(64) = {barrier(64):.3f} not below 2K")
        return 1

    # (3) fresh-cell escape rate vs own Langer rate
    N, Dv, T = 8, 0.20, 900.0
    ev, singles = escape_run(N, Dv, T, seed=1234)
    r_meas = ev / T
    r_lang = langer_rate(N, Dv)
    nat = abs(math.log(max(r_meas, 1e-12)) - math.log(r_lang))
    band = 2 / math.sqrt(max(ev, 1)) + 0.7
    if MUTANT == "barrier-free":
        ev2, _ = escape_run(N, 0.30, 300.0, seed=1235)
        dln = abs(math.log(max(ev2 / 300.0, 1e-12)) - math.log(max(r_meas, 1e-12)))
        if dln > 0.2:
            print(f"FAIL: escape rate moves {dln:.2f} nat between D = 0.2 and 0.3 - "
                  "the barrier is real (derived 0.77 nat)")
            return 1
    if nat > band or singles / max(ev, 1) < 0.95:
        print(f"FAIL: fresh cell rate {r_meas:.4f} vs Langer {r_lang:.4f} "
              f"({nat:.2f} nat, band {band:.2f}); purity {singles / max(ev, 1):.2f}")
        return 1

    if MUTANT:
        print(f"FAIL: mutant {MUTANT} did not break the verification")
        return 1
    print(f"PASS: live rung-1 decay on its CAS curve; saddle stationary; fresh "
          f"cell (N=8, D=0.2) escapes at {r_meas:.4f} beside its own Langer "
          f"rate {r_lang:.4f} with {ev} single-step slips; barrier saturates "
          "below 2K - substrates forget exactly as derived")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # falsifier contract: FAIL line, no traceback
        print(f"FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
