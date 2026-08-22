#!/usr/bin/env python3
"""Refutation of einstein-from-kuramoto-chain-a (harmonics Proof Chain
A: Einstein's equations follow uniquely from Kuramoto dynamics via the
Kuramoto -> ADM dictionary at K = 1 and Lovelock's theorem). Three
independent checks, each a computation, each sufficient alone:

1. GRADIENT FLOW, NOT HAMILTONIAN. With symmetric coupling and fixed
   frequencies Kuramoto is theta' = -dV/dtheta with V = -sum omega_i
   theta_i - K sum cos(theta_j - theta_i): V is a Lyapunov function and
   the linearisation about any locked state is self-adjoint with real
   spectrum, so no reversible (Hamiltonian) evolution of the ADM type
   is a coarse-graining of it. The computed signature: a small
   perturbation of a locked lattice spreads diffusively, width ~
   t^(1/2); the inertial mutant (a genuinely second-order chain)
   gives ~1. Necessary-condition check only (nonlinear gradient flows
   can move fronts ballistically); the Lyapunov argument is the proof.

2. THE DICTIONARY'S LAPSE IS CONSTANT BY DEFINITION. adm_dictionary.md
   line 153: "a clock at x ticks at rate r, and its phase is psi"; but
   in a locked state every oscillator has the same frequency (that is
   what locked means), so the clock rate is uniform whatever r(x)
   does - and PROOF_A P7 sets r = 1 outright. Checked on a locked ring
   with HETEROGENEOUS natural frequencies, so that the local coherence
   genuinely varies (recorded), while max |theta_i' - Omega| -> 0.

3. THE DICTIONARY'S METRIC IS A GRAPH METRIC. adm_dictionary.md line
   64 defines gamma_ij = delta_ij - d_i theta d_j theta (positivity
   needs |grad theta| < 1, lines 41-49; the bracket average is over a
   single smooth field, so the tensor is rank-one as the source argues
   it). That is the induced metric of the SPACELIKE graph z = theta(x)
   in Minkowski R^(n,1); its curvature obeys the corresponding Gauss
   equation (in 2D: K = -det(Hess theta)/(1-|grad theta|^2)^2). Checked
   against the Brioschi formula on random theta with |grad theta| < 1.
   Codimension-one flat (pseudo-Euclidean) embeddings are a thin
   subfamily: one free function against three for a general 3-metric
   modulo diffeomorphisms (Janet-Cartan), so the chain's gamma cannot
   be the spatial metric of arbitrary matter, and Lovelock's
   uniqueness presupposes a general metric. Of record: the first
   version of this script used delta + grad grad (the wrong sign) -
   found by a context-free audit 2026-08-22.

Also of record, not computed: P8 invokes Lovelock (1971) with "general
covariance" supplied by "SL(2,R) acts transitively"; Diff(M) is
infinite-dimensional and SL(2,R) is three-dimensional - the hypothesis
is not met. Exit 0 iff checks 1-3 confirm the refutation."""

import cmath
import math
import random
import sys

MUTANT = sys.argv[sys.argv.index("--mutant") + 1] if "--mutant" in sys.argv else None


