#!/usr/bin/env python3
"""P-27 derivation layer (pre-registration): the decoherence-diffusion
squeeze on classical gravity. Oppenheim's postquantum classical
gravity (PRX 13, 041040) survives only inside a two-sided squeeze:
interferometric coherence LOWER-bounds the spacetime diffusion D2
(long coherence demands noise), while low-force-noise experiments
UPPER-bound it (the noise would shake test masses). OSSW (Nature
Comms 14, 7910 / arXiv 2203.01982) derive three kernel-class
squeezes, eqs. (44), (46), (47); Janse et al. (PRR 6, 033076 /
arXiv 2403.08912) tighten the upper side with 45 modern experiments
through the figure of merit FOM_D2 = N S_a. Everything here has a
derivable answer and runs before the registered window table.

Derived facts:
  EQ1  mechanized dimensional analysis: all three squeeze
       inequalities are dimensionally consistent, with D2 carrying
       kg^2 s m^-3; the lower bounds carry lambda in the
       DENOMINATOR (long coherence -> more required diffusion) -
       any lambda flip fails the unit algebra.
  EQ2  the six OSSW printed bounds recomputed from their own pinned
       inputs (N = 1e26, sigma_a = 1e-7 m s^-2, dT = 100 s - the
       averaging time OSSW never print; Janse attest it - r_N =
       1e-15 m, m_N = 1e-26 kg, V_b = r_E^2 h, fullerene M_lambda =
       1e-24 kg, lambda = 10 s^-1, V_lambda = 1e-25 m^3, R_lambda =
       1e-9 m). The three LOWER bounds reproduce exactly; the three
       printed UPPER bounds sit 1.3-2.7 orders from their own
       inputs' arithmetic (signed deltas pinned) - order-of-
       magnitude prose, mechanized.
  EQ3  the Janse Table I internal audit: S_a = S_F/m and
       FOM = N S_a^2 per row, machine-checked across all 46 rows;
       N vs m consistency spot-checked where the composition is
       unambiguous.
  EQ4  the update rule is a pure FOM rescaling: bound_new =
       bound_OSSW x FOM_new/FOM_Cavendish (FOM_Cav = 1e14); Janse
       eqs. (4)-(5) reproduce under it from the Gisler row (FOM
       0.298). Their eq. (5) lower bound 1e-35 is NOT derivable
       from any stated input set; candidates computed and pinned
       (OSSW printed 1e-40; Fein-updated M^2/(R lambda) = 1.3e-38).
  EQ5  closure figures of merit: the FOM at which each surviving
       window shuts, FOM_close = FOM_Cav x lower/upper.
Pinned -> p27_registration.json.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAILURES = []

G = 6.674e-11
LP = 1.616e-35
MP = 2.176e-8
AMU = 1.66054e-27


def check(name, ok, detail=""):
    print(f"  {name}: {'ok' if ok else 'FAIL'} {detail}")
    if not ok:
        FAILURES.append(name)
    return ok


# ----------------------------------------------------------------- EQ1
class Dim:
    """Dimension vector (kg, m, s)."""

    def __init__(self, kg=0, m=0, s=0):
        self.v = (kg, m, s)

    def __mul__(self, o):
        return Dim(*[a + b for a, b in zip(self.v, o.v)])

    def __truediv__(self, o):
        return Dim(*[a - b for a, b in zip(self.v, o.v)])

    def __pow__(self, k):
        return Dim(*[a * k for a in self.v])

    def __eq__(self, o):
        return self.v == o.v

    def __repr__(self):
        return f"kg^{self.v[0]} m^{self.v[1]} s^{self.v[2]}"


U = {
    "G": Dim(-1, 3, -2), "D2": Dim(2, -3, 1), "sigma_a": Dim(0, 1, -2),
    "T": Dim(0, 0, 1), "N": Dim(), "r_N": Dim(0, 1, 0),
    "m_N": Dim(1, 0, 0), "V_b": Dim(0, 3, 0), "M_l": Dim(1, 0, 0),
    "lam": Dim(0, 0, -1), "V_l": Dim(0, 3, 0), "R_l": Dim(0, 1, 0),
    "l_P": Dim(0, 1, 0), "m_P": Dim(1, 0, 0),
}


def eq1():
    print("EQ1 mechanized dimensional analysis")
    u = U
    # eq. (44): sigma_a^2 N r_N^4 T / (V_b G^2) >= D2 >= M_l^2/(V_l lam)
    lhs44 = u["sigma_a"] ** 2 * u["N"] * u["r_N"] ** 4 * u["T"] \
        / (u["V_b"] * u["G"] ** 2)
    rhs44 = u["M_l"] ** 2 / (u["V_l"] * u["lam"])
    check("EQ1 (44) lhs = D2 units", lhs44 == u["D2"], repr(lhs44))
    check("EQ1 (44) rhs = D2 units", rhs44 == u["D2"], repr(rhs44))
    # eq. (46): sigma_a^2 N r_N^4 T/(m_N G^2) >= lP^3 D2/mP >= M_l/lam
    lhs46 = u["sigma_a"] ** 2 * u["N"] * u["r_N"] ** 4 * u["T"] \
        / (u["m_N"] * u["G"] ** 2)
    mid46 = u["l_P"] ** 3 * u["D2"] / u["m_P"]
    rhs46 = u["M_l"] / u["lam"]
    check("EQ1 (46) lhs = mid units", lhs46 == mid46, repr(lhs46))
    check("EQ1 (46) rhs = mid units", rhs46 == mid46, repr(rhs46))
    # eq. (47): sigma_a^2 N r_N^3 T/G^2 >= lP^2 D2 >= M_l^2/(R_l lam)
    lhs47 = u["sigma_a"] ** 2 * u["N"] * u["r_N"] ** 3 * u["T"] \
        / u["G"] ** 2
    mid47 = u["l_P"] ** 2 * u["D2"]
    rhs47 = u["M_l"] ** 2 / (u["R_l"] * u["lam"])
    check("EQ1 (47) lhs = mid units", lhs47 == mid47, repr(lhs47))
    check("EQ1 (47) rhs = mid units", rhs47 == mid47, repr(rhs47))
    # the lambda-flip mutant target: multiplying by lambda breaks all
    bad = u["M_l"] ** 2 * u["lam"] / u["V_l"]
    check("EQ1 lambda flipped fails", bad != u["D2"], repr(bad))
    return {}


# ----------------------------------------------------------------- EQ2
INPUTS = {
    "N": 1e26, "sigma_a": 1e-7, "T": 100.0, "r_N": 1e-15,
    "m_N": 1e-26, "r_E": 6.371e6, "h_atm": 1e4,
    "M_l": 1e-24, "lam": 10.0, "V_l": 1e-25, "R_l": 1e-9,
}
PRINTED = {
    "cont_upper": 1e-41, "cont_lower": 1e-24,
    "disc_upper": 1e-1, "disc_lower": 1e-25,
    "nonloc_upper": 1e-9, "nonloc_lower": 1e-40,
}


def recompute_bounds(p=INPUTS):
    Vb = p["r_E"] ** 2 * p["h_atm"]
    core = p["sigma_a"] ** 2 * p["N"] * p["T"]
    return {
        "cont_upper": core * p["r_N"] ** 4 / (Vb * G ** 2),
        "cont_lower": p["M_l"] ** 2 / (p["V_l"] * p["lam"]),
        "disc_upper": core * p["r_N"] ** 4 / (p["m_N"] * G ** 2),
        "disc_lower": p["M_l"] / p["lam"],
        "nonloc_upper": core * p["r_N"] ** 3 / G ** 2,
        "nonloc_lower": p["M_l"] ** 2 / (p["R_l"] * p["lam"]),
    }


def eq2():
    print("EQ2 OSSW printed bounds vs their own inputs")
    rec = recompute_bounds()
    deltas = {}
    for k, printed in PRINTED.items():
        d = math.log10(printed / rec[k])
        deltas[k] = d
        tol = 0.5 if k.endswith("lower") else 3.0
        check(f"EQ2 {k}: printed {printed:.0e} vs recomputed "
              f"{rec[k]:.2e}", abs(d) <= tol,
              f"delta {d:+.2f} orders")
    return {"recomputed": rec, "printed": PRINTED,
            "signed_deltas_orders": deltas}


# ----------------------------------------------------------------- EQ3
COMPOSITIONS = {  # unambiguous rows: (molar mass g/mol, atoms/molecule)
    # The Cavendish row is deliberately excluded: its N = 1e26 is
    # OSSW's stylized kg-mass input (already pinned in EQ2), not a
    # composition-derived count (1 kg of Pb has 2.9e24 atoms).
    "Gisler": (140.28, 7), "Seis": (140.28, 7), "Norte": (140.28, 7),
    "Martynov": (60.08, 3), "Monteiro": (60.08, 3),
    "Fuchs": (1081.1, 17), "Timberlake ’23": (1081.1, 17),
    "Armano": (196.97, 1), "Westphal": (196.97, 1),
}


def load_table():
    with open(os.path.join(HERE, "janse_table1.json")) as f:
        return json.load(f)


def eq3():
    print("EQ3 Janse Table I internal audit (46 rows)")
    pin = load_table()
    bad_sa, bad_fom, bad_n = [], [], []
    for r in pin["rows"]:
        if r["SF"] and r["m_kg"] and r["Sa"]:
            if abs(r["SF"] / r["m_kg"] / r["Sa"] - 1) > 0.05:
                bad_sa.append(r["ref"])
        if r["N"] and r["Sa"] and r["FOM"]:
            if abs(r["N"] * r["Sa"] ** 2 / r["FOM"] - 1) > 0.05:
                bad_fom.append(r["ref"])
        for key, (mm, nat) in COMPOSITIONS.items():
            if r["ref"].startswith(key):
                n_chk = r["m_kg"] / (mm * 1e-3 / 6.02214076e23) * nat
                if abs(n_chk / r["N"] - 1) > 0.10:
                    bad_n.append((r["ref"], n_chk, r["N"]))
    check("EQ3 S_a = S_F/m rows within 5%", len(bad_sa) <= 2,
          f"violators: {bad_sa}")
    check("EQ3 FOM = N S_a^2 rows within 5%", len(bad_fom) <= 2,
          f"violators: {bad_fom}")
    check("EQ3 N vs composition within 10%", len(bad_n) <= 1,
          f"violators: {bad_n}")
    return {"bad_sa": bad_sa, "bad_fom": bad_fom,
            "bad_n": [b[0] for b in bad_n]}


# ----------------------------------------------------------------- EQ4
FOM_CAV = 1e14
FEIN = {"M": 25000 * AMU, "lam": 133.0}


def eq4():
    print("EQ4 the FOM rescaling rule and the Janse windows")
    pin = load_table()
    gisler = [r for r in pin["rows"] if r["ref"].startswith("Gisler")][0]
    disc_new = PRINTED["disc_upper"] * gisler["FOM"] / FOM_CAV
    nonloc_new = PRINTED["nonloc_upper"] * gisler["FOM"] / FOM_CAV
    check("EQ4 Janse eq (4) upper from Gisler",
          abs(math.log10(disc_new / 1e-16)) <= 0.5,
          f"{disc_new:.2e} vs printed 1e-16")
    check("EQ4 Janse eq (5) upper from Gisler",
          abs(math.log10(nonloc_new / 1e-24)) <= 0.5,
          f"{nonloc_new:.2e} vs printed 1e-24")
    # their eq (5) lower 1e-35: candidates
    fein_disc = FEIN["M"] / FEIN["lam"]
    fein_nonloc = FEIN["M"] ** 2 / (INPUTS["R_l"] * FEIN["lam"])
    check("EQ4 Fein discrete lower stays ~1e-25",
          abs(math.log10(fein_disc / 1e-25)) <= 0.7,
          f"{fein_disc:.2e}")
    print(f"  EQ4 nonlocal lower candidates: OSSW printed 1e-40; "
          f"Fein-updated {fein_nonloc:.2e}; Janse print 1e-35 "
          f"(underivable from stated inputs - pinned as audit note)")
    return {"disc_upper_gisler": disc_new,
            "nonloc_upper_gisler": nonloc_new,
            "fein_disc_lower": fein_disc,
            "fein_nonloc_lower": fein_nonloc}


# ----------------------------------------------------------------- EQ5
def eq5():
    print("EQ5 closure figures of merit")
    out = {
        "disc_close": FOM_CAV * PRINTED["disc_lower"]
        / PRINTED["disc_upper"],
        "nonloc_close_ossw": FOM_CAV * PRINTED["nonloc_lower"]
        / PRINTED["nonloc_upper"],
        "nonloc_close_janse": FOM_CAV * 1e-35 / PRINTED["nonloc_upper"],
    }
    for k, v in out.items():
        print(f"  EQ5 {k}: FOM = {v:.1e} m^2 s^-3")
    return out


def main():
    pins = {"inputs": INPUTS, "printed": PRINTED, "fom_cav": FOM_CAV,
            "fein": FEIN}
    pins["EQ1"] = eq1()
    pins["EQ2"] = eq2()
    pins["EQ3"] = eq3()
    pins["EQ4"] = eq4()
    pins["EQ5"] = eq5()
    out = os.path.join(HERE, "p27_registration.json")
    with open(out, "w") as f:
        json.dump(pins, f, indent=1)
    print(f"\npinned -> {out}")
    if FAILURES:
        print("DERIVATION FAILURES:", FAILURES)
        return 1
    print("all derivations ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
