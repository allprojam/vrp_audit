# vrp_audit — can an individual harvest the BTC variance risk premium?

**Status: 🔒 PREREG LOCKED `e1cc0def…`, analysis NOT yet run.** Nothing here is a result.

## The question

Eleven passes in `gold_macro` showed public daily-bar **prediction** fails out-of-sample. The
variance risk premium is a different kind of claim: not a forecast, but a **payment for absorbing
risk** someone else wants transferred. It is the one accessible structural premium neither
`gold_macro` nor `aegis` measured. `aegis/vrp_test.py` was written on 2026-10-05 and never run.

## The split that decides everything

| claim | meaning | gates |
|---|---|---|
| **C1** | a premium exists: BTC 30d implied vol exceeds subsequently realized vol | G1 ∧ G2 ∧ G5 |
| **C2** | an individual can capture it after spread and tail | G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5 |

**C1 PASS with C2 FAIL is a successful, publishable result** — and the expected one.

## What is already known, before running anything

| finding | consequence |
|---|---|
| DVOL returns max **1000 daily points** | ~2.7 years. `n_eff ≈ 33`, barely above the floor of 30 |
| **No historical bid/ask archive** at Deribit | spread-capture backtesting is **impossible**, not merely unwise |
| Historical fills too sparse (4 trades/30d on a sampled strike) | cannot reconstruct spreads from trades either |
| Live chain median relative bid-ask **3.85%** | context only — but larger than any point in the cost sweep, so the spread may exceed the premium entirely |

That last row is a **prior, not a result.** The study exists to test it.

## Run it

```bash
python3 src/check_all.py      # verify the locked state (3/3 now)
python3 src/vrp.py            # NOT yet run — writes runs/vrp.json
```

Then write `docs/RESULT.md` from the template, report gates **as written**, and register every
figure in `PROVENANCE.md`.

## Files

```
docs/HYPOTHESIS.md   LOCKED prereg: claim, gates, kill conditions, anti-shopping
src/fetch.py         one-time Deribit pull -> data/*.csv
src/vrp.py           analysis; CSV only, no network
src/check_*.py       executable citation + namespace + hash guards
DECISIONS.md         V-01..V-05 for this study, plus the template's A-series
STATE.md             phase, feasibility findings, next steps
```

## The rule this repo inherits

**Prose interpolates across gaps; executables don't.** Every number quoted must resolve to a
`file:line` or JSON key, checked by script (`check_provenance.py`), and cross-repo decision IDs
carry a prefix. Both guards exist because they caught their authors.
