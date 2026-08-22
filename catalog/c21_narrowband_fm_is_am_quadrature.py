"""Narrowband FM (beta << 1) has the same carrier and sideband amplitudes as AM of depth m = beta, differing only in the sign of the lower sideband: AM's pair is symmetric (resultant in phase with the carrier), FM's is antisymmetric (resultant in quadrature).
Source: Armstrong 1936; Carlson, Communication Systems ch. 5: cos(wc t + beta sin wm t) ~ cos wc t + (beta/2)[cos(wc+wm)t - cos(wc-wm)t]. Checked by DFT. Mutant: claim FM's lower sideband has the same sign as its upper."""
import cmath, math, sys
from _common import mutant_flag, finish

N, fc, fm, beta = 4096, 64, 4, 0.05
m = beta       # AM depth matching the first-order FM sideband amplitude (J1(beta) ~ beta/2 = m/2)
def dft(x, k):
    return sum(x[n] * cmath.exp(-2j * math.pi * k * n / N) for n in range(N)) / N
fmsig = [math.cos(2 * math.pi * fc * n / N + beta * math.sin(2 * math.pi * fm * n / N)) for n in range(N)]
amsig = [(1 + m * math.cos(2 * math.pi * fm * n / N)) * math.cos(2 * math.pi * fc * n / N) for n in range(N)]
def sidebands(sig):
    C, U, Lo = dft(sig, fc), dft(sig, fc + fm), dft(sig, fc - fm)
    return abs(U) / abs(C), cmath.phase(Lo / U)     # amplitude ratio; lower-vs-upper relative phase
ratio_fm, rel_fm = sidebands(fmsig)
ratio_am, rel_am = sidebands(amsig)
amp_match = abs(ratio_fm - ratio_am) / ratio_am < 0.02          # same sideband/carrier amplitude ratio
am_symmetric = abs(rel_am) < 0.05                                 # AM: lower in phase with upper
fm_antisym = abs(abs(rel_fm) - math.pi) < 0.05                    # FM: lower anti-phase to upper
claim_fm = (abs(rel_fm) < 0.05) if mutant_flag() else fm_antisym
ok = amp_match and am_symmetric and claim_fm
sys.exit(finish(ok, f"sideband/carrier: FM {ratio_fm:.4f} vs AM {ratio_am:.4f}; lower-vs-upper phase FM {math.degrees(rel_fm):+.0f} deg, AM {math.degrees(rel_am):+.0f} deg"))
