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
