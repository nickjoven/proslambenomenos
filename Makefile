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

handoff:
	$(PYTHON) scripts/handoff.py --pack && $(PYTHON) scripts/recap_html.py

handoff-preview:
	$(PYTHON) scripts/handoff.py && cat HANDOFF.md

owner-commands:
	@grep -E "^\s+command: \"." OPEN.yml | sed -E "s/^\s+command: \"(.*)\"/\1/"

# ───────────────────────── Notebooks ─────────────────────────
# Curriculum notebooks (notebooks/*.ipynb, authored by scripts/nb_build.py):
# run every code cell with stdlib Python; exit nonzero on any exception.
notebooks:
	$(PYTHON) scripts/nb_run.py

# Rebuild the notebooks from their source and render notebooks/index.html.
notebooks-html:
	$(PYTHON) scripts/nb_build.py && $(PYTHON) scripts/nb_html.py

.PHONY: notebooks notebooks-html

wt:
	git worktree add ../wt-$(TASK) -b $(TASK) main && echo "../wt-$(TASK) on branch $(TASK)"

wt-done:
	git worktree remove ../wt-$(TASK) && git branch -d $(TASK)

spec:
	$(PYTHON) tests/run_spec.py

# ---- LLM-efficiency tooling (2026-08-30): replayable mechanics ----
# land: the whole landing pipeline, one digest. Run from a task
# worktree: make land TITLE="..." MSG=path/to/msgfile [BODY=file]
land:
	scripts/tools/land.sh "$(TITLE)" "$(MSG)" $(BODY)

# law-pin: append LAW-$(N) with the full covered-set hash pin;
# prose comes from WHY=file (first line = header suffix)
law-pin:
	$(PYTHON) scripts/tools/law_pin.py $(N) $(WHY)

# rentry: R-entry skeleton with numbers pasted from results JSON
# (R-18a rule). make rentry R=R-37 P=P-38 JSON=path
rentry:
	$(PYTHON) scripts/tools/rentry.py $(R) $(P) $(JSON)

# jstest: extract + syntax-check + stub-run a page's inline JS
jstest:
	scripts/tools/jstest.sh $(FILE)
