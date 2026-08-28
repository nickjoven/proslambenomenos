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

## LC-13 — 2026-08-26 — what PRB 111, 184519 actually states
prediction: P-22
claims-checked:
- Danner, Hoehe, Padurariu, Ankerhold, Kubala, Phys. Rev. B 111,
  184519 (2025): dc-biased Josephson junction coupled to a microwave
  cavity emits correlated photon pairs; bias-voltage noise enters
  the junction phase as the integral of V(t) and causes phase
  diffusion that destroys coherence; a weak ac reference added to
  the dc bias (or injected into the cavity) stabilizes the emission.
  Extracted verbatim from the PDF text: the two-photon/squeezed
  scenario "relies on the injection of a signal at twice the
  frequency of the emitted radiation", showing "strikingly
  different features" from standard locking; the conclusion places
  the phenomenon in the class of "the respective universal
  phenomenological Adler and Kuramoto models" (their ref [52] is
  Adler, Proc. IRE 34, 351 (1946)); fundamental-resonance locking
  (one photon per Cooper pair) is treated in their ref [42].
- Extraction honesty: the paper's display equations are not
  machine-extractable from the PDF (glyph-encoded); P-22 therefore
  reproduces the NAMED universality class (Adler dynamics, with the
  twice-frequency injection entering as sin(2 theta)), not the
  paper's device-specific coefficients - declared in the P-22
  scope, and the reason no clause references their figures.
- Adler 1946 (Proc. IRE 34, 351): locking range proportional to
  injection amplitude, beat sqrt(detuning^2 - range^2) - the
  closed forms the P-22 derivation layer re-checks by quadrature
  (EQ1) before anything stochastic runs.

## LC-14 — 2026-08-27 — the golden flux line's imports
prediction: P-7
claims-checked:
- The critical almost-Mathieu total-bandwidth plateau q S(q) ->
  32 G / pi = 9.32995 with G Catalan's constant: Thouless, Phys.
  Rev. B 28, 4272 (1983) and Commun. Math. Phys. 127, 187 (1990)
  (asymptotic scaling for the Harper bandwidth; the constant is
  imported - P-7 measures only the APPROACH, and lands the
  terminal-pair mean 0.0011 away).
- Hofstadter, Phys. Rev. B 14, 2239 (1976): the rational-flux band
  structure and the butterfly; Chambers relation for the
  k-dependence entering only through cos(q k1) + cos(q k2) -
  the two-extremal-point band-edge construction P-7 validates
  against CAS closed forms at q = 2, 3.
- The Cantor spectrum at irrational flux (Ten Martini): Avila,
  Jitomirskaya, Ann. Math. 170, 303 (2009) - IMPORTED context only;
  nothing Cantor is computed in P-7 and the scope says so.
- c25 interop confirmed in-repo: the alpha = 1/2 anchor's band
  maximum 2 sqrt 2 equals the pi-flux Dirac dispersion maximum of
  catalog c25 (Affleck-Marston 1988; Lieb 1994), and the central
  touch at E = 0 is the same Dirac point.
## LC-11 — 2026-08-25 — the ALF literature and the imaging-resolution arithmetic
prediction: P-19 (ALF period lattice)
claims-checked:
- Guettler, "Wave analysis of a string bowed to anomalous low
  frequencies", CAS Journal 2(6), 1994: ALF divides into two groups
  triggered by transverse and torsional waves respectively, and the
  mechanism is triggering waves taking "an extra turn" on the string
  before the release from the bow-hair grip; typical lowered
  intervals third, octave, octave plus fifth (publisher metadata and
  the author's publication list; the CASJ text itself is paywalled
  and the thesis PDF at knutsacoustics.com is image-scanned, so
  FORMULA-level verification - whether Guettler states
  P = T0(1 + m(1-beta)) explicitly - remains open; the registered
  expectation in P-19 anticipated exactly this split). The
  extra-rounds MECHANISM is therefore prior art; the claim's
  torsional-family exclusion matches Guettler's two-group finding.
