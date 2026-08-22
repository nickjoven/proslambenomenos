<!-- evidence: scripts/experiments/p4_twisted_inertial_ring.py, scripts/experiments/p4_lowdamp.py, scripts/experiments/p4_forcebalance.py, scripts/experiments/p4_results_lowdamp.json, scripts/experiments/p4_mud_results.json -->
# P-4 working document: holonomy vs gate on a twisted inertial ring

Governed by P-4 (PREDICTIONS.md): expects the period-doubling gating
threshold UNCHANGED between twisted and control; mind-change is a
threshold shift surviving N, friction parameters, drive velocity, and
independent reimplementation. Model and both runs:
scripts/experiments/p4_twisted_inertial_ring.py; results in
p4_results_pinned.json / p4_sweep_pinned.log and
p4_results_clamp.json / p4_sweep_clamp.log. Prose carries no load.

## Run 1 - substrate-pinned ring (outside the Kawano regime)

Ring of N inertial phase oscillators, sine coupling J = 1, damping
0.05, bow node at N/2 dragged at v = 0.3 with Coulomb stick-slip
(mu_s = 1, mu_d = 0.5, normal force F_N swept), one bond with offset
pi (twisted) or 0 (control). First smoke run with NO restoring term:
0 slips at every F_N - a free ring co-rotates with the bow (rigid
rotation zero mode). Added on-site -K sin(theta), K = 1.

Result: slip period ~ 8 time units at N = 8, 9, 16, 17 alike
(period/round-trip 1.0 at N = 8-9, 0.5 at N = 16-17). The slip clock
is local (substrate + bow), not a returning corner: the on-site term
gaps the chain and kills propagation. No period doubling anywhere.
The variant does not implement the Kawano/Guettler mechanism and
cannot answer P-4. Stuck threshold F_N = 2.1 identical in all 8
configurations - trivially, the bound 2J + gamma*v = 2.015.
Unregistered observation: sliding -> stick-slip onset is higher in
the twisted ring at every N (control 1.1/1.2/<=0.9/1.1, twisted
1.2/1.4/1.1/1.3 for N = 8/9/16/17).

## Run 2 - clamped ring (Helmholtz regime)

Substrate removed; site 0 clamped (the bridge); bow at N/2; so the
ring is a string of length N fixed at one point with the bow at its
midpoint, Helmholtz period 2N/c = 2 T_round. F_N from 0.6 to 2.3,
T = 400, slips counted after T = 200, Euler dt = 0.01 (not
symplectic - numerical caveat stands).

Findings, stated only as far as the data goes:
1. Slip period/round-trip sits at 2.1-2.6 for all N and both twist
   states across the stick-slip band: the clamp variant IS in the
   Helmholtz regime. The f0/2 analog would be ratio ~4.
2. Ratios >= 4 appear ONLY in twisted rings near the stuck edge:
   N = 8 at F_N = 1.8/1.9 (4.37, 7.47; 6 and 5 slips), N = 9 at
   1.9/2.0 (5.62, 5.38; 4 and 3 slips). Control maxima in the same
   band: 2.66 (N=8), 3.06 (N=9), 2.87 (N=16), 2.43 (N=17). At N = 16
   and 17 the twisted rings reach only 3.06 and 2.67. With 3-6 slips
   per window the ratio is a median of 2-5 gaps: statistically thin.
   This leans AGAINST P-4's expectation at small N and does not meet
   P-4's own bar (does not survive N at this resolution; no parameter
   variation; no reimplementation). Recorded as inconclusive.
3. Robust and unregistered: the twisted ring's sliding -> stick-slip
   onset is higher at every N in this variant too (control 0.8/1.1/
   1.3/1.8, twisted 1.1/0.8*/1.8/1.2 - *N = 9 is the exception in
   onset but then shows a wide sliding island; N = 17 twisted is
   mostly sliding). Same sign as run 1 in 7 of 8 configurations.
   Mechanism not identified; a twisted clamped ring must carry a
   half-winding background (pi/N per bond) and the bow node sits in
   it - whether that background changes the stick force balance is a
   one-page calculation not yet done.

## Next (designed, not run unless chosen)

Refinement run near the stuck edge: F_N 1.5-2.1 step 0.05, T = 1200,
count after 400, N = 8, 9, 16, 17, both twist states; then the
half-winding force-balance calculation; then a second
implementation (velocity-Verlet, independent code) before any claim
touches the P-4 mind-change condition.

