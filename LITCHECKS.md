# Literature-check ledger (append-only)

Each entry: what was checked, when, how (search angles), and the verdict
with citations. A claim may carry `novelty: checked-novel` only by
referencing an entry here; `classical`/`folklore` carry their citation
inline. An entry is a record of a search, not a proof of absence.

## LC-1 — Klein-bottle orientation-bundle Laplacian spectrum (2026-08-19)

Claim checked: complete eigenmode classification under
f(x+L₁, y) = −f(x, L₂−y): (half-integer x ⊗ cos y) ⊕ (integer x ⊗ sin y),
constant excluded. **Verdict: KNOWN in substance / folklore.** The general
twisted-spectra machinery covers it as a minimal special case
(Miatello–Rossetti, Ann. Global Anal. Geom. 21 (2002) 341–376); the
anti-invariant torus-mode decomposition appears in Gordon–Rossetti
(arXiv:math/0111016); physics instances from Banach–Dowker, J. Phys. A 12
(1979); recent compactification papers state the integer⊗half-integer /
no-zero-mode quantization (arXiv:2510.05270 App. A). No single source
found displaying the packaged eigenbasis as a named theorem (~65%
confidence on that absence). Angles searched: flat-manifold twisted
spectra, Hodge isospectrality, Courant-sharp eigenfunction papers,
twisted-field QFT/Casimir, Klein-bottle compactification/pin structures,
string Klein-bottle amplitudes. Method: web search, 19 tool calls,
independent agent.

## LC-2 — Farey antipodal orbit counts, denominators coprime to 6 (2026-08-19)

Claim checked: orbit plateaus 1, 3, 6, 11, 17, 25 (endpoints included)
under p/q → (q−p)/q; increments φ(q)/2. **Verdict: ROUTINE.** Decomposes
into the classical Farey symmetry x → 1−x (Hardy & Wright ch. III),
evenness of φ, and ½Σφ(q) over restricted denominators; the
restricted-denominator Farey literature contains strictly stronger
counting results (Boca–Cobeli–Zaharescu arXiv:math/0201046; Haynes JNT
2003; arXiv:0907.0163, arXiv:0907.2171). OEIS: exact sequence absent
(reflecting triviality); near-coincidences A003022, A001859 both diverge
later. The "(q−1)/2" increment reading holds only at primes (φ(q)/2 in
general; first divergence q = 25). "Skips 15" carries no significance —
partial sums with increments ≥ 2 skip most integers. Method: web + OEIS
search + independent brute-force recomputation, separate agent.

## LC-3 — P-1 prior art: twisted-lattice windings, mean frequency, driven half-turn ring (2026-08-21)
prediction: P-1

Three statements checked by an independent context-free agent (web
search, 19 tool calls). Verdicts, blunt:

S1 (spatial, claim klein-twisted-gradient-xor). 1D part KNOWN,
classical: a ring with one pi-junction carries half-integer flux /
half-integer phase winding (Bulaevskii, Kuzii, Sobyanin, JETP Lett. 25,
290 (1977); arrays: Hilgenkamp group, Nature Phys. 4, 32 (2008)); the
XY model with twist phi = pi across the boundary has two
chirality-degenerate uniform gradients of winding +-1/2 (Khairnar &
Vojta, Phys. Rev. E 111, 024114 (2025), arXiv:2312.04468, in the
Fisher-Barber-Jasnow helicity-modulus lineage). 2D Klein-bottle
enumeration (half-integer-x XOR pi-staggered-y) NOT FOUND for XY/phase
fields - Klein-lattice work found is Ising/dimer (Lu & Wu PRE 2001;
Kaneda & Okabe PRL 86, 2134 (2001); arXiv:2010.11047) or fermionic
(arXiv:1909.02232). Agent's label: elementary corollary, "a 3-line
symmetry argument, not a result anyone would regard as deep."
Disposition: novelty = classical for the ring statement; the 2D
enumeration stays unchecked-and-unlabeled (no "novel" word is earned
for a trivial corollary).

S2 (temporal, claim klein-twisted-mean-frequency-identity). KNOWN,
textbook, very high confidence: odd coupling on an undirected graph
cancels edgewise, so the mean frequency equals the mean natural
frequency identically, for any boundary twist (Kuramoto 1984 ch. 5;
Strogatz, Physica D 143, 1 (2000); Acebron et al., Rev. Mod. Phys. 77,
137 (2005) sec. II; Dorfler & Bullo, SIAM J. Control Optim. 50, 1616
(2012) - the Sakaguchi-Kuramoto lag model is introduced precisely as
the case where it fails). Twisted states on rings use the same fact
(Wiley, Strogatz, Girvan, Chaos 16, 015103 (2006); Medvedev, Chaos 31,
103106 (2021)). Disposition: novelty = classical with citation.

