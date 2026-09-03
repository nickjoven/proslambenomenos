<!-- evidence: scripts/experiments/p46_derive.py, scripts/experiments/p46_derive.json, scripts/experiments/p46_aftermath.py, scripts/experiments/p46_results.json, scripts/verify/p46_aftermath.py -->
# P-46 working document: the slip aftermath is off-band

A-25 asked for slip aftermaths recorded with wavebench against the
P-45 current. Recording is cheap; the line exists because the
reading R-44 attached to its recording was wrong twice, and a
reading that is wrong twice wants a registration, not a caption.

## What R-44 got wrong, and what the momentum law says instead

R-44 read the rotor at ~56 at event + 40 and explained it as a mean
drag from the adjacent bonds. Summing the equation of motion over
the ring kills every bond force by telescoping: dP/dt = f - gamma P
for the total momentum P = sum v, at every instant, slip or no
slip. The rotor is spinning up on the damping time 1/gamma = 50,
and 1 - e^{-40/50} = 0.55 of the terminal f/gamma = 98 is 54. The
registered run reads the fraction 0.569 at Delta = 40, 0.870 at
100, 0.982 at 200. No drag.

R-44 also read "182 out-flowed into the ring" as an aftermath
number. The bookkeeping had accumulated from t = 0, and the
pre/post split in this line shows where it came from: before the
event the loaded site pumps the ring's rigid drift f/(N gamma)
(pre-event out-flow 183 at gamma = 0.02); after the event the ring
returns about 1. The ring's share obeys, exactly,
dP_ring/dt = -gamma P_ring - (sin D_b - sin D_{b-1}): the rotor's
torque on the ring is the two-bond force, and the derive layer's
mutant that drops one bond fails this identity at O(1).

## What the derive layer did to the design

- The linear-chain anchor (L-9) caught three instrument errors
  before registration: the lock-in read half the amplitude (a real
  sinusoid demodulates to A/2); the continuous-time response was
  off by ~(dt Omega)^2, the size of the gamma = 0.02 band, so the
  registered response is the exact Euler-Cromer discrete one; and
  the rotor's phase as reference was detuned by 1.5 percent by the
  ring's residual drift, so the reference is the bond phase.
- R-45b (2026-09-03): the '(dt Omega)^2' above was the order of the
  map's frequency error, not of the amplitude gap. The discrete and
  continuous responses differ in |A_1| by 4.13e-04 / 1.21e-04 /
  6.64e-05 at gamma 0.02 / 0.04 / 0.1, inside the floors (1.33e-03 /
  2.58e-04 / 6.27e-04); the registered band is the floor, and clause
  (c) is integrator-blind at that precision. Under dt halving
  (p46_results_dt0.0005.json, p46_dt_check.py) A_1 keeps its offset
  from the map's response to 1e-5 - the residual below the floor is
  the cell's, not the step's.
- Two lock-in floors are derived and read from each run: the
  in-band wave leaks 2a/(T(Omega - 2)), and the demodulated
  product's 2-Omega term leaks A_d/(Omega T). The anchors'
  residuals (2e-4, 1e-4) are the second floor. The floors decide
  the registered offsets: offset 2 is unmeasurable at gamma = 0.02
  (floor 12x the signal for any window in the run), offset 3
  nowhere.
- The DC-torque clause was removed. Step-quantized cycle windows
  leaked A_T dt/T_w, which at Omega^3/gamma scaling read K ~ 50 to
  850 for a coefficient expected near 1; interpolating the
  crossings fixed that, and the two clean readings then disagreed
  in sign (-0.917 at gamma 0.1, +1.899 at gamma 0.04, floors 0.004
  and 0.55). The leading-order lag argument does not give the
  coefficient. Reported against the 1-percent-held-drift scale;
  not registered.
- The drift clause's reference moved from the event to Delta = 10,
  because the rotor crosses the band edge inside the first unit
  and the launch phase is exactly the part the linear picture does
  not cover.

## What the registered run read (R-45)

All three clauses at all three gammas. The reading worth keeping:
the aftermath of a slip on this ring has no propagating footprint
in the evanescent phase. The rotor's neighbour moves at 1/Omega,
the next site at c/Omega^2 of that, and at gamma = 0.02 the third
site would sit at 1e-10 - under any floor the run can reach. The
ring's drift, which the loaded site had pumped for two hundred
units before the event, drains at rate gamma to a part in 10^4,
and what the rotor gives back is 0.4 units of energy against the
183 it took. The released strain wave circling the loop is on the
wavebench page and is the one thing this line records without
claiming; its shape is A-25's remaining question if anyone wants
it, and the current is now the instrument to ask it with.

The unpinned DC torque stays on record: K = -0.738 at gamma 0.1
and 0.139 +- 0.519 at 0.04 in the registered run, -0.917 and
+1.899 in the validation cells. A coefficient that changes sign
between two cells above its floor is not a coefficient yet.