## Force-balance check (p4_forcebalance.py, 2026-08-21)

Static: site 0 clamped, pi bond adjacent, uniform gradient pi/N per
bond is balanced at every free node - no static pre-load at the bow.
Displacing the bow node by phi against both arcs (N/2 bonds each)
gives restoring force 2J cos(pi/N) sin(2 phi/N) twisted versus
2J sin(2 phi/N) control: the twisted ring holds LESS, so static
analysis predicts an EARLIER stick-slip onset for the twisted ring -
the opposite of the observed shift. Dynamic probe at F_N = 1.0
("sliding"): the bow node is in fact stationary (mean w_B - v =
-0.300, ring force 0.514 against kinetic friction 0.500), the bow
slides over it, and the statistics are identical to three decimals
for twisted and control at N = 8 and 16. Conclusion: the onset shift
is not a static holonomy effect; it arises in the transient where
the node is first dragged, and is unexplained. Mood: the static
calculation is elementary and checkable; the "unexplained" is
literal.

## Run 3 - refinement (p4_results_refine.json, T = 1200, count after 400, F_N 1.50-2.10 step 0.05)

With 3x longer windows and gap min/max recorded alongside the median:

1. Control rings are in a CLEAN periodic Helmholtz regime: gap_min =
   gap_max = 2.4-2.7 round trips across the stick-slip band at every
   N, irregular only at the stuck edge (F_N >= 1.95 for N = 8, 9;
   2.00 for N = 17; never for N = 16).
2. Twisted rings lose periodicity much earlier: from F_N = 1.70 (N=8),
   intermittently from 1.55 (N=9), from 1.85 (N=16), 2.00 (N=17).
   The irregular state is BURSTY - gaps from 0.3-0.5 round trips
   (chatter: slip, brief stick, slip) up to 10-19 round trips - not a
   period-doubled sequence. Run 2's ratios of 4-7 were medians of
   this bursty distribution over 3-6 events and are hereby retracted
   as evidence of doubling. No period doubling exists in this model
   at this resolution, in either ring.
3. RETRACTED: the "robust onset shift" of runs 1-2. With longer
   windows the sliding -> stick-slip onset is: N=8 control <=1.50 vs
   twisted 1.60; N=9 control 1.60 vs twisted <=1.50; N=16 1.70 vs
   1.75; N=17 1.80 vs 1.70 - two each way. The earlier 15/16
   consistency was a short-window artifact. The longer window did
   what it is for.
4. Standing: the twist advances the loss of Helmholtz periodicity in
   3 of 4 N (absent at N=17). Same sign where present. This is NOT
   P-4's registered observable (there is no doubling threshold to
   shift), has no parameter variation, and the sub-transit chatter
   gaps are exactly where an Euler stick-slip switch could be
   generating numerical artifacts - so an independent velocity-Verlet
   implementation is required before this is even a recorded
   observation rather than a hint.

P-4 status: OPEN, and the model class may not contain the gate the
prediction is about (as P-1's model class did not contain the index
set). Before any R-entry: find period doubling in the CONTROL ring
first (Kawano's regime is high force AND slow bow; v_bow has not been
varied), then test the twist against it. If no parameter regime of
this model doubles, P-4 resolves as model-class vacuity and says so.

## Run 4 - control-only v_bow sweep (p4_results_vsweep.json, T = 1200, count after 400)

v_bow in {0.05, 0.1, 0.2, 0.5}, F_N 1.2-2.0, N = 8 and 16, clamped
control ring. All stick-slip sequences are strictly periodic (gap_min
= gap_max) except at the v = 0.5 stuck edge.

1. Two regimes, no doubling between them. FAST bow (v = 0.5): period
   2.2-2.6 round trips, flat in F_N - wave-locked (Helmholtz). SLOW
   bow (v <= 0.1): period grows continuously with F_N and scales as
   ~F_N/v (N=8: 6.8 -> 16.3 at v = 0.05; 4.2 -> 8.2 at v = 0.1), taking
   non-integer values (6.8, 7.3, 8.0, ...) - bow-limited relaxation
   oscillation: the slip fires when quasi-static loading reaches
   mu_s F_N, and the launched wave has decayed (damping 0.05 over
   7-16 round trips) before it could matter. The corner never
   triggers anything in this regime.
