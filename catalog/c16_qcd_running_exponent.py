"""The one-loop QCD mass-running exponent gamma0/(2 beta0) is 12/23 for n_f = 5 (gamma0 = 8, beta0 = 11 - 2 n_f/3, both per d ln mu^2 with alpha_s/4pi).
Source: standard RGE (e.g. Buras, Les Houches lectures); PDG QCD review. Mutant: harmonics' mixed-normalisation formula (8/3)/(2*(33 - 2 n_f)/(12 pi)) = 2.19 (ERRATA E20)."""
import math, sys
from _common import mutant_flag, finish

nf = 5
expo = (8.0 / 3) / (2 * (33 - 2 * nf) / (12 * math.pi)) if mutant_flag() else 8.0 / (2 * (11 - 2 * nf / 3))
ok = abs(expo - 12 / 23) < 1e-9
sys.exit(finish(ok, f"exponent = {expo:.4f} (12/23 = {12/23:.4f})"))
