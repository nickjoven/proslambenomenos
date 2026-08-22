# Synonym table: one object, many names

Groups of terms that name the same mathematical object across the
domains this repository has touched, with the standard term first
and the VOCABULARY.md term in bold. Last block: the coinages of
D. Gunter, "The Hodge Conjecture Through Half-Center Geometry"
(Medium, 2025-06-25), mapped to what they denote - included because
the owner asked, and because several of its terms are ordinary
objects under new names (one with an error).

## Structural (the "count" side)

| standard | synonyms across domains | repo term |
|---|---|---|
| holonomy | gluing data; transition function; Aharonov-Bohm phase; flux per plaquette; twist; seam offset; Berry phase (closed path); Volterra mismatch (disclination angle); pin/spin structure choice (sign case) | **holonomy** |
| winding number | rotation number (per period); degree; topological charge; turns; vorticity (quantised); Chern number (2D analogue); impact count m per n periods | **winding / count** |
| locally constant function of the medium | sector; bundle class; superselection sector; quantised plateau; (m,n) orbit label; parity class; w_1 | **sector / class** |
| invariant integral | Gauss-Bonnet total; index (Atiyah-Singer); deficit-angle sum; circulation of a closed form over a cycle; Hall conductance | **invariant integral** |
| rational locking ratio p/q | Arnold tongue label; Devil's-staircase plateau; Shapiro step index; Farey/Stern-Brocot node; (m,n) impact orbit; mode-locked state; commensurate phase | **locking / plateau** |

## Dynamical (the "anchor" side)

| standard | synonyms | repo term |
|---|---|---|
| external periodic forcing | drive; pinning (lab-frame potential); bias current; bow; pump (parametric); clock; stroboscope | **drive** |
| tongue width | locking range; hold-in range (PLL); capture range; Adler range; plateau width; Shapiro-step width | medium part of **locking** |
| weak discontinuity | corner (Helmholtz); kink in slope; characteristic front; wavefront; pulse edge; shock (WRONG synonym - strong discontinuity, LC-4) | **corner** |
| soliton | solitary wave; Toda/KdV pulse; breather (oscillating case); fluxon (Josephson); semifluxon (half, pi-junction); gravisoliton (Belinski-Zakharov, by mechanism only) | **soliton** |
| critical point / marginal case | saddle-node; grazing; tangency to the line at infinity (parabola, E = 0 orbit); null ray; Dirac point (bands touching); Q = 1 (Toomre); K_c (Kuramoto); f_max (Schelleng) | **critical point** |
| dissipation | friction; damping; restitution loss (1 - r); entropy production; irreversibility; record-making; Landauer cost | **dissipation** |
| resolution limit | Gabor limit; time-bandwidth product; Nyquist (sampled case); finite-T bias of a rotation number (P-8); cosmic variance (one sky) | **resolution** |
| coarse-graining map | flow -> Poincare map; string -> delay line (d'Alembert); flight -> impact map; stroboscopic section; reflection function (MSW 1983) | (transform; no single term) |

## Conflations this repository has had to undo

| said | actually two objects | where |
|---|---|---|
| "forced" | driven (classical) vs necessitated-by-structure (the corpus) | R-1; the drive forces, counting labels the response |
| "the twisted sector" | half-integer-m modes (x-parity) vs the orientation bundle | LC-5, 7a |
| "chatter" | numerical artifact vs complete chatter (Budd-Dux) | P-4 audit S2; c30 |
| "shock" | strong discontinuity vs weak (corner) | LC-4 S5 |
| "mass" | mass values (numerology on an anchor) vs mass gap (spectral) | X-9 |
| "non-commutative" | operator algebra (QM) vs "built on a manifold" (content-free) | LC-8 |
| "cut / clamp" | boundary condition vs the absence of a gluing (holonomy lost) | P-4 audit S1 |

## Gunter's "Half-Center Geometry" (Medium, 2025), term by term

| coinage | what it denotes in standard language | status |
|---|---|---|
| Half-Center Space H = {u in [-1/2, 1/2], v in R}/((-1/2,v) ~ (1/2,v)} with ds^2 = du^2 + dv^2 | the flat cylinder S^1 x R, circumference 1, in coordinates centred at 0 | ordinary object; "half-centre" names the coordinate choice |
| involution sigma(u,v) = (-u,v) | the reflection of the cylinder | ordinary; its fixed set on S^1 is TWO lines, u = 0 and u = 1/2 - the article names only one |
| critical line u = 0 "corresponding to Re(s) = 1/2" | the fixed line of the reflection, identified by analogy with the zeta functional-equation symmetry s <-> 1 - s | analogy; no map between the cylinder and the s-plane is given |
| counting domain / measuring domain | discrete vs continuous; **count** vs **scale** in VOCABULARY.md | ordinary distinction; the repo's version is earned by artifacts, the article's by assertion |
| manipulation domain, "puncture" | undefined - no set, map, or equation | content-free |
| prime-phase resonance pattern psi(u,v) = sum_p a_p e^{2 pi i (p u + phi_p(v))} | a Fourier series on the circle whose frequencies are restricted to primes | ordinary object (prime-supported Fourier series); "resonance" unearned |
| stability criterion: "maximum amplitude concentration on u = 0" | constructive interference at u = 0, i.e. the phases phi_p(0) aligned | a choice of where the maximum sits, true of any Fourier series with aligned phases at a point; not a property |
| H^{p,p} "on the critical line", H^{p,q} <-> H^{q,p} as sigma | the self-conjugate classes under complex conjugation H^{p,q} = conj(H^{q,p}) | the conjugation symmetry is standard Hodge theory; the identification with a line on a cylinder is analogy |
| cycle-resonance correspondence; balance condition; stability-realisability conjecture | restatements of the Hodge conjecture in the article's own words, with "stable attractor" undefined | not a reformulation: no object on the cylinder is constructed from a variety X |
| observer position; consciousness-modulated collapse (after Schepis) | no mathematical content | content-free |

Verdict on the article in the repo's terms: its geometric
scaffold is the flat cylinder with a reflection (two ordinary
objects), its "patterns" are prime-supported Fourier series, and
the Hodge conjecture is restated rather than attacked - the
statement "every Hodge class is algebraic" is given correctly and
then rephrased in terms no variety is ever mapped into. No equation
connects X to H. One checkable error: the reflection of the circle
fixes u = 1/2 as well as u = 0. Mood: none; everything above is
definitional.
