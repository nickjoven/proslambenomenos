# Lyapunov Functional and the Dissipation Argument for Uniqueness

N. Joven — March 2026 — CC0 1.0

---

## 1. The problem

The Kuramoto–Einstein framework maps gravitational equilibrium to a synchronization fixed point. The forward and inverse Renzo's Rule derivations ([ADM side](https://github.com/nickjoven/201/blob/main/renzos_rule_derivation.md), [Kuramoto side](renzos_rule_from_kuramoto.md)) show that at the fixed point, every baryonic feature is mirrored in the rotation curve and vice versa. But the fixed-point equations alone do not guarantee *uniqueness*.

The Schrödinger equation is time-symmetric, yet we observe irreversibility. The arrow of time is not in the equation — it is in the low-entropy initial state. Similarly, if the Kuramoto–Einstein equations admit multiple fixed points, the physical one is selected not by the equilibrium conditions but by the dissipative history that produced it.

> **Uniqueness is not a mathematical property of the equilibrium — it is a physical property of the path.**

This changes what needs to be written. Not a contraction proof — a dissipation argument.

## 2. The Kuramoto Lyapunov functional (finite case)

For the all-to-all Kuramoto model with $N$ oscillators and identical frequencies $\omega_i = \omega$ in the rotating frame:

$$\dot{\theta}_i \;=\; \frac{K}{N}\sum_{j=1}^{N} \sin(\theta_j - \theta_i)$$

the system admits a Lyapunov functional:

$$V[\theta] \;=\; -\frac{K}{2N}\sum_{i,j}\cos(\theta_i - \theta_j)$$

This satisfies:

$$\frac{dV}{dt} \;=\; -\sum_i \dot{\theta}_i^2 \;\leq\; 0$$

with equality only at fixed points. The system is gradient descent on $V$. The synchronized state ($\theta_i = \theta_j$ for all $i,j$) is the global minimum. This is textbook — established by Kuramoto (1984), formalized by Strogatz (2000).

For non-identical frequencies, the gradient structure is broken but the dissipative character persists: the system still contracts phase-space volume, still has attractors, and still selects unique asymptotic states from generic initial conditions.

## 3. Extension to the continuum

The spatially extended Kuramoto model:

$$\partial_t \theta(x,t) \;=\; \omega(x) + \int K(x,x')\,\sin[\theta(x',t) - \theta(x,t)]\,d^3x'$$

admits the continuum Lyapunov functional:

$$\mathcal{V}[\theta] \;=\; -\frac{1}{2}\iint K(x,x')\,\cos[\theta(x') - \theta(x)]\,d^3x\,d^3x'$$

with time derivative along solutions:

$$\frac{d\mathcal{V}}{dt} \;=\; -\int \left(\partial_t\theta - \omega\right)^2 d^3x \;\leq\; 0$$

The continuum model is gradient flow on $\mathcal{V}$, modulo the natural frequency drift. The key property: **the interaction energy decreases monotonically.** Oscillators that are coupled always tend toward alignment; the only thing preventing full synchronization is the frequency spread $\omega(x)$.

## 4. The Kuramoto–Einstein Lyapunov functional

