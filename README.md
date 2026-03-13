# Proslambenomenos

**The added tone: a fundamental reference frequency for synchronization gravity.**

N. Joven — March 2026 — [ORCID 0009-0008-0679-0812](https://orcid.org/0009-0008-0679-0812)

---

In ancient Greek music theory, the *proslambenomenos* (προσλαμβανόμενος) was the "added tone" — the lowest pitch in the Greater Perfect System, the reference from which every interval was measured. It did not belong to any tetrachord. It simply *was*, the ground note that made the entire harmonic structure intelligible.

This repository proposes a physical analogue: the cosmological constant $\Lambda$ sets a fundamental oscillation frequency

$$\nu_\Lambda \;=\; c\,\sqrt{\Lambda/3}$$

and the MOND acceleration scale, the Hubble rate, and the galactic synchronization threshold are all overtones of this single reference. They are not independent coincidences — they are intervals measured from the proslambenomenos.

## Contents

| Document | Description |
|----------|-------------|
| [`proslambenomenos.md`](proslambenomenos.md) | From $\Lambda$ to $a_0$: three constants, one frequency |
| [`lyapunov_uniqueness.md`](lyapunov_uniqueness.md) | Lyapunov functional and the dissipation argument for uniqueness |
| [`renzos_rule_from_kuramoto.md`](renzos_rule_from_kuramoto.md) | Renzo's Rule from Kuramoto self-consistency (companion to the ADM derivation in 201) |
| [`notebooks/`](notebooks/) | Companion Jupyter notebooks (stdlib Python only) |
| [`docs/`](docs/) | GitHub Pages walkthrough |

## Companion repositories

| Repository | Role |
|-----------|------|
| [intersections](https://github.com/nickjoven/intersections) | Stick-slip dynamics, galaxy rotation curves, Lagrangian relaxation |
| [201](https://github.com/nickjoven/201) | Unifying framework, Kuramoto–Einstein mapping, Renzo's Rule (ADM side) |

## What this closes

The [unifying framework](https://github.com/nickjoven/201/blob/main/joven_unifying_framework.md) and [Renzo's Rule derivation](https://github.com/nickjoven/201/blob/main/renzos_rule_derivation.md) in 201 left three gaps open after [PR #7](https://github.com/nickjoven/201/pull/7):

1. **Where does the coupling strength come from?** → The proslambenomenos: $\nu_\Lambda = c\sqrt{\Lambda/3}$ sets $K_c$ and therefore $a_0$.
2. **Mathematical proof replacing empirical uniqueness** → Lyapunov functional for the Kuramoto–Einstein system; dissipation selects a unique basin.
3. **Renzo's Rule from the synchronization side** → Derived from Kuramoto self-consistency, completing the circle with the ADM-side proof.

> **Uniqueness is not a mathematical property of the equilibrium — it is a physical property of the path.**

## License

[CC0 1.0 Universal](LICENSE) — No rights reserved.
