"""Koide's relation Q = (m_e + m_mu + m_tau)/(sqrt m_e + sqrt m_mu + sqrt m_tau)^2 equals 2/3 to 6e-6 with PDG 2024 pole masses.
Source: Koide 1982; PDG 2024 (m_e = 0.51099895, m_mu = 105.6583755, m_tau = 1776.86 MeV). Mutant: m_tau = 1700 MeV, which moves Q by 1e-2."""
import math, sys
from _common import mutant_flag, finish

me, mmu, mt = 0.51099895, 105.6583755, (1700.0 if mutant_flag() else 1776.86)
Q = (me + mmu + mt) / (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mt)) ** 2
ok = abs(Q - 2 / 3) < 1e-5
sys.exit(finish(ok, f"Q - 2/3 = {Q - 2/3:+.1e}"))
