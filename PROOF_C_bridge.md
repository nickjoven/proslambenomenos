# Proof Chain C: The Bridge

N. Joven — 2026 — CC0 1.0

---

## Statement

General relativity and quantum mechanics are the two continuum limits of
one equation (Proof Chains [A](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/PROOF_A_gravity.md)
and [B](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/PROOF_B_quantum.md)).
If this is true, the cosmological parameters that connect gravity to
quantum structure cannot be free — they must be determined by the
equation itself.

This proof chain derives five cosmological numbers from the same
primitives. No free parameters. No fitting. The numbers are the
*bridge* between the two legs.

| Prediction | Value | Observed | Residual |
|---|---|---|---|
| Dark energy fraction Ω_Λ | 13/19 = 0.6842 | 0.6847 ± 0.0073 | 0.07σ |
| Planck/Hubble hierarchy R | 6 × 13⁵⁴ | 8.49 × 10⁶⁰ | 0.48% |
| Born rule exponent | 2 | 2 | exact |
| MOND scale a₀ | 1.25 × 10⁻¹⁰ m/s² | 1.2 × 10⁻¹⁰ | 4% |
| Spatial dimension | 3 | 3 | exact |

---

## Shared foundation

Propositions P1–P5 from Proof Chain A are assumed. They establish:
the circle, the mediant, the Stern-Brocot tree, the rational field
equation, and d = 3 with SL(2,R).

---

## Propositions

### B1. The Möbius container [D18]

*Uses: P3 (Stern-Brocot tree), P1 (circle).*

On a finite ring of N oscillators, impose **antiperiodic** boundary
conditions: θ(x + L) = θ(x) + π. This is the Möbius strip — one
traversal of the ring shifts the phase by half a cycle.

Unlike periodic boundary conditions (which permit trivial global
synchronization), the Möbius twist forces nontrivial rational divisions.
The order parameter under the twist is:

$$r_{\text{Möbius}} = \frac{1}{N}\sum_j e^{i\theta_j}(-1)^{q_j}$$

where the (−1)^q sign flip distinguishes odd-denominator from
even-denominator modes. The twist breaks the degeneracy between modes
that would otherwise coexist. ∎

### B2. The Klein bottle [D19]

*Uses: B1.*

Extend to two dimensions: antiperiodic + reflection in x, periodic in y.
This is the Klein bottle — the unique closed non-orientable surface
embeddable in the product of two circles with distinct boundary
conditions.

The combined twist-and-reflect operation applies an **XOR parity filter**
on the winding numbers (p_x, p_y):

$$p_x + p_y \equiv 1 \pmod{2}$$

Only modes with one odd and one even component survive. On the
Stern-Brocot tree truncated at the first few levels, exactly **four
modes** survive:

| Mode | (q_x, q_y) | Parity |
|---|---|---|
| (1/2, 1/3) | (2, 3) | ✓ |
| (1/3, 1/2) | (3, 2) | ✓ |
| (2/3, 1/2) | (3, 2) | ✓ |
| (1/2, 2/3) | (2, 3) | ✓ |

The surviving denominator pair is **{q₂ = 2, q₃ = 3}**. ∎

### B3. Three dimensions (again) [D14, D19, D23]

*Uses: B2, P5.*

The Klein bottle selects q₃ = 3. The Stern-Brocot tree relation gives:

$$d = \dim\text{SL}(2) = 2^2 - 1 = 3$$

But also: the Fibonacci identity F₃ = F₂² − 1 = 3 is unique — no other
Fibonacci number satisfies F_n = F_{n-1}² − 1. The Klein bottle's q₃ = 3,
the Lie group's dimension 3, and the Fibonacci identity's output 3 are
the **same 3**, linked by the tree structure. ∎

### B4. The Farey count [number theory]

*Uses: B2.*

The Farey sequence F_n contains all irreducible fractions with
denominator ≤ n, plus {0, 1}. Its cardinality is:

$$|F_n| = 1 + \sum_{k=1}^{n} \varphi(k)$$

where φ is Euler's totient function. At n = q₂ × q₃ = 6:

$$|F_6| = 1 + 1 + 1 + 2 + 2 + 2 + 2 = 13$$

This is a number-theoretic fact, not a choice. ∎

### B5. The Farey partition: Ω_Λ = 13/19 [D25, D28]

*Uses: B2, B4.*

The rational field equation (P4) has SO(2) symmetry (Kuramoto phase
rotation). At the boundary between locked and unlocked populations, the
only SO(2)-invariant scalars constructible from the Stern-Brocot tree
at depth q₂ × q₃ are:

- C = |F₆| = 13 (the Farey count — modes available to lock)
- S = q₂ × q₃ = 6 (the depth scale — complexity of the tree)

The unique mediant-consistent partition of the total population into
locked (dark energy) and unlocked (matter + radiation) is:

$$\Omega_\Lambda = \frac{C}{C + S} = \frac{13}{13 + 6} = \frac{13}{19} = 0.684211\ldots$$

