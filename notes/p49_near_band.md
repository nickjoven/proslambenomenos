<!-- evidence: scripts/experiments/p49_derive.py, scripts/experiments/p49_derive.json, scripts/experiments/p49_near_band.py, scripts/experiments/p49_results.json, scripts/verify/p49_near_band.py -->
# P-49 working document: the late window

A-29 asked for the mechanism of P-48's near-band excess and an
instrument for the band. The layer's first move was an exact
accounting rather than a third estimate: each site's velocity split
into its drive-locked fundamental (least squares on the bond phase,
which is the drive's own phase), its running mean over a rotor
period, and the rest; each reference demodulating each piece.

Two things fell out. The bond-phase reading is the drive-locked
fundamental by construction, so the "reference excess" of R-47 was
the fundamental's own: at offset 2 it exceeds the linear root by 24
to 27 percent at Omega 5.6 to 3.9. And the rotor-phase reading is
that fundamental times the characteristic function of the
neighbour's displacement - 0.733 measured against 0.731 predicted
from an x_1 rms of 0.77 rad - plus slow and harmonic leakage that
at offset 2 offsets the excess. P-48's clause (c) held by leakage.
R-47a records that; the P-48 numbers stand.

## What the excess is

Tied to the slip's long-wavelength relaxation. At N = 64 the k = 1
mode is overdamped for gamma above 0.2 and decays at omega_1^2/gamma,
0.02 per unit at gamma 0.5, so every P-48 window sat inside it with
the neighbour wandering by half a radian. Six windows down the
relaxation show the excess falling 27, 4.1, 2.1, 0.9, 0.2, -0.1
percent as the slow displacement falls from 0.77 to 0.05 rad rms.
In a late window the tail law holds to a tenth of a percent at
Omega 3.9 and 5.6, and in band at Omega 1.69 to 0.2 percent of a
band top, with no wave floor at all: the launched transient is gone
by decay, so frequency no longer has to separate it from the driven
tail. That is the in-band instrument A-29 asked for, and it is
cheaper than the one P-46 built.

The mechanism of the excess is not claimed. A_1's deficit is near-
linear in the slow amplitude and A_2's excess faster; a nonlinear
coupling of the slow strain into the drive-frequency response is
the candidate, and it is one derivation away from a clause. The
literature pass (LC-38a) found the root's source and the undamped
chain's in-band and edge behaviour, and found nothing on
demodulation against a reference that carries the measured system's
own state - which is what L-14 now says in the ledger's voice.

## What is registered

The late-window tail law near and in the band; the monotone decay
of the excess with the slow mode; the smear identity. Reported: A_1
in band (6.6 percent below the linear end-site response at Omega
1.69 with the neighbour's strain at 0.42 rad and the rotor at 0.868
of f/gamma), offset 3, the shape of the excess.

## Corrections on record (R-48a, 2026-09-03)

The e^{-6} window holds at gamma 0.35 and 0.5 only (exponents 3.7 and
2.9 at 0.8 and 1.0); the in-band cells were read with slow content of
9 and 6 percent of A_2 inside bands 8 and 21 percent wide. The ratio
sits above the band proper at 0.35 and 1.0, A_1 below its band at 0.35
and 0.5, inside by the self floor. The smear identity is the
estimator's (its falsifier check passes on any series). Clause (c) is
co-decay, not attribution; A-30 is two interventions and a remainder,
and run C replaces the launch rather than removing its ripple. The
registered cells equal the derive layer's second pass, so R-48 is a
replication (L-15).
