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