2. The one Kawano-adjacent feature: at v = 0.2 the period JUMPS by
   about one round trip (N=8: 2.5 -> 3.3 between F_N 1.3 and 1.4;
   N=16: 2.4 -> 3.2 between 1.4 and 1.5) - consistent with the slip
   waiting one extra corner arrival. But the plateaus are not flat
   (3.3 -> 4.1 with F_N), so it is partial locking, not the gated
   every-second-arrival state, and it is a +1 step, not x2.
3. Diagnosis: Kawano's gate needs the RETURNING CORNER to be what
   tips the node over threshold. Here either the bow's loading does
   it alone (slow) or the wave does it every pass (fast); no regime
   has loading-alone insufficient AND corner-plus-loading sufficient
   with a corner that survives the trip. The control is damping 0.05
   per unit time against round trips of 8-16: the corner is gone.
   Next parameter, designed not run: damping g down to 0.01-0.005
   with v = 0.1-0.2, looking for flat integer plateaus at 2 and 4
   round trips in the control before any twist enters.

P-4 status unchanged: OPEN; the model has not yet exhibited the gate.

## Run 5 - low damping, slow bow, large N, control only (p4_lowdamp.py, p4_results_lowdamp.json)

N in {64, 128}, damping g in {0.01, 0.002}, v in {0.05, 0.1}, F_N
0.3-1.8, 40 round trips each, 14 parallel workers.

1. HELMHOLTZ MOTION REACHED, first time in this model: at g = 0.002
   and F_N <= 0.6 (v = 0.1) or F_N = 0.3 (v = 0.05), the slip period
   is 2.02-2.07 round trips, flat in F_N, identical at N = 64 and 128,
   gap_min = gap_max. Two round trips is the Helmholtz period of a
   string of length N bowed at its midpoint. At g = 0.01 the same
   rows are "sliding" (node stationary): the corner no longer
   survives the trip. The corner now exists and gates.
2. A FORMULA retracts the "integer plateaus": quasi-static loading of
   a ring whose stiffness at the bow is 4J/N reaches mu_s F_N after
   displacement N mu_s F_N/(4J), i.e. after time N mu_s F_N/(4 J v),
   so period/round-trip = mu_s F_N/(4 J v) with NO wave involved.
   This predicts 3.0 at (F_N, v) = (0.6, 0.05) and (1.2, 0.1) - the
   observed 3.07-3.20 - and tracks every loading-limited row to
   within ~15% (deviations grow with F_N as the sine coupling
   saturates). The "3" and "4.3" values are grid coincidences of
   F_N/(4v), not locking. Same trap as d4_nopin's rational snaps,
   caught the same way: derive the null before reading the grid.
   Run 4's periods obey the same formula.
3. The gate region is numerically contaminated. Kawano's every-
   second-arrival state would sit where loading alone fails within
   2 round trips but succeeds within 4, with the corner present:
   g = 0.002, v = 0.1, F_N between 0.8 and 1.1 (formula crosses 2 at
   F_N = 8v). Exactly those rows (F_N = 0.9, and 1.5 at both N) show
   100+ slips with gaps of 0.03-0.06 round trips - sub-transit
   chatter from the forward-Euler stick-slip switch, not physics.
   Nothing can be read there until the integrator is fixed.

Status: the control exhibits the corner-gated regime; the x2 gate is
not yet observed; its expected location is identified and is where
the current integrator fails. Next, designed not run: an event-
located stick-slip switch (or velocity-Verlet with sub-step root
finding on the stick condition), then F_N 0.7-1.2 in steps of 0.05 at
g = 0.002, v = 0.1, N = 128, control first. P-4 remains OPEN; the
twist has not been tested in any regime where the gate exists.

## Correction to run 5, item 2 (2026-08-22, from the catalog gate)

"Tracks every loading-limited row to within ~15%" overstated: the
rows whose predicted period is near the Helmholtz value 2 (F_N = 0.9,
v = 0.1 at both N) are 27-37% off - loading and wave timing interact
there. The formula holds to < 20% where F_N/(4 J v) >= 3 (10 rows);
catalog/c12 carries the scoped statement and would have failed on the
original wording.

## Adversarial audit (2026-08-22) and resolution

A context-free auditor refuted the thread's premise. Findings, in
severity order, each checked:

