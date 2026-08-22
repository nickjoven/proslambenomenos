#!/usr/bin/env python3
"""Author the curriculum notebooks as nbformat-4 JSON (stdlib only; no
nbformat). Source of record for notebooks/*.ipynb: edit here, run
`python3 scripts/nb_build.py`, then `python3 scripts/nb_run.py`.

Each module: (a) a markdown cell stating the fact(s) with citations
from notes/temporal_first_curriculum.md and notes/cross_domain_
connections.md - classical, nothing novel; (b) code cells that compute
the fact; (c) a final cell running the relevant catalog/verify mutant
and requiring it to fail (LAW-11/16 made visible)."""
import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks"

BOOT = '''\
import sys, math, json, cmath, random
from fractions import Fraction
from pathlib import Path
_root = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "CATALOG.md").exists())
sys.path.insert(0, str(_root / "notebooks"))
from nbkit import ROOT, show_svg, catalog, verify, mutant_must_fail, falsify
import termplot
print("repo root:", ROOT.name)'''


def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": textwrap.dedent(s).strip("\n")}


def code(s):
    return {"cell_type": "code", "metadata": {}, "source": textwrap.dedent(s).strip("\n"),
            "outputs": [], "execution_count": None}


def notebook(cells):
    return {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                     "language_info": {"name": "python"}},
        "cells": cells,
    }


NOTEBOOKS = {}

# ───────────────────────────── T0 ─────────────────────────────
NOTEBOOKS["T0_return"] = [
    md("""
    # T0 — Return

    **Facts used** (classical; module T0 of `notes/temporal_first_curriculum.md`,
    and X-6 of `notes/cross_domain_connections.md`).

    1. A process is periodic with period $T$ iff $x(t+T)=x(t)$ for all $t$. One
       return $x(t_1)=x(0)$ is compatible with non-periodicity; the second return
       at the same interval is the first witness of a period (X-6: "strictly the
       SECOND return certifies periodicity").
    2. Rotation by $\\alpha = p/q$ on the circle $\\mathbb{R}/\\mathbb{Z}$ first
       returns at step $q$; an irrational rotation never returns exactly
       (Poincaré; Hardy & Wright ch. XXIII for the approximation orders).
    3. A frequency estimated from $n$ periods of a sinusoid is fuzzy by
       $\\Delta f \\approx 1/(nT)$: the main lobe of the truncated signal's Fourier
       transform narrows as $1/n$ (Fourier uncertainty; X-6's "frequency-comb
       narrowing").
    4. Catalog c01 (Tusi couple, al-Tusi 1247): a circle rolling inside a circle
       of twice its radius traces a straight diameter. Catalog c02: the cycloid's
       cusp at the contact point is semicubical, $|y| \\sim |x|^{2/3}$. Catalog c24
       (Sós 1958; Świerczkowski 1959): an irrational rotation's orbit is dense
       with at most three gap lengths; a rational one revisits $q$ points forever.

    Everything below is computed; the final cell runs the catalog mutants and
    requires them to fail.
    """),
    code(BOOT),
    md("## 1–2. Counting returns"),
    code("""
    def first_return(alpha, eps=1e-9, max_steps=10000):
        th = 0.0
        for n in range(1, max_steps + 1):
            th = (th + alpha) % 1.0
            if min(th, 1 - th) < eps:
                return n
        return None

    golden = (math.sqrt(5) - 1) / 2
    for label, a in [("1/2", 0.5), ("2/5", 0.4), ("3/7", 3 / 7), ("golden", golden)]:
        print(f"alpha = {label:>6}: first exact return at step {first_return(a)}")

    # near-returns of the golden rotation happen at Fibonacci steps and never close
    th, best = 0.0, []
    for n in range(1, 200):
        th = (th + golden) % 1.0
        d = min(th, 1 - th)
        if not best or d < best[-1][1]:
            best.append((n, d))
    print("golden: record near-returns (step, distance):", [(n, f"{d:.2e}") for n, d in best[:8]])
    """),
    code("""
    def check(claimed=lambda p, q: q):
        ok = True
        for p, q in [(1, 2), (2, 5), (3, 7), (5, 11)]:
            ok &= first_return(p / q) == claimed(p, q)
        return ok

    # the falsifier discipline: the same check with a wrong claim must fail
    falsify(check, {"return-at-numerator": lambda: {"claimed": lambda p, q: p}})
    """),
    md("""
    One coordinate's return is not the process's return: the damped signal
    below returns to its starting *value* at equal intervals, yet its state
    $(x, x')$ never returns - each visit has a smaller velocity.
    """),
    code("""
    x = lambda t: math.sin(t) * math.exp(-t / 4)          # damped - not periodic
    # zero crossings of x(t) - x(0) with x(0) = 0
    ts = [i * 1e-3 for i in range(1, 12000)]
    crossings = [t for a, t in zip(ts, ts[1:]) if x(a) * x(t) <= 0 and x(t) != x(a)]
    intervals = [b - a for a, b in zip(crossings, crossings[1:])]
    print("return times:", [f"{t:.3f}" for t in crossings[:4]])
    print("intervals   :", [f"{d:.3f}" for d in intervals[:3]], "(equal - the value is periodic)")
    print("state (x, x') at successive returns:", [(round(x(t), 6), round((x(t + 1e-6) - x(t)) / 1e-6, 3)) for t in crossings[:3]])
    """),
    md("## 3. The circumference sharpens as $1/n$"),
    code("""
    def main_lobe_halfwidth(n_periods, T=1.0, samples_per_period=64):
        # |sum x(t) e^{-2 pi i f t}| for a cosine observed over n periods; find the first zero above f0 = 1/T
        N = n_periods * samples_per_period
        dt = T / samples_per_period
        xs = [math.cos(2 * math.pi * t * dt / T) for t in range(N)]
        f0 = 1.0 / T
        prev = None
        for k in range(1, 4000):
            f = f0 + k * (0.0005 / n_periods)
            amp = abs(sum(x * cmath.exp(-2j * math.pi * f * t * dt) for t, x in enumerate(xs)))
            if prev is not None and amp > prev:
                return f - f0
            prev = amp
        return None

    ns = [1, 2, 4, 8]
    ws = [main_lobe_halfwidth(n) for n in ns]
    for n, w in zip(ns, ws):
        print(f"n = {n} periods: main-lobe half-width {w:.4f}  (1/n = {1 / n:.4f})")
    slope = math.log(ws[-1] / ws[0]) / math.log(ns[-1] / ns[0])
    print(f"log-log slope of width vs n: {slope:.3f}")
    print(termplot.plot_xy([(math.log(n), math.log(w)) for n, w in zip(ns, ws)], width=50, height=10,
                           title="ln(half-width) vs ln(n periods)", xlabel="ln n", ylabel="ln dF"))
    """),
    code("""
    def check(exponent=-1.0):
        return abs(slope - exponent) < 0.05

    falsify(check, {"narrows-as-1/sqrt(n)": lambda: {"exponent": -0.5}})
    """),
    md("## 4. Two returns that make a line, and a cusp (catalog c01, c02)"),
    code("""
    def hypocycloid(R, r, t):
        return ((R - r) * math.cos(t) + r * math.cos((R - r) / r * t),
                (R - r) * math.sin(t) - r * math.sin((R - r) / r * t))

    pts = [hypocycloid(2.0, 1.0, 2 * math.pi * k / 400) for k in range(400)]
    print("Tusi couple R = 2r: max |y| =", f"{max(abs(y) for _, y in pts):.1e}", " x spans",
          f"[{min(x for x, _ in pts):.3f}, {max(x for x, _ in pts):.3f}]")
    pts3 = [hypocycloid(3.0, 1.0, 2 * math.pi * k / 400) for k in range(400)]
    print(termplot.plot_xy(pts3, width=44, height=14, title="R = 3r for contrast: a deltoid, not a line"))

    cyc = [(t - math.sin(t), 1 - math.cos(t)) for t in (1e-2, 3e-3, 1e-3)]
    exps = [math.log(cyc[i][1] / cyc[i + 1][1]) / math.log(cyc[i][0] / cyc[i + 1][0]) for i in range(2)]
    print("cycloid cusp: local exponent d ln y / d ln x =", [f"{e:.4f}" for e in exps], " (2/3 =", f"{2 / 3:.4f})")
    """),
    code("""
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2.2 -2.2 4.4 4.4" width="260" height="260">',
           '<circle cx="0" cy="0" r="2" fill="none" stroke="currentColor" stroke-width="0.03"/>']
    d = "M " + " L ".join(f"{x:.3f} {-y:.3f}" for x, y in pts3)
    svg.append(f'<path d="{d} Z" fill="none" stroke="#B45309" stroke-width="0.04"/>')
    d2 = "M " + " L ".join(f"{x:.3f} {-y:.3f}" for x, y in pts[::8])
    svg.append(f'<path d="{d2}" fill="none" stroke="#2F4BC7" stroke-width="0.06"/>')
    svg.append("</svg>")
    show_svg("".join(svg), "Tusi (blue, R=2r) and deltoid (orange, R=3r)")
    """),
    md("## Falsifier: the catalog mutants must fail"),
    code("""
    for entry in ("c01_tusi_couple", "c02_cycloid_cusp", "c24_three_gap_kronecker"):
        rc, _ = catalog(entry)
        assert rc == 0, entry
        rc, out = catalog(entry, mutant=True)
        mutant_must_fail(entry, rc, out)
    """),
]

