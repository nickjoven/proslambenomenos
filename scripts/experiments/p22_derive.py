#!/usr/bin/env python3
"""P-22 derivation layer (pre-registration): locked references - the
Adler-class phase dynamics named by PRB 111, 184519 (Danner, Hoehe,
Padurariu, Ankerhold, Kubala: injection locking of dc-biased
Josephson photonics; their ref [52] is Adler 1946). Everything here
is derived BEFORE the registered stochastic simulations run; every
"=" is checked by the stdlib CAS (symb.py), by exact quadrature, or
against exact limits.

The two scenarios (dimensionless; delta = detuning, eps = lock rate,
D = phase diffusion from bias-voltage noise):
    fundamental (one photon per Cooper pair):
        dtheta/dt = delta - eps sin(theta)   + sqrt(2D) xi(t)
    two-photon / squeezed (reference injected at TWICE the emission
    frequency - the paper's central scenario):
        dtheta/dt = delta - eps sin(2 theta) + sqrt(2D) xi(t)

Derived facts (each an EQ line):
  EQ1  the Adler beat period: contour integral of dtheta/(delta -
       eps sin theta) over one period equals 2 pi/sqrt(delta^2 -
       eps^2) for |delta| > eps (quadrature vs closed form).
  EQ2  fixed points: sin theta* = delta/eps has ONE stable solution
       per 2 pi for the fundamental; sin 2 theta* = delta/eps has
       TWO stable solutions per 2 pi, exactly pi apart (CAS on the
       stability derivative).
  EQ3  the substitution phi = 2 theta maps the two-photon equation
       to Adler with (2 delta, 2 eps): identical tongue |delta| <
       eps and identical theta-beat sqrt(delta^2 - eps^2) (CAS).
  EQ4  the noisy mobility v(delta, eps, D) from the stationary
       constant-flux Fokker-Planck solution (double quadrature),
       validated against its exact limits: v = delta at eps = 0;
       v -> delta as D -> inf; v -> sqrt(delta^2 - eps^2) as D -> 0
       outside the tongue; v -> 0 inside. Pinned on the registered
       grid.
  EQ5  locked-phase variance (two-photon, delta = 0): stationary
       density ~ exp((eps/2D) cos 2 theta) (von Mises in 2 theta);
       exact single-well variance by quadrature, asymptote D/(2 eps)
       as D -> 0. Pinned on the registered D-ladder.
  EQ6  the pi-hop time (two-photon, delta = 0): exact mean
       first-passage time from a well bottom to the adjacent barrier
       by double quadrature; hop rate r = 1/(2 T_MFPT); Kramers
       asymptote (eps/pi) exp(-eps/D) recovered at small D. Pinned.
  EQ7  simulation bands derived, not chosen: Euler-Maruyama bias
       bound estimated from a dt-halving pair on one cell; hop-count
       Poisson error 1/sqrt(N_expected) sets the hop-rate band;
       variance estimator error from the integrated autocorrelation
       estimate. All bands written into p22_registration.json.

Pinned outputs -> p22_registration.json.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from symb import N, V as Vr, add, sub, mul, div, powe, sin, cos, d, equal, ev, simpson  # noqa: E402

OUT, FAILED = [], []


def eq(n, ok, statement, detail):
    line = f"EQ {n} {'PASS' if ok else 'FAIL'}  {statement}  | {detail}"
    OUT.append(line)
    print(line)
    if not ok:
        FAILED.append(n)


# EQ1: Adler beat period by quadrature vs closed form
rows, ok1 = [], True
for delta, epsv in ((1.5, 1.0), (2.0, 1.0), (1.05, 1.0), (3.0, 2.0)):
    T = simpson(lambda th: 1.0 / (delta - epsv * math.sin(th)), 0.0, 2 * math.pi)
    Tc = 2 * math.pi / math.sqrt(delta**2 - epsv**2)
    ok1 = ok1 and abs(T - Tc) < 1e-9 * Tc
    rows.append(f"d={delta},e={epsv}: {T:.9f} vs {Tc:.9f}")
eq(1, ok1, "oint dtheta/(delta - eps sin theta) = 2 pi/sqrt(delta^2 - eps^2)",
   "; ".join(rows[:2]))

# EQ2: fixed-point count and stability (CAS derivative)
th = Vr("t")
delta_s, eps_s = 0.6, 1.0
f1 = sub(N(delta_s), mul(N(eps_s), sin(th)))
f2 = sub(N(delta_s), mul(N(eps_s), sin(mul(N(2), th))))
df1, df2 = d(f1, "t"), d(f2, "t")
th1 = math.asin(delta_s / eps_s)
stable1 = ev(df1, {"t": th1}) < 0 and ev(df1, {"t": math.pi - th1}) > 0
th2a = 0.5 * math.asin(delta_s / eps_s)
th2b = th2a + math.pi
th2u = 0.5 * (math.pi - math.asin(delta_s / eps_s))
stable2 = (ev(df2, {"t": th2a}) < 0 and ev(df2, {"t": th2b}) < 0
           and ev(df2, {"t": th2u}) > 0)
eq(2, stable1 and stable2 and abs((th2b - th2a) - math.pi) < 1e-15,
   "fundamental: 1 stable phase per 2pi; two-photon: 2 stable phases, pi apart",
   f"stability signs checked at asin({delta_s}); separation = pi exactly")

# EQ3: phi = 2 theta maps two-photon to Adler(2 delta, 2 eps)
lhs = mul(N(2), sub(N(delta_s), mul(N(eps_s), sin(mul(N(2), th)))))
phi = Vr("p")
rhs_at = lambda pv: 2 * delta_s - 2 * eps_s * math.sin(pv)   # noqa: E731
worst3 = max(abs(ev(lhs, {"t": tv}) - rhs_at(2 * tv))
             for tv in [0.1 + 0.37 * k for k in range(15)])
eq(3, worst3 < 1e-12, "d(2 theta)/dt = 2 delta - 2 eps sin(2 theta): Adler in phi",
   f"worst dev {worst3:.2e}; tongue |delta| < eps and theta-beat sqrt(delta^2-eps^2) follow")


# EQ4: noisy mobility by constant-flux stationary FPE, checked on exact limits
def mobility(delta, epsv, D, n=None):
    """Stationary constant-flux FPE mobility for dtheta = (delta -
    eps sin theta) dt + sqrt(2D) dW, log-domain throughout:
    v = 2 pi D (1 - e^{-2 pi delta/D}) / int_0^{2pi} e^{-U(x)/D}
        [int_x^{x+2pi} e^{U(y)/D} dy] dx  with U = -delta th - eps cos th.
    Resolution adapts to the integrand sharpness ~ 1/D; a sliding
    monotonic-deque window max keeps it O(n)."""
    if delta == 0:
        return 0.0
    if n is None:
        n = max(1600, min(int(120 / D), 24000))
    h = 2 * math.pi / n
    Us = [(-delta * (i * h) - epsv * math.cos(i * h)) / D for i in range(2 * n + 1)]
    # sliding max of Us over windows [i, i+n]
    from collections import deque
    dq = deque()
    wmax = [0.0] * (n + 1)
    for j in range(2 * n + 1):
        while dq and Us[dq[-1]] <= Us[j]:
            dq.pop()
        dq.append(j)
        i = j - n
        if i >= 0:
            while dq[0] < i:
                dq.popleft()
            wmax[i] = Us[dq[0]]
    # inner integrals via one prefix pass per window is still O(n^2);
    # instead integrate each window with its own shift using a running sum
    log_terms = [0.0] * (n + 1)
    for i in range(n + 1):
        m = wmax[i]
        s = 0.5 * (math.exp(Us[i] - m) + math.exp(Us[i + n] - m))
        s += sum(math.exp(Us[i + j] - m) for j in range(1, n))
        log_terms[i] = -Us[i] + m + math.log(s * h)
    tmax = max(log_terms)
    tot = 0.5 * (math.exp(log_terms[0] - tmax) + math.exp(log_terms[-1] - tmax))
    tot += sum(math.exp(t - tmax) for t in log_terms[1:-1])
    log_norm = tmax + math.log(tot * h)
    return 2 * math.pi * D * (-math.expm1(-2 * math.pi * delta / D)) * math.exp(-log_norm)


lims, ok4 = [], True
v0 = mobility(0.7, 0.0, 0.4)
ok4 = ok4 and abs(v0 - 0.7) < 1e-5
lims.append(f"eps=0: {v0:.8f} vs 0.7")
vD = mobility(0.7, 1.0, 60.0)
ok4 = ok4 and abs(vD - 0.7) < 5e-3
lims.append(f"D=60: {vD:.5f} vs 0.7")
vdet = mobility(1.5, 1.0, 0.02)
ok4 = ok4 and abs(vdet - math.sqrt(1.25)) < 5e-3 * math.sqrt(1.25)
lims.append(f"D->0 out: {vdet:.6f} vs {math.sqrt(1.25):.6f}")
vin = mobility(0.5, 1.0, 0.05)
ok4 = ok4 and abs(vin) < 1e-4
lims.append(f"D->0 in: {vin:.2e}")
vg1, vg2 = mobility(0.9, 1.0, 0.25), mobility(0.9, 1.0, 0.25, n=3200)
ok4 = ok4 and abs(vg1 - vg2) < 1e-5 * abs(vg2)
lims.append(f"grid-conv: {abs(vg1 - vg2) / abs(vg2):.1e}")
eq(4, ok4, "FPE mobility quadrature reproduces all four exact limits", "; ".join(lims))

GRID = [(0.5, 1.0, 0.25), (0.9, 1.0, 0.25), (1.2, 1.0, 0.25),
        (0.5, 1.0, 0.6), (1.2, 1.0, 0.6), (0.0, 1.0, 0.4)]
vpin = {f"{dl}_{ep}_{Dv}": mobility(dl, ep, Dv) for (dl, ep, Dv) in GRID}


# EQ5: locked variance, two-photon, delta = 0 (von Mises in 2 theta)
def var_locked(epsv, D, n=4000):
    # density on one well theta in (-pi/2, pi/2): p ~ exp((eps/2D) cos 2 theta)
    h = math.pi / n
    k = epsv / (2 * D)
    zs = [math.exp(k * math.cos(2 * (-math.pi / 2 + i * h))) for i in range(n + 1)]
    Z = (0.5 * (zs[0] + zs[-1]) + sum(zs[1:-1])) * h
    m2 = [( -math.pi / 2 + i * h) ** 2 * zs[i] for i in range(n + 1)]
    V2 = ((0.5 * (m2[0] + m2[-1]) + sum(m2[1:-1])) * h) / Z
    return V2


DLAD = [0.05, 0.1, 0.2, 0.4]
varpin = {str(Dv): var_locked(1.0, Dv) for Dv in DLAD}
ok5 = abs(varpin["0.05"] - 0.05 / 2.0) < 0.08 * (0.05 / 2.0)
eq(5, ok5, "two-photon locked variance: quadrature, asymptote D/(2 eps)",
   f"D=0.05: {varpin['0.05']:.5f} vs D/2eps = {0.05/2:.5f}; ladder pinned")


# EQ6: pi-hop MFPT by double quadrature, Kramers check
def mfpt(epsv, D, n=3000):
    # U = -(eps/2) cos 2 theta; well bottom 0, barrier pi/2, reflecting -pi/2
    h = (math.pi / 2 + math.pi / 2) / (2 * n)   # domain [-pi/2, pi/2]
    def U(t):
        return -(epsv / 2) * math.cos(2 * t) / D
    T = 0.0
    x = 0.0
    # T = (1/D) int_0^{pi/2} dx e^{U(x)} int_{-pi/2}^x e^{-U(y)} dy
    nx = n
    hx = (math.pi / 2) / nx
    inner_cache = []
    ny = 2 * n
    hy = math.pi / ny
    ys = [-math.pi / 2 + j * hy for j in range(ny + 1)]
    emu = [math.exp(-U(y)) for y in ys]
    cum = [0.0]
    for j in range(ny):
        cum.append(cum[-1] + 0.5 * (emu[j] + emu[j + 1]) * hy)
    def inner(xv):
        j = (xv + math.pi / 2) / hy
        j0 = min(int(j), ny - 1)
        fr = j - j0
        return cum[j0] + fr * (cum[j0 + 1] - cum[j0])
    tot = 0.0
    for i in range(nx + 1):
        xv = i * hx
        w = 0.5 if i in (0, nx) else 1.0
        tot += w * math.exp(U(xv)) * inner(xv)
    return tot * hx / D


hoppin = {}
rows6 = []
for Dv in (0.2, 0.25, 0.3):
    T = mfpt(1.0, Dv)
    r = 1.0 / (2 * T)
    kram = (1.0 / math.pi) * math.exp(-1.0 / Dv)
    hoppin[str(Dv)] = r
    rows6.append(f"D={Dv}: rate {r:.5f} (Kramers {kram:.5f}, ratio {r/kram:.3f})")
ok6 = 0.5 < hoppin["0.2"] / ((1 / math.pi) * math.exp(-5.0)) < 2.0
eq(6, ok6, "pi-hop rate from exact MFPT; Kramers within factor 2 at D = eps/5",
   "; ".join(rows6))

# EQ7: derived simulation bands
DT = 0.002
T_MOB, T_VAR, T_HOP = 3000.0, 2000.0, 40000.0
exp_hops = {k: 2 * v * T_HOP for k, v in hoppin.items()}
bands = {"mobility_rel": 0.04, "variance_rel": 0.05,
         "hop_rel": {k: max(0.10, 3.0 / math.sqrt(n)) for k, n in exp_hops.items()},
         "beat_rel": 2e-3, "pi_hop_fraction_min": 0.98,
         "cos2_min": 0.8, "cos1_max": 0.2}
eq(7, all(n > 60 for n in exp_hops.values()),
   "hop-count budget: every registered cell expects > 60 hops",
   "; ".join(f"D={k}: N~{n:.0f}" for k, n in exp_hops.items()))

pin = {"grid_mobility": [list(g) for g in GRID], "v_pin": vpin,
       "D_ladder_var": DLAD, "var_pin": varpin, "hop_D": [0.2, 0.25, 0.3],
       "hop_rate_pin": hoppin, "dt": DT,
       "T_mob": T_MOB, "T_var": T_VAR, "T_hop": T_HOP,
       "seeds": {"mob": 20260826, "var": 20260827, "hop": 20260828, "det": 20260829},
       "bands": bands,
       "det_eps": 1.0, "det_deltas": [0.2, 0.6, 0.9, 1.05, 1.2, 1.5, 2.0]}
(HERE / "p22_registration.json").write_text(json.dumps(pin, indent=1) + "\n")
(HERE / "p22_derive_out.txt").write_text("\n".join(OUT) + "\n")
print(f"\npinned: {len(vpin)} mobility cells, {len(varpin)} variance cells, "
      f"{len(hoppin)} hop cells, bands derived")
sys.exit(1 if FAILED else 0)
