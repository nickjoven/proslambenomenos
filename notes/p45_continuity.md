<!-- evidence: scripts/experiments/p45_derive.py, scripts/experiments/p45_derive.json, scripts/experiments/p45_continuity.py, scripts/experiments/p45_results.json, scripts/verify/p45_continuity.py -->
# P-45 working document: ring energy continuity, the footprint as a derived current

The P-36 line ended with a slip observed and classified by its
channel, and with the aftermath unregistered: the loaded node tears
out and spins, the ring relaxes, and "where the energy went" was a
description, not an observable. L-2 says the fix is a conservation
identity derived up front. This line is that identity, in the
convention the lattice heat-transport literature already uses
(LC-34: Lepri-Livi-Politi 2003, eqs. 11, 16, 17):

    h_j = v_j^2/2 + (u_{j-1} + u_j)/2,   u_j = 1 - cos D_j
    J_j = -(1/2) sin(D_j) (v_j + v_{j+1})
    dh_j/dt + (J_j - J_{j-1}) = -gamma v_j^2 + f v_j delta_{jb}

The pi bond enters only through D_j = theta_{j+1} - theta_j - A_j,
so the identity has no seam term; summed over the ring the current
telescopes to dE/dt = f v_b - gamma sum v^2.

## What the derive layer did to the design

Three things changed between the design and the registration, all
forced by measurements in p45_derive.py:

1. The residual band. The design said "1e-13". A fixed number is a
   guessed band (L-3); the registered bound is 32 eps T_j, the
   floating-point floor scaled by the state's own term magnitudes,
   so it is derived per state and follows the velocity scale (the
   rotor regime has v ~ 100). The layer reads the residual at ~4
   percent of that bound at both scales.
2. The convergence clause. The design said "the defect halves
   under dt -> dt/2; pin the ratio, band from the pin". The rotor
   validation cell (control N = 16 above its fold, dt = 0.001
   ladder) read ratios 2.0016 and 2.0017 for the per-site defect:
   the deviation from 2 did not contract, because at that step
   size the ratio is already at 2 to a part in a thousand and the
   residual deviation is not first-order dominated. A contraction
   clause would have fired on instrument grounds. Replaced by the
   order-discrimination band [2^0.5, 2^1.5] (the geometric
   midpoints between a first-order scheme's ratio 2 and its
   neighbours 1 and 4) plus monotone decrease; contraction is
   reported, not registered.
3. The slip cell's load. The design said "the P-36 slip cell",
   whose onset sat one grid step BELOW the derived fold (R-34: an
   inertial-transient effect). Under refinement that event could
   vanish; the registered cell sits at fold + 0.005, where no
   equilibrium exists and the event is dt-independent by the
   static argument (8c). The step size there comes from the rotor
   speed f/gamma: dt0 = 0.001 gives 0.098 rad per step where
   P-36's 0.02 gave ~2 rad per step - P-36's channel classification
   never depended on resolving the rotor (it read the winding's
   lattice departure), but a balance through the slip does.

## The mutants, and what the global balance cannot see

The current-blind mutant (J = -sin(D_j) v_j, no velocity average)
fails the per-site identity at O(1) and passes the global balance
at 1e-15: any J whatsoever telescopes away on a ring. The
site-resolved clause is therefore the load-bearing one, and a
line that had registered only the global balance would have had
no falsifier for the current at all. The sink-blind mutant fails
both. The gauge-blind mutant (A dropped from u) is identical to
the clean identity on the control ring and fails only at the two
seam sites of the twisted ring - the deterministic signature of
"A enters only through D", which is what clause (c) measures.

## The falsifier's route

scripts/verify/p45_continuity.py takes the site-energy time
derivative by forward-mode dual numbers (h evaluated on
theta + eps v, v + eps a), not by the hand-written chain rule; own
seed, N = 48, own velocity-Verlet trajectory with the damping at
the old velocity. Its first draft tripped its own bound at a
ratio of 1.36 on the control ring: the term sum T had counted
only the final derivative, not the pieces it was assembled from,
so the 32-operation budget was being charged against too small a
magnitude. Fixed to sum the exposed pieces; the ratio then reads
0.03, in line with the experiment's route. Recorded because it is
the same species of error as the bound it guards against.

## What the registered run read (R-44)

All five clauses held; the numbers are in R-44 and
p45_results.json. The reading worth keeping here is the aftermath
in the derived current: at event + 40 the loaded site holds 1570
of the 2828 injected, dissipated 1076 on the spot, and passed 182
into the ring through its two bonds; the ring dissipated 166 of
that and kept 16. Relative to the pre-event state every other
site LOST energy (0.4 to 1.1 each): before the slip the free ring
drifted rigidly at f/(N gamma) = 1.54, and once the loaded node
took the load alone the rest decelerated. The footprint radius is
zero. The rotor spins at ~56 at event + 40 (the stored 1566 = v^2/2)
rather than f/gamma = 98 because the adjacent bonds carry a mean
drag - that drag IS the 182 - and a drive at 56 sits nearly
thirty times above the lattice band edge at 2,
so nothing propagates. None of this is claimed; it is what the
current reads, and A-25 is the registration that would claim it.