# ───────────────────────────── T1 ─────────────────────────────
NOTEBOOKS["T1_two_rhythms"] = [
    md("""
    # T1 — Two rhythms: rotation number and locking

    **Facts used** (classical; module T1; compendium C8/C9/C10 reimplemented
    here in Python).

    1. For the sine circle map $\\theta \\mapsto \\theta + \\Omega - (K/2\\pi)\\sin 2\\pi\\theta$
       the rotation number $\\rho(\\Omega) = \\lim (\\theta_n - \\theta_0)/n$ exists, is
       monotone non-decreasing in $\\Omega$, and locks on intervals at every
       rational (Poincaré; Arnold 1961; Jensen–Bak–Bohr 1983).
    2. Tongue widths scale as $w(p/q) \\propto K^q$ for small $K$ (Arnold 1961);
       hence $d\\ln(w_{1/2}/w_{1/3})/d\\ln K \\to -1$ (compendium C9).
    3. Adler (1946): $\\varphi' = \\Delta\\omega - 2K\\sin\\varphi$ locks iff
       $|\\Delta\\omega| \\le 2K$; below threshold the beat frequency is
       $\\sqrt{\\Delta\\omega^2 - (2K)^2}$ (compendium C10; catalog c23 states the
       same fact with coupling $K$ in place of $2K$).

    The rationals are the lockable ratios; the tongue edges are found below by
    the tangency condition rather than by scanning, so the widths are derived
    from the map and not read off a grid.
    """),
    code(BOOT),
    code("""
    def step(th, Om, K):
        return th + Om - (K / (2 * math.pi)) * math.sin(2 * math.pi * th)

    def rho(Om, K, iters=900, transient=250):
        th = 0.0
        for _ in range(transient):
            th = step(th, Om, K)
        start = th
        for _ in range(iters):
            th = step(th, Om, K)
        return (th - start) / iters

    K = 1.0
    grid = [(i / 200, rho(i / 200, K)) for i in range(201)]
    mono = all(b[1] >= a[1] - 1e-3 for a, b in zip(grid, grid[1:]))
    print("monotone on a 200-point grid:", mono)
    print(termplot.staircase(grid, width=64, height=18, title="rho(Omega) at K = 1: the devil's staircase",
                             xlabel="Omega", ylabel="rho", markers={"1/2": 0.5, "1/3": 1 / 3, "2/3": 2 / 3}))
    """),
    md("""
    ## Tongue edges by tangency

    $\\rho = p/q$ is locked iff $g(\\theta) = f^q(\\theta) - \\theta - p$ has a zero.
    $g$ increases with $\\Omega$ for every $\\theta$, so the left edge is the
    $\\Omega$ where $\\max_\\theta g = 0$ and the right edge where $\\min_\\theta g = 0$.
    """),
    code("""
    def g_extrema(Om, K, p, q, n=720):
        lo, hi = float("inf"), float("-inf")
        for i in range(n):
            th0 = i / n
            th = th0
            for _ in range(q):
                th = step(th, Om, K)
            v = th - th0 - p
            lo, hi = min(lo, v), max(hi, v)
        return lo, hi

    def tongue(p, q, K, span=0.02, scan=200):
        target = p / q
        # the tongue need not contain p/q itself (its centre shifts by O(K^2) for q >= 3):
        # scan for one locked Omega, then bisect each edge from there
        inside = None
        for i in range(scan + 1):
            Om = target - span + 2 * span * i / scan
            lo, hi = g_extrema(Om, K, p, q, n=360)
            if lo <= 0 <= hi:
                inside = Om; break
        assert inside is not None, "no locked point found in the scan"
        def bisect(fn, a, b):               # fn increasing in Om, fn(a) < 0 <= fn(b)
            for _ in range(40):
                m = (a + b) / 2
                if fn(m) < 0: a = m
                else: b = m
            return (a + b) / 2
        left = bisect(lambda Om: g_extrema(Om, K, p, q)[1], inside - span, inside)
        right = bisect(lambda Om: g_extrema(Om, K, p, q)[0], inside, inside + span)
        return left, right

    widths = {}
    for K in (0.2, 0.4):
        for p, q in ((1, 2), (1, 3)):
            l, r = tongue(p, q, K)
            widths[(K, q)] = r - l
            print(f"K = {K}: tongue {p}/{q} = [{l:.6f}, {r:.6f}]  width {r - l:.4e}")
    print("compendium C9 reference widths: 3.147e-3, 1.2533e-2 (1/2); 2.83e-4, 2.183e-3 (1/3)")
    """),
    code("""
    def check(q_offset=0, slope_target=-1.0):
        r12 = widths[(0.4, 2)] / widths[(0.2, 2)]
        r13 = widths[(0.4, 3)] / widths[(0.2, 3)]
        abs_ok = abs(r12 - 2 ** (2 + q_offset)) / 2 ** (2 + q_offset) < 0.15 and \\
                 abs(r13 - 2 ** (3 + q_offset)) / 2 ** (3 + q_offset) < 0.15
        slope = math.log((widths[(0.2, 2)] / widths[(0.2, 3)]) / (widths[(0.4, 2)] / widths[(0.4, 3)])) / math.log(0.2 / 0.4)
        print(f"  doubling K: w(1/2) x{r12:.2f}, w(1/3) x{r13:.2f}; ratio-law slope {slope:.3f}")
        return abs_ok and abs(slope - slope_target) < 0.15

    falsify(check, {"exponent-q-plus-1": lambda: {"q_offset": 1},
                    "ratio-law-slope-zero": lambda: {"slope_target": 0.0}})
    """),
    md("## Adler's threshold"),
    code("""
    def beat(dw, K, coef=2.0, T=400.0, dt=0.002):
        # integrate phi' = dw - coef K sin phi with RK4; count rotations. Lock must emerge, not be assumed.
        f = lambda p: dw - coef * K * math.sin(p)
        phi, rot, last = 0.0, 0, 0.0
        n = int(T / dt)
        for _ in range(n):
            k1 = f(phi); k2 = f(phi + dt * k1 / 2); k3 = f(phi + dt * k2 / 2); k4 = f(phi + dt * k3)
            phi += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            while phi - last > 2 * math.pi:
                rot += 1; last += 2 * math.pi
        return rot * 2 * math.pi / T

    K = 0.3
    rows = []
    for dw in (0.45, 0.6, 0.62, 0.7, 0.9):
        b = beat(dw, K)
        pred = 0.0 if abs(dw) <= 2 * K else math.sqrt(dw * dw - 4 * K * K)
        rows.append((dw, b, pred))
        print(f"K = {K}, dw = {dw:.2f}: beat {b:.4f}   sqrt(dw^2 - (2K)^2) = {pred:.4f}")
    print(termplot.plot_xy([(dw, b) for dw, b, _ in rows] + [(dw, p) for dw, _, p in rows], width=50, height=10,
                           title="beat frequency vs dw (measured and formula)", xlabel="dw", ylabel="beat"))
    """),
    code("""
    def check(thr_factor=2.0, coef=2.0):
        thr = thr_factor * K
        pred = lambda dw: 0.0 if abs(dw) <= thr else math.sqrt(dw * dw - thr * thr)
        b1, b2, b3 = beat(0.45, K, coef), beat(0.62, K, coef), beat(0.9, K, coef)
        return b1 == pred(0.45) and b2 > 0 and abs(b2 - pred(0.62)) < 0.02 and abs(b3 - pred(0.9)) < 0.02

    falsify(check, {"threshold-K-not-2K": lambda: {"thr_factor": 1.0},
                    "ode-coefficient-K": lambda: {"coef": 1.0}})
    """),
    md("""
    The golden ratio is the most stubborn drifter: the gaps in the staircase
    at $K<1$ are the irrationals, and the one worst approximated by rationals
    (Hurwitz) is $(\\sqrt5 - 1)/2$. Not re-verified here; stated with citation only.

    ## Falsifier: catalog c23 (Adler, in the $\\delta - K\\sin\\theta$ convention) must fail under its mutant
    """),
    code("""
    rc, _ = catalog("c23_adler_locking_range")
    assert rc == 0
    rc, out = catalog("c23_adler_locking_range", mutant=True)
    mutant_must_fail("c23_adler_locking_range", rc, out)
    """),
]