S3 (temporal with per-site pinning, E1 step 3 shrink-not-shift). NOT
FOUND as stated, medium confidence, and the adjacent literature points
the OTHER WAY: in driven 0-pi Josephson systems a half-turn offset
CREATES half-integer Shapiro steps (Frolov et al., Phys. Rev. B 74,
020503(R) (2006); Lazarides, Supercond. Sci. Technol. 21, 045003 (2008)
- alternating 0-pi arrays give half-integer steps for EVEN junction
number and integer steps for odd, an explicit N-parity effect; Kikuchi
et al., Appl. Phys. Express (2021)). Coupled sine-circle-map lattices
(Kaneko 1984; Crutchfield & Kaneko 1987; Chatterjee & Gupte PRE 1996 /
Pramana 48 (1997)) have no frustrated bond. Disposition: the E1
finding is NOT labeled novel. Two reconciliations are owed before it
could be: (i) the drive here is per-site pinning sin(2*pi*theta_i)
(Frenkel-Kontorova-like), not a bias coupling to phase differences,
and the observable is rotation-number plateau width, not a voltage
step - the sign difference may be entirely this; (ii) Lazarides 2008
predicts N-parity dependence; E1 ran N = 4 only. An N-parity check is
the natural next experiment and is queued, not run.

## LC-4 — the Helmholtz corner, lattice dispersion, twist gauge, ALF prior art (2026-08-21)
prediction: P-4

Five statements from the P-4 discussion checked by an independent
context-free agent (web, 40 tool calls). Verdicts:

S1 corner = propagating weak discontinuity on characteristics:
mechanics correct; attributions loose. d'Alembert (1747) suffices for
the 1D wave equation; Hadamard, Lecons sur la propagation des ondes
(1903) for weak discontinuities; Hormander, Acta Math. 127 (1971) /
Duistermaat-Hormander 128 (1972) only for the general theorem.
Helmholtz's book is 1863 (preface 1862). Cremer's corner rounding is
Acustica 30, 119 (1974), mechanism losses PLUS stiffness balanced
against friction sharpening; the 1984 MIT Press book is secondary.
Raman, Bull. Indian Assoc. Cultiv. Sci. 15, 1 (1918) is a dynamical
theory. Woodhouse & Galluzzo, Acta Acustica 90, 579 (2004) correct.

S2 lattice dispersion spreads a sharp front: KNOWN - Schrodinger,
Ann. Phys. 349, 916 (1914), Bessel-function solution on the chain.
Caveats: a finite-difference string scheme at CFL = 1 is exactly
dispersion-free (Bilbao, Numerical Sound Synthesis, 2009), so the
dispersion is a property of the mass-chain ODE, not of numerics per
se; bowed-string simulators (McIntyre, Schumacher, Woodhouse, JASA
74, 1325 (1983); digital waveguides) use reflection functions and
deliberately band-limit the corner. No published "N sites needed to
hold a corner" statement found.

S3 twist gauge-invisible to linear waves except via background:
correct for ANTISYMMETRIC bond phases (Teitel & Jayaprakash, PRB 27,
598 (1983); twisted BC = Peierls phase on one bond); WRONG for a
same-sign offset at both ends, which is the Sakaguchi-Kuramoto
phase-lag model (Prog. Theor. Phys. 76, 576 (1986)), not removable.
The repo's scripts use the antisymmetric form (p4 lines 54-55;
p1_mean_frequency.py); the in-chat sentence was the sloppy one.

S4 topology/holonomy vs ALF onset in bowed strings: NOT FOUND.
ALF conditions KNOWN: bow force above Schelleng's f_max with slow
bow (Guettler, CASJ 2(6), 8 (1994); PhD KTH 2002; Guettler &
Schoonderwaldt, ISMA 2007; Kimura, J. New Music Res. 28, 178 (1999);
Hanson, Halgedahl, Schneider, CASJ 2(6), 1 (1994)). Schelleng, JASA
53, 26 (1973): f_max = 2 Z0 v_b / [beta (mu_s - mu_d)].

