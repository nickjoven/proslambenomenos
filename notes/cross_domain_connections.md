# Cross-domain connections — running ledger

Mood: design notes, mood-marked throughout; nothing here is a claim
until it enters claims/ through the gate. The organizing exemplar is
Rule 30: cellular automata sit at a triple point because of one
theorem — Curtis–Hedlund–Lyndon: the continuous shift-equivariant
maps on the Cantor space (topology) are exactly the local rules
(algebra/combinatorics), whose iteration is the dynamics. The lesson
is not "everything connects"; it is that a triple point exists where
an EQUIVARIANCE-plus-CONTINUITY condition forces a finite algebraic
presentation. Entries below are candidates for connections of that
grade, tied to the P-1 work.

## X-1 — The bridge question is CHL-shaped

P-1 asks for the natural maps between spectral indexing and locking
indexing. CHL says: on the symbolic side, naturality (continuity +
shift-equivariance) FORCES locality. Our D5 canonicity criteria
(deck-equivariance + involution-equivariance + boundary agreement)
play the same role. T+ would be a CHL-type rigidity theorem; T-
would be the statement that no CHL theorem exists here — both are
respectable shapes, which is why the criteria were fixed in advance.

## X-2 — Holonomy shifts the conjugate lattice (the E1 anchor)

The pattern behind both the spectral theorem-let and E1's first
datum: a flat-bundle character (topological datum, holonomy -1)
appears as a HALF-QUANTUM OFFSET of the lattice indexing excitations
in the conjugate variable. Instances across domains, all classical:
Aharonov-Bohm (flux shifts the momentum/interference lattice);
pi-junction and half-flux-quantum rings (shifted current-phase and
persistent-current states); antiperiodic (fermionic) fields in
imaginary time — Matsubara frequencies omega_n = (2n+1)*pi/beta,
which are LITERALLY the odd/2N lattice E1's twisted plateaus suggest
temporally. Mood: this makes E1's signature folklore-anchored rather
than novel; the litcheck, when run, should target exactly this
(discrete driven rings with a pi seam — likely known in Josephson
ladder / frustrated-ring literature). That is good news for
correctness and bad news for novelty, which is the right trade.

## X-3 — Rule 90 / Rule 30 as the linear/nonlinear split

Rule 90 is XOR = linear over F_2: fully solvable, Pascal-mod-2,
Sierpinski self-similarity. Rule 30 adds one nonlinearity and
becomes a randomness source with open problems. Our problem has the
same anatomy: the spectral side is the Rule-90 half (linear,
character theory, completely classified — C7, C14, the gradient
theorem-let); the locking side is the Rule-30 half (nonlinear,
tongue structure, open). The v1 corpus's signature move was solving
the Rule-90 half and claiming the Rule-30 half; P-1's discipline is
refusing the elision. Mood: analogy, load-bearing only as a
classifier of which sub-problems are hard.

## X-4 — The Farey triple point the corpus lived on without using

Stern-Brocot/Farey is itself a classical triple point: SL_2(Z)
(algebra) <-> geodesics and cusps on the modular surface
(topology/geometry) <-> continued fractions as the symbolic dynamics
of the Gauss map (dynamics). The corpus used all three faces
separately and never the dictionary between them. If P-1's temporal
side ever needs a canonical symbolic coding of locked states, THE
candidate is the Gauss-map coding, because it is the one the
dictionary already certifies as natural.

## X-5 — One object, three languages (the reflection)

The C4/C5 Farey mirror p/q -> (q-p)/q, the spectral cos/sin
branches, and the orbifold structure of the reflection quotient of
the circle (two mirror points, 0 and 1/2) are the same Z_2 in three
domains. E1's control/twisted contrast is a fourth appearance: the
crushed 1/2 plateau sits AT the mirror point. Mood: observed
pattern; the orbifold reading has not been used for anything yet.

## X-6 — When is the circle earned? (question from the owner, 2026-08-20)

