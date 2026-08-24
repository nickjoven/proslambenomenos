#!/usr/bin/env python3
"""P-13 registration layer: derive the null and every number the
prediction cites BEFORE the chain is integrated. Each "=" sign in
notes/p13_acoustic_chain.md carries an EQ id; this script checks that
identity and prints one line per check:

    EQ n PASS|FAIL  <statement>  | <detail>

Exit 0 iff every EQ passes. Output is committed as
p13_symbolic_out.txt and the pinned numbers as p13_registration.json;
the experiment compares against the pinned numbers, not re-derived
ones. Stdlib only (symb.py is the in-repo symbolic layer).

Model: chain of masses m[i], springs J[i] (spring i joins sites i,
i+1), lattice spacing a = 1, displacements u_i(t):

    m_i u_i'' = J_i (u_{i+1} - u_i) + J_{i-1} (u_{i-1} - u_i)
"""
import cmath
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from symb import N, V, add, sub, mul, div, powe, sqrt, sin, cos, exp, log, d, ev, equal, simpson  # noqa: E402
import p13_profiles as P  # noqa: E402

OUT = []
FAILED = []


def eq(n, ok, statement, detail):
    line = f"EQ {n} {'PASS' if ok else 'FAIL'}  {statement}  | {detail}"
    OUT.append(line)
    print(line)
    if not ok:
        FAILED.append(n)


# ---------------------------------------------------------------- EQ1
# Plane wave u(n,t) = cos(k n - w t) solves the uniform-chain EOM
# iff w^2 = (2J/m)(1 - cos k). Residual checked symbolically: the
# t-derivative is symbolic (symb.d); the neighbour shift is literal
# substitution n -> n +/- 1.
k, n_, t, J, m = V("k"), V("n"), V("t"), V("J"), V("m")
w = mul(N(2), sqrt(div(J, m)), sin(mul(N(0.5), k)))          # the claimed w(k)
phase = sub(mul(k, n_), mul(w, t))
u = cos(phase)
u_p = cos(sub(mul(k, add(n_, N(1))), mul(w, t)))             # u_{n+1}
u_m = cos(sub(mul(k, add(n_, N(-1))), mul(w, t)))            # u_{n-1}
lhs = mul(m, d(d(u, "t"), "t"))
rhs = mul(J, add(u_p, u_m, mul(N(-2), u)))
box = {"k": (0.01, 2.5), "n": (0.0, 40.0), "t": (0.0, 40.0),
       "J": (0.3, 3.0), "m": (0.3, 3.0)}
ok, worst, nv = equal(lhs, rhs, box)
eq(1, ok, "m u'' = J(u_{n+1} - 2u_n + u_{n-1}) for u = cos(kn - wt), w = 2 sqrt(J/m) sin(k/2)",
   f"worst rel delta {worst:.2e} over {nv} samples of (k,n,t,J,m)")

# ---------------------------------------------------------------- EQ2
# Half-angle bridge: (2J/m)(1 - cos k) = (4J/m) sin^2(k/2).
lhs2 = mul(div(mul(N(2), J), m), sub(N(1), cos(k)))
rhs2 = mul(div(mul(N(4), J), m), powe(sin(mul(N(0.5), k)), N(2)))
ok, worst, nv = equal(lhs2, rhs2, box)
eq(2, ok, "(2J/m)(1 - cos k) = (4J/m) sin^2(k/2)", f"worst rel delta {worst:.2e}")

# ---------------------------------------------------------------- EQ3
# Group velocity dw/dk = sqrt(J/m) cos(k/2); sound speed c0 =
# sqrt(J/m) as k -> 0 (evaluated at k = 1e-8).
vg = d(w, "k")
vg_claim = mul(sqrt(div(J, m)), cos(mul(N(0.5), k)))
ok, worst, nv = equal(vg, vg_claim, box)
c0_num = ev(vg, {"k": 1e-8, "J": 1.0, "m": 1.0})
ok3 = ok and abs(c0_num - 1.0) < 1e-9
eq(3, ok3, "dw/dk = sqrt(J/m) cos(k/2); c0 = sqrt(J/m)",
   f"worst rel delta {worst:.2e}; c0(J=m=1) = {c0_num:.12f}")

# ---------------------------------------------------------------- EQ4
# Ramp eikonal closed form: c(x) = c0(1 + b x)  =>  T(x) =
# ln(1 + b x)/(c0 b). Checked two ways: d/dx T = 1/c(x) (symbolic),
# and adaptive Simpson agrees with the closed form at x = L.
x, b, c0v = V("x"), V("b"), V("c0")
T_closed = div(log(add(N(1), mul(b, x))), mul(c0v, b))
ok, worst, nv = equal(d(T_closed, "x"), div(N(1), mul(c0v, add(N(1), mul(b, x)))),
                      {"x": (0.0, 1000.0), "b": (1e-4, 1e-3), "c0": (0.5, 1.5)})
