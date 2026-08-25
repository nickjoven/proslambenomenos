"""The measured Bell-test history against the ladder's exact rungs: Aspect-Grangier-Roger 1982 measured S = 2.697 +/- 0.015, which is 46 standard deviations above the local ceiling S = 2 (exhaustive over all deterministic strategies) and 95.4% of the Tsirelson bound 2 sqrt 2; Freedman-Clauser 1972 measured delta = 0.050 +/- 0.008 against the local bound delta <= 0, a 6 sigma violation.
Source: Aspect, Grangier, Roger, PRL 49, 91 (1982); Freedman, Clauser, PRL 28, 938 (1972); litcheck LC-10, prediction P-17. Mutant: asserts the AGR value is statistically compatible with the local ceiling (within 3 sigma)."""
import itertools
import math
import sys

from _common import mutant_flag, finish

# the local ceiling, re-derived exhaustively (not assumed)
best = max(abs(a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1)
           for a0, a1, b0, b1 in itertools.product((-1, 1), repeat=4))
S_AGR, ERR_AGR = 2.697, 0.015
D_FC, ERR_FC = 0.050, 0.008
z_agr = (S_AGR - best) / ERR_AGR
z_fc = (D_FC - 0.0) / ERR_FC
frac_tsirelson = S_AGR / (2 * math.sqrt(2))
threshold = 3.0 if mutant_flag() else 40.0
ok = (best == 2 and (z_agr < threshold if mutant_flag() else z_agr > threshold)
      and z_fc > 6.0 and abs(frac_tsirelson - 0.954) < 2e-3)
sys.exit(finish(ok, f"local ceiling {best} (exhaustive); AGR z = {z_agr:.1f} sigma, "
                    f"{frac_tsirelson:.4f} of Tsirelson; FC z = {z_fc:.2f} sigma"))
