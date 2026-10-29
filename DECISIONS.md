# DECISIONS — the ADR ledger

> **This numbering is local to this repository.** It is not a global namespace, and it does not
> match `/root/agency_bot/workspace/gold_macro/DECISIONS.md`, which carries **A-09…A-20** (asset-
> specific findings and corrections) that are deliberately **absent here**, and which **has no
> A-24**. Cite across projects as `<repo>:A-NN`. A bare `A-23` is ambiguous once a second repo
> exists.

Locked decisions in order. Each has a status, the reason it exists, and where it can be checked.
Entries marked **CORRECTED** record a decision that was made, published, then found wrong by
measurement. They are kept, never deleted — a ledger with no corrections is a ledger nobody
checked.

---

## Method

### A-01 · Pre-register, hash, then run — LOCKED
No study runs before its prereg exists and its sha256 is in `runs/`. Check: `src/prereg.py verify`.

### A-02 · A gate is read exactly as written — LOCKED
A failed gate is reported as failed. A friendlier wording that would have passed is noted in an
addendum and **not adopted**.

### A-03 · Multiple metrics, all required — LOCKED
No single-metric wins. Calmar alone rewards raw drift; pair it with Sharpe, MaxDD and Ulcer.

### A-04 · Classify failures by mechanism, not by verdict — LOCKED
Separate *overfitting* (fixable by pruning) from *non-stationarity* (not fixable). They point at
different remedies.

### A-05 · Fixed seeds, no seed-shopping — LOCKED

## Data

### A-06 · Record provenance including what failed — LOCKED
A source that 403s is a finding. It saves the next session an hour.

### A-07 · Never splice two sources without proving they agree on the overlap — LOCKED
Record the correlation on the overlap window.

### A-08 · Prefer exact mechanics to convenient constants — LOCKED
A constant bond duration of 7.5 is wrong at 15% yields (true modified duration 4.72, 37% less rate
sensitivity). The constant overstated both the crash and the rally.

## Enforcement

### A-21 · A superseded report must banner itself — LOCKED
Any report whose numbers came from a since-fixed engine carries a banner naming what changed and
pointing at the current artifact, plus an entry in `STATE.md`'s report registry.

### A-22 · Every quoted figure resolves to a pointer — LOCKED
`| claim | value | file:line | token |` in `PROVENANCE.md`. No exceptions.

### A-23 · A-22 is enforced by a script, not by discipline — LOCKED
`src/check_provenance.py`, non-zero exit on failure.
**This is the most important entry in this file.** The prose rule was agreed first, and the first
registry written under it had **15 of ~43 citations wrong** — off-by-one lines, tokens from the
adjacent row, pointers into files that did not contain the figure at all. A human or model
applying a rule from memory to the thing the rule constrains will fail at a double-digit rate.
Only an executable catches it.

### A-24 · Corrections are permanent and visible — LOCKED
A corrected finding keeps its original entry, gains a **CORRECTED** marker, and states both the
wrong and the right number. Deleting the error destroys the evidence that the process works.

---

## This study

### V-01 · Existence and harvestability are separate claims — LOCKED
C1 (premium exists) and C2 (capturable at retail) have different gates and different data
requirements. A positive C1 with a failed C2 is a **successful** study. Conflating them is how
"the variance risk premium is real" becomes "you can harvest it," which is the same substitution
error as quoting an in-scope number for an out-of-scope claim (`gold_macro:A-25`).

### V-02 · Spread-capture is out of scope because the data does not exist — LOCKED
Verified before locking: Deribit exposes **no historical bid/ask archive**, and historical fills
are too sparse to estimate spreads (4 trades / 30 days on a sampled far strike). A market-making
backtest is therefore impossible, not merely unwise. Any later claim about capturing the spread
must be refused on this ground, not argued on its merits.
Live chain shows median relative bid-ask **3.85%** (p25 2.09%, p75 10.00%) — context only, and a
warning that the spread may exceed the premium entirely.