# ───────────────────────────── T2 ─────────────────────────────
NOTEBOOKS["T2_half_turn"] = [
    md("""
    # T2 — The first shape, and its half turn

    **Facts used** (module T2 and T6 of the curriculum note, placed here per
    X-6's dependency order "the parity material sits exactly one return deeper
    than the circle").

    1. The circle is $\\mathbb{R}/\\mathbb{Z}$: time modulo period (T2). Its
       functions are the modes $e^{2\\pi i m x}$, $m \\in \\mathbb{Z}$.
    2. With antiperiodic closure $f(x+1) = -f(x)$ the modes have
       $m \\in \\mathbb{Z}+\\tfrac12$ (Matsubara 1955; Scherk–Schwarz 1979; X-2, X-9).
       On a ring of $N$ phases with $\\theta_{i+N} = \\theta_i + \\pi$ the uniform
       gradients carry winding in $\\mathbb{Z}+\\tfrac12$ (Bulaevskii 1977 per LC-3;
       claim `klein-twisted-gradient-xor`).
    3. The half-translation $J: x \\mapsto x + \\tfrac12$ squares to
       $J^2 = (-1)^{2m}$ on every mode; the sign depends on the $x$-parity class,
       not on the bundle (claim `half-shift-squares-by-x-parity`;
       `scripts/verify/q_j_structure_sectors.py`).
    4. One traversal cannot tell periodic from antiperiodic return: $|f|^2$ is
       unchanged after one loop either way, and $f$ itself closes after two
       (X-6: the $2\\pi$-vs-$4\\pi$ fact).
    """),
    code(BOOT),
    md("## 1–2. Windings on a twisted ring"),
    code("""
    N = 8
    rows = []
    for twist in (0.0, math.pi):
        ws = []
        for k in range(-2, 3):
            delta = (twist + 2 * math.pi * k) / N            # uniform bond gradient closing with the twist
            total = N * delta
            ws.append(total / (2 * math.pi))
        rows.append((twist, ws))
        print(f"twist {twist:.3f}: windings of uniform gradients = {ws}")
    """),
    code("""
    def check(twist=math.pi, claimed_lattice=0.5):
        ws = [(twist + 2 * math.pi * k) / (2 * math.pi) for k in range(-3, 4)]
        return all(abs((w - claimed_lattice) - round(w - claimed_lattice)) < 1e-12 for w in ws)

    falsify(check, {"integer-windings-on-twisted-ring": lambda: {"claimed_lattice": 0.0}})
    """),
    md("## 3. $J^2$ on the flat Klein bottle's modes (reusing the verify script's functions)"),
    code("""
    import importlib.util
    spec = importlib.util.spec_from_file_location("qjs", ROOT / "scripts/verify/q_j_structure_sectors.py")
    qjs = importlib.util.module_from_spec(spec); spec.loader.exec_module(qjs)

    table = []
    for m in (0, 0.5, 1, 1.5, 2):
        for br in ("cos", "sin"):
            f = qjs.mode(m, 1, br)
            table.append((m, br, qjs.bundle(f), qjs.j2(f)))
            print(f"m = {m:<4} {br}  bundle = {table[-1][2]:<9}  J^2 = {table[-1][3]:+d}")
    """),
    code("""
    def check(rule="x-parity"):
        if rule == "x-parity":
            return all(s == (1 if float(m).is_integer() else -1) for m, _, _, s in table)
        return all(s == (-1 if b == "twisted" else 1) for _, _, b, s in table)

    falsify(check, {"bundle-decides": lambda: {"rule": "bundle"}})
    """),
    md("## 4. One loop is blind to the sign; two loops close"),
    code("""
    def traverse(m, loops, x=0.137):
        f = lambda x: cmath.exp(2j * math.pi * m * x)
        return f(x + loops) / f(x)

    for m in (1, 0.5, 1.5):
        one, two = traverse(m, 1), traverse(m, 2)
        print(f"m = {m}: after one loop f -> {one.real:+.0f} f,  |f|^2 ratio {abs(one) ** 2:.0f};  after two loops f -> {two.real:+.0f} f")
    """),
    code("""
    def check(loops_to_close=2):
        half = [0.5, 1.5, -0.5]
        intensity_blind = all(abs(abs(traverse(m, 1)) ** 2 - 1) < 1e-12 for m in half)
        closes = all(abs(traverse(m, loops_to_close) - 1) < 1e-12 for m in half)
        return intensity_blind and closes

    falsify(check, {"closes-after-one-loop": lambda: {"loops_to_close": 1}})
    """),
    md("## Falsifier: the verify script's named mutant must fail"),
    code("""
    rc, out = verify("q_j_structure_sectors.py")
    assert rc == 0
    rc, out = verify("q_j_structure_sectors.py", mutant="bundle-decides")
    mutant_must_fail("bundle-decides", rc, out)
    """),
]

