# The Proslambenomenos: From $\Lambda$ to $a_0$ via Synchronization

N. Joven — March 2026 — CC0 1.0

---

## 1. The numerical coincidence

Three quantities measured at cosmological and galactic scales share a suspiciously tight numerical relationship:

| Quantity | Value | Dimension |
|----------|-------|-----------|
| Hubble parameter $H_0$ | $\approx 2.2 \times 10^{-18}\;\text{s}^{-1}$ | frequency |
| MOND acceleration $a_0$ | $\approx 1.2 \times 10^{-10}\;\text{m s}^{-2}$ | acceleration |
| Cosmological constant $\Lambda$ | $\approx 1.1 \times 10^{-52}\;\text{m}^{-2}$ | inverse area |

The relationship $a_0 \approx cH_0 / 2\pi$ is well known in the MOND literature and unexplained. This document derives it rather than assuming it, by identifying all three as manifestations of a single reference frequency.

## 2. The vacuum's fundamental oscillation

The cosmological constant $\Lambda$ sets a frequency:

$$\nu_\Lambda \;=\; c\,\sqrt{\Lambda / 3}$$

Check:

$$c \sqrt{\Lambda/3} \;\approx\; 3 \times 10^8 \;\times\; \sqrt{1.1 \times 10^{-52} / 3} \;\approx\; 3 \times 10^8 \;\times\; 1.9 \times 10^{-26} \;\approx\; 5.7 \times 10^{-18}\;\text{s}^{-1}$$

The ratio $\nu_\Lambda / H_0 = \sqrt{\Omega_\Lambda} \approx 0.83$ follows exactly from the Friedmann equation. This is not a discovered coincidence — it is $\Lambda$CDM. In a pure de Sitter universe ($\Omega_\Lambda = 1$, no matter), the equality is exact: $H_\text{dS} = c\sqrt{\Lambda/3}$. At the present epoch, the matter contribution to the expansion rate accounts for the 17% difference.

What the synchronization framework adds is not the first link of the chain ($\nu_\Lambda \approx H_0$, which is Friedmann) but the second ($H_0 \to a_0$, which requires the Kuramoto critical coupling). The proslambenomenos is $\nu_\Lambda$ — the de Sitter limit of the Hubble rate, the frequency the vacuum would oscillate at if matter were absent. The present-day $H_0$ is this frequency plus the matter correction $H_0 = \nu_\Lambda / \sqrt{\Omega_\Lambda}$.

## 3. From frequency to acceleration

The relation $a_0 \approx cH_0$ has been noted since Milgrom (1983) and explored as a possible cosmological connection to MOND (Milgrom 1999, Sanders 2008). What has been missing is the factor that separates them and a physical mechanism that produces it.

In the Kuramoto model, synchronization onset occurs at a critical coupling $K_c$ that depends on the frequency distribution $g(\omega)$ of the oscillator population:

$$K_c \;=\; \frac{2}{\pi\, g(0)}$$

where $g(0)$ is the frequency distribution evaluated at the mean. For a Lorentzian distribution with half-width $\gamma$ — the natural choice, since it is the unique family for which the Ott–Antonsen reduction is exact — $g(0) = 1/(\pi\gamma)$ and $K_c = 2\gamma$.

The acceleration at which desynchronization occurs is the product of the reference frequency, the propagation speed $c$, and the critical coupling geometry:

$$a_0 \;=\; \frac{c\,\nu_\Lambda}{2\pi\,g(0)} \;=\; \frac{c\,\nu_\Lambda\,\pi\gamma}{2\pi} \;=\; \frac{c\,\nu_\Lambda\,\gamma}{2}$$

The parameter $\gamma$ is the spread of natural frequencies $\omega(x) = \sqrt{4\pi G\rho(x)}$ across the matter distribution. At the nonlinear scale of cosmic structure ($\delta\rho/\rho \sim 1$), the frequency spread is of order the mean frequency: $\gamma \sim \nu_\Lambda$. Under this condition, $g(0) = 1/(\pi\gamma) \sim 1/(\pi\nu_\Lambda)$, and:

$$\boxed{a_0 \;\approx\; \frac{cH_0}{2\pi}}$$

