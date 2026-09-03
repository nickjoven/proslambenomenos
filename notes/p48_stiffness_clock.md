<!-- evidence: scripts/experiments/p48_derive.py, scripts/experiments/p48_derive.json, scripts/experiments/p48_kappa.py, scripts/experiments/p48_results.json, scripts/verify/p48_kappa.py -->
# P-48 working document: the stiffness is a clock

The owner asked for a stiffness column kappa as the honest
refinement axis of the ring, after the audit noted that P-46's
"evanescent above the band edge" is a property of the lattice. The
first thing the layer measured was that kappa is not a parameter:

    (kappa, gamma, f, t)  =  (1, gamma / sqrt kappa, f / kappa, sqrt kappa t)

exactly, and exactly for the Euler-Cromer map when dt scales with
sqrt kappa. For dyadic sqrt kappa the two computations are the same
floating-point operations in a different order of scaling by powers
of two, and the trajectories are bit-identical through the slip
(deviation 0.0 at 409000 steps). For kappa 0.5, 2, 3 the roundings
differ and the trajectories part by 1e-10 on phases of 1e4 - the
accumulated rounding, against a derived bound of 1e-5.

So the band top 2 sqrt kappa and the rotor speed f/gamma move
together, and "the rotor sits above the band" is f/gamma > 2 at
kappa = 1: a statement about the damping the cells were run at.
P-46's cells sat at 98, 49, 20. The ladder kappa stood in for is a
damping ladder at fixed reduced load.

## What the ladder read, and the instrument it needed

Under the P-46 instrument unchanged, the tail ratio A_2/A_1 sat
inside its band at gamma 0.1 and 0.2 and then 19 to 33 percent
above the band top from gamma 0.35 to 0.8, against floors of 11 to
24 percent. The linear-chain anchor at the same frequencies landed
on the closed form to 4e-3, so the pipeline was clean and the
departure was the ring's. Two candidates:

- A parametric resonance of the rotating junction with the band
  (LC-37, Miroshnichenko et al. eq. 34: omega = Omega/2 in band for
  Omega < 4). Measured and refused: the Omega/2 content at offsets
  2 to 6 is 2e-3 against a far-field RMS of 3e-2, and the far field
  grows smoothly through Omega = 4. It is the slip's long-wavelength
  relaxation: at N = 64 the k = 1 mode (omega_1 = 0.098) is
  overdamped for gamma > 0.2 and decays at omega_1^2/gamma, 0.02 per
  unit at gamma 0.5, so it is alive in every near-band window.
- The reference. The bond phase theta_b - theta_{b+1} carries the
  neighbour's own displacement, and that slow relaxation moves the
  neighbour by about half a radian during the window. Demodulating
  against the rotor's phase alone puts the ratio inside the band at
  every cell, at the price of smearing A_1 by the neighbour's slow
  wander (to 0.69 to 0.86 of the bond reading). The smear is common
  to A_1 and A_2 and cancels in the ratio, which is what clause (c)
  registers.

The bond-reference excess itself is not explained. The first-order
mixing term of a reference carrying an Omega-component of index
A_1/Omega, (X/2) v_slow, covers a third of it where it peaks, and the
excess is not monotone along the ladder (4, 24, 23, 27, 16, 4
percent). Per L-3 that is a reading, not a clause; A-29 carries it.
On the falsifier's N = 16 ring the k = 1 mode is underdamped and gone
by the window, the two references agree to 0.6 percent, and a
reference-blind mutant cannot be made to bite - recorded, not
pinned.

## What is registered

The identity at the floor and bit for bit; the tail law under the
rotor reference from Omega = 9.8 to 2.35, a fifth above the band
top. Reported: the rotor's slowing along the ladder (0.999 to 0.954
of f/gamma, 0.868 in band), the event times lengthening with gamma
(the saddle-node bottleneck), the in-band cell at gamma 1 where the
wave floor is negative and the instrument is not built.

## What this does to the audit's worry

The grid smuggled less than it seemed and something different. The
band edge is a unit, not a smuggled number; what the lattice fixes
is that the slip has no continuum limit at all - the sine bond has
no small-strain limit at fixed winding, so kappa to infinity is a
linear string with no slip. The ring is an array. Its dictionary to
Josephson arrays is exact; its dictionary to a continuous pi ring
does not exist in this model.
