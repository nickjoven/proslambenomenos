"""Janosi-Hanamoto: under a driven wheel the soil shear stress builds monotonically from the front of the contact patch to the rear, tau(j) = tau_max (1 - e^(-j/K)) with shear displacement j = i x, so the imprint is front-back asymmetric whenever slip i > 0 - a track in mud records direction.
Source: Janosi & Hanamoto 1961; Wong, Theory of Ground Vehicles ch. 2. Mutant: claim the shear profile is symmetric about the patch centre."""
import math, sys
from _common import mutant_flag, finish

i, K, L = 0.2, 0.05, 0.4      # slip ratio, shear modulus length, patch length
tau = [1 - math.exp(-i * x / K) for x in [L * k / 100 for k in range(101)]]
monotone = all(b > a for a, b in zip(tau, tau[1:]))
symmetric = max(abs(tau[k] - tau[100 - k]) for k in range(101)) < 1e-6
ok = symmetric if mutant_flag() else (monotone and not symmetric)
sys.exit(finish(ok, f"shear at front {tau[0]:.3f}, centre {tau[50]:.3f}, rear {tau[100]:.3f}; monotone {monotone}; symmetric {symmetric}"))