# ───────────────────────────── T3 ─────────────────────────────
NOTEBOOKS["T3_counts_vs_anchors"] = [
    md("""
    # T3 — Counts versus anchors

    **Facts used** (classical; catalog c05, c08, c11, c14, c15). The organizing
    sentence: *the integer is structural, the anchor is medium* (X-10's
    "order + number"; X-11's "number enters only as count").

    1. Koenig (Goldstein ch. 1): $L = R_{cm}\\times P + L_{rel}$ and
       $T = \\tfrac12 M V_{cm}^2 + T_{rel}$ for any particle system (c08, c14); a
       uniform field exerts no torque about the CM (c15). The split is an identity
       in the masses - no medium enters.
    2. Toomre (1964; Binney & Tremaine eq. 6.55): the fluid-disk WKB dispersion
       $\\omega^2 = \\kappa^2 - 2\\pi G\\Sigma k + k^2\\sigma^2$ has growing modes iff
       $\\sigma\\kappa/(\\pi G\\Sigma) < 1$ (c05). The threshold **1** is the
       discriminant of a quadratic; $G, \\Sigma, \\kappa, \\sigma$ are the anchors.
    3. Schrödinger (1914): the nearest-neighbour chain has
       $\\omega(k) = 2\\sqrt{J/m}\\,|\\sin(k/2)|$ (c11). A ring of $N$ masses has
       exactly $N$ modes whatever $J/m$; $\\sqrt{J/m}$ only scales them.
    """),
    code(BOOT),
    md("## 1. Koenig: an identity in the masses"),
    code("""
    def koenig(seed):
        random.seed(seed)
        n = 7
        m = [random.uniform(0.5, 2) for _ in range(n)]
        r = [[random.uniform(-1, 1) for _ in range(3)] for _ in range(n)]
        v = [[random.uniform(-1, 1) for _ in range(3)] for _ in range(n)]
        M = sum(m)
        R = [sum(m[i] * r[i][k] for i in range(n)) / M for k in range(3)]
        V = [sum(m[i] * v[i][k] for i in range(n)) / M for k in range(3)]
        cross = lambda a, b: [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
        L = [sum(m[i] * cross(r[i], v[i])[k] for i in range(n)) for k in range(3)]
        L_rel = [sum(m[i] * cross([r[i][j] - R[j] for j in range(3)], [v[i][j] - V[j] for j in range(3)])[k] for i in range(n)) for k in range(3)]
        L_cm = cross(R, [M * V[k] for k in range(3)])
        T = sum(0.5 * m[i] * sum(v[i][k] ** 2 for k in range(3)) for i in range(n))
        T_rel = sum(0.5 * m[i] * sum((v[i][k] - V[k]) ** 2 for k in range(3)) for i in range(n))
        T_cm = 0.5 * M * sum(V[k] ** 2 for k in range(3))
        return L, L_rel, L_cm, T, T_rel, T_cm

    for seed in (1, 2, 3):
        L, L_rel, L_cm, T, T_rel, T_cm = koenig(seed)
        errL = max(abs(L[k] - L_rel[k] - L_cm[k]) for k in range(3))
        print(f"seed {seed}: |L - (R x P + L_rel)| = {errL:.1e}   |T - (M V^2/2 + T_rel)| = {abs(T - T_rel - T_cm):.1e}")
    """),
    code("""
    def check(keep_cm_term=True):
        L, L_rel, L_cm, T, T_rel, T_cm = koenig(5)
        w = 1.0 if keep_cm_term else 0.0
        return max(abs(L[k] - L_rel[k] - w * L_cm[k]) for k in range(3)) < 1e-12 and abs(T - T_rel - w * T_cm) < 1e-12

    falsify(check, {"omit-cm-term": lambda: {"keep_cm_term": False}})
    """),
    md("## 2. Toomre: the 1 is a discriminant"),
    code("""
    def min_omega2(sigma, G=1.0, Sigma=1.0, kappa=1.0):
        # omega^2(k) = kappa^2 - 2 pi G Sigma k + k^2 sigma^2; a quadratic in k with minimum at k* = pi G Sigma / sigma^2
        ks = [0.001 * j for j in range(1, 20000)]
        numeric = min(kappa ** 2 - 2 * math.pi * G * Sigma * k + k * k * sigma * sigma for k in ks)
        closed = kappa ** 2 - (math.pi * G * Sigma / sigma) ** 2
        return numeric, closed

    for anchors in ((1.0, 1.0, 1.0), (2.0, 0.5, 3.0), (0.3, 4.0, 0.7)):
        G, Sigma, kappa = anchors
        print(f"anchors G={G}, Sigma={Sigma}, kappa={kappa}:")
        for Q in (0.9, 0.99, 1.01, 1.1):
            sigma = Q * math.pi * G * Sigma / kappa
            num, clo = min_omega2(sigma, G, Sigma, kappa)
            print(f"   Q = {Q:<5} min omega^2 = {num:+.4f} (closed form {clo:+.4f}) -> {'unstable' if num < 0 else 'stable'}")
    """),
    code("""
    def check(threshold=1.0):
        ok = True
        for G, Sigma, kappa in ((1.0, 1.0, 1.0), (2.0, 0.5, 3.0), (0.3, 4.0, 0.7)):
            for Q in (0.5, 0.9, 0.99, 1.01, 1.1, 1.5):
                sigma = Q * math.pi * G * Sigma / kappa
                ok &= (min_omega2(sigma, G, Sigma, kappa)[0] < 0) == (Q < threshold)
        return ok

    falsify(check, {"threshold-2": lambda: {"threshold": 2.0}})
    """),
    md("## 3. The chain: $N$ modes, one anchor"),
    code("""
    def chain_modes(N, J, m):
        # eigenvalues of the ring Laplacian on plane waves k = 2 pi n / N
        return sorted(math.sqrt((2 - 2 * math.cos(2 * math.pi * n / N)) * J / m) for n in range(N))

    N = 12
    for J, m in ((1.0, 1.0), (4.0, 1.0), (1.0, 9.0)):
        w = chain_modes(N, J, m)
        scaled = [x / math.sqrt(J / m) for x in w]
        print(f"J/m = {J / m:<5}: {len(w)} modes; omega/sqrt(J/m) = {[round(s, 4) for s in scaled[:6]]} ...")
    ks = [2 * math.pi * n / N for n in range(N // 2 + 1)]
    print(termplot.plot_xy([(k, 2 * abs(math.sin(k / 2))) for k in ks] + [(k, k) for k in ks], width=50, height=12,
                           title="omega/sqrt(J/m): chain (curve) vs continuum line", xlabel="k", ylabel="omega"))
    """),
    code("""
    def check(law="chain"):
        worst = 0.0
        for n in (1, 5, 13, 31):
            k = 2 * math.pi * n / 64
            num = math.sqrt(2 - 2 * math.cos(k))
            claim = k if law == "continuum" else 2 * abs(math.sin(k / 2))
            worst = max(worst, abs(num - claim) / num)
        return worst < 1e-12

    falsify(check, {"continuum-law": lambda: {"law": "continuum"}})
    """),
    md("## Falsifier: every catalog mutant used here must fail"),
    code("""
    for entry in ("c05_toomre_fluid", "c08_koenig_angular_momentum", "c14_koenig_kinetic_energy",
                  "c15_cm_torque_uniform_gravity", "c11_chain_dispersion"):
        rc, _ = catalog(entry)
        assert rc == 0, entry
        rc, out = catalog(entry, mutant=True)
        mutant_must_fail(entry, rc, out)
    """),
]

