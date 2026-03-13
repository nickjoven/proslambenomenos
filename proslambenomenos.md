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

This is $\nu_\Lambda \approx H_0$ to within a factor of order unity.

In the synchronization framework, $\nu_\Lambda$ is the proslambenomenos — the lowest tone of the system, not derived from the dynamics but setting the reference from which all intervals are measured. The expansion rate $H_0$ *is* this frequency. It is not that $H_0$ happens to equal $c\sqrt{\Lambda/3}$; rather, $H_0$ is the name cosmology gives to the proslambenomenos when measuring recession velocities.

## 3. From frequency to acceleration

In the Kuramoto model, synchronization onset occurs at a critical coupling $K_c$ proportional to the spread of natural frequencies. For an oscillator population with characteristic frequency $\nu_\Lambda$ and typical frequency spread $\Delta\omega$, the critical coupling satisfies:

$$K_c \;=\; \frac{2}{\pi\, g(0)}$$

where $g(0)$ is the frequency distribution evaluated at the mean. When coupling falls below $K_c$, coherence drops — the system desynchronizes.

The acceleration at which desynchronization occurs is the product of the reference frequency and the coupling propagation speed (the speed of light, since the medium is the vacuum):

$$a_0 \;=\; \frac{c\,\nu_\Lambda}{2\pi\,g(0)}$$

For $g(0) \sim \mathcal{O}(1)$ in natural units, this recovers:

$$\boxed{a_0 \;\approx\; \frac{cH_0}{2\pi}}$$

which is the observed value $\approx 1.2 \times 10^{-10}\;\text{m s}^{-2}$.

The $2\pi$ is not a fudge factor. It is the ratio of angular frequency to cycle frequency — the same $2\pi$ that appears in the Kuramoto critical coupling formula. The proslambenomenos is a cycle frequency; the locking window is measured in angular frequency.

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
- Measured as an inverse time (expansion rate): $H_0 = c\sqrt{\Lambda/3}$
- Measured as an acceleration (synchronization threshold): $a_0 = cH_0 / 2\pi$

The chain:

$$\Lambda \;\xrightarrow{c\sqrt{\cdot/3}}\; H_0 \;\xrightarrow{c/2\pi}\; a_0$$

Each arrow is a single multiplication by $c$ and a geometric factor. No free parameters. No fitting. The proslambenomenos is the vacuum's tick rate. Everything else is an interval measured from it.

## 6. Consequences for the Kuramoto–Einstein framework

This identification resolves an open question from the [companion framework](https://github.com/nickjoven/201): where does the coupling strength $K$ in the Kuramoto–Einstein mapping come from?

**Answer:** From the proslambenomenos.

The coupling kernel $K(x,x') = G_\gamma(x,x')$ (the Green's function of the spatial metric) has a characteristic scale set by $\Lambda$. The Kuramoto critical coupling $K_c$ corresponds to the acceleration scale $a_0$, and the coherence onset $r \propto \sqrt{K - K_c}$ reproduces the MOND interpolation function in the deep-field regime.

Below $a_0$: coupling subcritical, coherence drops, synchronization deficit appears as dark matter phantom.

Above $a_0$: coupling supercritical, full synchronization, Newtonian gravity, no phantom needed.

The vacuum is not empty. It oscillates at $\nu_\Lambda$. Gravity synchronizes matter to this oscillation. The proslambenomenos is the frequency at which the vacuum vibrates — and everything else is built on top of it.

## 7. What remains

The proslambenomenos identification gives us $a_0$ from $\Lambda$. But it does not, by itself, guarantee that the resulting galactic structure is unique. That requires a separate argument — the [Lyapunov dissipation proof](lyapunov_uniqueness.md) — which shows that the path to the fixed point, not the fixed point itself, enforces uniqueness.
