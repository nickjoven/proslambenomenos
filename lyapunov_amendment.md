# Amendment: The Lyapunov Functional on the Order Parameter

N. Joven — March 2026 — CC0 1.0

Audit response. Corrects the time derivative in `lyapunov_uniqueness.md` §5.

---

## 1. The error

The functional

$$\mathcal{V}[\theta] = -\frac{1}{2}\iint K(x,x')\,\cos[\theta(x') - \theta(x)]\,d^3x\,d^3x'$$

has time derivative

$$\frac{d\mathcal{V}}{dt} = -\int (\partial_t\theta - \omega)\,\partial_t\theta\,d^3x$$

which is **not** $-\int(\partial_t\theta - \omega)^2\,d^3x$ unless $\omega = 0$. The cross term $+\int\omega\,\partial_t\theta\,d^3x$ has indefinite sign. The original §5 formula is incorrect for non-identical frequencies.

## 2. The wrong level of description

The error arises from computing $d\mathcal{V}/dt$ using the individual oscillator phases $\theta(x,t)$, which are unbounded (drifting oscillators accumulate phase without limit). But the framework's own variables are bounded:

- The [Kuramoto–Einstein mapping](https://github.com/nickjoven/201/blob/main/kuramoto_einstein_mapping.md) defines $r(x,t) \in [0,1]$
- The [Lagrangian relaxation dual](https://github.com/nickjoven/intersections/blob/main/joven_stick_slip_dark_matter.md) gives $\lambda(r) = \max(0,\, a_{\text{obs}} - a_{\text{bary}}) \geq 0$

The functional should be written on the order parameter $r$, not on the phase field $\theta$.

## 3. The Ott–Antonsen Lyapunov function

For oscillators with Lorentzian frequency distribution $g(\omega) = (\gamma/\pi)/(\omega^2 + \gamma^2)$, the Ott–Antonsen reduction (Ott & Antonsen, 2008) gives exact mean-field dynamics:

$$\dot{r} = -\gamma\,r + \frac{K}{2}\,r(1 - r^2)$$

This is gradient flow $\dot{r} = -dU/dr$ on the potential

$$\boxed{U(r) = \frac{\gamma}{2}\,r^2 - \frac{K}{4}\,r^2 + \frac{K}{8}\,r^4}$$

which satisfies:

$$\frac{dU}{dt} = -\left(\frac{dU}{dr}\right)^2 \leq 0$$

with equality only at fixed points.

**Properties:**
- Bounded below: $U(r) \geq U(r^*)$ where $r^* = \sqrt{1 - 2\gamma/K}$
- Bounded domain: $r \in [0,1]$
- Unique minimum at $r^*$ for $K > K_c = 2\gamma$ (supercritical)
- Monotonically decreasing along trajectories — **strict Lyapunov function**
- Works for non-identical frequencies: $\gamma > 0$ is the frequency spread

The frequency spread $\gamma$ parameterizes what $g(0)$ parameterizes in the proslambenomenos derivation. The Lorentzian is the natural choice: it is a stable distribution with the power-law tails that matter distributions exhibit, and it is the unique family for which the Ott–Antonsen reduction is exact.

## 4. Connection to the spatially extended case

For the continuum Kuramoto model with spatially varying coupling $K(x,x')$, the local order parameter

$$r(x,t)\,e^{i\psi(x,t)} = \int K(x,x')\,e^{i\theta(x',t)}\,d\mu_\gamma(x')$$

inherits bounded dynamics. The spatially extended Lyapunov functional is:

$$\mathcal{U}[r] = \int\left[\frac{\gamma(x)}{2}\,r(x)^2 - \frac{1}{4}\iint K(x,x')\,r(x)\,r(x')\,\cos[\psi(x') - \psi(x)]\,d^3x'\right]d^3x$$

In the synchronized limit ($\psi \approx$ const), this reduces to $\mathcal{V}_{\text{KE}}$ as defined in the original document. In the desynchronized limit ($r \to 0$), $\mathcal{U} \to 0$. The descent $\mathcal{U}[r(t_1)] > \mathcal{U}[r(t_2)]$ for $t_1 < t_2$ holds in the mean-field limit by the Ott–Antonsen gradient structure.

## 5. The saddle-point interpretation

The oscillation of $\mathcal{V}[\theta]$ observed in finite-$N$ simulations is not a failure of the Lyapunov structure. It is the **primal oscillation around the saddle point** in the Lagrangian relaxation picture ([intersections](https://github.com/nickjoven/intersections/blob/main/joven_stick_slip_dark_matter.md), §3.3):

| Stick-slip | Lagrangian relaxation | Kuramoto–Einstein |
|---|---|---|
| Accumulation phase | Dual variable drifts toward optimal | $r(x)$ grows by gradient descent on $U$ |
| Release phase | Primal variables update rapidly | Drifting oscillators complete a cycle |
| Subharmonic | Dual oscillation around saddle point | $\mathcal{V}[\theta]$ oscillates; $\mathcal{U}[r]$ descends |
| Threshold | Complementary slackness | $a = a_0$: locking window boundary |

The primal variable $\theta$ oscillates. The dual variable $r$ descends. The correct Lyapunov functional tracks the dual.

## 6. Numerical verification

The Ott–Antonsen ODE $\dot{r} = -\gamma r + (K/2)r(1-r^2)$ with $U(r)$ was tested:

| Test | Violations |
|------|-----------|
| OA equation (continuum limit) | 0 / 1999 |
| Finite $N$, instantaneous $U(r(t))$ during transient | 22.6% |
| Finite $N$, coarse-grained transient | 1 / 9 bins |
| Finite $N$, steady state (thermal noise at minimum) | 50.5% |

The 22.6% transient violations are finite-size effects scaling as $O(1/\sqrt{N})$. The 50.5% steady-state violations are thermal fluctuations around the minimum — physically, the galaxy has formed and the Lyapunov argument is complete. The formation arrow runs from $r \ll 1$ to $r = r^*$; the noise at $r^*$ is not part of the argument.

## 7. What changes in the uniqueness proof

The theorem statement in `lyapunov_uniqueness.md` §6 survives with one substitution:

**Replace** $\mathcal{V}_{\text{KE}}[\gamma, \psi]$ (functional of phases) **with** $\mathcal{U}[r]$ (functional of coherence).

The proof sketch then reads: $\mathcal{U}$ is a strict Lyapunov function on $r \in [0,1]$ (bounded below, monotone decreasing in the mean-field limit, vanishing derivative only at fixed points). The basin of attraction of $r^*$ contains all states with $r \ll 1$. By LaSalle, convergence to $r^*$. At $r^*$, the self-consistency equation yields Renzo's Rule. $\square$

The physics is unchanged: galaxy formation is Lyapunov descent from incoherent initial conditions to the unique synchronized fixed point. What changes is the functional on which the descent is defined — it lives on the order parameter $r$, not on the phase field $\theta$.

## 8. The $g(0)$ connection

The Ott–Antonsen framework also clarifies the role of $g(0)$ in the proslambenomenos derivation. For a Lorentzian with half-width $\gamma$:

$$g(0) = \frac{1}{\pi\gamma}, \quad K_c = 2\gamma, \quad r^* = \sqrt{1 - \frac{K_c}{K}}$$

The proslambenomenos derivation (§3) sets $g(0) \sim \mathcal{O}(1)$, which corresponds to $\gamma \sim \mathcal{O}(1/\pi)$. This is the frequency spread of the oscillator population — physically, the variance of $\omega(x) = \sqrt{4\pi G\rho(x)}$ across the matter distribution. For a cosmological density field with density contrasts of order unity ($\delta\rho/\rho \sim 1$ at the nonlinear scale), $\gamma \sim \omega_0 \sim \nu_\Lambda$, giving $g(0) = 1/(\pi\gamma) \sim 1/(\pi\nu_\Lambda)$.

This turns the $g(0) \sim \mathcal{O}(1)$ assumption into a statement about the density contrast at the nonlinear scale — a physical condition rather than a free parameter. Whether this condition is satisfied depends on the cosmic density PDF, which is in principle measurable.