### V-03 · Report three volatility estimators; CC alone is a fail — LOCKED
Close-to-close uses only closes, so it misses intraday extremes and gap risk — precisely the
variance a vol seller is short. It therefore **flatters** the seller. Parkinson and Garman-Klass
use the full bar and are the honest ones. Gate G2 fails C1 outright if the premium appears under
CC but not PK/GK.

### V-04 · Overlapping 30-day windows are not 999 observations — LOCKED
Daily sampling of 30-day windows overlaps 29/30. Nominal `n ≈ 999` is a fiction; `n_eff ≈ n/30`.
With DVOL's 1000-point cap the honest `n_eff` is **~33**, barely above the prereg floor of 30.
This is the binding limitation of the study and must be stated in any result.

### V-05 · Cost is swept, never asserted — LOCKED
Retail option fees are not verified from this host and will not be guessed. Cost is a sweep
`c ∈ {0,5,10,20,40}` bps. C2 passes only if it survives `c = 20`. Surviving `c = 0` alone is a FAIL
reported as a FAIL.

### V-06 · Cost must name its denominator, in the prereg, before locking — LOCKED
The locked text sweeps cost in "bps of notional" without saying **which** notional. For an option
that ambiguity spans an order of magnitude: 20 bp against *variance* notional eats **1.05%** of
gross P&L and the gate becomes nearly non-binding; against *premium* notional it is decisive.
Resolved in `docs/ADDENDUM_01.md` **before results**, under I-6: C2 must clear the stricter
(premium) basis. The prereg hash was not edited.
**Lesson for the next prereg:** a cost term is under-specified unless it states
`{per unit of X} / {round trip or one way} / {of what: premium, spot, or variance}`.

### V-07 · A gate that cannot fail is not a gate — LOCKED
G4 as originally coded would pass almost any result. A threshold is only meaningful relative to
the scale of the quantity it is subtracted from; before locking, compute the gate's bite on a
*plausible* value and confirm it can actually reject. This is the same class of error as a
`p < 0.05` threshold with no stated effect size.

### V-08 · Annualization must match the venue's convention — LOCKED
Deribit DVOL is annualised on a **365-day** 24/7 basis. Annualising perp realized vol with the
TradFi `sqrt(252)` would understate RV by `1 - sqrt(252/365) = 16.9%`, manufacturing a spurious
positive VRP of several vol points. **Verified in `src/vrp.py`: all three estimators (CC, PK, GK)
use `sqrt(365)`** — no fix needed. Recorded because the near-miss is the point.

### V-09 · Overlapping windows inflate t-statistics by sqrt(H) — LOCKED
1000 daily DVOL observations yield `n_eff ≈ 33` non-overlapping 30-day windows. Treating n=1000 as
independent inflates a t-statistic by `sqrt(30) ≈ 5.5x`. G5 exists to prevent exactly this, and
`n_eff ≈ 33` is the binding limit of the whole study.

### V-10 · Convert denominators at the point of comparison, not in prose — LOCKED
ADDENDUM 01 compared "3.85% relative spread" to "20 bps" and concluded the spread was *just over*
the gate, while in the same breath rendering the spread as "~22 bp of **spot**". Correctly stated
the spread is **385 bp of premium = 19.2x** the gate. Both individual numbers were right; the
sentence joining them was wrong. **Rule:** never place two figures in one comparison unless they
share a denominator, and write the conversion inline when they do not. Same failure class as
`gold_macro`'s "0 for 9" — true components, untrue aggregate.

### V-11 · A tail gate must be checked against sample length — LOCKED
G3's 50%-of-cumulative-premium threshold is nearly non-binding: cumulative premium grows ~linearly
while drawdown grows ~`sd*sqrt(n)`, so the ratio falls as `n` rises. Monte Carlo (2,000 paths x 33
periods) puts the fail rate at **0%** on a plausible IV-RV gap, 22% only when the premium is thin.
Retained as written for the verdict; a stricter diagnostic (`mdd / mean_pnl`) is added and reported
beside it. A tail test whose bite depends on the sample is not a tail test.

