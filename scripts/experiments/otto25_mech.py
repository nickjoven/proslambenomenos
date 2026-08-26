#!/usr/bin/env python3
"""Mechanization of H. H. Otto, "What Tells Geometrical Reciprocity
about the Universe and its Mass Constituents?" (2025, ResearchGate):
every numbered relation that asserts a numeric equality is executed
and classified. Four bins:

  EXACT      |lhs - rhs| < 1e-12 relative: true algebra (the paper's
             real mathematical content).
  NEARMISS   approximate relation between pure numbers: reported with
             its relative deviation, to be read against the
             pigeonhole baseline (a pool of 34 named constants in
             [1,2] already contains nine pairs closer than 0.35%,
             three of them at 0.154% - see notes).
  EXCLUDED   relation targeting a MEASURED constant: deviation
             expressed in experimental standard deviations.
  INCONSISTENT  the framework's own alternative values for the same
             quantity, measured against each other.

Reference values: CODATA alpha^-1 = 137.035999177(21) (the paper's
own quote); g_e = 2.00231930436182(52) (the paper's eq. 49);
m_H = 125.20 +/- 0.11 GeV (PDG 2024); Planck 2018 Omega_L =
0.6847 +/- 0.0073, Omega_m = 0.3153 +/- 0.0073, Omega_b = 0.0493
+/- 0.0005. Stdlib only, deterministic. Output: otto25_mech.json.

A control block runs the classical exact identities from Riemann's
prime-counting machinery (J(x) = sum pi(x^{1/n})/n term-recount and
ln zeta(s) = sum_p sum_m 1/(m p^{ms})) to show what an identity that
RUNS looks like on the same substrate."""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PHI = (math.sqrt(5) - 1) / 2          # 0.618...  (paper's phi)
PHI_BIG = PHI + 1                     # 1.618...  (paper's Phi)
PI = math.pi

ALPHA_INV = (137.035999177, 2.1e-8)
GE = (2.00231930436182, 5.2e-13)
MH = (125.20, 0.11)
OM_L = (0.6847, 0.0073)
OM_M = (0.3153, 0.0073)
OM_B = (0.0493, 0.0005)

rows = []


def rel(tag, lhs, rhs, note=""):
    if rhs == 0.0:
        dev = abs(lhs)                 # residual check against zero
        cls = "EXACT" if dev < 1e-9 else "NEARMISS"
    else:
        dev = abs(lhs - rhs) / max(abs(lhs), abs(rhs), 1e-300)
        cls = "EXACT" if dev < 1e-12 else "NEARMISS"
    rows.append({"id": tag, "lhs": lhs, "rhs": rhs, "rel_dev": dev,
                 "class": cls, "note": note})


def meas(tag, value, target, note=""):
    t, s = target
    sig = abs(value - t) / s
    rows.append({"id": tag, "lhs": value, "target": t, "sigma_exp": sig,
                 "class": "EXCLUDED" if sig > 5 else "UNEXCLUDED", "note": note})


# ---- section 2: phi-pi near-misses (1a-f), icosahedron (2), alpha (3) ----
r6 = math.sqrt(6 / (5 * PI))
rel("1a", PHI, 0.5 * (1 + r6 - 6 / (5 * PI)), "phi from pi")
rel("1e", PHI**5, 2.5 * (r6 - 6 / (5 * PI)) - 0.5, "phi^5 from pi")
rel("1f", PHI**5, math.sqrt(2 * PI) * PI * (PI * (PI + 1) - 13), "phi^5 from pi,13")
rel("2b", math.sin(math.radians(math.degrees(math.acos(-math.sqrt(5) / 3)))), 2 / 3,
    "sin(dihedral) = 2/3")
