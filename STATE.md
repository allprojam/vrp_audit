# STATE — BTC variance risk premium audit

**Phase:** ✅ **PREREG LOCKED, analysis not yet run** · **Verdict: pending**

---

## Status

| | |
|---|---|
| Prereg | **LOCKED** `e1cc0def…` at 2026-10-29T20:51Z — `python3 src/prereg.py verify docs/HYPOTHESIS.md` |
| Data | fetched & committed: 1000 DVOL days (2024-02-03→2026-10-29), 1101 perp days |
| Analysis | `src/vrp.py` written, **deliberately not executed** |
| Result | `runs/vrp.json` — does not exist yet |
| Open blockers | none to running it |

## The question, and why it is the right one

Eleven passes in `gold_macro` showed public daily-bar **prediction** fails. The VRP is not a
prediction — it is a payment for absorbing risk. It sits at the "insurance counter," and it is the
one accessible structural premium neither repository has measured.
`aegis/vrp_test.py` was written 2026-10-05 and never run. This replaces it.

## Feasibility findings (verified, before locking)

| finding | consequence |
|---|---|
| DVOL returns **max 1000 daily points** regardless of requested span | ~2.7 y history. `n_eff ≈ 33`. Thin, but above the prereg's `n_eff >= 30` floor |
| **No historical bid/ask archive** exists | spread-capture backtesting is **impossible**. Market-making claims are out of scope by construction |
| Options chain is current-only; 938 of 1004 quotable | usable for context, not for a time series |
| Historical per-instrument fills are sparse (4 trades / 30 d on a sampled far strike) | cannot estimate historical spreads from fills either |

**For context only, not a cost input:** median relative bid-ask on the live chain is **3.85%**
(p25 2.09%, p75 10.00%). The prereg forbids asserting retail fees, so cost is a sweep
`c ∈ {0,5,10,20,40}` bps. This number is here to warn that 3.85% is far larger than any point in
that sweep — the spread may dominate the premium entirely. That is a **prior**, not a result.

## Pre-registered decision rule (fixed before results)

- **C1** (premium exists) needs G1 ∧ G2 ∧ G5.
- **C2** (harvestable at retail) needs G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5.
- **C1 PASS with C2 FAIL is a successful study**, and the expected outcome.

## Kill conditions

See `docs/HYPOTHESIS.md` §Kill conditions — five of them, including "if I find myself explaining
why a negative number is really positive, stop and re-run the accounting."

## Next steps

1. `python3 src/vrp.py` → `runs/vrp.json`.
2. Write `docs/RESULT.md` from `docs/RESULT_TEMPLATE.md`. Report gates **as written** (I-7).
3. Register every quoted figure in `PROVENANCE.md`; `python3 src/check_all.py` must pass.

## Do not do

- Do not add a fourth vol estimator after seeing results.
- Do not report the CC estimator alone — it is the one that flatters a vol seller.
- Do not convert this into a market-making claim. The data cannot support one.

## Verify the board

```bash
python3 src/check_all.py
```
