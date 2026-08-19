# The drip queue

One item per release. Each entry: the old derivation number, its honest
mathematical reduction (what actually enters the gate), the expected
computed label, and what does NOT come along. Items enter claims/ and
the compendium one at a time, in order. The physics identification that
rode on each derivation never re-enters by adjacency — it re-enters
only with new evidence, through the gate, or not at all.

Already in the compendium from the extraction pass: the Stern-Brocot
package (C1), Klein twisted spectrum (C7), staircase (C8), tongue
scaling (C9), Adler (C10), Chebyshev identity (C11), divergence null
(C12), and the Farey/orbit items (C4, C5). The queue below covers the
a0 spine and the numbered derivations not yet individually dripped.

## Q0 — the a0 opener (Track 1, before the numbered drip)

The discriminating-test note: a0 = cH0/(2*pi) ~ 1.04e-10 m/s^2 vs
observed 1.2e-10 (the Milgrom coincidence, imported); the a0(z)
proportional-to-H(z) conjecture with its falsifier stated (BTFR zero-
point shift ~0.5 dex at fixed V by z=2; low-mass rotation curves
V_flat 50-120 km/s at z > 1.5; N > 20 per redshift bin against the
systematic floor); the rival scalings laid side by side (constant a0,
cH(z)/(2*pi), (1+z)^(3/4)). Labels: imported (the coincidence),
asserted-with-falsifier (the scaling conjecture). Nothing derived.
Source basis: v1 a0_high_z.py + predict_highz.py (both repaired
2026-08-17).

## Q1 — from D1 (born_rule.md)

Reduction: the saddle-node normal form dth/dt = mu + th^2 has escape
time T ~ pi/sqrt(mu), so locking-window widths scale as the square
root of the unfolding parameter with universal exponent 1/2 —
classical (Guckenheimer-Holmes; Strogatz ch. 4). Enters as imported +
a reproduced/verified numerical check. Does NOT come along: the
identification of the exponent with quantum probability (|psi|^2).
That identification is a conjecture with no discriminating test on
record; it stays out until one exists.

## Q2 — from D3 (a0_threshold.md)

Reduction: K_c = 2/(pi*g(0)) for the Kuramoto model with unimodal
frequency density (imported, Kuramoto 1984/Strogatz 2000); the
consistency identity L = c/(2*pi*H) given a0 = cH/(2*pi) (one line,
proven-as-identity). Does NOT come along: the 2*pi derivation
(declined, D-3); the coupling-chain route (breaks at v1
a0_threshold.md:142-155).

## Q3 — from D4 (spectral_tilt_reframed.md)

Reduction: golden-mean renormalization of the critical circle map has
Shenker's scaling delta ~ 2.83361 (classical, Shenker 1982; Feigenbaum-
Kadanoff-Shenker); the v1 phi^2 = 2.618 claim is refuted by its own
measured ratios and recorded as such. Enters as imported + the
refutation record. Does NOT come along: n_s ~ 0.965 as a derived tilt
(the identification rides the declined substrate reading; and any
numeric-agreement form hits the pigeonhole cap).

## Q4 — from D6 (planck_scale.md)

Reduction: the Planck-unit identities (hbar/t_P = m_P c^2 = E_P etc.)
enter labeled as what v1 itself called them — tautological
(definitional closure of the unit system); the Iwasawa decomposition
of SL(2,R) (imported, standard). Solve-candidate flagged, not entered:
v1's "every nontrivial continuous subgroup kills exactly one Iwasawa
stage" has an incomplete proof (2-dimensional Borel subgroups
unaddressed; discrete case misstated) — the salvageable dimension
statement is a small, well-posed Lie-theory exercise someone could
actually finish. Queue it as work, not as a claim.

## Q5 — from D7 (address_and_quantity.md)

Reduction: inspect for a separable mathematical statement behind the
tau * delta-theta uncertainty form; expected outcome is definitional
(a bandwidth-duration inequality instance, imported from Fourier
analysis if stated correctly). If nothing separable survives, the
entry is a one-line QUEUE note saying so — a null drip is a valid
drip.

## Q6 — from D8/D9 (a1_from_saddle_node.md)

