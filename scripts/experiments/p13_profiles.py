"""P-13 substrate profiles, shared by the symbolic registration layer
(p13_symbolic.py), the experiment (p13_acoustic_chain.py), and the
verify script, so that the profile the prediction was registered
against is byte-identical to the one the chain integrates.

A chain of N_SITES masses m[i] joined by N_SITES-1 springs J[i]
(spring i connects sites i and i+1), lattice spacing a = 1. The
local sound speed and impedance are the two independent pieces of
substrate data:

    c(i) = sqrt(J(i)/m(i))        (EQ3: the acoustic metric)
    Z(i) = sqrt(m(i)*J(i))        (what the metric does not see)

Profiles:
  control  m = J = 1 everywhere; flat metric, the null system.
  ramp     c falls 1.0 -> 0.5 linearly over sites 150..1350 (J = 1,
           m = 1/c^2): metric varies, impedance varies.
  lens     c(x) = 1 - 0.35*exp(-(x-750)^2 / (2*130^2)): a dip.
  zramp    same c(x) as ramp but m = 1/c, J = c: impedance
           identically 1 while the metric changes by a factor 2.
  jc       abrupt junction at site 750: m,J both x4 on the right.
           c identical on both sides; Z jumps by 4.
  jz       abrupt junction at site 750: m x4, J /4 on the right.
           Z identical on both sides; c drops by 4.
Junction bond convention: spring i for i >= JN-1 belongs to the
right medium (the bond into the junction node carries the right
medium's J), matching the lattice matching solve in p13_symbolic.py.
"""
import math

N_SITES = 1500
JN = 750               # junction site for jc / jz
RAMP_LO, RAMP_HI = 150, 1350
C_MIN = 0.5
LENS_DEPTH, LENS_X0, LENS_SIG = 0.35, 750.0, 130.0


def c_ramp(x):
    if x <= RAMP_LO:
        return 1.0
    if x >= RAMP_HI:
        return C_MIN
    return 1.0 + (C_MIN - 1.0) * (x - RAMP_LO) / (RAMP_HI - RAMP_LO)


def c_lens(x):
    return 1.0 - LENS_DEPTH * math.exp(-((x - LENS_X0) ** 2) / (2 * LENS_SIG ** 2))


def profile(name):
    """Return (m, J): masses (len N_SITES) and springs (len N_SITES-1)."""
    n = N_SITES
    if name == "control":
        return [1.0] * n, [1.0] * (n - 1)
    if name == "ramp":
        m = [1.0 / c_ramp(i) ** 2 for i in range(n)]
        return m, [1.0] * (n - 1)
    if name == "lens":
        m = [1.0 / c_lens(i) ** 2 for i in range(n)]
        return m, [1.0] * (n - 1)
    if name == "zramp":
        m = [1.0 / c_ramp(i) for i in range(n)]
        J = [c_ramp(i + 0.5) for i in range(n - 1)]
        return m, J
    if name == "jc":
        m = [1.0 if i < JN else 4.0 for i in range(n)]
        J = [1.0 if i < JN - 1 else 4.0 for i in range(n - 1)]
        return m, J
    if name == "jz":
        m = [1.0 if i < JN else 4.0 for i in range(n)]
        J = [1.0 if i < JN - 1 else 0.25 for i in range(n - 1)]
        return m, J
    raise ValueError(f"unknown profile {name!r}")


def c_site(m, J, i):
    """Local sound speed at site i (spring to the right; last site
    reuses its left spring - an O(1/N) end convention stated in the
    registration)."""
    j = J[i] if i < len(J) else J[-1]
    return math.sqrt(j / m[i])


def z_site(m, J, i):
    j = J[i] if i < len(J) else J[-1]
    return math.sqrt(j * m[i])


def eikonal(m, J, j0, j1):
    """Discrete eikonal time sum_{i=j0}^{j1-1} 1/c(i): the registered
    arrival-time prediction between sites j0 and j1."""
    return sum(1.0 / c_site(m, J, i) for i in range(j0, j1))


def junction_solve(m1, J1, m2, J2, k1):
    """Exact lattice junction (bond into the junction node carries J2,
    the profile convention above): incident + reflected plane wave on
    the left, transmitted on the right; the two interface EOMs solved
    as a 2x2 complex system. Returns (R, T_e) with R = |r|^2 and
    T_e the energy-flux transmission; R + T_e = 1 is checked as EQ7.
    Raises ValueError when the right medium is evanescent at this
    frequency (omega above its band edge 2*sqrt(J2/m2))."""
    import cmath
    w2 = 4 * J1 / m1 * math.sin(k1 / 2) ** 2
    s2 = math.sqrt(w2) / (2 * math.sqrt(J2 / m2))
    if s2 > 1:
        raise ValueError("evanescent on the right")
    k2 = 2 * math.asin(s2)
    e1, e1i = cmath.exp(1j * k1), cmath.exp(-1j * k1)
    e2, e22 = cmath.exp(1j * k2), cmath.exp(2j * k2)
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
    return abs(r) ** 2, (m2 * vg2) / (m1 * vg1) * abs(tt) ** 2


def fresnel(m1, J1, m2, J2):
    """Continuum impedance law ((Z1-Z2)/(Z1+Z2))^2, Z = sqrt(mJ)."""
    z1, z2 = math.sqrt(m1 * J1), math.sqrt(m2 * J2)
    return ((z1 - z2) / (z1 + z2)) ** 2
