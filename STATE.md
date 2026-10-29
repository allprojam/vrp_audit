# STATE — BTC variance risk premium audit

**Phase:** ✅ **RUN COMPLETE** · **Verdict: C1 FAIL (G2 estimator robustness) · C2 FAIL (all gates)**

> ⚠️ **ADDENDUM 01 exists and is binding.** The locked cost gate G4 said "bps of notional"
> without naming a denominator. Under *variance* notional, `c=20bp` eats **1.05%** of gross P&L and
> the gate cannot fail — which inverts its purpose. Resolved **before results**, without editing the
> prereg: C2 must clear the **premium-notional** basis, which is **34.9× harsher** at 20 bp.
> See `docs/ADDENDUM_01.md`, `V-06`, `V-07`.
>
> ⚠️ **ADDENDUM 02 also exists and is binding.** Two further pre-run findings: (a) **G3 is nearly
> non-binding** (Monte Carlo fail rate **0%** on a plausible premium) — retained as written, with a
> stricter diagnostic reported beside it; (b) ADDENDUM 01's prose compared **22 bp of spot** to
> **20 bp of premium** — the correct comparison is **385 bp of premium = 19.2x the gate**, at which
> round-trip cost in variance-P&L units is **~1.34** against gross premium **~0.19**.
> **Expect C2 to fail.** See `docs/ADDENDUM_02.md`, `V-10`–`V-12`.

---

## Status

| | |
|---|---|
| Prereg | **LOCKED** `e1cc0def…` at 2026-10-29T20:51Z — `python3 src/prereg.py verify docs/HYPOTHESIS.md` |
| Data | fetched & committed: 1000 DVOL days (2024-02-03→2026-10-29), 1101 perp days |
| Analysis | **executed 2026-10-29**, `runs/vrp.json` written |
| Result | **C1 FAIL · C2 FAIL** — see `docs/RESULT.md` |
| Addenda | **04** Oct 29 event snapshot, EXPLORATORY (V-19..V-22) · **03** post-run decomposition (V-16..V-18) · **01** G4 cost denominator · **02** G3 tail threshold + spot/premium conversion (both binding, pre-results) |
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

## Findings (executed)

| est | mean VRP (vol pts) | IV>RV | mean variance P&L | net at observed spread |
|---|---|---|---|---|
| CC | +0.0549 | 70.6% | +0.1119 | −1.2504 |
| PK | +0.0156 | 65.6% | −0.0238 | −1.3861 |
| GK | +0.0029 | 62.8% | −0.0747 | −1.4370 |

**The premium collapses 95% from CC to GK** — it is largely an artifact of under-measuring realized
vol. **C1 fails G2. C2 fails everything, by ~10x, not at the margin.**

## Next steps

1. ~~Run `src/vrp.py`~~ — done.
2. ~~Write `docs/RESULT.md`~~ — done.
3. ~~Register figures in `PROVENANCE.md`~~ — done, 34/34 (5 more added by ADDENDUM_03).
4. **This study is closed.** No further passes on this dataset.

## Do not do

- Do not add a fourth vol estimator after seeing results.
- Do not report the CC estimator alone — it is the one that flatters a vol seller.
- Do not convert this into a market-making claim. The data cannot support one.

## Verify the board

```bash
python3 src/check_all.py
```

## Oct 29 2026 Binance hack — event snapshot (exploratory)

**Not pre-registered.** Measured before any lock could be written, so it carries the 0.85 ceiling.
`runs/oct29_event.json` · `docs/ADDENDUM_04.md` · `src/event_oct29.py`. `runs/vrp.json` untouched.

| | |
|---|---|
| UTC candle | O 79,769 · H 81,922 · L 78,199 · C 78,805 |
| DVOL | 37.26 → **41.83 (+12.3%)** |
| single-day RV (√365) | CC **23.2%** · PK **53.4%** · GK **61.2%** |
| RV > IV? | CC ✗ · **PK ✓** · **GK ✓** |

**GK/CC = 2.63×** — `G2` reproducing inside a single day. The close moved −1.21% while the range was
4.76%; a CC view says "quiet day, sell vol," the honest view says the day realized 1.5× implied.

Two defects found while preparing it: **V-19** (committed Oct 29 bar was fetched 3h10m before close
and is stale — `fetch.py` now drops open bars) and **V-22** (CoinGecko's "−2.75%" is a *rolling*
window; the UTC candle was **−1.21%**).
