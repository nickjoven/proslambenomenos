# P-9: N-parity of plateau shrinkage on the pinned twisted ring

Registered (PR #41, first commit) before computing; run 2026-08-23 in
worktree wt-p9-nparity. Script scripts/experiments/p9_nparity.py;
results p9_results.json (E1's initial condition) and
p9_results_attractor.json (attractor-controlled; pinned by catalog
c28). Model and edge-resolution method identical to E1 step 3
(d4_edge_resolved.py) with N a variable.

## Run 1 - E1's initial condition theta_i = 0.13 i: confounded

| K | N=4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|
| 1.0 control | 0.0740 | 0.0740 | 0.0354 | 0.0119 | 0.0031 | 0.0014 |
| 1.0 twisted | 0.0237 | 0.0292 | 0.0350 | 0.0342 | 0.0331 | 0.0326 |
| 1.4 control | 0.137 | 0.137 | 0.115 | 0.100 | 0.091 | 0.117 |

The control's plateau collapses with N. The control ring has
identical sites and should lock as a single circle map (width
0.07397 at K = 1): E1's initial condition spans 0.13 (N - 1) turns,
which for N >= 6 lands the ring in a winding attractor with a
different (narrower) plateau. E1 step 3 at N = 4 (0.39 turns) reached
the in-phase attractor and is unaffected; the method is not N-safe.
Correction of record against E1's method, not its N = 4 result.

## Run 2 - attractor-controlled initial conditions (control in-phase; twisted half-winding i/2N)

| K | N=4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|
| 1.0 control | 0.07397 at every N |
| 1.0 ratio | 0.301 | 0.399 | 0.473 | 0.471 | 0.447 | 0.444 |
| 1.4 control | 0.137 at every N |
| 1.4 ratio | 0.110 | 0.161 | 0.297 | 0.437 | 0.274 | 0.215 |

## Against P-9
Mind-change (even/odd alternation in Lazarides' sense) did NOT fire:
the sign pattern of r(N+1) - r(N) is (+,+,0,-,-) at K = 1.0 and
(+,+,+,-,-) at K = 1.4 - no alternation at either coupling. The core
expectation (no parity selection; the Josephson sign discrepancy is
the drive type) holds. The secondary expectation FAILED: r(N) does
not approach 1. At K = 1.0 it saturates near 0.45 from N = 6 on - the
seam's effect is not diluted by more sites; at K = 1.4 it rises to a
maximum at N = 7 and falls - non-monotone, unexplained, and with
differences between consecutive N well above the ~3% measurement
resolution of P-8. Mood: the saturation is consistent with the twist
acting through the half-winding background strain pi/N on EVERY bond
(each site sits at a different phase of the pinning potential) rather
than through the seam alone; untested. Not claimed: bias-driven
arrays; absolute widths; any mechanism for the K = 1.4 maximum.