- arXiv:2502.11902 (the imaging paper the model is built against):
  shutter 1/3000 s, frame rate 3000 fps (0.33 ms per frame); steel
  G string, reference frequency 196.9 Hz, diameter 0.8 mm, length
  325 mm - all as imported by the model. The paper states the slip
  event "occurs every 5 ms in the normal technique and at half that
  frequency in the subharmonic technique" and describes the sound
  as "approximately one octave lower" with the bow "approximately
  5 cm from the bridge" (beta ~ 0.154 on 325 mm). It ALSO states
  the subharmonic pitch "can be tuned by varying the bow position
  and applied pressure" - a qualitative anticipation of the
  lattice's beta-dependence, with no quantitative period formula or
  slope given. The arithmetic behind the null_system line: at
  196.9 Hz, T0 = 5.079 ms, and the gap between the lattice lock at
  beta ~ 0.154 (about 1.89 T0) and exact doubling 2.000 T0 is about
  0.56 ms, under two frame intervals; between 1.94 T0 and 2.00 T0
  it is 0.30 ms, under one. Frame-quantized period estimates at
  3000 fps therefore cannot separate the lattice from exact
  doubling at this f0, and the paper's own "approximately" is
  consistent with either reading.
- Not found in any accessible source: the dP/dbeta = -1 slope
  discriminator, the two-generator lattice statement, or a
  bow-position pitch-shift measurement protocol for ALF. The
  novelty split registered in P-19 (mechanism classical, formula
  possibly classical, discriminator and protocol not found) stands,
  with the formula question still open pending CASJ 1994 access.