# ───────────────────────────── T4 ─────────────────────────────
NOTEBOOKS["T4_gradient_vs_hamiltonian"] = [
    md("""
    # T4 — Gradient flow versus Hamiltonian flow

    **Facts used** (classical; `scripts/verify/kuramoto_einstein_refutation.py`
    check 1, claim `einstein-from-kuramoto-chain-a`, refuted).

    1. With symmetric coupling, $\\theta' = -\\partial V/\\partial\\theta$ with
       $V = -K\\sum\\cos(\\theta_j - \\theta_i)$: $V$ is a Lyapunov function and the
       linearization about a locked state is self-adjoint (Strogatz 2000).
    2. The signature computed here: a small perturbation of a locked chain
       spreads diffusively, width $\\sim t^{1/2}$; the same chain with inertia
       (a wave equation) spreads ballistically, width $\\sim t^{1}$. The verify
       script reports 0.5 versus 0.989 at $N=401$, 4000 steps; this notebook
       runs a smaller, faster version of the same computation.
    3. Curriculum T4 names curvature as the holonomy of clock transport; that
       material is cited only (Sagnac 1913; MTW sec. 17). Nothing here derives it.
    """),
    code(BOOT),
    code("""
    def spread(inertial, N=201, K=1.0, dt=0.02, steps=2000, every=400):
        th = [0.0] * N
        w = [0.0] * N
        th[N // 2] = 1e-3
        out = []
        V0 = None
        for k in range(1, steps + 1):
            F = [K * (math.sin(th[(i + 1) % N] - th[i]) + math.sin(th[i - 1] - th[i])) for i in range(N)]
            if inertial:
                for i in range(N):
                    w[i] += F[i] * dt
                    th[i] += w[i] * dt
            else:
                for i in range(N):
                    th[i] += F[i] * dt
            if k % every == 0:
                m0 = sum(abs(v) for v in th)
                m2 = sum(abs(v) * (i - N // 2) ** 2 for i, v in enumerate(th))
                V = -K * sum(math.cos(th[(i + 1) % N] - th[i]) for i in range(N))
                out.append((k * dt, math.sqrt(m2 / m0), V))
        return out

    res = {name: spread(flag) for name, flag in (("overdamped", False), ("inertial", True))}
    expo = {}
    for name, rows in res.items():
        (t0, w0, _), (t1, w1, _) = rows[0], rows[-1]
        expo[name] = math.log(w1 / w0) / math.log(t1 / t0)
        print(f"{name:>10}: widths {[round(w, 2) for _, w, _ in rows]}  exponent {expo[name]:.3f}")
    print(termplot.plot_xy([(math.log(t), math.log(w)) for t, w, _ in res['overdamped']] +
                           [(math.log(t), math.log(w)) for t, w, _ in res['inertial']], width=50, height=12,
                           title="ln width vs ln t (lower: overdamped ~1/2, upper: inertial ~1)", xlabel="ln t", ylabel="ln w"))
    """),
    code("""
    def check(model="overdamped", target=0.5):
        return abs(expo[model] - target) < 0.1

    falsify(check, {"inertial": lambda: {"model": "inertial"}})
    """),
    md("## The Lyapunov function decreases; the inertial energy does not"),
    code("""
    Vs = [V for _, _, V in res["overdamped"]]
    print("overdamped V(t) samples:", [f"{v:.9f}" for v in Vs])
    print("monotone non-increasing:", all(b <= a + 1e-12 for a, b in zip(Vs, Vs[1:])))
    """),
    md("## Falsifier: the verify script's `inertial` mutant must fail"),
    code("""
    rc, out = verify("kuramoto_einstein_refutation.py", mutant="inertial")
    mutant_must_fail("inertial", rc, out)
    """),
]

