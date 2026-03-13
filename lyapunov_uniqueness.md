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

## 5. Monotone decrease and the arrow of formation

The central result. Along physical trajectories:

$$\frac{d\mathcal{V}_{\text{KE}}}{dt} \;=\; -\int \left(\partial_t\psi - \sqrt{4\pi G\rho}\right)^2 \sqrt{\gamma}\,d^3x \;\leq\; 0$$

This is the gravitational arrow of time for structure formation. A protogalactic cloud begins desynchronized and descends:

**Phase 1 — Incoherent** ($r \ll 1$, high $\mathcal{V}_{\text{KE}}$):
Oscillators are uncorrelated. Coupling is subcritical everywhere. The system is fully in the MOND regime. The synchronization deficit (dark matter phantom) compensates everywhere. Rotation curve is flat and featureless.

**Phase 2 — Nucleation** ($r$ growing, $\mathcal{V}_{\text{KE}}$ falling):
Synchronization nucleates where density is highest (protogalactic core, where $\omega(x)$ is closest to $\Omega$). Coherent patches expand outward. The rotation curve develops baryonic features as the synchronized domain grows.

**Phase 3 — Relaxation** ($r \to r_\infty$, $\mathcal{V}_{\text{KE}}$ at minimum):
The system reaches its unique fixed point. Rotation curve, dark matter profile, and baryonic distribution are all determined. Renzo's Rule holds.

## 6. Why uniqueness follows

The Lyapunov functional is:
- **Bounded below** (the cosine is bounded, the integral is finite for localized sources)
- **Monotonically decreasing** along physical trajectories
- **Coercive** in the relevant topology (desynchronized states have higher $\mathcal{V}_{\text{KE}}$ than synchronized ones)

By LaSalle's invariance principle, every trajectory converges to the largest invariant set within $\{d\mathcal{V}_{\text{KE}}/dt = 0\}$. This set consists of fixed points where $\partial_t\psi = \omega(x)$ everywhere — i.e., all oscillators either locked or freely drifting at their natural frequency.

**The physical initial condition selects the basin.** A protogalactic cloud starts desynchronized: $r(x,0) \ll 1$, density approximately homogeneous, no preexisting coherence structure. From this initial condition:

- Local minima of $\mathcal{V}_{\text{KE}}$ that require preexisting coherence structure are **unreachable** — they are not in the basin of the physical initial condition.
- Saddle points are **unstable** — the flow passes through them.
- The global minimum is **the only attractor reachable from generic desynchronized initial data**.

Therefore: for each baryonic distribution $\rho_b(x)$, the physical Lyapunov descent from homogeneous, desynchronized initial conditions produces a unique fixed point, and the rotation curve at that fixed point is uniquely determined.

**Theorem (Lyapunov uniqueness).** Let $\rho_b(x)$ be a baryonic density distribution with finite total mass. Let the Kuramoto–Einstein system evolve from initial data with $r(x,0) \ll 1$ (desynchronized) and $\psi(x,0)$ approximately uniform. Then the $t \to \infty$ limit exists, is unique, and the corresponding rotation curve $v(R)$ satisfies Renzo's Rule: every feature in $\rho_b$ is mirrored in $v(R)$ and every feature in $v(R)$ has a baryonic origin.

*Proof sketch.* $\mathcal{V}_{\text{KE}}$ is a strict Lyapunov function (bounded below, monotone decreasing, vanishing derivative only at fixed points). The basin of attraction of the global minimum contains all states with $r \ll 1$ (no preexisting coherence can trap the trajectory in a local minimum). By LaSalle, convergence to the global minimum. At the global minimum, the Kuramoto self-consistency equation and smoothing kernel yield Renzo's Rule ([companion derivation](renzos_rule_from_kuramoto.md)). $\square$

## 7. The analogy made precise

| Thermodynamics | Kuramoto–Einstein |
|---------------|-------------------|
| Entropy $S$ | $-\mathcal{V}_{\text{KE}}$ |
| Second law: $dS/dt \geq 0$ | $d\mathcal{V}_{\text{KE}}/dt \leq 0$ |
| Equilibrium: max $S$ | min $\mathcal{V}_{\text{KE}}$ |
| Arrow of time ← initial conditions | Arrow of formation ← initial coherence |
| Boltzmann: $S = k\ln W$ | $\mathcal{V}_{\text{KE}} = -\tfrac{1}{2}\iint K\cos\Delta\psi$ |

If the Kuramoto–Einstein Lyapunov functional exists, it plays exactly the role entropy plays in thermodynamics: it does not tell you the equations are asymmetric (they are not — the Kuramoto fixed-point equations are symmetric). It tells you the *physics* is asymmetric, because dissipation breaks the degeneracy.

The arrow of time is not in the Schrödinger equation. It is in the low-entropy initial state. The uniqueness of galactic structure is not in the fixed-point equations. It is in the dynamics that produced the fixed point.

You cannot derive it from the fixed-point equations alone because it is not there. It is in the dynamics.