## LC-15 — 2026-08-27 — the causal-set spectral-dimension literature, and a printed-formula defect
prediction: P-16
claims-checked:
- Eichhorn, Mizera, Class. Quantum Grav. 31, 125007 (2014): random
  walk on the sprinkled causet's Hasse diagram, undirected,
  transition probability 1/degree, d_s = -2 dln P/dln sigma;
  finding: d_s INCREASES at small scales (superdiffusion from the
  causet's radical nonlocality); a "causal spectral dimension" from
  two-walker meeting probability gives similar results (their
  footnote 1). Reproduced on our sprinklings in R-21 at growth
  1.023 across N = 64..256.
- Belenchia, Benincasa, Marciano, Modesto, PRD 93, 044017 (2016):
  heat kernel of the REGULARISED nonlocal d'Alembertian gives
  universal dimensional reduction d_s -> 2 in all dimensions (their
  eq. 12); numerics show a superdiffusive maximum at s ~ l and slow
  approach to the Hausdorff value from above (their Fig. 2); the
  unregularised operator gives the meaningless d_s = 4 rho s in
  d = 2 (their eq. 14 - reproduced by us at ratio 1.000); their
  conclusion explicitly flags the possible "universal description
  which interpolates" between their result and EM's.
- THE DEFECT: BBMM's printed eq. (15) - the d = 2 minimal operator
  with a = -2, b = {4, -8, 4} and Gaussian weight
  exp(-(sqrt(pi)/4) xi^2) - fails the paper's own stated IR limit
  g -> -k^2: the psi-sum identity sum b_n psi(n+1) = -2 forces
  g(0) = 4/sqrt(pi) - 2 = 0.256758, confirmed numerically to 1e-6
  by two independent implementations (E1 closed form and direct
  double quadrature agreeing to 4e-4). The SOURCE operator
  (Aslanbeigi, Saravani, Sorkin, JHEP 1406, 024, eq. 5:
  g = -Z e^{Z/2} E2(Z/2)) has the correct limits exactly (IR -Z;
  UV -2 + 8/Z - 48/Z^2), and reproduces BBMM's own Fig. 2
  (maximum 2.260 at s = 1.34) - so their numerics evidently used
  the source form and eq. (15) as printed carries a transcription
  defect in the prefactor/weight.
- Carlip, arXiv:1506.08775 (their note added): similar
  dimensional-reduction results, contemporaneous - context only.

## LC-16 — 2026-08-28 — the everpresent-Lambda vs DESI DR2 sources
prediction: P-26
claims-checked:
- DESI Collaboration, arXiv 2503.14738v3 (DESI DR2 Results II,
  PRD 112, 083515): BAO from 14M+ galaxies/quasars; Table 4 per-
  tracer D_V/r_d, D_M/r_d, D_H/r_d with printed D_M-D_H
  correlations (machine-parsed into
  scripts/experiments/desi_dr2_table4.json; LRG3/ELG1 rows excluded
  per the table's own caption as superseded by LRG3+ELG1); flat
  LCDM fit to BAO alone: Omega_m = 0.2975 +- 0.0086, h r_d =
  101.54 +- 0.73 Mpc, corr -0.92 (their eq. 17) — REPRODUCED by
  our 13-point Gaussian compression in R-23 (0.2970, 101.56);
  BAO-ALONE preference for w0waCDM is characterized by the paper
  itself as equivalent to 1.7 sigma (their Sec. VII.1) — the
  headline preferences need more data: dchi2_MAP = -12.5 (3.1
  sigma) for DESI+CMB, driven per their own text by CMB lensing
  (dropping to 2.4 sigma / -8.0 under simple early-universe
  priors), and 2.8 / 3.8 / 4.2 sigma with Pantheon+ / Union3 /
  DESY5 SNe respectively; their eq. 22 sigma<->dchi2 map
  reproduced by us to 0.005 at the 3.1-sigma point (EQ3).
- Wang, Mota, arXiv 2504.15222 (EPJC): the contest — tensions
  among CMB, BAO and SN datasets undermine the combined-analysis
  claim; individual datasets cannot independently detect cosmic
  acceleration at significant levels under dynamical dark energy.
  Imported as the reason P-26 scores only the BAO likelihood it
  can recompute, with combination verdicts imported not asserted.
- Das, Nasiri, Yazdi, arXiv 2307.13743 (Aspects of Everpresent
  Lambda II): Model 1 (the Zwane-Afshordi-Sorkin lineage,
  arXiv 1703.06265) update Lambda_t = [Lambda V + 8 pi alpha xi
  sqrt(dV)]/V_t with xi standard normal, V the past-lightcone
  4-volume, alpha explored over 0.001-0.025, V_0 SPECIFIED at the
  z ~ 1e5 start (the detail our first run got wrong; R-23);
  their verdicts imported: Pantheon+SH0ES best seed chi2 1481.9 vs
  LCDM 1485.3 with 16 of 90000 seeds better (our EQ3 prices this
  at net -10.0 bits); CMB fails by dchi2 >= +156 vs LCDM even
  with their LSS suppression (2495.6 baseline, 2358.5 suppressed,
  vs LCDM ~2339); their own framing: the models are works in
  progress, not quantitative improvements on LCDM.
- Sorkin's order-of-magnitude success stays what c31 recorded:
  1/sqrt(N) count fluctuation lands 0.4 orders from the observed
  Lambda. P-26 scores the DYNAMICS that produce that magnitude,
  on DR2 BAO, and finds them priced out (R-23).

## LC-17 — 2026-08-28 — the postquantum-classical-gravity squeeze sources
prediction: P-27
claims-checked:
- Oppenheim, PRX 13, 041040 (2023): the postquantum theory of
  classical gravity - consistent CQ coupling requires stochastic
  metric fluctuations; formally renormalisable per arXiv
  2402.17844. Imported as the theory under test; not recomputed.
- Oppenheim, Sparaciari, Soda, Weller-Davies, Nature Comms 14,
  7910 (2023) / arXiv 2203.01982 (one arXiv version only): the
  decoherence-diffusion trade-off. Their Section V squeezes,
  eqs. (44)/(46)/(47), pinned with their stated inputs (Cavendish
  sigma_a ~ 1e-7 m/s^2, N ~ 1e26, r_N ~ 1e-15 m, V_b ~ r_E^2 h;
  fullerene M = 1e-24 kg, lambda < 10/s, V ~ 1e-25 m^3, R ~ 1e-9
  m). AUDIT FINDINGS (EQ2): the averaging time T in eq. (42) is
  never given a value in Section V (Janse et al. attest dT =
  100 s); the three printed lower bounds reproduce exactly from
  the stated inputs, while the three printed upper bounds sit
  +2.26 / -1.35 / +1.65 orders from their own inputs' arithmetic
  (continuous / discrete / nonlocal) - order-of-magnitude prose,
  now mechanized with signed deltas. Their verdicts imported:
  ultra-local continuous models with Phi-independent diffusion are
  ruled out (need ~20 orders of suppression); discrete and
  nonlocal-continuous classes survive with ~24 and ~31 orders of
  window.
- Janse, Uitenbroek, van Everdingen, Plugge, Hensen, Oosterkamp,
  PRR 6, 033076 (2024) / arXiv 2403.08912: the modern upper-bound
  review through FOM_D2 = N S_a (their eq. 3, Table I, 45
  experiments + the stylized Cavendish row). Machine-parsed into
  scripts/experiments/janse_table1.json. AUDIT FINDINGS (EQ3/EQ4):
  all 46 rows internally consistent on S_a = S_F/m and
  FOM = N S_a^2 to 5%; the Monteiro '20 row's printed N is 8x the
  SiO2-composition value (its FOM column is nonetheless internally
  consistent); their eqs. (4)-(5) are FOM rescalings of OSSW's
  printed bounds from the Gisler row (FOM 0.298 vs Cavendish
  1e14), reproduced to a factor 3; their eq. (5) lower bound 1e-35
  is underivable from any stated input set (OSSW printed 1e-40;
  Fein-updated M^2/(R lambda) = 1.3e-38) - the source of their
  "one order of magnitude" gap statement for Asenbaum, recorded as
  convention-dependent. Their applicability caveats imported
  unresolved: differential/relative acceleration measurements
  (Asenbaum atom interferometry FOM 2.41e-11, LISA Pathfinder
  1.78e-5) may not validly bound D2, and the same experiment
  serving as both upper and lower bound is an open question their
  text raises.
- Experiment primaries behind the pinned rows (not re-derived):
  Gisler 2022 (nanowire, FOM 0.298); Fein et al. 2019 Nat. Phys.
  (25 kDa interference, lambda = 133 Hz per Janse); Asenbaum 2017
  (Rb interferometry); Armano 2018 (LISA Pathfinder).

## LC-18 — 2026-08-28 — the gap-labeling literature
prediction: P-28
claims-checked:
- Satija, Frontiers in Physics (2026), "The Hofstadter butterfly:
  bridging condensed matter, topology, and number theory" (the
  review A-12 cites): the gap-labeling relation N = s + t phi with
  N the integrated density of states and t the Chern number of
  Hall conductivity (their eqs. 6-7 region), identified through
  the Streda formula (their eq. 9). Small audit note: the review's
  "for rational flux p/q, there are q gaps" counts the closed
  gaps; the ladder has q-1 gap indices and P-7's parity rule
  closes the central one for even q — and EQ1 shows the
  Diophantine label is AMBIGUOUS (t = +-q/2) at exactly that gap:
  the number theory and the spectrum agree on which gap cannot be
  labeled.
- Thouless-Kohmoto-Nightingale-den Nijs, PRL 49, 405 (1982): the
  Hall conductance of a filled gap is the integer t of the
  Diophantine equation r = s q + t p (TKNN). Imported as the
  physical meaning of t; the Hall conductance itself (Kubo route)
  is NOT recomputed here - our computed content is the label
  arithmetic plus the Streda slope from band counting.
- Streda, J. Phys. C 15, L717 (1982): sigma_xy = e^2/h dN/dB at
  fixed E in a gap. Mechanized here as the exact rational
  identity (EQ4): across unimodular (Farey-neighbor) flux pairs,
  the band-count slope dN/dalpha equals t with no error term.
- Wannier, pss(b) 88, 757 (1978) and Claro-Wannier, PRB 19, 6068
  (1979): the gap-labeling ansatz N = s + t alpha predates TKNN;
  the |t| <= q/2 window convention. Context import.
- Avila-Jitomirskaya, Ann. Math. 170, 303 (2009): the Ten Martini
  theorem (Cantor spectrum at irrational flux). Context only: the
  irrational limit is NOT-CLAIMED in P-28; all statements are at
  the ladder's rational rungs.

## LC-19 — 2026-08-28 — the Farey bridge sources, and the Bandt distinction
prediction: P-29
claims-checked:
- Stern 1858 / Brocot 1860-61 / GKP 1989 (LC-7 interop): the
  mediant (a+c)/(b+d) of Farey neighbors is the unique
  minimal-denominator fraction in the open interval - re-verified
  exhaustively per registered interval (EQ1, scan to q = 40).
- Arnold 1961 / standard circle-map theory: subcritical (K < 1)
  sine-map tongues at every rational rotation number, with width
  ~ K^q at small K (the q-th order resonance mechanism) -
  MEASURED as our EQ2 anchor (width ratios 3.998 / 7.992 against
  2^2 / 2^3 for q = 2, 3), not assumed. c23 (Adler) and c27
  (finite-T plateau bias) are the repo's own tongue-adjacent
  instruments.
- Hofstadter 1976: the butterfly's recursive structure follows
  the continued-fraction/Farey organization of the flux; P-7 and
  P-28 are the repo's computed instances (bandwidth ladder, gap
  labels). The composite's butterfly observable S(p/q) is P-7's
  own object.
