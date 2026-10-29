# ADDENDUM 02 — G3's drawdown threshold, and a denominator error in ADDENDUM 01's prose

**Written:** 2026-10-29T21:2xZ · **Before any VRP statistic was computed.** `runs/vrp.json` does not
exist. `docs/HYPOTHESIS.md` remains untouched (`e1cc0def…` verifies). I-6 mechanism.

---

## 1. G3 is close to non-binding — the same defect as G4, one gate over

`HYPOTHESIS.md` G3: *worst single period does not draw down more than 50% of cumulative premium to
that point.*

Cumulative premium grows roughly linearly while its max drawdown grows like `sd * sqrt(n)`. With
`n_eff ≈ 33`, the ratio `mdd / cum` therefore **shrinks as the sample grows** — so the 50%
threshold is easiest to trip early and nearly impossible to trip over the full sample. A Monte
Carlo of 2,000 paths × 33 periods puts the pass rate at:

| scenario | G3 fails |
|---|---|
| plausible IV−RV gap (mean 0.19, sd 0.15 per period) | **0%** |
| thin premium (mean 0.05, sd 0.15) | 22% |
| fat tails (mean 0.19, sd 0.30) | 1% |

**A 50% ratio is not a tail test.** It is a test that only bites if the premium is thin, and then it
bites for the right reason. But the gate was described in the prereg as protecting against tail
risk, and it does not do that. This is **V-07 again**: a threshold chosen without checking its
bite on a plausible value.

### Binding clarification (fixed before results)

1. **G3 is retained exactly as written** for the C2 verdict — the prereg does not move.
2. **A stricter tail diagnostic is added and reported alongside it**, not as a substitute:
   - worst 30-day period P&L,
   - worst peak-to-trough of the cumulative premium path in *units of mean period premium*
     (`mdd / mean_pnl` — how many periods of average premium the worst stretch gave back),
   - fraction of periods where `RV > IV` (the seller loses).
3. **If G3 passes but the stricter diagnostic shows `mdd / mean_pnl > 12`** (i.e. the worst stretch
   gave back more than ~12 periods' worth of average premium), `RESULT.md` must say plainly that
   C2 rests on a favourable sample and that the tail was not adequately tested by G3.

## 2. Correction to ADDENDUM 01's prose: the observed spread is 19.2× over the gate, not "just above"

ADDENDUM 01 compared the live chain's median relative bid-ask (**3.85% = 385 bp of premium**) to
G4's `c = 20` and then, in the same sentence, expressed the spread as **~22 bp of spot**. That
invites a unit confusion I should have caught: **22 bp of *spot* and 20 bp of *premium* are not
comparable numbers.**

Correctly stated:

- G4's gate is **20 bp of premium notional**.
- The observed spread is **385 bp of premium notional**.
- Therefore the observed spread is **19.2× the gate**, not marginally outside the sweep.

The "~22 bp of spot" figure is right and stays, but only as a conversion:
`3.85% × premium(5.73% of spot) ≈ 22 bp of spot`.

**Consequence, stated before results.** At the observed spread the round-trip cost in
variance-P&L units is about `2 × 0.0385 / 0.0573 = 1.34`, against gross premium of about `0.19`.
Net is deeply negative. **C2 will fail at the observed spread**, and the prereg's sweep
`{0,5,10,20,40}` bp only explores the region where costs are 10–20× too low.

This does not change the verdict procedure — G4 is evaluated on the sweep as locked, and the sweep
result is reported as the locked answer. The observed-spread computation is reported beside it, and
**if the two disagree, C2 is FAIL** (the locked sweep passing does not rescue it, per ADDENDUM 01's
stricter-basis rule and the plain fact that the sweep is optimistic).

**Lesson, logged as `V-10`:** converting a cost between denominators is only safe if the
conversion is written down at the point of comparison. Both numbers were individually correct and
the sentence joining them was wrong — the same failure as "0 for 9," which was also a true set of
findings wrapped in an untrue aggregate.