rel("2c", PI, math.sqrt(2 / 3) / (2 ** (1 / 3) - 1), "pi from icosahedron")
meas("3a", 4 * PI**3 + PI * (PI + 1), ALPHA_INV, "alpha^-1 = 4pi^3+pi(pi+1)")
meas("3b", 5**3 * (1 + PHI**5) + 2 * PHI**2, ALPHA_INV)
meas("3c", 2 * (12 + 8 / (PI - 3) + PHI**5 / 5), ALPHA_INV)
meas("3d", PI**5 / math.sqrt(5) + 2 * PHI**5, ALPHA_INV)
meas("3e", math.sqrt(137**2 + PI**2), ALPHA_INV)
meas("3g", 1 / (4 * PI**4 + PI**2 * (PI + 1) + 2 / PI), (GE[0] - 2, GE[1]),
    "Delta g_e from pi alone")
rel("4", math.sqrt(2 * PHI * ALPHA_INV[0]), PI * (PI + 1), "sqrt(2 phi/alpha) ~ pi(pi+1)")
meas("5a", 0.8 * 171 + PHI**3, ALPHA_INV, "icosahedron 171 route")
meas("5c", ((13 + 1 / 13) ** 2 - PHI_BIG) / (2 * PHI), ALPHA_INV)

# ---- icosahedron quartic H(x,1) = x^4 - 228x^3 + 494x^2 + 228x + 1 ----
coef = [1.0, -228.0, 494.0, 228.0, 1.0]


def quartic_roots():
    # exact radicals from the paper's appendix
    s5, s3 = math.sqrt(5), math.sqrt(3)
    x1 = -25 * s5 - 5 * s3 * math.sqrt(85 - 38 * s5) + 57
    x2 = -25 * s5 + 5 * s3 * math.sqrt(85 - 38 * s5) + 57
    x3 = 25 * s5 - 5 * s3 * math.sqrt(85 + 38 * s5) + 57
    x4 = 25 * s5 + 5 * s3 * math.sqrt(85 + 38 * s5) + 57
    return [x1, x2, x3, x4]


roots = quartic_roots()
for i, x in enumerate(roots, 1):
    val = (((coef[0] * x + coef[1]) * x + coef[2]) * x + coef[3]) * x + coef[4]
    rel(f"app-root{i}", val / max(abs(x) ** 4, 1.0), 0.0, "appendix radical is a root")
rel("14", sum(roots), 228.0, "Vieta: sum of roots")
rel("11", roots[1], -1 / roots[0], "x2 = -1/x1 reciprocity")
rel("12", roots[1], 228 - (4 / 3) * 13**2, "x2 ~ 228-4/3*169  (claimed 2.666)")
rel("9", (13 + 1 / 13) ** 2, 171.0, "(13+1/13)^2 ~ 171")

# ---- (15)-(18): the depressed quartic around 13 ----
x12 = math.sqrt((169 + math.sqrt(169**2 - 4)) / 2)
rel("16-17", x12**4 - 169 * x12**2 + 1, 0.0, "root check")
rel("17", x12, 13.0, "x ~ 13 (claimed 12.99977)")

# ---- section 3: continued-fraction identities (19)-(23) ----
rel("19", PHI, 1 / (1 + PHI), "phi CF fixed point")
rel("20", PHI**3, math.sqrt(5) - 2, "phi^3 = sqrt5 - 2")
rel("20cf", PHI**3, 1 / (4 + PHI**3), "phi^3 CF in 4s")
rel("22", PHI**5, (math.sqrt(125) - 11) / 2, "phi^5 closed form")
rel("22cf", PHI**5, 1 / (11 + PHI**5), "phi^5 CF in 11s")
rel("24", PHI ** (1 / 6), 12 / 13 - 1 / (3 * (3 + PHI) ** 6), "6th root vs 12/13 term")
rows.append({"id": "24-digits", "lhs": PHI ** (1 / 6),
             "class": "NEARMISS",
             "note": f"claimed repeating '922929922'; actual digits "
                     f"{PHI ** (1/6):.12f} break the pattern at the 8th decimal"})