- Bandt, Adv. Math. 324, 437 (2018), "Finite orbits in
  multivalued maps and Bernoulli convolutions" (the reader's
  candidate inspiration, examined): the (t, x) parameter
  landscapes ("projections") of Bernoulli-convolution densities
  are organized by KNEADING/address curves with landmarks at
  Pisot, Perron, multinacci and doubling parameters - the terms
  Farey, mediant, and Stern-Brocot do not occur in the paper
  (machine census: 0 hits each vs kneading 69, Pisot 68). The
  skeleton is the substitution/kneading tree, NOT the mediant
  tree, so the projections do not transfer to P-29's registered
  mechanism - recorded here precisely so the visual resemblance
  is never cited as evidence. What DOES transfer: (i) phi enters
  as the FIRST MULTINACCI (x^2 = x + 1 heading the ladder
  x^n = x^{n-1} + ... + 1), and Bandt's own Fig. 2 finding that
  the golden parameter t2 ~ 0.618 "apparently marks a phase
  transition" (structure below, blur above) is a new
  ADDRESS-route datum for the VOCABULARY phi taxonomy, imported
  not computed; (ii) a second-bridge candidate is queued (A-18):
  Farey tree vs kneading tree as organizing skeletons, with
  finite-orbit windows of the two-map system {beta x, beta x + 1
  - beta} as the third instrument - a registered claim there
  would need its own shared premise stated in advance.