### V-12 · The locked cost sweep is optimistic by an order of magnitude — LOCKED
The prereg sweeps `c ∈ {0,5,10,20,40}` bp of premium. The observed live spread is **385 bp of
premium** — 19.2x the sweep's top end. At that spread the round-trip cost in variance-P&L units is
`~1.34` against gross premium `~0.19`. **C2 should be expected to fail**, and a locked-sweep pass
must not be reported as C2 PASS without also reporting this computation. The next prereg must
derive the cost range from a measured spread rather than choosing round numbers.

### V-13 · Gate the quantity that determines P&L, not a proxy for it — LOCKED
G1 was written on `mean(IV − RV)` in **vol points**, but the trade's P&L is
`(IV² − RV²)/IV²` — **quadratic** in vol. On PK and GK, G1 PASSES (`+0.0156`, `+0.0029`) while the
variance trade LOSES (`−0.0238`, `−0.0747`). Both are correct; they measure different things. One
spike at RV = 1.20 vs IV = 0.50 costs 4.76 in variance units and erases ~25 benign periods at +0.19.
The prereg therefore had a gate that could pass while the position lost money. **Not patched** — the
verdict is already FAIL and rewriting it post-results would be exactly the crime the lock prevents.
The finding is logged instead. Next prereg: every gate names the P&L quantity it gates.

### V-14 · A premium measured on closes only is not a premium — CONFIRMED
The pre-run rule (V-03) was: report CC, PK and GK, and fail C1 if the premium shows under CC only.
It did. Mean VRP falls **+0.0549 → +0.0156 (−72%) → +0.0029 (−95%)** from close-to-close to
Parkinson to Garman-Klass. CC ignores intraday extremes and gap risk, which is exactly the variance
a seller is short, so it manufactures a premium by under-measuring RV. **G2 is the single most
valuable gate in this study**: without it the result would have been reported as a clean C1 PASS.

### V-15 · C2 fails by an order of magnitude, not at the margin — CONFIRMED
At the live chain's median relative bid-ask (3.85% of premium, premium ≈ 5.65% of spot), net mean
variance P&L is **−1.2504 / −1.3861 / −1.4370** on CC / PK / GK against gross of **+0.1119 /
−0.0238 / −0.0747**. The locked cost sweep `{0,5,10,20,40}` bp tops out ~19x below the real spread.
C2 is impossible for a price-taker here regardless of estimator or tail treatment.

### V-16 · A payoff has three estimators; the prereg must name which one gates — LOCKED
The same strategy has at least three defensible "mean variance P&L": the **per-period mean**
`mean((IV²−RV²)/IV²)`, the **mean-based identity** `(E[IV²]−E[RV²])/E[IV²]`, and the **cumulative**
sum. They differ here by up to **0.055** in variance-P&L units — 100% of the result at these
magnitudes (CC: +0.1119 vs +0.1670). The prereg did not specify, so the code chose the per-period
mean silently. **Next prereg states the payoff estimator explicitly and reports all three.**

### V-17 · Persist the per-period series, not just aggregates — LOCKED
`runs/vrp.json` stored aggregates only, so the post-run decomposition could not be computed from
the committed artifact. Any explanation offered for a result must be checkable from a committed
file or it is prose. Fixed by `runs/vrp_decomp.json`. **Rule:** a results artifact must contain
enough to recompute every claim made in `RESULT.md`.

### V-18 · Attribute the mechanism, not just the sign — CONFIRMED
The Jensen/dispersion explanation for negative PK/GK P&L is **real but not dominant**. Measured:
dispersion effect **−0.037 to −0.044** (roughly constant); `1/IV²` weighting effect
**−0.046 to −0.055** (larger); and the primary driver is that **E[RV] ≈ E[IV]** once intraday
ranges are counted (gap −3.9 to −5.2 vol points from CC). Crediting convexity alone with the
reversal overstates it. Both effects are genuine; they are ranked wrongly in the post-mortem.