# ---- series identities (25)-(31) ----
rel("25", sum(PHI**n for n in range(1, 200)), PHI_BIG, "sum phi^n = Phi")
rel("27", 1 / sum(13.0 ** -n for n in range(1, 60)), 12.0, "(sum 13^-n)^-1 = 12")
rel("29", 1 / sum(13.0 ** -n for n in range(1, 60, 2)), 13 - 1 / 13, "odd-n sum")
rel("31", (13 + 1 / 13) ** 2, 4 + (13 - 1 / 13) ** 2, "(m+1/m)^2 = 4+(m-1/m)^2")
rel("32", PHI**5 / (1 + PHI**5), 1 / (12 + PHI**5), "identity in disguise")
rel("32b", PHI**5 / (1 + PHI**5), 1 / 13 + 1 / 13**2, "vs 1/13+1/169")

# ---- Guynn beta_g relations (33)-(45): pure-number near-misses ----
BETA_G = 0.0904274 ** 3               # from (34): |beta_g|^(1/3) = 0.0904274
rel("33", PI * BETA_G, 1 / (PI * ALPHA_INV[0]), "pi|beta_g| ~ 1/(pi alpha^-1)")
rel("34", PHI**5, BETA_G ** (1 / 3), "phi^5 ~ cbrt(beta_g)")
g1 = 2 ** (1 / 3)
rel("36-37", math.sqrt(3) * (g1 - 1), math.sqrt(2) / PI, "beta_m two ways")
rel("38", math.sqrt(3) * (g1 - 1), 5 * PHI**5, "beta_m ~ 5 phi^5")
rel("40a", g1, 1 + 5 * PHI**5 / math.sqrt(3), "cbrt2 from phi^5")
rel("41", g1 + 1 / g1, PHI ** (-1.5), "gamma1+1/gamma1 ~ phi^-3/2")
rel("45", PI, 2 * (g1**2 + g1**-2), "pi from cbrt4")

# ---- gyromagnetic factor (46)-(49) ----
x = PHI**6 / 24
meas("46", 2 + 0.5 * (1 + PHI**6 / 24 - 1 / (1 + PHI**6 / 24)), GE, "g_e golden form 1")
meas("47c", PHI**6 / 12 + math.log(1 - x), (GE[0] - 2, GE[1]), "Delta g_e = phi^6/12+ln(1-phi^6/24)")
rel("47id", 2 * x - (x + x**2 / 2 + x**3 / 3 + x**4 / 4 + x**5 / 5 + x**6 / 6
                     + x**7 / 7), x + math.log(1 - x) + x**8 / 8, "series identity (truncation)")

# ---- Hardy function (50)-(54): the one exact quantum number ----
# max of P = p^2 (1-p)/(1+p) over [0,1]
lo, hi = 0.0, 1.0
for _ in range(200):
    m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
    f = lambda p: p * p * (1 - p) / (1 + p)   # noqa: E731
    if f(m1) < f(m2):
        lo = m1
    else:
        hi = m2
p_star = 0.5 * (lo + hi)
rel("50max-loc", p_star, PHI, "argmax of Hardy P is phi")
rel("50max-val", p_star**2 * (1 - p_star) / (1 + p_star), PHI**5,
    "max Hardy probability = phi^5 EXACTLY")
rel("50closed", PHI**5, (5 * math.sqrt(5) - 11) / 2, "phi^5 = (5 sqrt5 - 11)/2")
# (53) identity h(x) = x^2 (1-x)/(1+x) = x^2 (1-x)^2 gamma^2
worst53 = max(abs(xx**2 * (1 - xx) / (1 + xx) - xx**2 * (1 - xx) ** 2 / (1 - xx**2))
              for xx in [i / 50 for i in range(1, 50)])
rel("53", worst53, 0.0, "h(x) two forms, grid worst")
# (52) q(x) = x^4-2x^3+(1+phi^5)x^2: q(phi) = q(1) = phi^5 exactly
q = lambda xx: xx**4 - 2 * xx**3 + (1 + PHI**5) * xx**2   # noqa: E731
rel("52a", q(PHI), PHI**5, "q(phi) = phi^5")
rel("52b", q(1.0), PHI**5, "q(1) = phi^5")
qp = 4 * PHI**3 - 6 * PHI**2 + 2 * (1 + PHI**5) * PHI
rel("52c", qp, 0.0, "is x=phi a critical point of q? (claimed 'exactly')")

