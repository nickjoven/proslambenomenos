# Kuramoto-Einstein Mapping: Explicit Derivatives

N. Joven — March 2026 — CC0 1.0

*Technical supplement to the [proslambenomenos framework](proslambenomenos.md).*

---

## Motivation

The [proslambenomenos](proslambenomenos.md) derives $a_0$ from $\Lambda$ via the Kuramoto critical coupling. The [Lyapunov uniqueness proof](lyapunov_uniqueness.md) and [Renzo's Rule derivation](renzos_rule_from_kuramoto.md) build on a mapping between Kuramoto synchronization fields and ADM gravitational variables. This document works through that mapping component by component, writing down the explicit time and spatial derivatives on both sides.

The goal is to show that the ADM evolution equations — the dynamical content of Einstein's field equations — have a natural reading as continuum Kuramoto dynamics on a manifold, and to identify precisely where the two systems constrain each other.

---

## 1. The Two Systems of Equations

### 1.1 Continuum Kuramoto on a Manifold

The standard Kuramoto model for $N$ discrete oscillators is:

$$\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N} \sum_{j=1}^{N} \sin(\theta_j - \theta_i)$$

In the continuum limit on a Riemannian manifold $(M, \gamma)$, the phase field $\theta(x, t)$ evolves as:

$$\frac{\partial \theta}{\partial t}(x,t) = \omega(x) + \int_M K(x, x') \sin\bigl(\theta(x',t) - \theta(x,t)\bigr) \, d\mu_\gamma(x')$$

where $d\mu_\gamma = \sqrt{\det \gamma} \, d^3x$ is the Riemannian volume element.

The **local order parameter** is:

$$r(x,t) \, e^{i\psi(x,t)} = \int_M K(x, x') \, e^{i\theta(x',t)} \, d\mu_\gamma(x')$$

where $r(x,t) \in [0,1]$ measures local coherence and $\psi(x,t)$ is the local mean phase. This simplifies the continuum Kuramoto equation to:

$$\boxed{\frac{\partial \theta}{\partial t} = \omega(x) + r(x,t) \sin\bigl(\psi(x,t) - \theta(x,t)\bigr)}$$

The **coherence field** $r(x,t)$ has its own dynamics. Differentiating the order parameter definition:

$$\frac{\partial r}{\partial t} e^{i\psi} + i r \frac{\partial \psi}{\partial t} e^{i\psi} = \int_M K(x, x') \, i \frac{\partial \theta}{\partial t}(x',t) \, e^{i\theta(x',t)} \, d\mu_\gamma(x')$$

Separating real and imaginary parts gives the coupled evolution:

$$\frac{\partial r}{\partial t} = \int_M K(x,x') \frac{\partial \theta}{\partial t}(x',t) \sin\bigl(\theta(x',t) - \psi(x,t)\bigr) \, d\mu_\gamma(x')$$

$$r \frac{\partial \psi}{\partial t} = \int_M K(x,x') \frac{\partial \theta}{\partial t}(x',t) \cos\bigl(\theta(x',t) - \psi(x,t)\bigr) \, d\mu_\gamma(x')$$

### 1.2 ADM Formulation of Einstein's Equations

The ADM decomposition writes the spacetime metric as:

$$ds^2 = -N^2 dt^2 + \gamma_{ij}(dx^i + N^i dt)(dx^j + N^j dt)$$

where $N$ is the lapse, $N^i$ is the shift, and $\gamma_{ij}$ is the spatial metric on each time slice $\Sigma_t$.

The dynamical content of Einstein's equations splits into **evolution equations** and **constraint equations**.

**Evolution equations:**

$$\frac{\partial \gamma_{ij}}{\partial t} = -2N \mathcal{K}_{ij} + D_i N_j + D_j N_i$$

$$\frac{\partial \mathcal{K}_{ij}}{\partial t} = -D_i D_j N + N\bigl({}^{(3)}R_{ij} + \mathcal{K}\mathcal{K}_{ij} - 2\mathcal{K}_{ik}\mathcal{K}^k{}_j\bigr) + \mathcal{L}_{\vec{N}} \mathcal{K}_{ij} - 8\pi G \, N \Bigl(S_{ij} - \frac{1}{2}\gamma_{ij}(S - \rho)\Bigr)$$

where $\mathcal{K}_{ij}$ is the extrinsic curvature, $D_i$ is the covariant derivative on $\Sigma_t$, ${}^{(3)}R_{ij}$ is the spatial Ricci tensor, and $\rho$, $S_{ij}$ are matter projections.

**Constraint equations:**

$${}^{(3)}R + \mathcal{K}^2 - \mathcal{K}_{ij}\mathcal{K}^{ij} = 16\pi G \rho \qquad \text{(Hamiltonian constraint)}$$

$$D_j(\mathcal{K}^{ij} - \gamma^{ij}\mathcal{K}) = 8\pi G \, j^i \qquad \text{(momentum constraint)}$$

---

## 2. The Dictionary

The mapping identifies Kuramoto fields with ADM fields:

| Kuramoto Field | ADM Field | Interpretation |
|---|---|---|
| $r(x,t)$ — local coherence | $N$ — lapse function | **Coherence is clock rate.** Full synchronization ($r = 1$): clocks tick at coordinate rate. Decoherence ($r \to 0$): clocks freeze. At the event horizon $r = 0 \Leftrightarrow N = 0$. |
| $\partial_i \psi$ — mean phase gradient | $N_i$ — shift vector | **Phase gradients are coordinate drift.** A spatial gradient in the mean phase means the synchronization pattern drifts across slices. |
| $C_{ij}(x,t)$ — coherence tensor | $\gamma_{ij}$ — spatial metric | **Synchronization structure is geometry.** The two-point phase correlation $C_{ij} \sim \langle e^{i(\theta(x) - \theta(x+dx))} \rangle$ defines an effective metric on the oscillator manifold. |
| $\partial_t C_{ij}$ — coherence evolution | $\partial_t \gamma_{ij}$ — metric evolution | **Desynchronization rate is extrinsic curvature.** See §3. |
| $\omega(x)$ — natural frequency | $\sqrt{4\pi G \rho(x)}$ — local Jeans frequency | **Matter sets the natural frequency.** The Jeans frequency $\omega_J = \sqrt{4\pi G\rho}$ is the natural oscillation frequency of a self-gravitating fluid element (Binney & Tremaine, §5.2). Energy density determines how fast the local oscillator wants to tick. |
| $K(x,x')$ — coupling kernel | $G_\gamma(x,x')$ — Green's function of $D^2$ on $(\Sigma, \gamma)$ | **Coupling propagates through the spatial geometry.** The Laplacian's Green's function is the gravitational potential propagator. |

### 2.1 The Coherence Tensor

The spatial metric $\gamma_{ij}$ needs a synchronization-theoretic definition. Define the **coherence tensor** from the two-point function of the phase field:

$$C_{ij}(x) = \lim_{\epsilon \to 0} \frac{1}{\epsilon^2} \Bigl\langle \cos\bigl(\theta(x + \epsilon \, \hat{e}_i) - \theta(x)\bigr) \cos\bigl(\theta(x + \epsilon \, \hat{e}_j) - \theta(x)\bigr) \Bigr\rangle$$

For a nearly synchronized field ($\theta$ slowly varying), expand to second order:

$$C_{ij}(x) \approx \delta_{ij} - \langle \partial_i \theta \, \partial_j \theta \rangle$$

The metric is:

$$\gamma_{ij} = \frac{C_{ij}}{C_0}$$

where $C_0$ normalizes to the background coherence. Perfect synchronization ($\partial_i \theta = 0$ everywhere) gives the flat metric. Phase gradients deform it.

### 2.2 The Jeans frequency identification

The identification $\omega(x) = \sqrt{4\pi G\rho(x)}$ deserves explicit justification, since the rest of the framework builds on it.

For a self-gravitating fluid element at density $\rho$, the Jeans analysis (Jeans 1902; Binney & Tremaine 2008, §5.2) gives the dispersion relation:

$$\omega^2 = c_s^2 k^2 - 4\pi G\rho$$

where $c_s$ is the sound speed and $k$ is the wavenumber. The Jeans frequency $\omega_J = \sqrt{4\pi G\rho}$ is the natural oscillation frequency at $k = 0$ — the frequency at which a uniform self-gravitating medium oscillates under its own gravity when sound-speed support is negligible.

This is the gravitational analogue of the plasma frequency $\omega_p = \sqrt{ne^2/(\epsilon_0 m_e)}$: the collective oscillation frequency set by the density of the medium. In both cases, the frequency scales as the square root of the density, and the collective oscillation at this frequency is the mechanism by which the medium responds to perturbations.

In the Kuramoto picture, each spatial position $x$ hosts an oscillator whose natural frequency is set by the local density: faster where dense, slower where dilute. This is not a postulate — it is the Jeans frequency, which is textbook gravitational physics. The Kuramoto model adds the coupling mechanism (synchronization through the gravitational Green's function) and the order parameter (coherence $r \leftrightarrow$ lapse $N$).

---

## 3. Explicit Derivative Mapping

### 3.1 First Time Derivative: Metric Evolution ↔ Desynchronization Rate

**ADM side:**

$$\frac{\partial \gamma_{ij}}{\partial t} = -2N\mathcal{K}_{ij} + D_i N_j + D_j N_i$$

**Kuramoto side:** Differentiating the coherence tensor,

$$\frac{\partial C_{ij}}{\partial t} = -2 \left\langle \partial_i \theta \, \partial_j \left(\frac{\partial \theta}{\partial t}\right) \right\rangle$$

Substituting the Kuramoto equation $\partial_t \theta = \omega + r \sin(\psi - \theta)$:

$$\frac{\partial C_{ij}}{\partial t} = -2 \bigl\langle \partial_i \theta \, \partial_j \bigl[\omega + r \sin(\psi - \theta)\bigr] \bigr\rangle$$

$$= -2 \langle \partial_i \theta \, \partial_j \omega \rangle - 2 \bigl\langle \partial_i \theta \, \partial_j \bigl[r \sin(\psi - \theta)\bigr] \bigr\rangle$$

Under the dictionary $r \leftrightarrow N$ and $\partial_i \psi \leftrightarrow N_i$, the second term expands as:

$$\partial_j \bigl[r \sin(\psi - \theta)\bigr] = (\partial_j r) \sin(\psi - \theta) + r \cos(\psi - \theta)(\partial_j \psi - \partial_j \theta)$$

**Matching term by term:**

| Kuramoto Term | ADM Term | Reading |
|---|---|---|
| $-2 r \langle \partial_i \theta \cos(\psi - \theta) \, \partial_j \theta \rangle$ | $-2N\mathcal{K}_{ij}$ | **Extrinsic curvature is the phase-weighted desynchronization.** $\mathcal{K}_{ij} \sim \langle \partial_i \theta \cos(\psi - \theta) \partial_j \theta \rangle$ measures how phase gradients rotate relative to the mean field. |
| $r \langle \partial_i \theta \cos(\psi-\theta) \rangle \partial_j \psi + (i \leftrightarrow j)$ | $D_i N_j + D_j N_i$ | **Lie derivative of the shift is the symmetric coupling between phase gradient and mean-field drift.** |
| $-2 \langle \partial_i \theta \, \partial_j \omega \rangle$ | (matter source) | **Natural frequency gradients source metric evolution.** Spatial variation in $\omega(x)$ — i.e., matter density gradients — drives geometric change. |

This gives the **explicit identification of extrinsic curvature**:

$$\boxed{\mathcal{K}_{ij}(x,t) = \bigl\langle \partial_i \theta(x,t) \, \cos\bigl(\psi(x,t) - \theta(x,t)\bigr) \, \partial_j \theta(x,t) \bigr\rangle}$$

Extrinsic curvature measures how much the local phase gradients are *misaligned with the mean field*. When $\theta \approx \psi$ (near synchronization), $\cos(\psi - \theta) \approx 1$ and $\mathcal{K}_{ij}$ reduces to the phase gradient correlation. When $\theta$ and $\psi$ are orthogonal, $\mathcal{K}_{ij} = 0$ — complete decoherence contributes no extrinsic curvature.

### 3.2 Second Time Derivative: Curvature ↔ Synchronization Acceleration

**ADM side:** The evolution of extrinsic curvature contains the spatial Ricci tensor ${}^{(3)}R_{ij}$ — second spatial derivatives of the metric. Through the dictionary, these become second spatial derivatives of the coherence tensor, i.e., the curvature of the synchronization landscape.

Differentiating $\mathcal{K}_{ij}$:

$$\frac{\partial \mathcal{K}_{ij}}{\partial t} = \bigl\langle \partial_i \dot{\theta} \cos(\psi - \theta) \, \partial_j \theta \bigr\rangle + \bigl\langle \partial_i \theta \cos(\psi - \theta) \, \partial_j \dot{\theta} \bigr\rangle + \bigl\langle \partial_i \theta \bigl[-\sin(\psi-\theta)(\dot{\psi}-\dot{\theta})\bigr] \partial_j \theta \bigr\rangle$$

where $\dot{\theta} = \omega + r\sin(\psi - \theta)$.

**The $-D_i D_j N$ term** (second spatial derivatives of the lapse):

$$-D_i D_j r = -\partial_i \partial_j r + \Gamma^k{}_{ij} \partial_k r$$

In the Kuramoto picture, $\partial_i \partial_j r$ is the **Hessian of the coherence field** — how the synchronization quality curves in space. This is the tidal term: spatial variation in coherence generates tidal forces.

$$\boxed{-D_i D_j N \quad \longleftrightarrow \quad -\nabla_i \nabla_j r \quad = \quad \text{tidal synchronization gradient}}$$

**The ${}^{(3)}R_{ij}$ term** (spatial Ricci curvature):

Through the coherence tensor, ${}^{(3)}R_{ij}$ involves second derivatives of $C_{ij}$, which are fourth-order in the phase field:

$${}^{(3)}R_{ij} \sim \partial^2 C \sim \partial^2 \langle \partial \theta \, \partial \theta \rangle$$

This has the structure of a **phase stiffness tensor** — the cost of bending the synchronization pattern. Large ${}^{(3)}R_{ij}$ means the phase landscape is highly curved and resists deformation.

$$\boxed{{}^{(3)}R_{ij} \quad \longleftrightarrow \quad \text{phase stiffness: } \partial_k \partial_l \langle \partial_i \theta \, \partial_j \theta \rangle}$$

**The $\mathcal{K}\mathcal{K}_{ij} - 2\mathcal{K}_{ik}\mathcal{K}^k{}_j$ terms** (extrinsic curvature self-interaction):

These are quadratic in $\mathcal{K}$, hence quartic in phase gradients weighted by the alignment cosine. They represent **nonlinear feedback of desynchronization on itself** — the synchronization landscape's self-interaction.

### 3.3 Spatial Derivatives: The Constraint Equations

**Hamiltonian constraint** (energy conservation on each slice):

$${}^{(3)}R + \mathcal{K}^2 - \mathcal{K}_{ij}\mathcal{K}^{ij} = 16\pi G\rho$$

In Kuramoto language:

$$\underbrace{\text{phase stiffness scalar}}_{\text{spatial Ricci}} + \underbrace{(\text{tr}\,\mathcal{K})^2 - \mathcal{K}_{ij}\mathcal{K}^{ij}}_{\text{desynchronization balance}} = 16\pi G\rho$$

This says: **the total phase stiffness plus the net desynchronization balance equals the matter content.** Matter sources synchronization structure. The constraint is that the synchronization landscape must be consistent with the matter that generates it.

**Momentum constraint** (momentum conservation on each slice):

$$D_j(\mathcal{K}^{ij} - \gamma^{ij}\mathcal{K}) = 8\pi G \, j^i$$

In Kuramoto language: **the divergence of the desynchronization tensor equals the matter current.** Flowing matter creates a divergence in the phase-misalignment pattern. This is why a spinning mass drags the synchronization field (frame-dragging = synchronization-dragging).

---

## 4. What the Mapping Produces

### 4.1 Geodesic Equation as Phase-Gradient Following

A test particle follows a geodesic:

$$\frac{d^2 x^\mu}{d\tau^2} + \Gamma^\mu{}_{\alpha\beta} \frac{dx^\alpha}{d\tau} \frac{dx^\beta}{d\tau} = 0$$

The Christoffel symbols $\Gamma^\mu{}_{\alpha\beta}$ are first derivatives of the metric, hence (through the dictionary) first derivatives of the coherence tensor — gradients of the synchronization pattern.

The geodesic equation says: **a free particle moves along the path of steepest phase coherence.** The Christoffel connection tells the particle how the synchronization landscape tilts at each point. "Falling" is following the coherence gradient.

In the Newtonian limit ($N \approx 1 + \Phi/c^2$, i.e. $r \approx 1 + \Phi/c^2$):

$$\frac{d^2 x^i}{dt^2} \approx -\partial_i \Phi = -c^2 \partial_i (r - 1) = -c^2 \partial_i r$$

**Gravitational acceleration is the gradient of coherence.** Objects accelerate toward regions of higher synchronization. This is the precise statement of "gravity is synchronization" at the level of individual trajectories.

### 4.2 Einstein's Equation as Synchronization Self-Consistency

The full Einstein equation $G_{\mu\nu} = 8\pi G T_{\mu\nu}$, when unpacked through the ADM split and the Kuramoto dictionary, becomes:

$$\text{(coherence curvature)} + \text{(desynchronization rate)}^2 = \text{(matter content)}$$

$$\nabla \cdot \text{(desynchronization tensor)} = \text{(matter current)}$$

$$\frac{\partial}{\partial t}\text{(coherence tensor)} = -\text{coherence} \times \text{desynchronization} + \text{phase drift}$$

$$\frac{\partial}{\partial t}\text{(desynchronization)} = -\nabla^2\text{coherence} + \text{phase stiffness} \times \text{coherence} + \text{nonlinear feedback} - \text{matter stress}$$

This is a closed system: coherence and desynchronization evolve coupled to each other and to matter, with matter setting the natural frequencies (energy density $\rho$) and currents ($j^i$) that the synchronization field must accommodate.

### 4.3 The MOND Regime from Weak Coherence

In the MOND regime ($a \ll a_0$), the framework predicts $r \ll 1$ — weak coherence, far from synchronization. In this limit:

- $\cos(\psi - \theta)$ oscillates rapidly and its average drops
- $\mathcal{K}_{ij}$ is suppressed (extrinsic curvature becomes sub-dominant)
- The coupling integral $\int K(x,x') \sin(\theta' - \theta) \, d\mu$ is dominated by **collective modes** rather than local interactions

The Kuramoto model in the incoherent-to-coherent transition gives:

$$r \propto \sqrt{K - K_c} \quad \text{for } K \gtrsim K_c$$

Near the transition, $N = r \propto \sqrt{K - K_c}$, and the gravitational acceleration:

$$a = c^2 |\nabla r| \propto c^2 |\nabla \sqrt{K - K_c}|$$

For a coupling kernel that falls as $K \propto GM/r_{\text{gal}}$ (gravitational coupling at galactic scales), this produces the MOND scaling:

$$a \propto \sqrt{a_N \cdot a_0}$$

where $a_N = GM/r_{\text{gal}}^2$ is the Newtonian acceleration and $a_0 \propto K_c$. This is the MOND deep-regime relation, emerging from the square-root onset of the Kuramoto order parameter.

---

## 5. Summary of Explicit Derivatives

| Derivative | ADM Expression | Kuramoto Expression |
|---|---|---|
| $\partial_t \gamma_{ij}$ | $-2N\mathcal{K}_{ij} + D_i N_j + D_j N_i$ | $-2r \langle \partial_i\theta \cos(\psi-\theta)\partial_j\theta \rangle + \text{phase drift}$ |
| $\partial_t \mathcal{K}_{ij}$ | $-D_iD_jN + N({}^{(3)}R_{ij} + \mathcal{K}\mathcal{K}_{ij} - 2\mathcal{K}_{ik}\mathcal{K}^k{}_j) + \ldots$ | $-\nabla_i\nabla_j r + r \cdot \text{phase stiffness} + \text{nonlinear}$ |
| $\nabla^2 N$ | Appears in Hamiltonian constraint | $\nabla^2 r$ = Laplacian of coherence |
| $\partial_i N$ | Gravitational acceleration (Newtonian limit) | $\partial_i r$ = coherence gradient |
| $D_j \mathcal{K}^{ij}$ | Momentum constraint | Divergence of desynchronization = matter current |
| $\Gamma^\mu{}_{\alpha\beta}$ | Christoffel connection | First derivatives of coherence tensor |
| ${}^{(3)}R_{ij}$ | Spatial Ricci tensor | Phase stiffness: $\sim \partial^2 \langle \partial\theta\partial\theta \rangle$ |

---

## 6. What This Constrains

The explicit mapping imposes requirements in both directions:

**On the Kuramoto side** (what gravity demands of synchronization):
1. The coherence tensor $C_{ij}$ must satisfy the constraint equations. Not every synchronization pattern is gravitationally valid — only those where the phase stiffness plus desynchronization balance equals the matter content.
2. The coupling kernel $K(x,x')$ must be the Green's function of the spatial Laplacian. Gravity demands that coupling propagates as a solution to Poisson's equation on the spatial geometry.
3. The order parameter onset must be square-root: $r \propto \sqrt{K - K_c}$. This is a property of the standard Kuramoto model and is what produces the MOND scaling. If the onset were linear or cubic, the low-acceleration phenomenology would differ.

**On the Einstein side** (what synchronization demands of gravity):
1. The lapse function $N$ must be interpretable as a coherence measure bounded by $[0, 1]$. This is automatically satisfied: $N = 0$ at horizons, $N \to 1$ at infinity.
2. The extrinsic curvature must decompose into phase-gradient correlations weighted by alignment. This constrains the allowed $\mathcal{K}_{ij}$ to those expressible as two-point phase statistics.
3. The spatial Ricci tensor must be expressible as a phase stiffness. This is a non-trivial requirement — it says the geometry of space is entirely determined by the cost of bending the synchronization pattern.

---

## 7. Open Steps

This mapping is kinematic — it identifies the fields and their derivatives. What remains beyond the kinematic dictionary:

1. **Dynamical equivalence.** Show that the Kuramoto evolution equations, with coupling kernel = gravitational Green's function and $r \leftrightarrow N$, reproduce the ADM evolution equations as an identity, not just a structural parallel. This requires fixing the normalization and verifying all numerical prefactors. The [Renzo's Rule derivation](renzos_rule_from_kuramoto.md) confirms the variational principle but does not verify prefactors.

2. ✓ **The Stribeck function.** *Resolved.* The Kuramoto model uses $\sin(\psi - \theta)$ as the coupling function. The framework claims the vacuum has a Stribeck-type impedance. The [Renzo's Rule derivation §7.1](renzos_rule_from_kuramoto.md#71-deriving-the-interpolation-function-from-the-kuramoto-onset) shows that replacing $\sin(\cdot)$ with a Stribeck-weighted coupling function and setting $\delta = 1/2$ reproduces the MOND interpolation — $\delta = \frac{1}{2}$ recovers the RAR form exactly (see [`renzos_rule_from_kuramoto.md` §7.1](renzos_rule_from_kuramoto.md#71-deriving-the-interpolation-function-from-the-kuramoto-onset)).

3. **Strong-field regime.** The mapping above works perturbatively (small phase gradients). Near black holes, $r \to 0$, and the perturbative expansion of $C_{ij}$ breaks down. The Feigenbaum cascade (period-doubling toward the stuck singularity) should emerge from the Kuramoto dynamics in the $r \to 0$ limit.

4. **Gravitational waves.** Linearizing the mapping around flat space ($r = 1$, $\partial_i \theta = 0$) should produce wave equations for coherence perturbations that match the linearized Einstein equations (gravitational waves). The prediction: gravitational waves are propagating synchronization disturbances in the vacuum.

### Cross-project progress

The [harmonics](https://github.com/nickjoven/harmonics) repository introduces a synchronization cost framework that addresses the kinematic–dynamic gap from a variational direction. The [FRAMEWORK](https://github.com/nickjoven/harmonics/blob/main/sync_cost/FRAMEWORK.md) identifies the objective function (total synchronization cost: coupling + drift, subject to the Hamiltonian constraint) whose KKT conditions produce the dark-matter dual variable. This does not discharge the dynamical equivalence requirement (item 1) — prefactors remain unverified — but it provides the variational structure that was missing from the optimization side of the argument.

---

*License: [CC0](LICENSE) — No rights reserved.*