S5 "shocks and pulse edges are the same object as the corner": WRONG.
Weak discontinuity (derivative jump, characteristic speed,
non-dissipative) vs strong discontinuity / shock (field jump,
Rankine-Hugoniot speed, dissipative, born from smooth data) -
Hadamard 1903; Courant & Friedrichs, Supersonic Flow and Shock Waves
(1948). Lattice "shocks" (Holian, Flaschka, McLaughlin, PRA 24, 2595
(1981)) are dispersive shock waves, a third object.

## LC-5 — the half-shift J, Pin structures, odd-ring frustration, phi even (2026-08-22)
prediction: P-1

Triggered by the scrutiny that refuted twisted-sector-complex-structure.
Independent context-free agent, 7 tool calls.

S1 (J^2 = -I on the twisted sector). Agent verdict WRONG - agreeing
with the refutation but via a different normalization: it took the
x-period to be g^2's shift, so its J is the full glide shift (= the
reflection pullback up to sign), which squares to +1 on both bundles.
The claim's J is HALF the glide shift, an order-4 operator on sections
(J^4 = g^2); on the real span of cos(pi x/L1), sin(pi x/L1) it is a
90-degree rotation. Translating the agent's mode table ("m odd ->
even in y, m even -> odd in y" in its units) into the claim's units
gives (half-integer m, cos) and (integer m, sin) as the twisted
bundle - the counterexample of q_j_structure_sectors.py. Both
analyses agree the bundle does not determine the sign. What the
object is: a Z_4 extension acting faithfully on the half-integer-m
(antiperiodic-in-x) modes, the standard half-shift of freely acting /
Scherk-Schwarz orbifolds and of antiperiodic XXZ "twisted translation"
operators (Niekamp, Wirth, Frahm 2009); folklore, no source found
stating it as a theorem; arXiv:2606.07041 (2026) is adjacent and
should be read before any claim here. Pin: the "reflection lift
squares to -1" analogy is Pin^-(1) = Z_4 vs Pin^+(1) = Z_2 x Z_2 group
theory (Kirby & Taylor, LMS Lecture Notes 151 (1990), 177-242;
Witten arXiv:1508.04715 sec. 2), not a fact about line-bundle
sections; K^2 has w_2 = w_1^2 = 0 so four Pin^+ and four Pin^-
structures (Kirby-Taylor; arXiv:2112.07290). The "discrete analog of
4 pi spinor periodicity" sentence: not defensible beyond metaphor;
the precise statement is the central extension 1 -> Z_2 -> Z_4 -> Z_2
-> 1, same shape as Spin -> SO, different object. Disposition: the
replacement claim half-shift-squares-by-x-parity carries the
(-1)^(2m) arithmetic only, novelty = classical (folklore half-shift).

S2 (M even needed for the pi-staggered branch). KNOWN, textbook:
"topological frustration" / frustrated boundary conditions on odd
rings - Maric, Giampaolo, Kuic, Franchini, New J. Phys. 22, 083024
(2020); Maric, Giampaolo, Franchini, Commun. Phys. 3, 220 (2020);
Lazarides, PRB 77, 214419 (2008) even/odd 0-pi arrays. Disposition:
the M-even condition in klein-twisted-gradient-xor is a named lattice-
parity artifact; the claim's classical citation is extended here.

S3 (phi(q) even for q > 2; the Farey involution fixed-point-free for
q > 2). KNOWN, trivial: Hardy & Wright ch. V; the pairing p <-> q - p
IS the standard proof of evenness, so farey-antipodal-orbit-counts'
"phi even gives fixed-point-freeness" has the logic backwards in
emphasis (the pairing is primary). Already ROUTINE per LC-2.

## LC-6 — a0 ~ cH0/2pi: the de Sitter temperature reading (2026-08-22)
prediction: P-5

Literature pointer for claim a0-tracks-hubble-conjecture (status
coincidence-unruled, unchanged). The coincidence a0 ~ cH0 is the
oldest observation of the MOND program: Milgrom, ApJ 270, 365 (1983).
The 2pi is the Gibbons-Hawking de Sitter temperature T = H/2pi
(Gibbons & Hawking, Phys. Rev. D 15, 2738 (1977)); Milgrom, "The
modified dynamics as a vacuum effect," Phys. Lett. A 253, 273 (1999)
proposes a0 as the acceleration at which an observer's Unruh
temperature equals the de Sitter temperature. This is a heuristic
identification, not a derivation: no interpolating function, no BTFR
normalisation, and no relativistic completion follows from it, and
the relativistic completions that exist (TeVeS, Bekenstein 2004,
excluded by GW170817; RelMOND, Skordis & Zlosnik, PRL 127, 161302
(2021)) do not use it. Disposition: the corpus's a0 thread presented
the 1983 observation and the 1999 reading's 2pi without either
citation; both are now on record; the claim's cap stands. Method:
from memory of the primary sources, flagged for independent check
before any citation-kind evidence is added to the claim.