which gives $\approx 1.0 \times 10^{-10}\;\text{m s}^{-2}$, compared to the observed value $\approx 1.2 \times 10^{-10}\;\text{m s}^{-2}$ (McGaugh 2016). The ratio is 0.87 using Planck $H_0 = 67.4$ and 0.94 using SH0ES $H_0 = 73.0$.

The $2\pi$ is not a fudge factor. It is the ratio of angular frequency to cycle frequency — the same $2\pi$ that appears in the Kuramoto critical coupling formula. This is the novel content: the Milgrom coincidence $a_0 \sim cH_0$ acquires a specific geometric factor from synchronization theory. The remaining $\sim 10$% discrepancy is absorbed by the condition $\gamma \sim \nu_\Lambda$, which is an approximation — a precise prediction requires computing $g(0)$ from the cosmic density PDF.

## 4. The interval structure

The proslambenomenos does not belong to any tetrachord — it stands outside the system as its ground. Similarly, $\Lambda$ does not participate in the dynamics of any particular galaxy. It sets the stage:

| Role | Quantity | Expression |
|------|----------|------------|
| Reference frequency | $\nu_\Lambda$ | $c\sqrt{\Lambda/3}$ |
| Expansion rate | $H_0$ | $\approx \nu_\Lambda$ |
| Synchronization threshold | $a_0$ | $c\nu_\Lambda / 2\pi$ |
| Coupling constant | $\kappa = 8\pi G/c^4$ | Sets impedance of the medium |

A single reference frequency, set by the cosmological constant, generates the characteristic scales of gravitational physics through the synchronization mechanism — just as the proslambenomenos generated the Greek tonal system by providing a fixed reference for every interval.

## 5. Three constants, one origin

The framework's claim:

> $\Lambda$, $H_0$, and $a_0$ are not three independent measurements. They are one frequency measured in three different units.

- Measured as an inverse area (curvature): $\Lambda$
- Measured as an inverse time (expansion rate): $H_0 = \nu_\Lambda / \sqrt{\Omega_\Lambda}$ (Friedmann)
- Measured as an acceleration (synchronization threshold): $a_0 = cH_0 / 2\pi$ (Kuramoto)

The chain:

$$\Lambda \;\xrightarrow{c\sqrt{\cdot/3}}\; \nu_\Lambda \;\xrightarrow{\div\sqrt{\Omega_\Lambda}}\; H_0 \;\xrightarrow{c/2\pi}\; a_0$$

The first arrow is the Friedmann equation (known). The second is the Kuramoto critical coupling (new). The $2\pi$ and the condition $\gamma \sim \nu_\Lambda$ are the only inputs beyond standard cosmology. The proslambenomenos is the vacuum's tick rate — what the Hubble rate converges to as matter dilutes.

## 6. Consequences for the Kuramoto–Einstein framework

This identification resolves an open question from the [companion framework](https://github.com/nickjoven/201): where does the coupling strength $K$ in the Kuramoto–Einstein mapping come from?

**Answer:** From the proslambenomenos.

The coupling kernel $K(x,x') = G_\gamma(x,x')$ (the Green's function of the spatial metric) has a characteristic scale set by $\Lambda$. The Kuramoto critical coupling $K_c$ corresponds to the acceleration scale $a_0$, and the coherence onset $r \propto \sqrt{K - K_c}$ reproduces the MOND interpolation function in the deep-field regime.

Below $a_0$: coupling subcritical, coherence drops, synchronization deficit appears as dark matter phantom.

Above $a_0$: coupling supercritical, full synchronization, Newtonian gravity, no phantom needed.

The vacuum is not empty. It oscillates at $\nu_\Lambda$. Gravity synchronizes matter to this oscillation. The proslambenomenos is the frequency at which the vacuum vibrates — and everything else is built on top of it.

## 7. What remains

The proslambenomenos identification gives us $a_0$ from $\Lambda$. But it does not, by itself, guarantee that the resulting galactic structure is unique. That requires a separate argument — the [Lyapunov dissipation proof](lyapunov_uniqueness.md) — which shows that the path to the fixed point, not the fixed point itself, enforces uniqueness.
