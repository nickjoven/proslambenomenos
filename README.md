# Proslambenomenos

**The added tone: a fundamental reference frequency for synchronization gravity.**

N. Joven — March 2026 — [ORCID 0009-0008-0679-0812](https://orcid.org/0009-0008-0679-0812)

---

In ancient Greek music theory, the *proslambenomenos* (προσλαμβανόμενος) was the "added tone" — the lowest pitch in the Greater Perfect System, the reference from which every interval was measured. It did not belong to any tetrachord. It simply *was*, the ground note that made the entire harmonic structure intelligible.

This repository proposes a physical analogue: the cosmological constant $\Lambda$ sets a fundamental oscillation frequency

$$\nu_\Lambda \;=\; c\,\sqrt{\Lambda/3}$$

and the MOND acceleration scale, the Hubble rate, and the galactic synchronization threshold are all overtones of this single reference. They are not independent coincidences — they are intervals measured from the proslambenomenos.

## Positioning: from galaxies to global cosmic mechanics

The MOND acceleration scale $a_0 \approx 1.2 \times 10^{-10}\;\text{m s}^{-2}$ has long been recognized as an empirical threshold below which Newtonian gravity underpredicts galactic rotation curves. The numerical coincidence $a_0 \approx cH_0 / 2\pi$ ties this galactic-scale phenomenon to the cosmological expansion rate, but MOND as traditionally formulated does not explain *why* such a connection exists.

This framework provides the missing mechanism. The Kuramoto synchronization model, applied to self-gravitating matter on a manifold via the ADM decomposition of general relativity, produces the MOND transition as a phase transition in oscillator coherence:

- **Above $a_0$**: coupling is supercritical, oscillators fully synchronize, and Newtonian gravity holds.
- **Below $a_0$**: coupling is subcritical, coherence drops as $r \propto \sqrt{K - K_c}$, and the synchronization deficit appears as a dark-matter-like phantom in the rotation curve.

The $2\pi$ factor in $a_0 = cH_0 / 2\pi$ is not a coincidence or a fit parameter — it is the ratio of angular frequency to cycle frequency that appears in the Kuramoto critical coupling formula $K_c = 2 / (\pi\, g(0))$, where $g(0)$ is the oscillator frequency distribution evaluated at its mean.

The extrapolation from galactic phenomenology to global cosmic mechanics is therefore structural: $\Lambda$, $H_0$, and $a_0$ form a single chain

$$\Lambda \;\xrightarrow{c\sqrt{\cdot/3}}\; \nu_\Lambda \;\xrightarrow{\div\sqrt{\Omega_\Lambda}}\; H_0 \;\xrightarrow{c/2\pi}\; a_0$$

where the first arrow is the Friedmann equation (standard cosmology) and the second is the Kuramoto critical coupling (this framework). The cosmological constant is not merely correlated with the MOND scale — it *sets* it, through the synchronization mechanism.

## Glossary

- **$\Lambda$ (cosmological constant)**: A constant in Einstein's field equations representing the energy density of empty space. It drives the accelerating expansion of the universe.
- **$\nu_\Lambda$ (proslambenomenos frequency)**: The fundamental oscillation frequency $c\sqrt{\Lambda/3}$ set by the cosmological constant. In a pure de Sitter universe (vacuum, no matter), this equals the Hubble rate exactly.
- **$H_0$ (Hubble parameter)**: The present-day expansion rate of the universe, approximately $2.2 \times 10^{-18}\;\text{s}^{-1}$.
- **$a_0$ (MOND acceleration scale)**: The acceleration threshold ($\approx 1.2 \times 10^{-10}\;\text{m s}^{-2}$) below which galactic dynamics deviate from Newtonian predictions. Empirically determined from galaxy rotation curves.
- **MOND (Modified Newtonian Dynamics)**: A phenomenological framework (Milgrom 1983) that modifies Newtonian gravity below the acceleration scale $a_0$ to explain galaxy rotation curves without invoking dark matter.
- **Kuramoto model**: A mathematical model of coupled oscillators (Kuramoto 1975) that exhibits a phase transition from incoherence to synchronization at a critical coupling strength $K_c$. The order parameter $r \in [0,1]$ measures the degree of coherence.
- **ADM formalism**: The Arnowitt–Deser–Misner decomposition of general relativity, which splits spacetime into spatial slices evolving in time. The dynamical variables are the spatial metric $\gamma_{ij}$ (geometry of each slice), the lapse $N$ (clock rate), and the shift $N^i$ (coordinate drift between slices).
- **Lyapunov function**: A function that decreases monotonically along the trajectories of a dynamical system, proving stability and convergence to an equilibrium.
- **Ott–Antonsen reduction**: An exact dimensionality reduction (Ott & Antonsen 2008) for Kuramoto oscillators with Lorentzian frequency distributions, reducing the infinite-dimensional phase dynamics to a low-dimensional ODE on the order parameter $r$.
- **Renzo's Rule**: The empirical observation (Sancisi 2004) that every feature in a galaxy's baryonic luminosity profile is mirrored in its rotation curve and vice versa — there are no unexplained kinematic features.
- **Order parameter ($r$)**: In the Kuramoto model, the magnitude of the complex mean field of the oscillator phases. $r = 0$ means complete incoherence; $r = 1$ means perfect synchronization. In the Kuramoto–Einstein mapping, $r$ corresponds to the lapse function $N$.

## Contents

| Document | Description |
|----------|-------------|
| [`PROOF_C_bridge.md`](PROOF_C_bridge.md) | **Proof Chain C: The Bridge** — end-to-end geometric proof from the polynomial to Ω_Λ = 13/19, R = 6×13⁵⁴, and a₀. Connects [Proof A (gravity)](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/PROOF_A_gravity.md) and [Proof B (quantum)](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/PROOF_B_quantum.md). |
| [`proslambenomenos.md`](proslambenomenos.md) | From $\Lambda$ to $a_0$: three constants, one frequency |
| [`kuramoto_einstein_mapping.md`](kuramoto_einstein_mapping.md) | The Kuramoto–Einstein dictionary: explicit derivative mapping between synchronization and ADM gravity |
| [`lyapunov_uniqueness.md`](lyapunov_uniqueness.md) | Lyapunov functional and the dissipation argument for uniqueness |
| [`renzos_rule_from_kuramoto.md`](renzos_rule_from_kuramoto.md) | Renzo's Rule from Kuramoto self-consistency |
| [`notebooks/`](notebooks/) | Companion Jupyter notebooks |
| [`docs/`](docs/) | GitHub Pages walkthrough |

### Notebooks

| Notebook | Description |
|----------|-------------|
| [`01_proslambenomenos_derivation.ipynb`](notebooks/01_proslambenomenos_derivation.ipynb) | Numerical chain: $\Lambda \to \nu_\Lambda \to H_0 \to a_0$ |
| [`02_lyapunov_functional.ipynb`](notebooks/02_lyapunov_functional.ipynb) | Lyapunov descent, uniqueness from 10 random ICs, galaxy formation |
| [`03_renzo_from_kuramoto.ipynb`](notebooks/03_renzo_from_kuramoto.ipynb) | Forward/inverse Renzo's Rule, MOND transition |
| [`04_phase_portrait.ipynb`](notebooks/04_phase_portrait.ipynb) | Animated phase portrait: Newtonian → MOND sweep on NGC 2403 |

## Walkthrough

[**nickjoven.github.io/proslambenomenos**](https://nickjoven.github.io/proslambenomenos/) — interactive overview with status map and companion links.

## License

[CC0 1.0 Universal](LICENSE) — No rights reserved.