Under the Kuramoto–Einstein mapping ([companion document](https://github.com/nickjoven/201/blob/main/kuramoto_einstein_mapping.md)):

| Kuramoto | Einstein (ADM) |
|----------|---------------|
| $\theta(x,t)$ | Phase field |
| $\omega(x)$ | $\sqrt{4\pi G\rho(x)}$ |
| $K(x,x')$ | $G_\gamma(x,x')$ (Green's function of $\gamma_{ij}$) |
| $r(x,t)$ | Lapse $N$ |
| $\cos[\theta - \theta']$ | Phase correlation |

the Lyapunov functional maps to:

$$\mathcal{V}_{\text{KE}}[\gamma, \psi] \;=\; -\frac{1}{2}\iint G_\gamma(x,x')\,\cos[\psi(x') - \psi(x)]\,\sqrt{\gamma(x)}\,\sqrt{\gamma(x')}\,d^3x\,d^3x'$$

where $\psi(x)$ is the mean phase field at position $x$.

**In the synchronized limit** ($\psi(x) \approx \psi_0$ everywhere, full coherence):

$$\mathcal{V}_{\text{KE}} \;\approx\; -\frac{1}{2}\iint G_\gamma(x,x')\,\sqrt{\gamma(x)}\,\sqrt{\gamma(x')}\,d^3x\,d^3x'$$

This is, up to sign and boundary terms, the **gravitational potential energy functional** — the standard Newtonian self-energy. The Lyapunov function of Newtonian gravity is the synchronized limit of the Kuramoto–Einstein Lyapunov functional.

**In the desynchronized limit** ($\psi$ incoherent, $r \ll 1$):

$$\mathcal{V}_{\text{KE}} \;\approx\; 0$$

because the cosine averages to zero over incoherent phases. The system starts near zero and descends to the gravitational potential well. Galaxy formation *is* Lyapunov descent.

## 5. Why $\mathcal{V}_\text{KE}[\theta]$ oscillates — and what descends instead

The interaction energy $\mathcal{V}[\theta] = -\frac{1}{2}\iint K\cos(\theta - \theta')\,d^3x\,d^3x'$ has time derivative:

$$\frac{d\mathcal{V}}{dt} \;=\; -\int(\partial_t\theta - \omega)\,\partial_t\theta\,d^3x$$

For non-identical frequencies ($\omega(x) \neq 0$), this has indefinite sign: the cross term $\int\omega\,\partial_t\theta\,d^3x$ can be positive. This is the **primal oscillation** around the saddle point in the Lagrangian relaxation picture ([intersections](intersections/joven_stick_slip_dark_matter.md), §3.3). Tracking $\mathcal{V}[\theta]$ is tracking the wrong variable — the phases $\theta$ are unbounded for drifting oscillators.

The correct variable is the order parameter $r(x,t) \in [0,1]$, which the [Kuramoto–Einstein mapping](201/kuramoto_einstein_mapping.md) provides as a bounded quantity. For a Lorentzian frequency distribution with half-width $\gamma$, the Ott–Antonsen reduction (Ott & Antonsen, 2008) gives exact mean-field dynamics:

$$\dot{r} \;=\; -\gamma\,r + \frac{K}{2}\,r(1 - r^2)$$

This is gradient flow $\dot{r} = -dU/dr$ on:

$$\boxed{U(r) \;=\; \frac{\gamma}{2}\,r^2 - \frac{K}{4}\,r^2 + \frac{K}{8}\,r^4}$$

with $\frac{dU}{dt} = -\left(\frac{dU}{dr}\right)^2 \leq 0$, equality only at fixed points. $U(r)$ is bounded below, defined on $r \in [0,1]$, and monotonically decreasing along trajectories. It is a strict Lyapunov function.

For $K > K_c = 2\gamma$ (supercritical), $U$ has exactly two critical points: an unstable maximum at $r = 0$ and a global minimum at $r^* = \sqrt{1 - 2\gamma/K}$. All trajectories with $r(0) > 0$ converge to $r^*$. There are no local minima to trap the dynamics.

The spatially extended version replaces $r$ with the coherence profile $r(x)$ and $U$ with the functional:

$$\mathcal{U}[r] \;=\; \int\left[\frac{\gamma(x)}{2}\,r(x)^2 - \frac{1}{4}\int K(x,x')\,r(x)\,r(x')\,\cos[\psi(x') - \psi(x)]\,d^3x'\right]d^3x$$

In the synchronized limit ($\psi \approx$ const), this reduces to $\mathcal{V}_\text{KE}$. In the desynchronized limit ($r \to 0$), $\mathcal{U} \to 0$. The descent from 0 to $\mathcal{U}(r^*)$ is the arrow of galaxy formation:


**Phase 1 — Incoherent** ($r \ll 1$, high $\mathcal{V}_{\text{KE}}$):
Oscillators are uncorrelated. Coupling is subcritical everywhere. The system is fully in the MOND regime. The synchronization deficit (dark matter phantom) compensates everywhere. Rotation curve is flat and featureless.

**Phase 2 — Nucleation** ($r$ growing, $\mathcal{V}_{\text{KE}}$ falling):
Synchronization nucleates where density is highest (protogalactic core, where $\omega(x)$ is closest to $\Omega$). Coherent patches expand outward. The rotation curve develops baryonic features as the synchronized domain grows.

**Phase 3 — Relaxation** ($r \to r_\infty$, $\mathcal{V}_{\text{KE}}$ at minimum):
The system reaches its unique fixed point. Rotation curve, dark matter profile, and baryonic distribution are all determined. Renzo's Rule holds.

## 6. Why uniqueness follows

The Ott–Antonsen potential $U(r)$ satisfies:
- **Bounded below:** $U(r) \geq U(r^*)$ for all $r \in [0,1]$
- **Monotonically decreasing** along mean-field trajectories: $dU/dt = -(dU/dr)^2 \leq 0$
- **No local minima:** For $K > K_c$, $U$ has exactly one minimum ($r^*$) and one maximum ($r = 0$)

By LaSalle's invariance principle on the compact interval $[0,1]$, every trajectory with $r(0) > 0$ converges to the unique minimum $r^*$. There are no local traps, no saddle points on the interior, and no basin boundary to characterize — the entire interval $(0,1]$ is the basin of $r^*$.

**Theorem (Lyapunov uniqueness).** Let $\rho_b(x)$ be a baryonic density distribution with finite total mass. Let the Kuramoto–Einstein system evolve from initial data with $r(x,0) \ll 1$ (desynchronized) and $\psi(x,0)$ approximately uniform. Then the $t \to \infty$ limit exists, is unique, and the corresponding rotation curve $v(R)$ satisfies Renzo's Rule: every feature in $\rho_b$ is mirrored in $v(R)$ and every feature in $v(R)$ has a baryonic origin.

*Proof sketch.* $U(r)$ is a strict Lyapunov function on $[0,1]$ (bounded below, monotone decreasing, vanishing derivative only at $r = 0$ and $r = r^*$). The maximum at $r = 0$ is unstable; any $r > 0$ flows to $r^*$. Desynchronized initial data has $r > 0$ (any finite matter distribution has nonzero coherence). By LaSalle, convergence to $r^*$. At $r^*$, the Kuramoto self-consistency equation and smoothing kernel yield Renzo's Rule ([companion derivation](renzos_rule_from_kuramoto.md)). $\square$

## 7. The analogy made precise

| Thermodynamics | Kuramoto–Einstein |
|---------------|-------------------|
| Free energy $F$ | $U(r)$ (Ott–Antonsen potential) |
| Second law: $dF/dt \leq 0$ | $dU/dt = -(dU/dr)^2 \leq 0$ |
| Equilibrium: min $F$ | min $U$ at $r^*$ |
| Arrow of time ← low-entropy initial state | Arrow of formation ← desynchronized initial state ($r \ll 1$) |
| Order parameter (magnetization) | $r \in [0,1]$ (coherence) |

The Ott–Antonsen potential $U(r)$ plays exactly the role of a Landau free energy: it is bounded, monotone along trajectories, and selects a unique equilibrium from symmetric initial conditions. The primal interaction energy $\mathcal{V}[\theta]$ oscillates — this is the saddle-point oscillation familiar from Lagrangian relaxation ([intersections](intersections/joven_stick_slip_dark_matter.md), §3.3). The dual variable $r$ descends.

The arrow of time is not in the Schrödinger equation. It is in the low-entropy initial state. The uniqueness of galactic structure is not in the fixed-point equations. It is in the gradient flow on $U(r)$ that produced the fixed point.
