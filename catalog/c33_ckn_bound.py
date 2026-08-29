"""Cohen-Kaplan-Nelson: an effective field theory whose IR box of size L must not contain states that would collapse to a black hole obeys L^3 Lambda_UV^4 <~ L M_P^2, i.e. rho_max ~ M_P^2 / L^2; taking L = the Hubble radius gives rho_CKN ~ M_P^2 H0^2, which lands within ~1.1 orders of magnitude of the observed dark-energy density, while the naive EFT estimate rho ~ M_P^4 misses by ~122 orders.
Source: Cohen, Kaplan, Nelson, PRL 82, 4971 (1999) (their eq. 1); observed density from Planck 2018 (H0 = 67.4 km/s/Mpc, Omega_Lambda = 0.685). CKN's own lab consequence (their g-2 discussion) interops with LC-21. Mutant: use the naive cutoff rho = M_P^4.
"""
import math
import sys

from _common import mutant_flag, finish

H0 = 67.4 * 1000.0 / 3.0857e22        # s^-1 (Planck 2018)
OMEGA_L = 0.685                        # Planck 2018
G = 6.67430e-11                        # m^3 kg^-1 s^-2 (CODATA 2018)
C = 2.99792458e8                       # m/s (exact)
HBAR = 1.054571817e-34                 # J s (CODATA 2018)

# observed dark-energy density (J/m^3)
rho_obs = OMEGA_L * 3.0 * H0 ** 2 * C ** 2 / (8.0 * math.pi * G)
# CKN: rho_max ~ M_P^2 / L^2 in natural units; in SI with L = c/H0
# this is rho_CKN = c^2 H0^2 / G x (1/1) up to O(1):
rho_ckn = C ** 2 * H0 ** 2 / G
# naive EFT: Planck density rho_P = c^7/(hbar G^2)
rho_naive = C ** 7 / (HBAR * G ** 2)
pred = rho_naive if mutant_flag() else rho_ckn
gap = abs(math.log10(pred) - math.log10(rho_obs))
ok = gap <= 2.0
sys.exit(finish(ok, f"rho_obs = 10^{math.log10(rho_obs):.2f} J/m^3; "
                    f"CKN M_P^2 H0^2 -> 10^{math.log10(rho_ckn):.2f} "
                    f"(gap {abs(math.log10(rho_ckn) - math.log10(rho_obs)):.2f} dex); "
                    f"naive M_P^4 -> 10^{math.log10(rho_naive):.2f} "
                    f"(gap {abs(math.log10(rho_naive) - math.log10(rho_obs)):.1f} dex)"))
