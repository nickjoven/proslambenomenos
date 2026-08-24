"""Sorkin's everpresent-Lambda count fluctuation: if Lambda is a Poisson fluctuation in the causal-set element count N of the Hubble 4-volume, Lambda ~ 1/sqrt(N) in Planck units lands within 2 orders of magnitude of the observed Lambda*l_P^2 ~ 2.9e-122 (it lands within ~0.4); the naive 1/N misses by ~120 orders, and this was in the literature before the 1998 supernova measurement.
Source: Sorkin, Int. J. Theor. Phys. 36, 2759 (1997) and earlier (1990); Ahmed, Dodelson, Greene, Sorkin, Phys. Rev. D 69, 103523 (2004); observed Lambda from Planck 2018 (A&A 641, A6 (2020)): H0 = 67.4 km/s/Mpc, Omega_Lambda = 0.685. Mutant: use 1/N instead of 1/sqrt(N)."""
import math
import sys

from _common import mutant_flag, finish

H0 = 67.4 * 1000.0 / 3.0857e22        # s^-1  (Planck 2018)
OMEGA_L = 0.685                        # Planck 2018
T_P = 5.391247e-44                     # Planck time, s (CODATA 2018)
L_P = 1.616255e-35                     # Planck length, m (CODATA 2018)
C = 2.99792458e8                       # m/s (exact)

lam_obs = 3.0 * OMEGA_L * H0 ** 2 / C ** 2 * L_P ** 2   # dimensionless: Lambda * l_P^2
N = (1.0 / (H0 * T_P)) ** 4            # Hubble 4-volume in Planck 4-volumes
pred = N ** (-1.0 if mutant_flag() else -0.5)
ok = abs(math.log10(pred) - math.log10(lam_obs)) <= 2.0
sys.exit(finish(ok, f"N = (1/(H0 t_P))^4 = 10^{math.log10(N):.1f}; "
                    f"fluctuation estimate 10^{math.log10(pred):.1f} vs observed "
                    f"Lambda l_P^2 = 10^{math.log10(lam_obs):.1f}"))