def spreading_exponent(inertial):
    N, K, dt = 401, 1.0, 0.02
    th = [0.0] * N
    w = [0.0] * N
    th[N // 2] = 1e-3
    widths = []
    times = []
    for k in range(1, 4001):
        F = [K * (math.sin(th[(i + 1) % N] - th[i]) + math.sin(th[i - 1] - th[i])) for i in range(N)]
        if inertial:
            for i in range(N):
                w[i] += F[i] * dt
                th[i] += w[i] * dt
        else:
            for i in range(N):
                th[i] += F[i] * dt
        if k % 800 == 0:
            m0 = sum(abs(v) for v in th)
            m2 = sum(abs(v) * (i - N // 2) ** 2 for i, v in enumerate(th))
            widths.append(math.sqrt(m2 / m0))
            times.append(k * dt)
    # log-log slope between first and last sample
    return math.log(widths[-1] / widths[0]) / math.log(times[-1] / times[0])


def locked_clock_rates():
    # locked ring with HETEROGENEOUS natural frequencies (zero mean about
    # Omega) and strong coupling: the locked state is not in-phase, so the
    # local coherence r_i = |mean of e^{i theta} over i-1, i, i+1| varies
    # with position - and yet every theta_i' -> Omega.
    N, Om, K, dt = 64, 0.3, 3.0, 0.01
    random.seed(2)
    om = [random.uniform(-0.5, 0.5) for _ in range(N)]
    m = sum(om) / N
    om = [Om + (o - m) for o in om]
    th = [0.0] * N
    spread = []
    for k in range(1, 100001):
        F = [om[i] + K * (math.sin(th[(i + 1) % N] - th[i]) + math.sin(th[i - 1] - th[i])) for i in range(N)]
        for i in range(N):
            th[i] += F[i] * dt
        if k in (50000, 100000):
            spread.append(max(abs(f - Om) for f in F))
    r = []
    for i in range(N):
        z = sum(cmath.exp(1j * th[j % N]) for j in (i - 1, i, i + 1)) / 3
        r.append(abs(z))
    return spread[0], spread[1], min(r), max(r)


def gauss_check():
    random.seed(3)
    worst = 0.0
    for _ in range(5):
        a = [random.uniform(-0.3, 0.3) for _ in range(6)]   # keep |grad theta| < 1
        th = lambda x, y: a[0] * x * x + a[1] * x * y + a[2] * y * y + a[3] * x ** 3 + a[4] * y ** 3 + a[5] * x * y * y
        h = 1e-3
        x0, y0 = random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)
        d = lambda f, x, y: ((f(x + h, y) - f(x - h, y)) / (2 * h), (f(x, y + h) - f(x, y - h)) / (2 * h))
        tx, ty = d(th, x0, y0)
        txx = (th(x0 + h, y0) - 2 * th(x0, y0) + th(x0 - h, y0)) / h ** 2
        tyy = (th(x0, y0 + h) - 2 * th(x0, y0) + th(x0, y0 - h)) / h ** 2
        txy = (th(x0 + h, y0 + h) - th(x0 + h, y0 - h) - th(x0 - h, y0 + h) + th(x0 - h, y0 - h)) / (4 * h * h)
        K_graph = -(txx * tyy - txy ** 2) / (1 - tx * tx - ty * ty) ** 2   # spacelike graph in R^(2,1)
        # Brioschi via Christoffel symbols on g = I + grad theta grad theta^T
        def g(x, y):
            px, py = d(th, x, y)
            return (1 - px * px, -px * py, 1 - py * py)   # gamma = delta - grad grad (adm_dictionary.md:64)
        def K_brioschi(x, y):
            H = 1e-2
            E, F, G = g(x, y)
            Ex = (g(x + H, y)[0] - g(x - H, y)[0]) / (2 * H); Ey = (g(x, y + H)[0] - g(x, y - H)[0]) / (2 * H)
            Fx = (g(x + H, y)[1] - g(x - H, y)[1]) / (2 * H); Fy = (g(x, y + H)[1] - g(x, y - H)[1]) / (2 * H)
            Gx = (g(x + H, y)[2] - g(x - H, y)[2]) / (2 * H); Gy = (g(x, y + H)[2] - g(x, y - H)[2]) / (2 * H)
            Exx = (g(x + H, y)[0] - 2 * E + g(x - H, y)[0]) / H ** 2
            Gyy = (g(x, y + H)[2] - 2 * G + g(x, y - H)[2]) / H ** 2
            Fxy = (g(x + H, y + H)[1] - g(x + H, y - H)[1] - g(x - H, y + H)[1] + g(x - H, y - H)[1]) / (4 * H * H)
            Gxx = (g(x + H, y)[2] - 2 * G + g(x - H, y)[2]) / H ** 2
            Eyy = (g(x, y + H)[0] - 2 * E + g(x, y - H)[0]) / H ** 2
            def det3(m):
                return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
            A = det3([[-0.5 * Eyy + Fxy - 0.5 * Gxx, 0.5 * Ex, Fx - 0.5 * Ey], [Fy - 0.5 * Gx, E, F], [0.5 * Gy, F, G]])
            B = det3([[0, 0.5 * Ey, 0.5 * Gx], [0.5 * Ey, E, F], [0.5 * Gx, F, G]])
            return (A - B) / (E * G - F * F) ** 2
        worst = max(worst, abs(K_graph - K_brioschi(x0, y0)) / (abs(K_graph) + 1e-3))
    return worst


def main() -> int:
    ok = True
    inertial = MUTANT == "inertial"
    e = spreading_exponent(inertial)
    print(f"1. perturbation spreading exponent: {e:.3f} (diffusive 0.5; ballistic 1.0)")
    ok &= abs(e - 0.5) < 0.1
    r1, r2, rmin, rmax = locked_clock_rates()
    print(f"2. locked heterogeneous ring: local coherence ranges {rmin:.3f}-{rmax:.3f}, "
          f"yet max |theta' - Omega| = {r1:.2e} -> {r2:.2e} (lapse uniform)")
    ok &= r2 <= r1 and r2 < 1e-6 and (rmax - rmin) > 0.01
    w = gauss_check()
    print(f"3. gamma = I - grad theta grad theta^T obeys the Minkowski-graph Gauss equation: rel. err {w:.2e}")
    ok &= w < 5e-2
    print("REFUTATION " + ("CONFIRMED" if ok else "NOT CONFIRMED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
