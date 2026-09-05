#!/usr/bin/env python3
"""a35_untwisted.py - the untwisted control for A-35 at its own fold
(fold_fc(N, 0) + 0.005; at the twisted fold's load the untwisted ring
does not slip within t_cap). Same runner and readout as
a35_odd_control.py. Writes a35_untwisted.json / .txt."""
import json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from p35_ring import fold_fc  # noqa: E402
from a35_odd_control import run, analyse, N  # noqa: E402
def main():
    dt = 0.001; f = fold_fc(N, 0.0) + 0.005; t0 = time.time(); lines = []
    def log(s):
        print(s, flush=True); lines.append(s)
    res = {"N": N, "f": f, "dt": dt, "cells": {}}
    for g in (0.5, 0.35):
        t1 = time.time(); rec = run(g, f, dt, 380.0, False, 0)
        if rec["event_t"] is None:
            log("gamma %g untwisted: no slip" % g); continue
        log("gamma %g untwisted   event %.1f (%.0f s)" % (g, rec["event_t"], time.time() - t1))
        res["cells"]["gamma_%g_untwisted" % g] = analyse(rec, g, dt, log)
    res["seconds_total"] = time.time() - t0; log("total %.0f s" % res["seconds_total"])
    json.dump(res, open(os.path.join(HERE, "a35_untwisted.json"), "w"), indent=1)
    open(os.path.join(HERE, "a35_untwisted.txt"), "w").write("\n".join(lines) + "\n")
if __name__ == "__main__":
    main()
