#!/usr/bin/env python3
"""P-36 derive addendum: what P-35's first cells exposed, derived.

P-35's registered onset detector was the NET covariant winding W.
The first registered cells showed twisted onsets one grid step
below the fold - and no control onset at any grid level, while the
raw strain at the contact diverged. The diagnosis is derivable and
lives here (run before P-36's registration):

  EQ8  control fold closed form: the binding constraint of the
       control profile sin(s_j) = c + m f/N is the CONTACT PAIR -
       by symmetry c = -f(N-1)/(2N), and the fold is where the two
       bonds at the loaded node saturate TOGETHER at -+1:
       f(N-1)/N = 2, i.e. fold(control) = 2N/(N-1) exactly
       (solver agrees to 2e-6 = bisection floor). The
       supercritical motion is a symmetric PAIRED slip: +2 pi
       through one contact bond, -2 pi through the other, net
       W unchanged - the loaded node tears out and spins at
       ~ f/gamma. A net-W detector is blind to this channel BY
       SYMMETRY. Observed in the P-35 cells: raw strain 4.7e4
       while W held 0.000 at every sample.
  EQ9  twisted fold channel: the loop constraint sum s_j = +-pi
       forces the profile off-center, so the TOP bond saturates
       alone (top sin = 1.000000, bottom -0.933 / -0.956 / -0.967
       at N = 64 / 96 / 128): an asymmetric single slip that
       changes W by +-1. THE HOLONOMY SELECTS THE SLIP CHANNEL:
       paired and W-neutral without the pi bond, net and
       W-changing with it - P-4's "orbits close on the base vs
       the double cover", reborn as a derived, registerable
       observable.
  EQ10 the channel-blind detector replaced: a BOND-slip detector
       e_j(t) = raw covariant strain minus its initial value;
       event when max_j |e_j| > 1.5 pi. Pre-fold bound: on the
       quasi-static branch every |s_j| < pi/2, so |e_j| < pi;
       the extra pi/2 is inertial-ringing margin (stated, not
       derived sharply; the event amplitude is 2 pi, so the
       window [pi, 2 pi) has slack on both sides). This detector
       reaches both channels.
  EQ11 P-35 clause (e) diagnosed: the spectral address is a
       SECTOR observable of the unloaded ring only. Under load
       the phase profile accumulates O(N) radians of excursion
       and the DFT peak leaves the sector address long before
       onset (quantified below at half-load). The address is
       demoted to the derive layer's unloaded statement (EQ5);
       it is not registered under load in P-36.

Run: python3 scripts/experiments/p36_channel.py
"""
import json
import math
import os

TAU = 2 * math.pi


def fold_fc(N, total):
    def sum_s(c, f):
        s = 0.0
        for m in range(N):
            x = c + m * f / N
            if x <= -1.0 or x >= 1.0:
                return None
            s += math.asin(x)
        return s

    def has_root(f):
        lo, hi = -0.999999, 1.0 - (N - 1) * f / N - 1e-12
        if hi <= lo:
            return False
        slo, shi = sum_s(lo, f), sum_s(hi, f)
        if slo is None or shi is None:
            return False
        return (slo - total) * (shi - total) <= 0

    lo, hi = 0.0, 4.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if has_root(mid):
            lo = mid
        else:
            hi = mid
    return lo


def profile_c(N, total, f):
    lo, hi = -0.999999, 1.0 - (N - 1) * f / N - 1e-9

    def S(c):
        return sum(math.asin(c + m * f / N) for m in range(N))

    slo = S(lo)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if (S(mid) - total) * (slo - total) <= 0:
            hi = mid
        else:
            lo, slo = mid, S(lo)
    return 0.5 * (lo + hi)


def main():
    out = {"EQ8": {}, "EQ9": {}, "EQ11": {}}
    for N in (64, 96, 128):
        fc = fold_fc(N, 0.0)
        closed = 2.0 * N / (N - 1)
        ft = fold_fc(N, math.pi)
        c = profile_c(N, math.pi, ft)
        out["EQ8"][str(N)] = {"fold_solver": fc, "closed_2N_N1": closed,
                              "diff": abs(fc - closed)}
        out["EQ9"][str(N)] = {"fold_twisted": ft,
                              "top_sin": c + (N - 1) * ft / N,
                              "bottom_sin": c,
                              "ratio": ft / closed}
    # EQ11: DFT address of the loaded control profile at half-fold
    N = 64
    f = 0.5 * fold_fc(N, 0.0)
    c = profile_c(N, 0.0, f)
    s = [math.asin(c + m * f / N) for m in range(N)]
    th, acc = [], 0.0
    for j in range(N):
        th.append(acc)
        acc += s[j]
    best, bidx = -1.0, None
    for kk in [x / 8.0 for x in range(-16, 17)]:
        re = sum(math.cos(th[j] - TAU * kk * j / N) for j in range(N))
        im = sum(math.sin(th[j] - TAU * kk * j / N) for j in range(N))
        a = math.hypot(re, im)
        if a > best:
            best, bidx = a, kk
    excurs = max(th) - min(th)
    out["EQ11"] = {"half_load_dft_peak": bidx,
                   "sector_address": 0.0,
                   "phase_excursion_rad": excurs}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "p36_channel.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
