# proslambenomenos — canonical entry points.
# Gates are the law; plots are the companion; experiments are exploration.

PYTHON ?= python3

# ───────────────────────── Gates ─────────────────────────

# Run every gate (the eight-check suite). CI runs the same thing.
gates:
	$(PYTHON) scripts/run_all.py

# Message gate over the full governed range (what CI enforces on push).
gates-all:
	$(PYTHON) scripts/check_messages.py --all

# ───────────────────────── Plots ─────────────────────────

# All terminal-graphics demos, including a live render of the latest
# D4 sweep results if present. THEME=mono|blocks|dark|light
THEME ?= mono
plots:
	$(PYTHON) scripts/termplot_demo.py --theme $(THEME)

# ─────────────────────── Experiments ───────────────────────
# Exploration tier: NOT evidence until promoted to scripts/verify/
# behind a claim. Outputs are data for the notes.

# E1 baseline: twisted vs control temporal staircase (N=3 and N=4).
e1-staircase:
	$(PYTHON) scripts/experiments/d4_twisted_ring_staircase.py 3
	$(PYTHON) scripts/experiments/d4_twisted_ring_staircase.py 4

# E1 step 2: K x J sweep; writes scripts/experiments/d4_sweep_results.json
e1-sweep:
	$(PYTHON) scripts/experiments/d4_kj_sweep.py

.PHONY: gates gates-all plots e1-staircase e1-sweep

catalog:
	$(PYTHON) scripts/check_catalog.py