Below one period the circle fails twice: topologically it is a
hypothesis (return not yet witnessed; strictly the SECOND return
certifies periodicity), and metrically it is undefined in principle —
time-frequency uncertainty gives delta_T/T > 1 for duration < T, a
circumference fuzzy by more than itself, sharpening as 1/n with n
periods (frequency-comb narrowing). Distinctions worth keeping: the
circle-as-state-space-of-a-law (exists before any trajectory closes;
period inferable from an arc) versus circle-as-witnessed-recurrence
(earned at return two) — different objects, different birthdays.
Physics instance: super-horizon modes are treated as frozen
constants, not phases. Twist corollary: periodic vs antiperiodic
return is undetectable in ONE traversal (the 2pi-vs-4pi fact), so
the parity material sits exactly one return deeper than the circle —
fixing the T2 -> T6 dependency order in the curriculum. Mood:
design note; the uncertainty statement is classical.

## X-7 — The hourglass is the collapsed Mobius band (owner question, 2026-08-21)

The double cone x^2 + y^2 = z^2 is interesting at exactly one point:
the apex, whose link is two disjoint circles (non-manifold; the
A1/nodal singularity; in Lorentzian signature, the light cone). Every
level circle is ordinary — only the DEGENERATE circle needs a
decision, and the two canonical decisions are both objects already in
this repo's orbit: (1) crush it — collapse the central circle of the
cylinder R x S^1 — giving the singular hourglass, the "phase
forgotten at zero amplitude" reading, X-6's unearned circle
geometrized; (2) quotient it — a real oscillation x = A cos(2 pi
theta) carries the free involution (A, theta) ~ (-A, theta + 1/2),
whose quotient is smooth and is precisely the open MOBIUS BAND with
the zero-amplitude circle as core: the state space of a real
oscillator, where crossing zero amplitude traverses the half-twist
and the sign flip IS the pi. So hourglass = collapsed Mobius band;
the Mobius band is its resolution. Ties together: v1's D18 Mobius
container and the bicone + Z_2 vortex experiments (same structure,
no dictionary), the twisted seam's pi offset (an amplitude zero
crossed somewhere on the loop), and X-6. Mood: connection note;
the quotient identification is standard covering-space material and
checkable; nothing here is claimed novel. Rendering: cones and
level-circle wireframes draw fine in termplot via parametric
projection into plot_xy (demo run 2026-08-21).

## X-8 — Two Z_2's: holonomy forces the count, a threshold selects it (2026-08-21)

Kawano, Kobayashi, Suzuki, Ichiji, arXiv:2502.11902 (2025): the bowed
violin subharmonic f0/2 is NOT parametric resonance. Mechanism
(Guettler 2002, now filmed at 3000 fps): with high bow force and slow
bow the returning Helmholtz corner fails to trigger slip, the contact
point becomes a conditionally reflecting boundary, slip fires on every
second corner arrival, and the bridge receives n*(f0/2) while the f0
component stays trapped nut-side. Their own ablation: one transverse
polarization + wave equation (inertia) + one stick-slip friction node
+ constant-velocity bow suffices; no tension modulation, no second
polarization, no damping.

The connection: a twisted loop (holonomy pi) has half-integer
harmonics in its spectrum kinematically - "closing on the double
cover" is a property of the bundle, always on. Kawano's f0/2 is the
same count selected dynamically by a threshold, switchable by bow
pressure, with f0 coexisting on one side of the gate. Josephson 0-pi
arrays under drive (Frolov 2006; Lazarides 2008, LC-3) sit between:
fixed pi bond + drive creates half-integer steps. Reading: a bundle
class can only force which counts are AVAILABLE; a non-smooth
threshold is what SELECTS among them. The source corpus used the
first as if it did the second. This repo's current model space
(first-order Kuramoto, smooth odd coupling, smooth pinning) lacks all
three Kawano ingredients: inertia, a stick/slip state variable, a
moving drive. The only f/2 it can produce is the K > 1
non-invertible regime of the sine circle map - local period doubling,
not a gated reflection. Mood: connection note; the Kawano summary is
from an independent literature agent reading the arXiv HTML; the
"forces vs selects" reading is a framing, not a theorem. Experiment
preregistered as P-4.