# numeric instance on the registered ramp: c falls 1 -> 0.5 over the span
span = P.RAMP_HI - P.RAMP_LO
beta = (P.C_MIN - 1.0) / span                       # signed slope of c
T_simpson = simpson(lambda xx: 1.0 / (1.0 + beta * xx), 0.0, float(span))
T_exact = math.log(1.0 + beta * span) / beta
ok4 = ok and abs(T_simpson - T_exact) < 1e-8 * abs(T_exact)
eq(4, ok4, "c = c0(1+bx) => T = ln(1+bx)/(c0 b)",
   f"d/dx check worst {worst:.2e}; Simpson {T_simpson:.6f} vs closed {T_exact:.6f}")

# ---------------------------------------------------------------- EQ5
# Continuum integral vs the discrete eikonal sum the prediction
# actually uses, for both registered inhomogeneous profiles: the two
# must agree to O(1/N) (< 0.5%).
rows5 = []
ok5 = True
for name, cf in (("ramp", P.c_ramp), ("lens", P.c_lens)):
    m_a, J_a = P.profile(name)
    disc = P.eikonal(m_a, J_a, 0, P.N_SITES - 1)
    cont = simpson(lambda xx: 1.0 / cf(xx), 0.0, float(P.N_SITES - 1))
    rel = abs(disc - cont) / cont
    ok5 = ok5 and rel < 5e-3
    rows5.append(f"{name}: sum {disc:.3f} vs integral {cont:.3f} (rel {rel:.2e})")
eq(5, ok5, "discrete eikonal sum = continuum integral of 1/c to O(1/N)", "; ".join(rows5))


# ---------------------------------------------------------------- EQ6
# Lattice junction: media (m1,J1 | m2,J2), bond into the junction
# carries J2 (profile convention). Incident + reflected on the left,
# transmitted on the right; the two interface EOMs are solved exactly
# (2x2, cmath). Claim: energy reflection R -> ((Z1-Z2)/(Z1+Z2))^2
# with Z = sqrt(mJ) as k -> 0, for BOTH junctions:
#   jc (c matched, Z ratio 4)  -> Fresnel R = (3/5)^2 = 0.36
#   jz (Z matched, c ratio 4)  -> Fresnel R = 0
def lattice_junction(m1, J1, m2, J2, k1):
    w2 = 4 * J1 / m1 * math.sin(k1 / 2) ** 2
    wv = math.sqrt(w2)
    s2 = wv / (2 * math.sqrt(J2 / m2))
    if s2 > 1:
        raise ValueError("evanescent on the right")
    k2 = 2 * math.asin(s2)
    e1, e1i = cmath.exp(1j * k1), cmath.exp(-1j * k1)
    e2, e22 = cmath.exp(1j * k2), cmath.exp(2j * k2)
    # unknowns r, tt;  u_n = e^{ik1 n} + r e^{-ik1 n} (n<=0), tt e^{ik2 n} (n>=1)
    # node 0 (mass m1, left spring J1, right spring J2):
    #   -m1 w^2 u0 = J1(u_{-1} - u0) + J2(u_1 - u0)
    # node 1 (mass m2, both springs J2):
    #   -m2 w^2 u1 = J2(u_0 - u1) + J2(u_2 - u1)
    # eqs as a_r r + a_t tt = rhs, with u0 = 1 + r, u_{-1} = e1i + r e1,
    # u1 = tt e2, u2 = tt e22:
    # eq0: -m1 w2 (1+r) = J1((e1i + r e1) - (1+r)) + J2(tt e2 - (1+r))
    a_r0 = -m1 * w2 - J1 * (e1 - 1) + J2
    a_t0 = -J2 * e2
    rhs0 = m1 * w2 + J1 * (e1i - 1) - J2
    # eq1: 0 = m2 w2 tt e2 + J2(1 + r - tt e2) + J2 tt(e22 - e2)
    a_r1 = J2
    a_t1 = m2 * w2 * e2 - J2 * e2 + J2 * (e22 - e2)
    rhs1 = -J2
    det = a_r0 * a_t1 - a_t0 * a_r1
    r = (rhs0 * a_t1 - a_t0 * rhs1) / det
    tt = (a_r0 * rhs1 - rhs0 * a_r1) / det
    vg1 = math.sqrt(J1 / m1) * math.cos(k1 / 2)
    vg2 = math.sqrt(J2 / m2) * math.cos(k2 / 2)
    R = abs(r) ** 2
    Te = (m2 * vg2) / (m1 * vg1) * abs(tt) ** 2
    return R, Te


