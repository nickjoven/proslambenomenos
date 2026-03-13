# Deriving Renzo's Rule from the Kuramoto–Einstein Fixed-Point Structure

N. Joven — March 2026 — CC0 1.0

---

## 1. Scope

This document derives Renzo's Rule — the observation that every feature in a galaxy's baryonic luminosity profile is mirrored in its rotation curve — directly from the Kuramoto self-consistency equation.

The [companion derivation in 201](https://github.com/nickjoven/201/blob/main/renzos_rule_derivation.md) proves the same result from the ADM side (Einstein–Hilbert action, Hamiltonian constraint, KKT conditions). This derivation starts from the Kuramoto side and meets in the middle. The two proofs are independent: neither assumes the other's starting point.

## 2. The Kuramoto self-consistency equation

At the synchronization fixed point, the continuum Kuramoto model satisfies:

$$r(x)\,e^{i\psi(x)} \;=\; \int K(x,x')\,\rho_{\text{locked}}(x')\,e^{i\psi(x')}\,d^3x' \;+\; \int K(x,x')\,\rho_{\text{drift}}(x')\,\langle e^{i\theta}\rangle_{\text{drift}}\,d^3x'$$

The first integral runs over locked oscillators (synchronized matter); the second over drifting oscillators (desynchronized component). At the fixed point, the drifting contribution averages to zero by incoherence:

$$r(x)\,e^{i\psi(x)} \;=\; \int K(x,x')\,\rho_{\text{locked}}(x')\,e^{i\psi(x')}\,d^3x'$$

Taking the modulus:

$$r(x) \;=\; \int K(x,x')\,\rho_{\text{locked}}(x')\,\cos[\psi(x') - \psi(x)]\,d^3x'$$

This is the equation that determines the coherence profile $r(x)$ from the locked-oscillator distribution.

## 3. Where baryons enter

The locked-oscillator density at position $x'$ is:

$$\rho_{\text{locked}}(x') \;=\; \rho_b(x') \;\times\; P_{\text{lock}}(x')$$

where $P_{\text{lock}}$ is the fraction of oscillators at $x'$ whose natural frequency $\omega(x') = \sqrt{4\pi G\rho_b(x')}$ falls within the locking window $|\omega - \Omega| < K\,r(x')$. The locking probability depends on $\rho_b$ through $\omega$ and on $r$ through the window width.

This means the self-consistency equation is:

$$r(x) \;=\; \int K(x,x')\;\rho_b(x')\;P_{\text{lock}}\!\left[\rho_b(x'),\, r(x')\right]\;\cos[\psi(x') - \psi(x)]\;d^3x'$$

**The baryonic density $\rho_b$ appears explicitly in the integrand.** Every spatial feature in $\rho_b$ — a density peak, a trough, a ring, a bar — modifies the integrand at that location and therefore modifies $r(x)$.

## 4. From coherence to rotation curve

Under the Kuramoto–Einstein mapping, the lapse function $N(x) \leftrightarrow r(x)$. The gravitational potential satisfies:

$$\Phi(x) \;=\; c^2 \ln N(x) \;=\; c^2 \ln r(x)$$

and the rotation velocity at galactocentric radius $R$ is:

$$v^2(R) \;=\; R\,\frac{\partial\Phi}{\partial R} \;=\; R\,c^2\,\frac{\partial \ln r}{\partial R}$$

Therefore $v^2(R)$ is determined by the radial gradient of $\ln r$, which is determined by the self-consistency integral, which depends explicitly on $\rho_b$.

## 5. Forward Renzo's Rule: baryonic features mirror in $v(R)$

**Claim.** A localized perturbation $\delta\rho_b$ at radius $R_0$ produces a localized perturbation $\delta v^2$ at the same radius.

*Derivation.* Linearize the self-consistency equation around the background solution $(r_0, \rho_{b,0})$:

$$\delta r(x) \;=\; \int K(x,x')\left[\delta\rho_b(x')\,P_{\text{lock},0}(x') \;+\; \rho_{b,0}(x')\,\frac{\partial P_{\text{lock}}}{\partial \rho_b}\,\delta\rho_b(x') \;+\; \rho_{b,0}(x')\,\frac{\partial P_{\text{lock}}}{\partial r}\,\delta r(x')\right]\cos\Delta\psi\;d^3x'$$

The first two terms are source terms driven by $\delta\rho_b$. The third is the self-consistent response. Writing schematically:

$$\delta r \;=\; \mathcal{K}[\delta\rho_b] \;+\; \mathcal{L}[\delta r]$$

where $\mathcal{K}$ is a linear operator applied to $\delta\rho_b$ and $\mathcal{L}$ is a linear operator on $\delta r$. Solving:

$$\delta r \;=\; (I - \mathcal{L})^{-1}\,\mathcal{K}[\delta\rho_b]$$

The operator $(I - \mathcal{L})^{-1}\mathcal{K}$ has kernel dominated by $K(x,x')$, which for isolated gravitational systems decays as $1/|x - x'|$. A localized $\delta\rho_b$ at $R_0$ produces $\delta r$ peaked at $R_0$ with tails falling as $1/|R - R_0|$.

The rotation curve perturbation:

$$\delta v^2(R) \;=\; R\,c^2\,\frac{\delta r'(R)}{r_0(R)}$$

is therefore localized near $R_0$. **Every baryonic feature produces a rotation curve feature at the same radius.** This is forward Renzo's Rule. $\square$

## 6. Inverse Renzo's Rule: rotation curve features require baryonic origins

**Claim.** The synchronization deficit (dark matter phantom) cannot produce sharp features in $v(R)$ independently of $\rho_b$.

*Derivation.* The dark matter phantom density is the synchronization deficit:

$$\rho_{\text{phantom}}(x) \;=\; \rho_{\text{crit}}\,\left[1 - r(x)\right]$$

where $\rho_{\text{crit}}$ is determined by the [proslambenomenos](proslambenomenos.md) via $\Lambda$. Now $r(x)$ is determined by the self-consistency integral over $K(x,x')\,\rho_b(x')\,P_{\text{lock}}$.

The kernel $K(x,x') = G_\gamma(x,x')$ is the Green's function of an elliptic operator (the Laplacian on the spatial slice). It is smooth, positive, and its convolution with any distribution produces a result that is *at least as smooth as the kernel itself*.

Therefore $r(x)$ inherits the smoothness of $K$, and $\rho_{\text{phantom}} = \rho_{\text{crit}}(1 - r)$ is at least as smooth as $r$. It cannot contain features sharper than those in $\rho_b$ that source $r$.

**Contrapositive:** If the rotation curve has a sharp feature, it cannot come from $\rho_{\text{phantom}}$ alone — it must originate from $\rho_b$. This is inverse Renzo's Rule. $\square$

## 7. The proslambenomenos enters through the locking window

The derivation above has one free parameter: the reference frequency $\Omega$ around which oscillators lock. From the [proslambenomenos identification](proslambenomenos.md):

$$\Omega \;=\; 2\pi\,\nu_\Lambda \;=\; 2\pi\,c\sqrt{\Lambda/3}$$

This sets the center of the locking window. The MOND scale $a_0 = c\nu_\Lambda/2\pi$ marks the boundary between:

- **Supercritical** ($a > a_0$): Most oscillators locked, $P_{\text{lock}} \approx 1$, self-consistency integral dominated by $\rho_b$ directly. Renzo's Rule is one-to-one: baryons track rotation curve with no phantom.
- **Subcritical** ($a < a_0$): Few oscillators locked, $P_{\text{lock}} < 1$, self-consistency integral picks up the synchronization deficit. Renzo's Rule holds through the square-root interpolation: $v^4 \approx v_b^4 + (a_0 R)^2 \rho_b / \rho_{\text{crit}}$.

The transition between regimes is smooth (it is the Kuramoto order parameter onset curve, $r \propto \sqrt{K - K_c}$) and produces the MOND interpolation function without fitting.

## 8. Completing the circle

The ADM-side derivation in [201](https://github.com/nickjoven/201/blob/main/renzos_rule_derivation.md) proves Renzo's Rule from the Hamiltonian constraint: the algebraic, local coupling of baryonic density and geometry on each spatial slice.

This derivation proves the same result from the Kuramoto self-consistency equation: the integral coupling of baryonic density and coherence through the synchronization kernel.

The two proofs are independent. Their agreement is the consistency check. Their shared conclusion:

| Property | ADM derivation | Kuramoto derivation |
|----------|---------------|-------------------|
| Forward Renzo's Rule | Hamiltonian constraint is algebraic and local | Self-consistency integral is sourced by $\rho_b$ |
| Inverse Renzo's Rule | Green's function kernel is smoothing | Same kernel, same smoothing |
| Uniqueness | Not proven (flagged open) | Proven via [Lyapunov dissipation](lyapunov_uniqueness.md) |
| Source of $a_0$ | Not derived (input parameter) | Derived from [proslambenomenos](proslambenomenos.md) |

The Kuramoto side closes the two gaps the ADM side left open: uniqueness and the origin of $a_0$.
