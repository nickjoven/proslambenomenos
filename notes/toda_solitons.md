# Solitons on the inertial nonlinear chain (the vocabulary's last term earned)

2026-08-23, worktree wt-solitons. scripts/experiments/toda_solitons.py
(results toda_results.json), toda_plots.py (figure page), catalog c29
(0.4 s, mutant = linear force). Figure page published as an artifact.

Model: unit-mass chain, fixed ends, neighbour force f(r) = 1 - e^{-r}
(Toda 1967) or f(r) = r (linear null; same sound speed c = 1).
Velocity-Verlet, dt = 0.02, N = 600. Exact one-soliton: r_n(t) =
-ln(1 + sinh^2(k) sech^2(k n - sinh(k) t), speed v/c = sinh(k)/k.

Results (all computed, all in the JSON):
1. Exact soliton, k = 1, 120 time units: Toda keeps peak 0.8676 ->
   0.8672 and width 3 sites while travelling 141 sites (v = 1.18c);
   the linear chain halves the peak and doubles the width.
2. Gaussian compression pulse (amp 1.2, width 4): the Toda chain
   emits a 1-2 site soliton at v ~ 1.37c plus a dispersive tail; the
   linear chain keeps width 7, moves at c, decays slowly.
3. Speed law: measured v/c = 1.050, 1.117, 1.183, 1.300, 1.483 at
   k = 0.5..1.6 against sinh(k)/k = 1.042, 1.110, 1.175, 1.306,
   1.485 - within 1%.

Of record: the first run used a periodic ring and a first-order
velocity field; the ring forced a compensating stretch at the wrap
(a bogus second pulse), and the velocity approximation shed 17% of
the peak as radiation. Fixed ends and exact finite-difference
velocities removed both. The catalog mutant (linear force) retains
65.5% of the peak - far from the 99.9% the fact requires.

Vocabulary: "soliton" moves from cited to demonstrated (c29). What
this does NOT demonstrate: collisions, the KdV continuum limit,
integrability, or anything about spacetime; gravitational solitons
(Belinski-Zakharov 1978), boson stars and oscillatons share the
name by the same balance (nonlinearity vs dispersion) and nothing
here computes them. Mood: none.
