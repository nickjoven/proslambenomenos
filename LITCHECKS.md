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