## LC-20 — 2026-08-28 — the indefinite-causal-order sources
prediction: P-30
claims-checked:
- Oreshkov, Costa, Brukner, Nat. Comms 3, 1092 (2012) / arXiv
  1105.4464: the causal game (Alice generates a and guesses x; Bob
  generates b, b' and guesses y; p = (1/2)[P(x=b|b'=0) +
  P(y=a|b'=1)]), the causal bound 3/4 (their eq. 2, derived from
  Causal Structure + Free Choice + Closed Laboratories), the
  process matrix W = (1/4)[1 + (sz^A2 sz^B1 + sz^A1 sx^B1
  sz^B2)/sqrt2] (their eq. 7), the protocol CJ operators (their
  eqs. 20-23), the reduced-process intermediates (eqs. 25-26),
  and the value (2+sqrt2)/4. THEIR OWN CAVEATS imported verbatim:
  whether (2+sqrt2)/4 is maximal is stated as an open question,
  and the paper itself notes both their bound and violation
  "match the corresponding numbers in the CHSH-Bell inequality" -
  P-30's EQ1 makes that exact (the affine map p = (S+4)/8). No
  physical realization of the OCB process is known (their
  discussion; CTC models break linearity).
- van der Lugt, Barrett, Chiribella, Nat. Comms 14 (2023) / arXiv
  2208.00719: Theorem 1 - under Definite Causal Order,
  Relativistic Causality, Free Interventions: p(b=0, a2=x1|y=0) +
  p(b=1, a1=x2|y=0) + p(b XOR c = yz|x1=x2=0) <= 7/4; the quantum
  switch with control entangled to spacelike Bob achieves 1/2 +
  1/2 + (2+sqrt2)/4 = 1.8536, stated by them as MAXIMAL for
  commuting-Bob scenarios via Tsirelson. Imported context: the
  switch in isolation violates no bipartite causal inequality
  (their refs [5, 6], extended to quantum-controlled circuits in
  [43, 44]).