# ───────────────────────────── T5 ─────────────────────────────
NOTEBOOKS["T5_corners"] = [
    md("""
    # T5 — Corners and weak discontinuities

    **Facts used** (classical; X-12 of `notes/cross_domain_connections.md`,
    corrected per LC-4; catalog c11).

    1. d'Alembert: $u(x,t) = \\tfrac12[f(x-ct) + f(x+ct)]$ for the ideal string with
       initial displacement $f$ and zero velocity. A slope jump in $f$ (a corner)
       travels on the characteristics unchanged - a *weak* discontinuity
       (Hadamard 1903), not a shock (Courant & Friedrichs 1948).
    2. On the mass chain $\\omega(k) = 2\\sqrt{J/m}|\\sin(k/2)|$ (c11; Schrödinger 1914),
       group velocity depends on $k$, and the corner disperses.
    3. X-12's table: the $\\pi$ twist is a class of the bundle (static, conserved
       as $\\mathbb{Z}_2$, dies under nothing); the corner is a singularity of the
       solution (moves at $c$, dies under dispersion and damping). Computed here:
       row "dies under dispersion".
    """),
    code(BOOT),
    code("""
    N, c = 256, 1.0
    def triangle(x, center=N // 2, half=24):
        return max(0.0, 1 - abs(x - center) / half)

    def sharpness(u):
        # largest second difference: the corner is where the slope jumps
        return max(abs(u[i + 1] - 2 * u[i] + u[i - 1]) for i in range(1, len(u) - 1))

    def dalembert(t):
        return [0.5 * (triangle(x - c * t) + triangle(x + c * t)) for x in range(N)]

    def chain(t_end, dt=0.05):
        u = [triangle(x) for x in range(N)]
        v = [0.0] * N
        steps = int(round(t_end / dt))
        for _ in range(steps):                              # leapfrog / Verlet on the linear chain
            a = [u[(i + 1) % N] - 2 * u[i] + u[(i - 1) % N] for i in range(N)]
            v = [v[i] + dt * a[i] for i in range(N)]
            u = [u[i] + dt * v[i] for i in range(N)]
        return u

    times = [0, 10, 20, 40, 60]
    rows = []
    for t in times:
        s_cont, s_chain = sharpness(dalembert(t)), sharpness(chain(t))
        rows.append((t, s_cont, s_chain))
        print(f"t = {t:>3}: corner sharpness  continuum {s_cont:.4f}   chain {s_chain:.4f}")
    print(termplot.plot_xy([(x, u) for x, u in enumerate(chain(40))], width=64, height=10,
                           title="chain displacement at t = 40 (the two half-corners, blurred)", xlabel="site"))
    print(termplot.plot_xy([(x, u) for x, u in enumerate(dalembert(40))], width=64, height=10,
                           title="d'Alembert at t = 40 (two half-corners, sharp)", xlabel="x"))
    """),
    code("""
    def check(chain_keeps_corner=False):
        cont = [s for _, s, _ in rows[1:]]
        ch = [s for _, _, s in rows[1:]]
        continuum_conserved = max(cont) - min(cont) < 1e-9 and abs(cont[0] - rows[0][1] / 2) < 1e-9
        chain_decays = all(b < a for a, b in zip(ch, ch[1:])) and ch[-1] < 0.5 * cont[-1]
        return continuum_conserved and (chain_decays != chain_keeps_corner)

    falsify(check, {"chain-is-non-dispersive": lambda: {"chain_keeps_corner": True}})
    """),
    md("## The reason: group velocity on the chain is not constant"),
    code("""
    def vg(k, J=1.0, m=1.0):
        return math.sqrt(J / m) * math.cos(k / 2) * (1 if k >= 0 else -1)

    ks = [i * math.pi / 16 for i in range(1, 16)]
    print("k/pi  v_group(chain)  v_group(continuum)")
    for k in ks[::2]:
        print(f"{k / math.pi:.3f}   {vg(k):.4f}          {c:.4f}")
    """),
    md("## Falsifier: c11's continuum mutant must fail"),
    code("""
    rc, _ = catalog("c11_chain_dispersion")
    assert rc == 0
    rc, out = catalog("c11_chain_dispersion", mutant=True)
    mutant_must_fail("c11_chain_dispersion", rc, out)
    """),
]

