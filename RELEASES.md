# The link protocol

A "link" is a completed step preserved so a future step can cite it
immutably and re-verify it independently. Chain = the sequence of
links. Two properties per link, in order of importance:

1. **Re-verifiable**: the link's gates re-run from its tree alone
   (`python3 scripts/run_all.py`; compendium checks headlessly; the
   `scripts/verify/` recipes). A link that can only be trusted is
   weaker than a link that can be re-checked.
2. **Immutable + attributable**: content-addressed by git's Merkle
   DAG (every commit hash commits to the full history), carried by an
   annotated tag whose message embeds the claim census, gate results,
   and SHA-256 digests of the evaluation documents — so the tag is
   self-contained evidence even outside this working copy.

## Making a link

    python3 scripts/run_all.py                  # must be worst rc 0
    git tag -a link-NNN -F <message-file>       # -s once signing is on
    # message contains: date, claim census, gate outputs,
    # sha256 of notes/*.md claims/*.yml compendium/index.html,
    # artifact URL, and the session provenance line

Every commit already carries a Claude-Session trailer — generation
provenance chains to the session transcript independently of this
protocol.

## Trust ladder (each rung optional, cumulative)

| Rung | Mechanism | What it adds | Status |
|---|---|---|---|
| 0 | git Merkle DAG | content-addressing, history binding | working now |
| 1 | annotated tag with embedded digests + census | self-contained link evidence | working now (link-001) |
| 2 | SSH-signed tags | cryptographic attribution (owner's key) | one command: `git config gpg.format ssh && git config user.signingkey ~/.ssh/id_ed25519.pub`, then `-s` |
| 3 | remote replication (GitHub) | survives disk loss; third-party receive timestamps | needs remote + owner push decision |
| 4 | OpenTimestamps on tag hashes | existence-by-date anchored in Bitcoin, offline-verifiable | needs ots client (no pip on this box) |
| 5 | Software Heritage save | SWHID persistent identifiers, citable content-address, independent archive | needs public repo; one POST |
| 6 | Zenodo DOI per milestone | scholarly citable, CERN-backed archive | owner account; outward-facing |

Deliberately not used: ket sealing for this repo — decoupling recorded
in README; git already provides the content-addressed chain here, and
a bare mirror on a second disk beats a second CAS for redundancy.
The published artifact (claude.ai) is presentation, not preservation.

## Chain so far

- link-001 — extraction complete: 20 gated claims, 18-section
  compendium, topology + modular/Koide evaluations. (2026-08-19)
- link-002 — pre-publication: context-free adversarial audit in the
  record with F1-F10 dispositions; LAW-3/4/5; seven gates; 21 claims.
  (2026-08-20)
- link-003 — P-1 opened: preregistration law (LAW-6/7/8, eighth gate),
  decomposition with discharged checkables, the gradient theorem-let
  (claim 22), E1 steps 1-2 with the odd/2N retraction on record, the
  termplot companion with themes, and the repo Makefile. (2026-08-21)
- link-004 — P-1 resolved: R-1 (headline met, mechanism corrected to
  domain vacuity), claims 23-24 (mean-frequency identity, bridge
  vacuity), E1 step 3 shrink-not-shift, D4 proper cross-tab and holes
  (a)/(b), litcheck LC-3 with classical labels and the unreconciled
  Josephson sign, X-7/X-8, P-4 preregistered, LAW-9. (2026-08-21)
- link-005 — scrutiny and mechanism: twisted-sector-complex-structure
  refuted (J^2 follows x-parity, not the bundle) and replaced; LAW-11
  null_system + falsifier rule with the four-claim sweep; Proof Chain A
  (Kuramoto -> Einstein) refuted as a first-class claim with a
  three-check script (LAW-12); P-4 runs 1-5 (Helmholtz regime reached
  in the control, gate region identified, no doubling yet); X-9..X-12;
  LC-4..LC-6; P-5. (2026-08-22)
- link-006 — overnight adversarial audits: five context-free agents on
  every open thread. P-3 resolved (R-2, Borel counterexample, classical
  classification as replacement); P-4 resolved as model-class vacuity
  (R-3: the clamp cut the loop); Proof Chain A refutation evidence
  corrected (sign, lapse, Lyapunov); LAW-14..17 (P-3 script; corrected
  refutation; six gate bypasses closed; compendium under the falsifier
  rule with 22 mutants); catalog 16 entries one mutant each. 28 claims.
  (2026-08-22)
- link-007 — executable everywhere: P-6 (R-4, circulant sync bound
  reproduced with an exhaustive n <= 20 certificate), P-8 (R-5, finite-T
  plateau exponent ~2), P-9 (R-6, no N-parity; E1 initial condition not
  N-safe); catalog c17-c30 (Gauss-Bonnet on polyhedra through the impact
  oscillator's grazing law); curriculum notebooks T0-T6 + capstone as
  the tenth gate (LAW-18); VOCABULARY.md earned in full (Toda solitons,
  c29); spec suite in a controlled grammar (55 rules, TDD red -> green)
  and the notes gate (LAW-20) - eleven gates; multi-actor worktree
  infrastructure (AGENTS.md); LC-8; LAW-14..20. 29 claims. (2026-08-23)
- link-008 — nulls before numbers: the derive-layer era. P-10..P-37
  registered and resolved (R-7..R-36; P-2 and P-5 finally closed;
  P-4 reopened per R-3's own recipe and answered as P-35/P-36 - the
  holonomy prices in at its derived O(1/N) strain budget and selects
  the slip channel). The instrument arc: AGENTS item 8 (detector
  nulls, conservation identities, domain validity as derive-layer
  obligations) with the R-32 corollary extended through power
  calculations (R-36); frustration classes; the horizon census
  pricing coincidences in net bits; the memory hierarchy and the
  price of a bit; the critical staircase reproduced by our own
  tongue instrument. Claims 29 -> 54 (26 verified, 17 proven, 6
  refuted honest); LAW-21..44 (covered set 63 files); LC-9..27;
  kernels/ extracted; the Pages site (plane, inviolables graph with
  21 running checks, gates board, walk, runway) and the
  fresh-context corpus audit that reproduced spot-checked numbers
  with independent code. Tooling: make land / law-pin / rentry /
  jstest. 54 claims. (2026-08-30)