- Liu et al., PRX Quantum (2026), "Toward an Experimental
  Device-Independent Verification of Indefinite Causal Order"
  (arXiv 2508.04643): photonic implementation of the VLBC
  scenario, spacelike-separated entangled photons, causal
  inequality violated by 24 standard deviations - WITH loopholes
  the authors flag; they expect loophole-free ICO tests to need
  "many generations of experiments" (the Bell-test arc). Imported
  as experimental status, not recomputed.
- Chiribella, D'Ariano, Perinotti, Valiron, PRA 88, 022318
  (2013): the quantum switch supermap W = |0><0| (x) FE +
  |1><1| (x) EF (VLBC eq. 7 convention). Basis of the circuit
  implementation.

## LC-21 — 2026-08-28 — the muon g-2 dissolution (A-17 hygiene)
prediction: none (ledger hygiene; the bit-accounting lesson entry)
claims-checked:
- Muon g-2 Collaboration, PRL (2025), "Measurement of the Positive
  Muon Anomalous Magnetic Moment to 127 ppb" (final report arXiv
  2506.03069-family; muon-g-2.fnal.gov/result2025.pdf): final
  combined a_mu(exp) = 116 592 070.5(14.8) x 10^-11 at 127 ppb;
  the E821+E989 world average quoted by WP25 is
  116 592 071.5(14.5) x 10^-11.
- Muon g-2 Theory Initiative, arXiv 2505.21476 (White Paper 2025,
  May 27 2025): a_mu(SM) = 116 592 033(62) x 10^-11, with the
  hadronic vacuum polarization now taken from LATTICE QCD (the
  2020 data-driven e+e- route is set aside: the low-energy
  cross-section datasets are mutually inconsistent even with
  CMD-3 excluded). Experiment minus theory: 38(63) x 10^-11 =
  0.6 sigma. CONSISTENT.
- The arithmetic of the dissolution, computed from the pinned
  numbers: WP2020 had a_mu(SM) = 116 591 810(43) x 10^-11 and the
  2021-era tension 251(59) x 10^-11 = 4.25 sigma. Between 2020
  and 2025 the THEORY value moved by +223 x 10^-11 (3.8 of the
  old combined sigma) while the EXPERIMENT moved by about
  +10 x 10^-11 (0.17 of it). The anomaly was a property of the
  theory estimate, not of the muon.
