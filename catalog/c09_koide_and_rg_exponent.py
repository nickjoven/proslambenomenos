"""Koide Q with PDG 2024 pole masses is 2/3 to 6e-6; the one-loop QCD mass-running exponent is gamma0/(2 beta0) = 12/23 for n_f = 5.
Source: Koide 1982; PDG 2024; gamma0 = 8 (mass anomalous dimension, d/d ln mu^2 with alpha_s/4pi), beta0 = 11 - 2 n_f/3. Mutant: harmonics' mixed-normalisation formula (8/3)/(2*(33-2 n_f)/(12 pi)) = 2.19."""
import math, sys
from _common import mutant_flag, finish

me, mmu, mt = 0.51099895, 105.6583755, 1776.86
Q = (me + mmu + mt) / (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mt)) ** 2
nf = 5
expo = (8.0 / 3) / (2 * (33 - 2 * nf) / (12 * math.pi)) if mutant_flag() else 8.0 / (2 * (11 - 2 * nf / 3))
ok = abs(Q - 2 / 3) < 1e-5 and abs(expo - 12 / 23) < 1e-9
sys.exit(finish(ok, f"Koide Q - 2/3 = {Q - 2/3:+.1e}; running exponent = {expo:.4f} (12/23 = {12/23:.4f})"))