## LC-7 — provenance of the Stern-Brocot tree: Stern's array, Brocot's gear table (2026-08-22)
prediction: P-1

Checked by an independent context-free agent (59 tool calls).
Stern: "Ueber eine zahlentheoretische Funktion", J. reine angew.
Math. 55 (1858) 193-220 - the diatomic ARRAY (rows built by inserting
sums of adjacent pairs; Stern credits Eisenstein 1850; OEIS A002487),
not a tree. Brocot: Achille Brocot, Paris clockmaker, "Calcul des
rouages par approximation, nouvelle methode", Revue chronometrique 3
(1861) 186-194, dated December 1860 (presented 10 June 1860 to the
Societe des horlogers); 97-page monograph of the same title, Paris
1862 (BnF ark:/12148/cb30164108s). Purpose confirmed from Brocot's
own text (Kirk's translation): replace a ratio such as 191/23 by one
with smaller terms and least error, because a 191-tooth wheel cannot
be cut; he used the MEDIANT explicitly, bracketing the target between
an under- and an over-approximation, with the error of the mediant
the mediant of the errors (Mansuy, CultureMATH 2008, Prop. 10); he
wanted semi-convergents, not just continued-fraction convergents.
His output is a three-column TABLE (wheel, pinion, error) for one
target - "Brocot table" survives as a horologists' term (Merritt,
Gear Trains, 1947). Neither author drew the binary tree; the tree
presentation and the name are Graham, Knuth, Patashnik, Concrete
Mathematics sec. 4.5 (1989/1994) - coinage not conclusively verified.
Secondary: Hayes, "On the Teeth of Wheels", American Scientist 88
(2000) 296.

Disposition: Side B's object (P-1) is native to the gear train - a
COMPOSITION OF ROTATIONS with rational ratio - and the tree is a 1989
presentation of an 1858 array and an 1860 algorithm. Consistent with
E1's spatial-to-temporal finding and with the wheel's-track reading
(X-11 discussion). No claim changes; the in-chat attribution
"Brocot 1861, independently of Stern 1858" stands with the date
refinement (Dec 1860 / 1861 / 1862).

## LC-8 — cosmic topology, Bell, and the absence of a cosmological staircase (2026-08-23)
prediction: P-1

Pointers from a context-free check of a speculative text the owner
was reviewing (not a repo document), kept because they bound the
corpus's own twist material. (1) Non-orientable flat 3-spaces E7-E10
are a live observational object: COMPACT Collaboration, "Cosmic
topology Part IIb: eigenmodes, correlation matrices, and detectability
of non-orientable Euclidean manifolds", arXiv:2510.05030 (2025); an
orientation-reversing holonomy gives matched circle pairs with
mirror-reversed temperature sequences (Cornish, Spergel, Starkman,
CQG 15, 2657 (1998)); circle searches exclude fundamental domains
smaller than ~ the last-scattering diameter (Planck 2013 XXVI; 2015
XVIII). Orientability is a global Z_2 class w_1 in H^1(M; Z_2): no
"local Klein regime" exists (Hatcher sec. 3.3). (2) Any "mode-locking
collapse" of a superposition would be a deterministic nonlinear
modification of quantum mechanics, excluded by Gisin, Phys. Lett. A
143, 1 (1990) (superluminal signalling); viable collapse models are
stochastic (GRW 1986; CSL; Diosi-Penrose, constrained by Donadi et
al., Nat. Phys. 2021). Any "entanglement as structural necessity of a
connecting network" is a local hidden-variable model, excluded by the
loophole-free Bell tests (Hensen et al., Nature 526, 682 (2015);
Giustina et al., PRL 115, 250401; Shalm et al., PRL 115, 250402).
(3) No published use of a Devil's staircase, Farey tree, or Arnold
tongue in cosmology: cosmic expansion has no two competing
frequencies and no circle map; the staircase's genuine homes are the
circle map (Jensen, Bak, Bohr 1983), Shapiro steps, charge-density
waves, Frenkel-Kontorova. (4) Jacobson 1995 derives the Einstein
equation from REVERSIBLE delta Q = T dS as an equation of state;
"geometry from entropy production" is not in it (Eling, Guedens,
Jacobson 2006 add production only for f(R) corrections). Disposition:
no claim changes; the text scored ~10% established / 30% wrong / 60%
content-free and is not pursued.