# ───────────────────────────── T6 ─────────────────────────────
NOTEBOOKS["T6_order_and_number"] = [
    md("""
    # T6 — Order + number

    **Cited only** (X-10; no computation here touches them): causal order
    determines the conformal geometry of a distinguishing spacetime
    (Hawking, King, McCarthy, J. Math. Phys. 17, 174 (1976); Malament, J. Math.
    Phys. 18, 1399 (1977)); the conformal factor is supplied by counting
    (Bombelli, Lee, Meyer, Sorkin, PRL 59, 521 (1987)). Overreach named in X-10:
    none of this derives spatial dimension from time.

    **Computed**: curvature as a count, without irrationals (X-11: a being with
    no metric whose "$\\pi$ is half"). For a closed polyhedral surface the angle
    deficit at a vertex is $1 - (\\text{sum of face angles})$ in *turns*; Descartes
    (c. 1630) / Gauss–Bonnet: the deficits sum to $\\chi$ turns, $\\chi = V - E + F$
    (Euler 1758); catalog c17 (Regge 1961). On a cube every deficit is $1/4$ turn
    and eight of them make 2 turns. Every number below is a `Fraction`.
    """),
    code(BOOT),
    md("## Voxel solids: every face angle is a quarter turn"),
    code("""
    def surface(voxels):
        # boundary unit squares of a set of unit cubes; each square as a frozenset of 4 vertices
        voxels = set(voxels)
        squares = []
        for (x, y, z) in voxels:
            for axis in range(3):
                for side in (0, 1):
                    nb = list((x, y, z)); nb[axis] += 1 if side else -1
                    if tuple(nb) in voxels:
                        continue
                    base = [x, y, z]; base[axis] += side
                    a, b = [i for i in range(3) if i != axis]
                    vs = []
                    for da, db in ((0, 0), (1, 0), (1, 1), (0, 1)):
                        p = list(base); p[a] += da; p[b] += db
                        vs.append(tuple(p))
                    squares.append(vs)
        return squares

    def euler_and_deficits(squares, turn=Fraction(1)):
        V = {v for sq in squares for v in sq}
        E = {frozenset((sq[i], sq[(i + 1) % 4])) for sq in squares for i in range(4)}
        chi = len(V) - len(E) + len(squares)
        count = {v: 0 for v in V}
        for sq in squares:
            for v in sq:
                count[v] += 1
        deficits = {v: turn - n * Fraction(1, 4) for v, n in count.items()}
        return chi, deficits

    solids = {
        "cube": [(0, 0, 0)],
        "2x1x1 box": [(0, 0, 0), (1, 0, 0)],
        "L-shape": [(0, 0, 0), (1, 0, 0), (0, 1, 0)],
        "3x3x1 ring (torus)": [(i, j, 0) for i in range(3) for j in range(3) if (i, j) != (1, 1)],
    }
    results = {}
    for name, vox in solids.items():
        chi, deficits = euler_and_deficits(surface(vox))
        total = sum(deficits.values())
        hist = {}
        for d in deficits.values():
            hist[d] = hist.get(d, 0) + 1
        results[name] = (chi, total)
        print(f"{name:>20}: chi = {chi:>2}; deficits {dict(sorted(hist.items()))} -> sum = {total} turn(s)")
    """),
    md("## Regular polyhedra: rational deficits, no $\\pi$"),
    code("""
    # (vertices, faces-per-vertex, corner angle of the face in turns): a regular p-gon has corner (p-2)/(2p)
    regular = {"tetrahedron": (4, 3, Fraction(1, 6)), "cube": (8, 3, Fraction(1, 4)),
               "octahedron": (6, 4, Fraction(1, 6)), "dodecahedron": (20, 3, Fraction(3, 10)),
               "icosahedron": (12, 5, Fraction(1, 6))}
    for name, (V, n, corner) in regular.items():
        d = 1 - n * corner
        print(f"{name:>12}: {V} vertices x deficit {d} = {V * d} turns")
    """),
    code("""
    def check(turn=Fraction(1), expected_total=None):
        ok = True
        for name, vox in solids.items():
            chi, deficits = euler_and_deficits(surface(vox), turn)
            ok &= sum(deficits.values()) == (chi if expected_total is None else expected_total)
        for name, (V, n, c) in regular.items():
            ok &= V * (turn - n * c) == (2 if expected_total is None else expected_total)
        return ok

    falsify(check, {"full-turn-is-three-quarters": lambda: {"turn": Fraction(3, 4)},
                    "deficits-sum-to-one-turn": lambda: {"expected_total": 1}})
    """),
    md("""
    The torus row is the point: its deficits are $+1/4$ at eight convex corners
    and $-1/4$ at eight saddle corners, summing to $0 = \\chi(T^2)$. Negative
    curvature as a count, no ambient space needed (Gauss; X-10's "embedding"
    baggage item).
    """),
    code("""
    chi, deficits = euler_and_deficits(surface(solids["3x3x1 ring (torus)"]))
    neg = sorted(v for v, d in deficits.items() if d < 0)
    print("saddle vertices (deficit -1/4):", neg)
    """),
    md("## Falsifier: catalog c17 (Descartes / Regge 1961) must fail under its mutant"),
    code("""
    rc, _ = catalog("c17_gauss_bonnet_polyhedra")
    assert rc == 0
    rc, out = catalog("c17_gauss_bonnet_polyhedra", mutant=True)
    mutant_must_fail("c17_gauss_bonnet_polyhedra", rc, out)
    """),
]

