# ADDENDUM 04 — Oct 29 2026 Binance-hack event snapshot (EXPLORATORY)

**Status: NOT pre-registered. Exploratory only. 0.85 ceiling applies.**

An event snapshot was requested. **The measurement was observed before any lock could be written**,
so a "pre-registered Oct 29 test" is not available and must not be claimed. What is available is a
transparent snapshot, clearly labelled, that anyone can re-run.

`runs/vrp.json` and the `e1cc0def` prereg are **untouched**. `runs/oct29_event.json` is separate.
Script: `src/event_oct29.py`.

---

## Two defects found while preparing this

### (a) Every committed Oct 29 bar is a stale, partial candle
`data/*.csv` were fetched at **20:50 UTC**. Deribit daily bars close at **00:00 UTC** (verified from
the data — not 08:00 UTC as one draft assumed). The committed Oct 29 row was therefore taken
**3h10m before its close** and has since moved materially:

| | committed 20:50 UTC | live 22:48 UTC |
|---|---|---|
| DVOL close | 37.94 | **41.83** |
| perp close | 79,208 | **78,805** |
| perp high | 81,922 | 81,922 |

**The frozen `runs/vrp.json` is unaffected** — the last IV observation is `2026-09-30` and the last
RV window ends `2026-10-28`, so no partial Oct 29 bar enters the result. Verified, not assumed.
**But the `data/*.csv` files contain a bar that is now known-wrong, and `src/fetch.py` has no
closed-bar guarantee.** Logged as `V-19`: a fetch must reject a bar whose close time is in the future.

### (b) CoinGecko's "−2.75% 24h" is a *rolling* window, not the UTC daily candle
BTC went **79,769 → 78,805 on the UTC candle (−1.21%)** but CoinGecko reported **−2.75%** over a
rolling 24h. Both correct, different denominators. Comparing a rolling-window return to a
UTC-candle realized vol is exactly the **V-10** error. This addendum uses the UTC candle only.

---

## Measured snapshot — Oct 29 2026, as-of 22:48 UTC, bar still open

```
O 79,769   H 81,922   L 78,199   C 78,805
DVOL  37.26 -> 41.83   (+12.3%)
```

| estimator | single-day, annualised `√365` (V-08) |
|---|---|
| **CC** (close-to-close) | **23.2%** |
| **PK** (high/low) | **53.4%** |
| **GK** (full OHLC) | **61.2%** |
| **DVOL** (implied) | **41.8%** |

- Intraday range **4.76%**, UTC daily move **−1.21%**.
- **GK / CC = 2.63×** — the estimator gap, visible inside a single day.
- **RV > IV on PK and GK. RV < IV on CC.**

## The pre-run prediction was wrong, and it was wrong in a pre-specifiable way

The prediction going in was: *$5.7B headline with only −2.75% spot ⇒ IV rises, RV stays low ⇒
`RV > IV` FAILS.*

**Two errors in that reasoning, both now measured:**

1. **Wrong denominator.** The UTC candle was **−1.21%**, not −2.75%. The −2.75% is a rolling window.
2. **It never checked the range.** `RV` measured with OHLC (**61.2%**) *exceeded* IV (**41.8%**) even
   though the close moved only −1.21%, because the intraday range was **4.76%**. The wick did the
   damage while the close did not.

**This is `G2` reproducing live.** A close-to-close view (23.2%) says "quiet day, IV is rich, sell
vol." The honest view (61.2%) says the day realized **1.5× implied**. Same day, opposite trades.

## What this does and does not establish

**Does:** show that on the hack day, IV rose ~12% while PK/GK realized vol exceeded it — i.e. a
short-vol seller was hurt both ways, on the day, by the honest estimator.

**Does not:** validate `V-13`. Single-day `RV > IV` is **necessary but not sufficient** for negative
30-day variance P&L, and ADDENDUM_03 already showed the dominant term there is not Jensen. Nor does
it validate C1/C2 in either direction — one day is not a test of a strategy.

**Cannot:** be called pre-registered. It isn't. Anyone quoting this as a locked result is
misrepresenting it, and that includes me if I ever summarise it that way.