## LC-10 — 2026-08-24 — the Bell ladder's constants
prediction: P-17
claims-checked:
- AGR 1982 measured S = 2.697 +/- 0.015, more than 40 sigma above
  the local bound, with the apparatus-corrected quantum prediction
  S_QM = 2.70 +/- 0.05 (Aspect, Grangier, Roger, PRL 49, 91 (1982);
  Nobel scientific background 2022; arXiv:2212.05535).
- Freedman-Clauser 1972: delta = 0.050 +/- 0.008 against delta <= 0,
  a 6 sigma violation (Freedman, Clauser, PRL 28, 938 (1972);
  arXiv:physics/0508180).
- Detection-loophole models reproducing the singlet exactly exist at
  MEAN efficiency 75% (Gisin, Gisin, Phys. Lett. A 260, 323 (1999),
  quant-ph/9905018; Pearle 1970 is the family's ancestor); the
  symmetric-efficiency threshold above which no such model exists is
  2/(1+sqrt 2) = 82.84% (Garg-Mermin; review arXiv:1407.0363). The
  two numbers are different facts and the chat draft of this line
  initially conflated them - corrected here.
- One classical bit suffices to simulate the singlet correlations
  exactly: Toner, Bacon, PRL 91, 187904 (2003).
- PR boxes collapse communication complexity (van Dam,
  quant-ph/0501159); information causality bounds quantum
  correlations at Tsirelson for the CHSH slice (Pawlowski et al.,
  Nature 461, 1101 (2009)).

## LC-12 — 2026-08-26 — the Otto 2025 corpus: sources checked
prediction: none (audit; see notes/otto25_mechanization.md)
claims-checked:
- Hardy's maximum nonlocality probability equals the fifth power of
  the golden mean, (5 sqrt 5 - 11)/2 = 0.0901699: REAL and
  peer-reviewed (Hardy, PRL 71, 1665 (1993); Mermin, Am. J. Phys.
  62, 880 (1994)). The one theorem-grade golden number in the
  paper's physics; everything else attaches by proximity.
- CODATA/PDG anchors used by the mechanization: alpha^-1 =
  137.035999177(21) (the paper's own quote); g_e =
  2.00231930436182(52) (its eq. 49, Penning-trap lineage); m_H =
  125.20 +/- 0.11 GeV (PDG 2024); Planck 2018 Omega_L = 0.6847 +/-
  0.0073.
- The paper's load-bearing physics sources are a self-referential
  non-peer-reviewed cluster: Guynn (viXra 1810.0456) for the
  "maximum galactic velocity" beta_g and the g_e "calculation
  without any QED construct"; Suleiman's Information Relativity
  (Nova book); El Naschie's E-infinity (Chaos Solitons Fractals,
  author-adjacent); Markoulakis's "superluminal graviton condensate"
  (10^22 c). None of these is an independent measurement; relations
  calibrated against beta_g inherit its status.
- Klein's icosahedral form z^20 - 228 z^15 + 494 z^10 + 228 z^5 + 1
  is genuine (Klein 1884; Nash 2013 exposition); the paper's quartic
  reduction and appendix radicals check out exactly (mechanization
  rows app-root1..4, 14, 11, 161).
- The Great Pyramid slope ambiguity is classical lore now
  quantified in-repo: Kepler sqrt(Phi) = 1.27202 vs 4/pi = 1.27324
  differ by 0.10%, inside the monument's build tolerance
  (surveyed 146.59 m / 230.33 m base); the phi-vs-pi debate is
  undecidable from the building.
- The 2025 companion PRB 111, 184519 (Danner, Hoehe, Padurariu,
  Ankerhold, Kubala): real Josephson-photonics work where an
  injected REFERENCE SIGNAL phase-locks squeezed microwave states
  (injection locking, Adler class) - the rigorous instance of the
  "reference wave" motif, and the target of the next locking-line
  heading (A-10).
