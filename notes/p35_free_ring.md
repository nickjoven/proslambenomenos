<!-- evidence: scripts/experiments/p35_derive.py, scripts/experiments/p35_derive.json -->
# P-35 working document: the reopened P-4 - holonomy on a free ring

R-3 resolved P-4 as model-class vacuity: the clamp cut the loop, so
no run had both a holonomy and a threshold, and "threshold
unchanged" held by construction. The audit tail wrote the reopen
recipe: keep the loop, massless/overdamped contact, N >= 64, low
damping, an observable the background half-winding can reach. P-35
is that line. This document holds the derive layer (run BEFORE
registration, per AGENTS.md item 8) and, after the registered
cells, the results.

## Design decisions and their reasons

1. FREE ring, pi offset on bond 0 (twisted) vs none (control).
   The loop is intact; the holonomy exists.
2. DEAD-LOAD contact: a constant point force f at the antipode
   b = N/2, ramped softly. Massless - the contact carries no
   state. A velocity-belt bow cannot pose the question here: a
   free ring in steady stuck co-rotation asks only gamma N v of
   grip (0.064 at N = 64, v = 0.05), two orders below the fold,
   so a belt-driven free ring sits forever in the trivial stuck
   state. The dead load reaches the fold. Stick-slip friction was
   P-4's costume and the source of R-3's S2/S6 artifacts; it is
   not part of the reopened question.
3. The reopened question, distilled from P-4's own mind-change
   text ("the bundle class does dynamical selection"): the
   holonomy's STATIC budget is derived below (the fold ratio);
   does low-damping inertial dynamics add selection beyond it?

## Derive layer (p35_derive.py, all before registration)

EQ1 - winding sectors, exact. Equilibria have uniform covariant
strain (2 pi n - pi)/N twisted vs 2 pi n/N control; covariant
winding W = n - 1/2 vs n. Numeric: damped relaxation from noise at
N = 64 lands on W = -0.5000000000000003 (twisted) and 3.5e-16
(control). The two twisted ground sectors are exactly degenerate.
Half-integer W is the kinematic content of the holonomy and an
observable that reaches it.

EQ2 - linear detector null. Stiffness about a twisted ground
sector is J cos(pi/N): any twisted-vs-control frequency ratio
inside [sqrt(cos(pi/N)), 1] is ground-state strain, not dynamics.
Width 6.0e-4 / 2.7e-4 / 1.5e-4 at N = 64 / 96 / 128.

EQ3 - conservation identity (8b). Bond forces cancel in Newton
pairs on the loop, so the site-mean obeys the same rigid-body
equation for twisted and control given the same contact history:
verified along a driven run at 1.1e-15 (bond sum) and 5.2e-18
(mean residual). The site-mean is holonomy-blind BY IDENTITY -
P-33's telescoping lesson derived up front. Registered observables
are therefore W(t), the bond-strain field, and the spatial DFT of
e^{i theta}.

EQ4 - the strain budget (the load-bearing derivation). In steady
drift each node needs force f/N, so bond forces climb linearly
around the loop with the single drop at the contact:
sin(s_j) = c + m f/N, m = 0..N-1, with the loop constraint
sum s_j = 2 pi n - pi (twisted) vs 0 (control) pinning c. The
quasi-static branch ends at the largest f admitting a root - the
fold, solved exactly:

    N     fold(control)  fold(twisted)  ratio      1 - ratio
    64    2.03174        1.96325        0.96629    0.0337
    96    2.02105        1.97623        0.97782    0.0222
    128   2.01575        1.98249        0.98350    0.0165

An O(1/N) shift (deficit ~ 2.1/N) with derived sign, size, and
N-scaling: this is precisely what the clamped model destroyed
(there the twist was gauge-equivalent to uniform strain and the
threshold difference was O(1/N^2) in frequency only).
Theorem-let: ring reflection about the pi bond maps sector
W = +1/2 to W = -1/2 at the same drive, so the two twisted folds
are EXACTLY degenerate (solver gap 3.6e-5 = bisection floor).
The degeneracy survives dynamics (the reflection commutes with
the equations of motion), so ANY measured sector split is
instrument noise: a self-calibrating null floor (8a).
Derivation error corrected before registration: a first pass
predicted a helping/hurting sector asymmetry (1 -+ sin(pi/N))
from a "hottest bond reaches capacity" shortcut; the exact solver
refuted it (arcsin's nonlinearity near the fold makes the
shortcut wrong, and the reflection symmetry makes any sector
asymmetry impossible). Kept in the record as a derivation error
caught by the layer it was designed for.
Numeric anchor (overdamped staircase, step 0.01, hold 250):
control 2.04 vs 2.0317; sectors both 1.98 vs 1.9633. The
staircase bias is one-sided (it can only overshoot the fold), and
the measured sector split is 0.00 at this resolution.