- The ledger lesson (the canonical uncertain-null case): every
  model tuned to "explain" the 251 x 10^-11 gap - SUSY slices,
  dark photons, leptoquark fits - spent its parameters buying
  surprisal against a null that was itself mis-estimated; the
  purchased number no longer exists. In bit-accounting terms this
  is the sharpest available warning that BITS BOUGHT AGAINST AN
  UNCERTAIN NULL ARE NOT BANKED, which is why this repo derives
  nulls before computing (register-then-compute) and why P-27's
  fired sign-stability clause treated order-of-magnitude source
  arithmetic as part of the error budget. Interop: the Otto
  mechanization (LC-12) binned alpha^-1 and g_e formulas at 788
  to 2e5 experimental sigma - numerology dies by measurement;
  here an ANOMALY died by theory correction. Both failure modes
  are now on the ledger.

## LC-22 — 2026-08-28 — the second-bridge sources (Bandt, in depth)
prediction: P-31
claims-checked:
- Bandt, Adv. Math. 324, 437 (2018), "Finite orbits in multivalued
  maps and Bernoulli convolutions" (extends LC-19's census): the
  two-map system pinned verbatim from their eq. (1): g0: [0, t] ->
  [0, 1], g0(x) = beta x and g1: [1-t, 1] -> [0, 1], g1(x) =
  beta x + 1 - beta, with t = 1/beta and overlap D = [1-t, t];
  finite orbits of the multivalued map ("network-like orbits", the
  branching tree closing on itself) occur at special algebraic
  parameters; the landmark families: multinacci phi_n (x^n =
  x^{n-1} + ... + 1; "the most obvious landmarks", their Section
  quoted in LC-19) and the doubling numbers psi_n (x^{n+1} =
  2 x^n - x + 1; "another family of Pisot numbers... We call them
  doubling numbers"; their Fig. 1 is drawn at s_2). Their golden
  phase-transition observation (structure below t_2, blur above)
  imported in LC-19.
- The supergolden number psi_2 = 1.754877666... (root of x^3 =
  2 x^2 - x + 1): our computed value matches the classical
  constant; s_2 = 1/psi_2 = 0.569840...
- What P-31 does NOT take from Bandt: none of his theorems are
  re-claimed; the orbit computations are our own instrument (exact
  Q(beta) arithmetic), the starting set (the overlap boundary
  {1-t, t}) is our registered choice, and the comparison against
  the Farey skeleton is our registered question, absent from his
  paper (LC-19's census: Farey/mediant/Stern occur zero times
  there).

## LC-23 — 2026-08-28 — the parity-factorial design imports
prediction: P-32
claims-checked:
- Imported from LC-3/LC-4 (not re-fetched): Frolov et al., PRB 74,
  020503(R) (2006) and Lazarides (Supercond. Sci. Technol. 21,
  045003 (2008); PRB 77, 214419 (2008)): in driven 0-pi Josephson
  arrays the half-turn offset CREATES half-integer Shapiro steps,
  with alternating 0-pi arrays giving half-integer steps for EVEN
  junction number and integer steps for odd - an explicit N-parity
  claim. LC-3's reconciliation hypothesis, never tested until now:
  the sign difference with E1's shrink-not-shift finding is the
  DRIVE TYPE (per-site pinning vs bias coupling to phase
  differences).
- P-9/R-6 (in-repo): no parity under per-site pinning on the
  one-seam ring, N = 4..9, attractor-controlled protocol; widths
  pinned in p9_results_attractor.json; the N = 7 non-monotonicity
  at K = 1.4 remains unexplained and is NOT this line's target.
- The derived refinement (EQ1, pure arithmetic, ours): an
  alternating-0-pi RING of N bonds carries net frustration
  f(N) = (floor(N/2)/2) mod 1 and, for odd N, an alternation
  defect. The imported even/odd claim therefore CANNOT be the
  whole story on a ring: evens split into {4, 8} (f = 0, clean)
  and {6} (f = 1/2), odds into {5, 9} (defect, f = 0) and {7}
  (defect + f = 1/2). P-32 registers f as the organizing variable
  and lets the data choose between f and plain parity. (The
  Josephson papers concern open/biased ARRAY geometries; the ring
  closure constraint is the source of the refinement - this
  difference is declared, not hidden.)