# ---- mass constituents (55)-(58) vs Planck 2018 ----
meas("55", 2 * PHI**5, (OM_B[0] / (OM_M[0] - OM_B[0]),
     OM_B[0] / (OM_M[0] - OM_B[0]) * 0.03), "Om_M/Om_DM vs 2 phi^5")
meas("56", 5 * PHI**5, (OM_M[0] / OM_L[0], OM_M[0] / OM_L[0] * 0.024),
     "Om_m/Om_L vs 5 phi^5")
meas("58", PHI / 4, (OM_B[0] / OM_M[0], OM_B[0] / OM_M[0] * 0.011),
     "baryon fraction vs phi/4")
# El Naschie chapter (66)-(72): the same quantities, different golden values
meas("66", PHI**5 / 2, OM_B, "Om_M = phi^5/2 vs Planck Om_b")
meas("69", 2 * PHI - 0.5, OM_L, "Om_DE = 2phi - 1/2")
meas("72", 1 - (5 * PHI**5 + 1 / (5 * PHI**5)) / 10, OM_L, "Om_PD variant")
inc = sorted([0.683, 0.68392, 0.68808, 0.736068, 0.7331])
rows.append({"id": "OmDE-spread", "class": "INCONSISTENT",
             "lhs": inc[0], "rhs": inc[-1],
             "note": f"five in-paper Omega_DE values spread "
                     f"{(inc[-1]-inc[0])/OM_L[1]:.1f} experimental sigma"})

# ---- absolute-space dimension (60), angles (74)-(120) ----
rel("60a", 5 * PHI, 3 + PHI**5, "5 phi = 3 + phi^5 (exact metallic identity)")
aF = math.degrees(math.atan(5 / (3 * math.sqrt(3)))) - 30
rel("74", aF, 13.897886, "Fibonacci net angle, self-consistency")
rel("76", aF, 4 * PI + (PI + 1) / PI, "alpha_F ~ 4pi+(pi+1)/pi")
rel("78", math.sin(math.radians(13.8863)), PI / (13 + PHI**5), "sine gimmick")
rel("87", (4 / 3) * (PI / math.sin(math.radians(13.900))) ** 2, 228.0,
    "228 from the net angle")
a1 = math.degrees(math.acos((1 / 2 ** (1 / 3)) / 1))  # cos a1 = r0/(2^{1/3} r0)... paper: r0/2r1? use their value
a1 = 50.9527898
rel("106", a1 / 360, PI - 3, "a1/360 ~ pi-3")
rel("107", a1 / 180, PI * PHI**5, "a1/180 ~ pi phi^5")
rel("111", PI**2 * PHI**5, math.radians(50.9899) * 180 / PI / (180 / PI) * 0 + 0.8899967,
    "a1 = pi^2 phi^5 rad = 50.99 deg: check via degrees")
rows[-1]["note"] += f" (pi^2 phi^5 rad = {math.degrees(PI**2 * PHI**5):.4f} deg)"
meas("112", a1 / PHI**2 * (0.938272 + 0.000511), MH,
     "Higgs mass from the DEGREE VALUE of an angle")
rel("114", (1e43 / PI) ** (1 / 20), a1 / PHI**2, "Dirac large number 20th root")
rel("116", math.asin(PHI**5), math.radians(5.173386), "alpha_m definition")
rel("117", math.degrees(math.asin(PHI**5)) * PI**2 / (180 / PI) * (180 / PI) / PI**0,
    51.05927 / PI**2 * PI**2, "am*pi^2 (degrees arithmetic)")
rel("120", PI**2, a1 * aF / 72, "pi^2 ~ a1*aF/72")