def fresnel(m1, J1, m2, J2):
    z1, z2 = math.sqrt(m1 * J1), math.sqrt(m2 * J2)
    return ((z1 - z2) / (z1 + z2)) ** 2


rows6, ok6 = [], True
econ_worst = 0.0
for tag, (m1, J1, m2, J2) in (("jc", (1, 1, 4, 4)), ("jz", (1, 1, 4, 0.25))):
    fr = fresnel(m1, J1, m2, J2)
    R1, Te1 = lattice_junction(m1, J1, m2, J2, 0.10)
    R2, Te2 = lattice_junction(m1, J1, m2, J2, 0.05)
    econ_worst = max(econ_worst, abs(R1 + Te1 - 1), abs(R2 + Te2 - 1))
    ok6 = ok6 and abs(R2 - fr) < 0.01 and abs(R2 - fr) <= abs(R1 - fr) + 1e-12
    rows6.append(f"{tag}: Fresnel {fr:.4f}, lattice R(k=0.10) {R1:.4f}, R(k=0.05) {R2:.4f}")
eq(6, ok6, "lattice junction R -> ((Z1-Z2)/(Z1+Z2))^2 as k -> 0 (both junctions)", "; ".join(rows6))

# ---------------------------------------------------------------- EQ7
# Energy conservation of the junction solve: R + T_e = 1 exactly
# (flux = per-site energy density x group velocity on each side).
eq(7, econ_worst < 1e-10, "R + (m2 vg2 / m1 vg1)|t|^2 = 1 at the junction",
   f"worst |R + Te - 1| = {econ_worst:.2e}")

# ---------------------------------------------------------------- EQ8
# The zramp profile holds Z = sqrt(mJ) = 1 to machine precision while
# c changes by a factor 2; the jc profile holds c equal across the
# junction while Z jumps by 4. (The construction the prediction's
# scattering claims rest on.)
m_z, J_z = P.profile("zramp")
zdev = max(abs(math.sqrt(m_z[i] * (J_z[i] if i < len(J_z) else J_z[-1])) - 1.0)
           for i in range(P.N_SITES))
# zramp Z uses J at bond midpoint vs m at site: allow the O(1/N) offset
m_c, J_c = P.profile("jc")
cl = P.c_site(m_c, J_c, 0)
cr = P.c_site(m_c, J_c, P.N_SITES - 2)
ok8 = zdev < 2e-3 and abs(cl - cr) < 1e-12
eq(8, ok8, "zramp: Z = 1 (+/- bond-midpoint O(1/N)); jc: c identical across junction",
   f"max |Z-1| = {zdev:.2e}; c_left {cl:.12f} c_right {cr:.12f}")

# ------------------------------------------------------- pinned numbers
CHECKPOINTS = list(range(200, 1301, 100))
pin = {
    "n_sites": P.N_SITES, "junction": P.JN,
    "pulse": {"shape": "half-sine displacement drive at site 0",
              "amplitude": 1.0, "tau": 60.0,
              "dominant_omega": round(math.pi / 60.0, 6),
              "group_deficit_at_k0.052": round(1 - math.cos(0.052 / 2), 8)},
    "dt": 0.05,
    "checkpoints": CHECKPOINTS,
    "eikonal": {},
    "fresnel": {"jc": fresnel(1, 1, 4, 4), "jz": fresnel(1, 1, 4, 0.25)},
    "lattice_R_at_k0.05": {"jc": lattice_junction(1, 1, 4, 4, 0.05)[0],
                           "jz": lattice_junction(1, 1, 4, 0.25, 0.05)[0]},
    "tolerances": {"control_speed_rel": 0.005, "airy_exponent_band": [0.23, 0.43],
                   "eikonal_rms_rel": 0.02, "shuffle_ratio_min": 10.0,
                   "junction_R_abs": 0.05, "quiet_R_max": 0.01,
                   "dt_halving_rel": 0.002},
}
for name in ("control", "ramp", "lens", "zramp"):
    m_a, J_a = P.profile(name)
    pin["eikonal"][name] = {str(j): round(P.eikonal(m_a, J_a, 0, j), 6) for j in CHECKPOINTS}

here = Path(__file__).resolve().parent
(here / "p13_registration.json").write_text(json.dumps(pin, indent=1) + "\n")
(here / "p13_symbolic_out.txt").write_text("\n".join(OUT) + "\n")
print(f"\npinned {len(CHECKPOINTS)} checkpoints x 4 profiles; "
      f"fresnel jc {pin['fresnel']['jc']:.4f}, jz {pin['fresnel']['jz']:.4f}")
sys.exit(1 if FAILED else 0)
