"""A tread with n-fold rotational symmetry leaves a track whose period is the circumference over n - indistinguishable from a trivial tread on a wheel of radius r/n (the deck-group ambiguity of track -> rim).
Source: covering-space theory (the track is the development of the rim); frieze classification. Mutant: claim radius r/(2n)."""
import math, sys
from _common import mutant_flag, finish

r, n = 1.0, 3
tread = lambda a: math.cos(n * a) + 0.3 * math.sin(2 * n * a)      # rim pattern with C_n symmetry
circ = 2 * math.pi * r
track = [tread(x / r) for x in [circ * i / 3000 for i in range(3000)]]   # development onto the line
# period of the track by autocorrelation: first lag where the pattern repeats
def period(samples, dx):
    N = len(samples)
    for lag in range(1, N // 2):
        if max(abs(samples[(i + lag) % N] - samples[i]) for i in range(0, N, 7)) < 1e-9:
            return lag * dx
    return None
P = period(track, circ / 3000)
radius_inferred = P / (2 * math.pi)
claimed = r / (2 * n) if mutant_flag() else r / n
ok = P is not None and abs(radius_inferred - claimed) < 1e-6
sys.exit(finish(ok, f"track period {P:.6f} -> inferred trivial-tread radius {radius_inferred:.6f} (claimed {claimed:.6f})"))