S1 (decisive). In the clamped variant the pi bond sits next to the
clamped site, so the force on site N-1 sees the clamp as phase pi
while site 1 sees it as phase 0: the "ring" is an open Dirichlet
chain with its ends held at 0 and pi. The loop that would carry a
holonomy is cut by the clamp. Linearised, the twisted equilibrium is
a uniform strain pi/N on every bond, so the twisted system is the
control with stiffness J cos(pi/N): same modes, speed lower by
sqrt(cos(pi/N)) - 4% at N = 8, 0.06% at N = 64. Measured Helmholtz
periods at N = 64: control 2.0292 / twisted 2.0309 (F_N = 0.3),
2.0714 / 2.0716 (0.6). Every run in the Helmholtz regime (2-5) was in
this variant; run 1, the only genuine ring, had no propagation. No
run had both ingredients of the registered question. P-4's
"threshold UNCHANGED" was guaranteed by construction and its
mind-change condition could not fire. Corollary: X-8's "half-integer
lines always on" is false for the force/velocity dynamics of
antisymmetric-offset phase oscillators, clamped or free - the
small-oscillation spectrum is integer in both; half-integer lines
live only in the Fourier transform of e^{i theta_j} along the site
index (the background half-winding), which the slip observable never
sees. T_round = N/c at N = 8, 9 is 4% short for the twisted ring.

S2 (wrong diagnosis). The sub-transit "chatter" is physical: the
minimum gap is 3.5-4.4 time units at every N, invariant under an 8x
change in dt (dt = 0.02 ... 0.0025 at N = 64: 104-114 slips, gap_min
0.046-0.064) - it is 2 pi / sqrt(2J) = 4.44, the massive bow node's
own oscillation period on its two bonds. A massive Coulomb contact
re-sticks on a velocity crossing and re-slips on its local period
whenever the ring force hovers near mu_s F_N; a continuum string's
bow point has no mass. The planned "event-located integrator" was
aimed at the wrong cause; the fix would be a massless or overdamped
contact. Also: the bulk update is Euler-Cromer (first-order
symplectic), so "Euler, not symplectic" in runs 2 and 5 was wrong.

S3 (formula incomplete). period/round = mu_s F_N/(4 J v) has the
right stiffness constant but assumes re-stick at zero ring force,
which holds only because mu_d = mu_s/2 makes the undamped overshoot
land at (2 mu_d - mu_s) F_N = 0. At N = 64, g = 0.01, v = 0.05, F_N =
0.9: mu_d = 0.25 -> 6.95, 0.5 -> 5.09, 0.75 -> 3.12 (recomputed;
catalog c13). Every "loading-limited" row also has slip duration
1.04-1.11 round trips - the node slides until the launched wave
returns - so "no wave involved" was false: the period is one wave-
limited slip plus a loading time depending on mu_s - mu_d. c12's
factor-2 mutant could not see this; c12 is rescoped and c13 added.

S4. "Helmholtz motion reached" rests on three rows; the auditor's
re-run recorded re-stick times and found slip fraction 0.52 of the
period, consistent with beta = 1/2 - the claim survives a check the
repo had not made.

S5. P-4's observable is not well posed in this model class: no
doubling in any run; with S1, "threshold unchanged" would stay true
even if a gate appeared; the N-parity expectation has no mechanism
(the uniform pi/N gradient is the ground state for every N).

S6. Code: friction is zero on the slip-onset step (rel == 0
placeholder); the re-stick condition is vacuous at rel == 0 and only
the force test prevents instant re-stick; the median of two gaps
returns the larger (run 2's retracted ratios were biased upward).

Resolution: P-4 resolves as MODEL-CLASS VACUITY (R-3): the registered
question cannot be posed in the clamped variant, and the free ring
has no corner. The expectation "threshold unchanged" held vacuously;
the secondary N-parity expectation was mechanism-free; the
prediction was not falsifiable in this class - a prediction-design
error, recorded as such. What survives: the stiffness constant 4,
the Helmholtz period 2N/c for the clamped geometry, run 3's
retraction of doubling, X-12's corner diagnosis, and the three-
decimal twisted/control identity - now understood as the expected
result, not a puzzle. Reopening would require a new P-line with a
model that keeps the loop (no clamp; a massless contact; N >= 64; low
damping) and an observable that the background half-winding can
actually reach.

## Wording correction (2026-08-23, from building the capstone notebook)

Run 5 item 2 said "the '3' and '4.3' values are grid coincidences of
F_N/(4v)". Only the 3.0 rows are exact grid values of the formula
((F_N, v) = (0.6, 0.05) and (1.2, 0.1)); the ~4.3 rows sit at
predictions 3.75 and 4.5, inside the formula's stated 25%. They are
loading-limited, not coincidences. The capstone notebook flags both
kinds in its table rather than repeating the sentence.
