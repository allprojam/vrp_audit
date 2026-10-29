# HYPOTHESIS — BTC variance risk premium: existence vs. harvestability

> Locked before any VRP statistic was computed. The author has not run `vrp` on this data.
> Feasibility (endpoint reachability, row counts, coverage) was checked; the answer was not.

## Claim

**Two separate claims, and they must not be conflated:**

- **C1 (existence).** BTC 30-day implied volatility exceeds subsequently realized volatility on
  average, over 2024-02 → 2026-10.
- **C2 (harvestability).** The premium in C1 is capturable by an individual trading Deribit
  options at retail, after crossing the spread and bearing the tail.

**C1 is expected to be true and is the easy half.** C2 is the hypothesis that matters and the one
this study is built to reject. A positive C1 with a failed C2 is a **successful** study.

## Why this question and not another

Eleven passes of `gold_macro` established that public daily-bar *prediction* fails. The variance
risk premium is not a prediction — it is a structural payment for absorbing risk someone else
wants transferred. It therefore sits at the "insurance counter," not the "casino counter," and is
the one accessible structural premium not yet measured in either repository.
`aegis/vrp_test.py` was written on 2026-10-05 and never run; this prereg replaces it.

## Data — verified reachable from this host

| series | source | endpoint | coverage | status |
|---|---|---|---|---|
| BTC implied vol (DVOL) | Deribit public | `get_volatility_index_data` | **1000 daily points max**, 2024-02-03 → 2026-10-29 | VERIFIED |
| BTC perpetual price | Deribit public | `get_tradingview_chart_data` | 1D bars, same span | VERIFIED |
| Options chain snapshot | Deribit public | `get_book_summary_by_currency` | 1004 instruments, 937 with both bid+ask | VERIFIED, **snapshot only** |

### The data limitation that constrains the whole study — state it plainly

- **DVOL is capped at 1000 points (~2.7 years).** This is the entire available history.
- **There is no historical bid/ask archive.** Historical *fills* exist for some instruments but are
  too sparse to estimate spreads: one sampled strike had **4 trades in 30 days**. Far strikes are
  effectively unfilled.
- Consequence: **a spread-capture backtest is not possible with free data.** Any claim about
  market making is therefore out of scope by construction, not by choice.

## Method

1. **Realized vol, three estimators.** For each day `t`, realized vol over `[t, t+30]`,
   annualised. Report all three, and treat close-to-close as the *least* trustworthy:
   - **CC** — close-to-close (`std(log ret)`)
   - **PK** — Parkinson (high–low range)
   - **GK** — Garman–Klass (OHLC)

   **Pre-committed:** CC systematically *understates* the variance a seller is short (no intraday
   extremes, no gap risk) and therefore makes the VRP look fattest. PK/GK are the honest ones.
   Reporting only CC is a fail (`gold_macro:A-08`, convenient-constant trap).

2. **VRP** = `IV(t) − RV(t→t+30)`, computed for each estimator.

3. **Effective sample size.** 30-day windows sampled daily overlap by 29/30. Nominal `n ≈ 999`
   is a fiction. **Pre-committed:** report `n_eff ≈ n/30` (non-overlapping) alongside nominal `n`.
   Any conclusion that holds only on nominal `n` is rejected.

4. **Short-vol P&L in variance terms.** Position sized so the seller receives `IV²` variance notional
   and pays `RV²` realized. Period P&L per unit notional = `(IV² − RV²) / IV²`. This is a
   *unit-free* quantity; it does not assume a contract size, a delta-hedge, or a fee level.

5. **Cost scenarios, not a cost estimate.** Retail option fees are not verified here and will not be
   asserted. The study sweeps entry+exit cost as `c ∈ {0, 5, 10, 20, 40} bps of notional per round
   trip`. **Pre-committed:** C2 may only be called PASS if it survives `c = 20` bps. Surviving only
   `c ∈ {0, 5}` is a FAIL, and must be reported as such.

## Gates — as written

| gate | condition | reads on |
|---|---|---|
| **G1** existence | `mean(IV − RV_PK) > 0` **and** `IV > RV_PK` in ≥50% of periods | C1 |
| **G2** not just CC | G1 also holds for **GK**. If it holds for CC but not PK/GK, C1 is **FAIL** | C1, estimator robustness |
| **G3** survivability | worst single period does not draw down more than **50%** of cumulative premium to that point | C2 |
| **G4** cost survival | G1 positive net of `c` for **all** `c` up to **20 bps** | C2 |
| **G5** effective n | all of the above hold on **non-overlapping** windows (`n_eff ≈ n/30`) | both |

**The decision rule, fixed in advance:**
- **C2 PASS** requires G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5.
- **C1 PASS** requires G1 ∧ G2 ∧ G5.
- **C1 PASS with C2 FAIL is a successful, publishable negative result** and the expected outcome.

## Kill conditions — what makes me abandon this

1. If PK/GK show no premium while CC does, the "premium" is an artefact of estimator choice. Abandon.
2. If G3 fails — a single period wipes half the cumulative premium — the tail dominates. Abandon
   for a retail book regardless of average.
3. If the result survives only at `c = 0`, the premium is smaller than the spread. Abandon.
4. If `n_eff < 30`, the sample cannot support any conclusion. Abandon and say so.
5. **If I find myself explaining why a negative number is really positive, stop and re-run the
   accounting** (`gold_macro:the rationalisation trap`).

## Anti-shopping commitments

- **One** configuration. No strike selection, no timing overlay, no vol-targeting the seller.
- No parameter is tuned. The three estimators are fixed above; no fourth will be added post hoc.
- Cost is a sweep, not a fitted parameter.
- Seed: N/A (deterministic). If resampling is added, seed = 0 and it is reported as an addendum.
- If additional variants are tried, they are a **separately locked second pass**, labelled as such.

## What would prove this wrong

C2 PASS: premium surviving 20 bps and the tail on non-overlapping windows. I expect this to fail,
which is exactly why it needs a prereg rather than a hunch.
