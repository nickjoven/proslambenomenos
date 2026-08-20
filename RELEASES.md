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