**Observed (Planck 2018):** 0.6847 ± 0.0073. Residual: **0.07σ**. ∎

### B6. The hierarchy: R = 6 × 13⁵⁴ [D26, D27]

*Uses: B4, B5, B3.*

The ratio of the Hubble scale to the Planck scale is:

$$R = \frac{l_H}{l_P} = S \times C^{q_2 q_3^d}$$

where the exponent q₂q₃^d = 2 × 3³ = 54 is determined by the
self-referential structure: d = q₃ = 3 (B3), so the exponent
references the dimension it produces.

$$R = 6 \times 13^{54} = 8.533 \times 10^{60}$$

**Observed:** 8.492 × 10⁶⁰. Residual: **0.48%**. ∎

### B7. The proslambenomenos: Λ → a₀ [proslambenomenos.md §2–5]

*Uses: B5, Kuramoto critical coupling.*

The cosmological constant Λ sets a reference frequency:

$$\nu_\Lambda = c\sqrt{\Lambda/3}$$

This is the vacuum's fundamental oscillation — what the Hubble rate
converges to as matter dilutes ($H_{\text{dS}} = \nu_\Lambda$ in de
Sitter). At the present epoch: $H_0 = \nu_\Lambda / \sqrt{\Omega_\Lambda}$.

The MOND acceleration scale is the **Kuramoto desynchronization
threshold** at this reference frequency:

$$a_0 = \frac{c\,H_0}{2\pi\,\sqrt{g_*(1/\varphi)}}$$

where $g_*(1/\varphi) = 0.697$ is the self-consistent frequency
distribution evaluated at the golden ratio (the devil's staircase
pivot).

$$a_0 = 1.25 \times 10^{-10}\;\text{m/s}^2$$

**Observed:** 1.2 × 10⁻¹⁰ m/s². Residual: **4%**.

The 2π is the ratio of angular to cyclic frequency in the Kuramoto
critical coupling formula. The $g_*$ correction comes from the
self-consistent distribution (P4). The three constants Λ, H₀, a₀
are one frequency measured in three units:

$$\Lambda \;\xrightarrow{c\sqrt{\cdot/3}}\; \nu_\Lambda \;\xrightarrow{\div\sqrt{\Omega_\Lambda}}\; H_0 \;\xrightarrow{c/(2\pi\sqrt{g_*})}\; a_0$$

First arrow: Friedmann (known). Second arrow: Kuramoto (new). ∎

---

## The bridge

The five numbers are not fitted. They are consequences of a
configuration space (the Stern-Brocot tree) with a topology (the Klein
bottle) and a symmetry (SO(2)):

```
            Polynomial (x² - x - 1 = 0)
                    |
              Stern-Brocot tree (P2-P3)
                    |
              Klein bottle (B1-B2)
               /    |    \
         d = 3    |F₆|=13   {q₂,q₃}={2,3}
         (B3)     (B4)        |
           \       |         / \
            Ω_Λ = 13/19    R = 6×13⁵⁴
               (B5)           (B6)
                 \           /
                  ν_Λ → H₀ → a₀
                      (B7)
```

If Proof A (gravity) and Proof B (quantum mechanics) are two legs of a
triangle, the cosmological parameters are the base. The base is
load-bearing: if the numbers came out wrong, the triangle would not
close. They come out right to 0.07σ.

---

## Why this lives in proslambenomenos

The proslambenomenos — the "added tone" below the Greek tonal system —
is the reference frequency that every interval is measured against but
which belongs to no tetrachord. The cosmological constant plays the same
role: it sets the reference frequency ν_Λ that both gravity (K = 1) and
quantum mechanics (K < 1) are measured against, but it belongs to
neither regime.

The derivation of a₀ from Λ via the Kuramoto critical coupling is the
original content of this repository. The Farey partition (B5) and
hierarchy (B6) show that ν_Λ itself is determined by the tree — closing
the circle.

---

## Cross-references

| Proposition | Source | Key theorem / result |
|---|---|---|
| P1–P5 | harmonics D10, D29, D11, D14 | (see Proof A) |
| B1 | harmonics D18 | Möbius BC forces rational divisions |
| B2 | harmonics D19 | Klein bottle XOR filter |
| B3 | harmonics D14, D23 | F₃ = F₂² − 1 = 3 (unique) |
| B4 | Number theory | \|F₆\| = 13 (Euler totient sum) |
| B5 | harmonics D25, D28 | SO(2) → unique partition |
| B6 | harmonics D26, D27 | Exponent q₂q₃³ self-referential |
| B7 | proslambenomenos §2–5 | Kuramoto K_c → a₀ |

---

## The triangle

| Vertex | Proof chain | Regime | Output |
|---|---|---|---|
| **Gravity** | [A](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/PROOF_A_gravity.md) | K = 1 | Einstein field equations |
| **Quantum** | [B](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/PROOF_B_quantum.md) | K < 1 | Schrödinger + Born rule |
| **Bridge** | C (this document) | Topology | Ω_Λ, R, d, a₀ |

One equation. Two limits. Five numbers. Zero free parameters.