EQ5 - spectral address, exact. The spatial DFT of e^{i theta_j}
in sector n peaks at fractional mode index n - 1/2 (twisted) vs n
(control), amplitude N: half-integer lines live in THIS
observable and nowhere in the displacement dynamics (R-3's S1
corollary, now the design instead of the post-mortem).

EQ6 - contact-timescale exclusion band (8a). A released node
rings at sqrt(2 J cos delta): period 4.446 at N = 64. Slip-gap
structure in [3.56, 5.33] is instrument, not holonomy. Gap
statistics are reported min/median/max (S6's median bias does not
recur).

EQ7 - domain validity (8c). Sweep grid derived from the fold:
f in [fold - 0.10, fold + 0.06] step 0.005 per configuration;
soft ramp T_ramp = 200 (impulse N v spread so the transient
constraint force stays an order below the fold); measurement
window T_meas = 500 >= 5/gamma at the smallest gamma = 0.01;
gamma in {0.01, 0.02, 0.04} (low-damping recipe, waves survive
33-130 round trips); dt = 0.02 with a dt/2 validation cell.

## Registered protocol (before any registered cell ran)

Cells: {control, twist n=0, twist n=1} x N in {64, 96, 128} at
gamma = 0.02, plus gamma in {0.01, 0.04} at N = 64. Onset f* =
first grid f whose held segment shows a winding change within
T_meas. Observables: f*, W(t) at every sample, spectral address
on the 1/8 fractional-mode grid, slip-gap min/median/max.
Validation cell (declared): N = 64 control, gamma = 0.02, onset
stable under dt -> dt/2 within one grid step; only stability
inspected.

Clause bands (each traced to a derivation or a measured
instrument floor, R-32 corollary):
(a) sector arithmetic: |W - (n - 1/2)| <= 1e-6 twisted (integer
    control) at every sample between slip events; slip events
    change W by integers.
(b) onset ratio: f*(twisted, N) / f*(control, N) within
    fold_ratio(N) +- band(N), band(N) = 2 x 0.005 / fold(N)
    + split(N) + 1e-4, where split(N) = |f*(n=1) - f*(n=0)| is
    the measured instrument floor from the exact degeneracy.
    Evaluated at split = one grid step: band(64) = 0.0075.
(c) sector degeneracy: split(N, gamma) <= 0.005 (one grid step)
    everywhere - the instrument null; a firing here means the
    instrument is broken, not physics.
(d) the ratio in (b) stays in band at gamma = 0.01 and 0.04
    (N = 64). Absolute onset vs the fold is reported UNREGISTERED
    (transient overshoot at low gamma has no derived band; P-2's
    lesson - no guessed windows).
(e) spectral address: the 1/8-grid DFT peak sits at n - 1/2
    (twisted) vs n (control) at every pre-onset sample.

## P-35 cells, R-33, and the reopening's second act (2026-08-29)

The quick cells (N = 64, gamma = 0.02, scripts/experiments/
p35_results.json): sector arithmetic held at 6.8e-13 / 1e-16;
sector degeneracy held at 3.6e-5 (floor: one grid step = 5e-3);
twisted onsets at fold - 0.005, both sectors. Clause (b) was
unmeasurable - no control onset at any level while the raw contact
strain diverged to 4.7e4 with W pinned at 0.000 - and (e) fired in
every cell (8/28 bad pre-onset address samples in control).
Diagnosis in scripts/experiments/p36_channel.py, derived not
patched: the control fold is the contact PAIR saturating together
(closed form 2N/(N-1), solver to 2e-6), so its supercritical
motion is a symmetric paired slip - +2 pi and -2 pi through the
two contact bonds, net W unchanged, the loaded node tearing out to
spin at ~ f/gamma. The twisted loop constraint (sum s = +-pi)
de-centers the profile and saturates the TOP bond alone (bottom
sin -0.933 at N = 64): a single W-changing slip. The holonomy
selects the channel. The address observable belongs to the
unloaded ring only (8.3 rad of profile excursion at half-fold
moves the DFT peak to -1/8 with no slip anywhere near).
R-33 records the firings as detector responses underived at
registration (both 8a); P-36 re-registers with a bond-slip
detector both channels reach and the channel itself as a derived
clause. This is the P-32 -> P-33 pattern; the stop rule (two
firings on one clause line) binds P-36.