# ---- geometric frustration (123)-(129) ----
rel("123", 0.5 * math.log(1.5), 0.20273, "Pauling ice entropy (their digits)")
rel("123b", 0.5 * math.log(1.5), 2 / PI**2, "vs 2/pi^2")
rel("124", 3 + PHI, math.sqrt(13 + PHI**5), "3+phi = sqrt(13+phi^5) EXACT?")
rel("125", 5 * (2 + 1 / PHI), 18 + PHI**5, "18+phi^5 from 5 turns")
rel("127", PHI**5 / (1 + PHI**5), 1 / (12 + PHI**5), "quasicrystal entropy identity")

# ---- superconductivity numerology (130)-(139) ----
rel("130", (8 / PI) * PHI**5, 3 / 13, "optimal doping ~ 3/13")
th = math.asin(math.sqrt(3) / 2) - math.asin(0.6083087)
rel("131", PHI**5 / th, (3 / 5) * PHI_BIG**2 / PHI_BIG**2 * (3 / 5) * (PHI_BIG ** 2) * 0 + 0.22918,
    "sigma0 via theta_ea (their 0.22918)")
rel("133", th, 5 * PHI**3 / 3, "theta_ea ~ 5 phi^3/3")
rel("133b", th, PI / 8, "theta_ea ~ pi/8")
d1 = 8.7210972
rel("136", 2 / d1, 0.22933, "sigma0 ~ 2/delta1 (their digits)")
rel("137", PHI**5, PI / (4 * d1), "phi^5 ~ pi/(4 delta1)")
meas("139", (3 / 5) * (228 + th), ALPHA_INV, "alpha^-1 from 228+theta_ea")

# ---- soccer ball (140) ----
v_exact = (6**2 / 5**3) * ((7 * PHI**-2 + PHI / 6) / (2 * math.sqrt(3) + (PHI**3 * math.sqrt(5)) ** -0.5)) ** 3
rel("140", v_exact, 15.89456977, "their exact expression, self-check")
rel("140b", 15.89456977, (4 / 3) ** (5 / 4) * PHI**-5, "approx 1")
rel("140c", 15.89456977, (13 * 2 / 3) ** (1 / 6) * PHI**-5, "approx 2")

# ---- palindromes and 137 decompositions (141)-(153) ----
rel("145", PI**3, 31.0, "pi^3 ~ 31")
rel("147", 137.0, 4 * 31 + 13, "integer identity")
rel("149", PI * math.sqrt(16 * PI**4 + 8 * PI**3 + 9 * PI**2 + 2 * PI), 137.0,
    "137 from pi (their 137.0002881)")
rel("151", (12 / 13) ** 6 + (13 / 12) ** 6, math.sqrt(5), "(12/13)^6+(13/12)^6 ~ sqrt5")
rel("152", 2 * PHI**5 / (5 * PI), (ALPHA_INV[0] - 137) / PI, "alpha residue vs phi^5")

# ---- Lucas 123 (154)-(164) ----
rel("154", math.sqrt(123 - 1 / 123), 11 + PHI**5, "sqrt(123-1/123) = 11+phi^5 EXACT?")
rel("155", (123 - 1 / 123) ** (1 / 5) / 1, PHI_BIG**2 / 1, "5th root = Phi^2?")
rel("156", (123 - 1 / 123) ** (1 / 10), PHI_BIG, "10th root = Phi?")
rel("159", math.sqrt(123 / 34), math.sqrt(3 + PHI), "123/34 vs 3+phi")
rel("161", 494.0, (13 / 6) * 228, "coefficient identity")
rel("163", 123 * PHI / 2, 494 / 13, "123 phi/2 ~ 38")

