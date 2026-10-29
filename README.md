# vrp_audit — can an individual harvest the BTC variance risk premium?

**Status: ✅ COMPLETE.** Prereg `e1cc0def` verified after the run.
**Verdict: C1 FAIL (estimator robustness) · C2 FAIL (all gates).**

## The result in four lines

| estimator | mean VRP (vol pts) | mean variance P&L | net at observed spread |
|---|---|---|---|
| CC (closes only) | +0.0549 | +0.1119 | **−1.2504** |
| PK (high/low) | +0.0156 | −0.0238 | −1.3861 |
| GK (full OHLC) | **+0.0029** | −0.0747 | −1.4370 |

**The premium falls 95% once realized vol is measured properly**, from +5.49 to +0.29 vol points.
That is the finding: the BTC variance risk premium is real in sign but mostly a measurement
artifact, and it is unreachable at retail spreads by ~10×.

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

## ⚠️ Addendum 01 — the cost gate had an ambiguity

The locked prereg swept cost in "bps of notional" without naming the denominator. Against
**variance** notional, 20 bp removes only **1.05%** of gross P&L — a gate that cannot fail.
Against **premium** notional it removes ~35× more. Resolved **before any result** without editing
the prereg (`e1cc0def` still verifies): C2 must clear the stricter premium basis.
See `docs/ADDENDUM_01.md`.

## ⚠️ Addendum 02 — G3 barely bites, and the spread is 19× the gate

Two more findings, both before any result:

- **G3 is close to non-binding.** Cumulative premium grows ~linearly while drawdown grows
  ~`sd·√n`, so a 50% ratio gets *easier* to pass as the sample grows. Monte Carlo (2,000 paths × 33
  periods): **0% fail** on a plausible premium, 22% only when the premium is thin.
- **The observed spread is 385 bp of premium = 19.2× the G4 gate.** ADDENDUM 01 compared it to the
  gate as "~22 bp of spot" — the right number against the wrong denominator. At the observed
  spread, round-trip cost is `~1.34` in variance-P&L units against gross premium `~0.19`.

**C2 should be expected to fail.** The locked sweep `{0,5,10,20,40}` explores only the region where
costs are 10–20× too low.

## Run it

```bash
python3 src/check_all.py      # 3/3 — prereg e1cc0def still verifies after the run
python3 src/vrp.py            # reproduces runs/vrp.json (offline, from data/*.csv)
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
