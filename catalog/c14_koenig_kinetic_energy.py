"""Koenig (kinetic energy): T = M V_cm^2/2 + T_relative for any particle system.
Source: Goldstein ch. 1. Mutant: omit the M V_cm^2/2 term."""
import random, sys
from _common import mutant_flag, finish

random.seed(5)
N = 7
m = [random.uniform(0.5, 2) for _ in range(N)]
r = [[random.uniform(-1, 1) for _ in range(3)] for _ in range(N)]
v = [[random.uniform(-1, 1) for _ in range(3)] for _ in range(N)]
M = sum(m)
R = [sum(m[i] * r[i][k] for i in range(N)) / M for k in range(3)]
V = [sum(m[i] * v[i][k] for i in range(N)) / M for k in range(3)]
cross = lambda a, b: [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
T = sum(0.5 * m[i] * sum(v[i][k] ** 2 for k in range(3)) for i in range(N))
T_rel = sum(0.5 * m[i] * sum((v[i][k] - V[k]) ** 2 for k in range(3)) for i in range(N))
T_pred = T_rel + (0.0 if mutant_flag() else 0.5 * M * sum(V[k] ** 2 for k in range(3)))
ok = abs(T - T_pred) / T < 1e-12
sys.exit(finish(ok, f"|T - split| / T = {abs(T - T_pred) / T:.1e}"))