# ---- Great Pyramid (165)-(170): Kepler-pyramid THEOREM vs monument ----
# For a square pyramid with cos(face angle) = phi (Kepler pyramid):
# insphere radius r = phi^{3/2} (half-base 1), height h = sqrt(Phi),
# V_sphere / V_pyramid = pi phi^{9/2} / sqrt(Phi) = pi phi^5  EXACTLY.
r_in = PHI ** 1.5
h_kep = math.sqrt(PHI_BIG)
ratio = ((4 / 3) * PI * r_in**3) / ((4 / 3) * h_kep)
rel("165", ratio, PI * PHI**5, "Kepler pyramid: V_O/V_pyr = pi phi^5 (exact theorem)")
rel("168", math.degrees(math.acos(PHI)), 51.82729, "Kepler face angle")
# the monument: base 230.33 m, height 146.59 m (surveyed originals)
slope_meas = 146.59 / (230.33 / 2)
rows.append({"id": "165-monument", "class": "NEARMISS",
             "lhs": slope_meas, "rhs": math.sqrt(PHI_BIG),
             "rel_dev": abs(slope_meas - math.sqrt(PHI_BIG)) / math.sqrt(PHI_BIG),
             "note": f"monument slope {slope_meas:.5f} vs Kepler sqrt(Phi) = "
                     f"{math.sqrt(PHI_BIG):.5f} vs pi-theory 4/pi = {4/PI:.5f}: "
                     "the two theories differ by 0.10%, inside build tolerance - "
                     "the monument cannot decide"})
meas("169", (4 / 3) * (math.degrees(math.acos(PHI)) + a1), ALPHA_INV, "alpha from two angles")

# ---- Table 5: the flexibility ladder ----
ladder = [50.911688, 50.929581, 50.94871, 50.952703, 50.952789, 50.957217,
          50.958916, 50.970739, 50.973355, 50.973452, 50.980384, 50.989902,
          51.026552, 51.059277]
rows.append({"id": "table5", "class": "INCONSISTENT",
             "lhs": ladder[0], "rhs": ladder[-1],
             "note": f"the paper's own Table 5 lists {len(ladder)} interchangeable "
                     f"'conditions' for alpha_1 spanning {ladder[0]:.3f}..{ladder[-1]:.3f} "
                     f"({(ladder[-1]-ladder[0])/ladder[0]*100:.2f}% wide): any target in the "
                     "window is 'matched' by construction"})

# ---- control: identities that RUN (the TV slide) ----
def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(2, n + 1) if sieve[i]]


P = primes_upto(200000)
lnz2 = sum(1 / (m * p ** (2 * m)) for p in P for m in range(1, 40)
           if p ** (2 * m) < 1e18)
rel("riemann-lnzeta", lnz2, math.log(PI**2 / 6), "ln zeta(2) = sum_p sum_m 1/(m p^2m)")
Px = [p for p in P if p <= 100]


def pi_of(y):
    return sum(1 for p in P if p <= y)


J100 = sum(1 / m for p in P for m in range(1, 8) if p**m <= 100)
J_from_pi = sum(pi_of(100 ** (1 / n)) / n for n in range(1, 8))
rel("riemann-J", J100, J_from_pi, "J(100) both ways")

# ---- summary ----
counts = {}
for r in rows:
    counts[r["class"]] = counts.get(r["class"], 0) + 1
worst_excl = sorted([r for r in rows if r["class"] == "EXCLUDED"],
                    key=lambda r: -r["sigma_exp"])
out = {"counts": counts, "rows": rows}
(HERE / "otto25_mech.json").write_text(json.dumps(out, indent=1) + "\n")
print("classification:", counts)
print("\nEXACT (the paper's true algebra):")
for r in rows:
    if r["class"] == "EXACT":
        print(f"  {r['id']:>12}  {r['note']}")
print("\nEXCLUDED against measurement (top):")
for r in worst_excl[:10]:
    print(f"  {r['id']:>12}  {r['sigma_exp']:.3g} sigma   {r['note']}")
print("\nNEARMISS pure-number relations (sorted by rel dev):")
nm = sorted([r for r in rows if r["class"] == "NEARMISS" and "rel_dev" in r],
            key=lambda r: r["rel_dev"])
for r in nm:
    print(f"  {r['id']:>12}  {r['rel_dev']:.2e}  {r['note']}")
for r in rows:
    if r["class"] == "INCONSISTENT":
        print(f"\nINCONSISTENT  {r['id']}: {r['note']}")
sys.exit(0)
