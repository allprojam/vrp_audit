# <NAME> — result

Prereg `docs/HYPOTHESIS.md`, sha256 `<hash>`, frozen before results.
Verify: `python3 src/prereg.py verify docs/HYPOTHESIS.md`.
Code: `src/<module>.py`. Results: `runs/<name>.json`.

## VERDICT: <PASS | FAIL | PARTIAL> — <one line>

State the verdict against the gates **as written**.

## Results

| metric | arm A | arm B | gate |
|---|---|---|---|
| | | | |

## What I expected and what happened

If they differ, say so before explaining. An explanation written after seeing the number is a
rationalisation until proven otherwise — mark it as such.

## Provenance

Every figure above must appear in `PROVENANCE.md` and pass `python3 src/check_provenance.py`.

## Corrections to earlier claims

If this invalidates a previously published figure, say so here **and** add a banner to the old
report (A-21) **and** an entry to `DECISIONS.md`.