# ───────────────────────────── capstone ─────────────────────────────
NOTEBOOKS["capstone_null_before_grid"] = [
    md("""
    # Capstone — Derive the null before reading the grid

    A worked example from the repo's own record (P-1, resolved as R-1 in
    `PREDICTIONS.md`; `notes/p1_decomposition.md` D4 hole (a);
    `notes/p4_twisted_inertial_ring.md` run 5).

    1. **d4_nopin**: a Kuramoto lattice with no per-site drive, twisted and
       control, 101 values of $\\Omega$. The first reading counted 7 "rational
       snaps" per row. The null: $\\rho = \\Omega$ identically (claim
       `klein-twisted-mean-frequency-identity`; each undirected edge contributes
       $\\sin x + \\sin(-x) = 0$), so a "snap" is any grid point where $\\Omega$ itself
       is a rational with $q \\le 8$. Computed below: the snap set equals that
       grid set.
    2. **P-4 run 5**: slip periods near 3.0 (and 4.3) round trips were read as
       integer plateaus. The null: quasi-static loading with stiffness $4J/N$
       gives period/round-trip $= F_N/(4Jv)$ with no wave involved (catalog c12,
       within 25% on the 16 rows with prediction $\\ge 3$); $F_N/(4v) = 3.0$ at
       $(0.6, 0.05)$ and $(1.2, 0.1)$ - a grid coincidence, flagged in the table.
       Catalog c13 records what the formula cannot see (a $2.2\\times$ swing with
       $\\mu_d$ at fixed $F_N, v$).
    """),
    code(BOOT),
    md("## 1. The snaps are the grid"),
    code("""
    rows = json.loads((ROOT / "scripts/experiments/d4_nopin_results.json").read_text())
    TOL = 5e-4
    def snaps(rows):
        out = []
        for r in rows:
            for q in range(2, 9):
                p = round(r["rho"] * q)
                if abs(r["rho"] - p / q) < TOL and math.gcd(p, q) == 1 and 0 < p < q:
                    out.append(round(r["Omega"], 2)); break
        return sorted(set(out))

    grid_rationals = sorted({k / 100 for k in range(101)
                             if 0 < k < 100 and Fraction(k, 100).denominator <= 8})
    print("grid points that ARE rationals with q <= 8 (the null):", grid_rationals)
    maxdev = 0.0
    for Delta in (0.05, 0.2):
        for tw in (False, True):
            sel = [r for r in rows if r["Delta"] == Delta and r["twisted"] == tw]
            s = snaps(sel)
            maxdev = max(maxdev, max(abs(r["rho"] - r["Omega"]) for r in sel))
            print(f"Delta {Delta:<5} {'twisted' if tw else 'control':>8}: snaps {s} == null: {s == grid_rationals}")
    print(f"max |rho - Omega| over all {len(rows)} runs: {maxdev:.1e}")
    """),
    code("""
    def check(tol=TOL, null="grid"):
        ok = abs(maxdev) < 1e-10
        for Delta in (0.05, 0.2):
            for tw in (False, True):
                sel = [r for r in rows if r["Delta"] == Delta and r["twisted"] == tw]
                s = snaps(sel)
                ok &= (s == grid_rationals) if null == "grid" else (len(s) > 2.2 and s != grid_rationals)
        return ok

    falsify(check, {"snaps-are-locking": lambda: {"null": "locking"}})
    """),
    md("The identity behind the null, with its own named mutant:"),
    code("""
    rc, out = verify("p1_mean_frequency.py")
    assert rc == 0
    rc, out = verify("p1_mean_frequency.py", mutant="phase-lag")
    mutant_must_fail("phase-lag", rc, out)
    """),
    md("## 2. The loading formula"),
    code("""
    data = json.loads((ROOT / "scripts/experiments/p4_results_lowdamp.json").read_text())
    sel = [r for r in data if r["g"] == 0.01 and r["regime"] == "stick-slip" and r["F_N"] / (4 * r["v"]) >= 3 - 1e-9]
    print(f"{'N':>3} {'F_N':>5} {'v':>5} | observed  F_N/(4Jv)  rel.err")
    errs = []
    for r in sorted(sel, key=lambda r: (r["N"], r["v"], r["F_N"])):
        pred = r["F_N"] / (4 * r["v"])
        e = abs(r["ratio"] - pred) / r["ratio"]
        errs.append(e)
        flag = "  <- F_N/(4v) = 3.0 on the grid" if abs(pred - 3.0) < 1e-9 else ("  <- read as '4.3'" if abs(r["ratio"] - 4.3) < 0.1 else "")
        print(f"{r['N']:>3} {r['F_N']:>5} {r['v']:>5} | {r['ratio']:8.3f}  {pred:8.3f}  {e:6.2f}{flag}")
    print(f"{len(sel)} rows; worst relative error {max(errs):.2f}")
    print(termplot.plot_xy([(r['F_N'] / (4 * r['v']), r['ratio']) for r in sel] + [(x / 2, x / 2) for x in range(4, 30)],
                           width=50, height=12, title="observed period vs F_N/(4Jv) (diagonal = formula)", xlabel="F/(4Jv)", ylabel="period"))
    """),
    code("""
    mud = json.loads((ROOT / "scripts/experiments/p4_mud_results.json").read_text())["rows"]
    print("mu_d dependence at fixed (N, g, v, F_N) where the formula predicts 4.5 for every row:")
    for r in mud:
        print(f"   mu_d = {r['mu_d']}: period {r['ratio']}")
    """),
    md("## Falsifiers: c12 and c13 mutants must fail"),
    code("""
    for entry in ("c12_p4_loading_formula", "c13_p4_mud_dependence"):
        rc, _ = catalog(entry)
        assert rc == 0, entry
        rc, out = catalog(entry, mutant=True)
        mutant_must_fail(entry, rc, out)
    """),
    md("""
    The lesson both rows share (P-4 note, run 5): a plateau read off a grid is
    not a plateau until the null that would put it there has been derived and
    ruled out. That is the same discipline as LAW-11: a check without a failing
    mutant is a restatement.
    """),
]


def main() -> int:
    OUT.mkdir(exist_ok=True)
    for name, cells in NOTEBOOKS.items():
        path = OUT / f"{name}.ipynb"
        path.write_text(json.dumps(notebook(cells), indent=1, ensure_ascii=False) + "\n")
        print("wrote", path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