Reduction: same mathematics as Q1 (saddle-node 1/2-exponent), applied
at threshold — enters only as the instantiation check, cross-linked to
Q1 rather than duplicated. Does NOT come along: the a1/a0 threshold
identification.

## Q7 — from D10 (minimum_alphabet.md)

Reduction: the four primitives as definitions and Axiom 1 as a
declared axiom (already the honest v1 framing); the mod-Z quotient
stipulation is DECLINED.md D-6. Enters as definitions — no theorem
content expected.

## Q8 — from D11/D12/D13 (rational field equation, continuum limits, Einstein-from-Kuramoto)

Reduction: the FLRW/ADM constraint computation (textbook GR,
imported, with the 16*pi*G constraint labeled as the import it is);
staircase completeness at K = 1 (imported, Jensen-Bak-Bohr — already
C12's premise). Does NOT come along: the K_eff = d/2 bridge (declined,
D-5); the sync-to-spacetime identification.

## Q9 — from D14 (three_dimensions.md)

Nothing to drip: the route is DECLINED.md D-1 (refuted as forced).
The queue entry exists so the number line is complete and the
disposition is visible in sequence.

## D16+ — already extracted or declined

D16/D18/D19 (Klein bottle line) -> compendium C7. D25/D28 (Farey/Omega
partition) -> compendium C5 plus the bare partition as definition.
D26 (hierarchy) -> numerology, declined welds; the ord_27(13) = 9
correction is recorded in v1's audit trail. Numbers above D28 will be
triaged the same way when the drip reaches them, against INDEX.md's
map.

## Follow-through report (2026-08-19): where the reasoning breaks

The queue was executed from Q0 until the process stopped adjudicating.
It held through Q3 and broke in three places — all three are
boundaries of mechanization, not execution defects.

**Break 1 — Q0, immediately: the pigeonhole gate is ill-posed for
singleton coincidences.** Computing a permutation-null p for
a0 ~ c*H0/(2*pi) requires choosing an expression ensemble: which
constants, which operations, what tolerance. The choice determines the
p-value, and nothing inside the system audits the choice — v1's own
Region-C machinery had this exact dependence (its ensemble was the
framework's integers). So the spine claim enters coincidence-unruled
and NO computation available to this repo can move it; only a
community-defensible ensemble convention could, and adopting one is a
modeling commitment, not a calculation. The gate's first contact with
a real physics claim lands on the look-elsewhere boundary and honestly
stalls there. This is recorded in the claim file itself.

**Break 2 — Q2: the curation vacuum appears.** The planned identity
claim (a0 = cH/(2*pi) <=> c^2/a0 = 2*pi*c/H) is one line of algebra
that restates the conjecture without adding content; it was not
created. From Q4 on, the census is: Q4 definitional + one queued
exercise, Q5 expected null, Q6 cross-link only, Q7 definitions, Q8
textbook imports, Q9 declined. The drip therefore contains roughly
FOUR substantive releases (Q0 note, Q1, Q3's import+refutation pair,
and Q4's Iwasawa exercise as work) before the numbered spine is
exhausted. That is the precise measurement of v1's separable
mathematical content, and it means the drip is a finite curation
program: past Q3-Q4, continuation requires the solve-candidates —
new research the strategy can gate but cannot generate.

**Break 3 — "worth recording" is not computable.** kuramoto-critical-
coupling entered as legitimately as any deep result; a thousand
textbook imports would too, and no gate would go red. The registry
degenerating into a bibliography is prevented only by editorial
judgment, which re-enters at the one door the intake law cannot
guard. The law bounds dishonesty; it cannot supply significance.

Disposition of the breaks: 1 is permanent and documented (the honest
status IS the community's status — "unexplained coincidence"); 2 is
the expected terminus — the queue tail exists for completeness, and
the frontier after Q4 is the two solve-candidates plus Track 1's
empirical wait; 3 is accepted as the boundary of mechanization —
noted here so nobody later mistakes registry size for content.

## Cadence rules

- One queue item per release; a release = claim file(s) + compendium
  section (if any) + gates green.
- A null drip ("nothing separable survives; here is why") is a valid
  and complete release.
- Any novelty label beyond classical requires a LITCHECKS entry first.
- Track 1 (Q0) may ship independently of the numbered sequence.
