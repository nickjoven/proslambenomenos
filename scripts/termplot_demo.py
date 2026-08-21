"""Demos for termplot using domain data. Run: python3 scripts/termplot_demo.py"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import termplot
from termplot import plot_xy, staircase, heatmap, bars

import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("--theme", default=None, choices=["mono", "blocks", "dark", "light"],
                 help="termplot theme (default: TERMPLOT_THEME env or mono)")
_args, _ = _ap.parse_known_args()
if _args.theme:
    termplot.set_theme(_args.theme)

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "experiments", "d4_sweep_results.json")


def rotation_number(omega, K=1.0, n_iter=800, transient=200):
    """rho for the sine circle map  theta' = theta + Omega - (K/2pi) sin(2pi theta)."""
    two_pi = 2 * math.pi
    th = 0.0
    for _ in range(transient):
        th += omega - (K / two_pi) * math.sin(two_pi * th)
    th0 = th
    for _ in range(n_iter - transient):
        th += omega - (K / two_pi) * math.sin(two_pi * th)
    return (th - th0) / (n_iter - transient)


def demo_staircase():
    n = 200
    pts = [(i / (n - 1), rotation_number(i / (n - 1))) for i in range(n)]
    print(staircase(pts, title="Devil's staircase: rho(Omega), sine circle map K=1",
                    xlabel="Omega", ylabel="rho",
                    markers={"1/3": 1 / 3, "1/2": 1 / 2, "2/3": 2 / 3}))
    return pts


def demo_heatmap():
    # Synthetic mode-locking tongue widths: plateau width of p/q vs coupling K.
    Ks = [0.2, 0.4, 0.6, 0.8, 1.0]
    qs = [1, 2, 3, 4, 5, 6]
    grid = [[(K ** q) / q for q in qs] for K in Ks]
    print(heatmap(grid, row_labels=["K=%.1f" % K for K in Ks],
                  col_labels=["q=%d" % q for q in qs],
                  title="Synthetic tongue width ~ K^q / q"))


def demo_bars(pts):
    targets = [("0/1", 0.0), ("1/4", 0.25), ("1/3", 1 / 3), ("1/2", 0.5),
               ("2/3", 2 / 3), ("3/4", 0.75), ("1/1", 1.0)]
    d_omega = pts[1][0] - pts[0][0]
    labels, widths = [], []
    for lbl, r in targets:
        labels.append(lbl)
        widths.append(sum(d_omega for _, rho in pts if abs(rho - r) < 5e-4))
    print(bars(labels, widths, width=50,
               title="Measured plateau widths at K=1 (|rho - p/q| < 5e-4)"))


def demo_passage_time():
    # Saddle-node ghost passage time T = pi / sqrt(mu).
    pts = [(mu, math.pi / math.sqrt(mu))
           for mu in (0.001 + i * (0.5 - 0.001) / 199 for i in range(200))]
    print(plot_xy(pts, title="Saddle-node passage time  T = pi/sqrt(mu)",
                  xlabel="mu", ylabel="T"))


def demo_sweep_results():
    if not os.path.exists(RESULTS):
        return
    with open(RESULTS) as fh:
        data = json.load(fh)
    runs = data.get("runs", [])
    if not runs:
        return
    npts = data.get("omega_pts", 1)
    Ks = sorted({r["K"] for r in runs})
    Js = sorted({r["J"] for r in runs})
    by_kj = {(r["K"], r["J"]): r for r in runs}
    print("\n== D4 sweep (N=%s, %s Omega pts/run) ==" % (data.get("N"), npts))
    for kind in ("control", "twisted"):
        grid = [[sum(v for q, v in by_kj[(K, J)][kind].items()
                     if q not in ("0/1", "1/1")) / npts
                 for J in Js] for K in Ks]
        print(heatmap(grid, row_labels=["K=%g" % K for K in Ks],
                      col_labels=["J=%g" % J for J in Js],
                      title="%s: nontrivial locked fraction" % kind))
        print()
    mid = by_kj[(Ks[len(Ks) // 2], Js[len(Js) // 2])]
    qs = sorted((q for q in mid["control"]
                 if max(mid["control"].get(q, 0), mid["twisted"].get(q, 0)) >= 3),
                key=lambda s: int(s.split("/")[0]) / int(s.split("/")[1]))
    labels, vals = [], []
    for q in qs:
        labels += ["%s ctrl" % q, "%s twist" % q]
        vals += [mid["control"].get(q, 0), mid["twisted"].get(q, 0)]
    print(bars(labels, vals, width=50,
               title="Plateau points >= 3, K=%g J=%g (control vs twisted)"
                     % (mid["K"], mid["J"])))


def main():
    pts = demo_staircase()
    print()
    demo_heatmap()
    print()
    demo_bars(pts)
    print()
    demo_passage_time()
    demo_sweep_results()


if __name__ == "__main__":
    main()
