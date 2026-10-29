# ADDENDUM 01 — cost denominator ambiguity in G4

**Written:** 2026-10-29T21:0xZ · **Before any VRP statistic was computed.** `runs/vrp.json` does not
exist at the time of writing. The prereg `docs/HYPOTHESIS.md` is **NOT** edited; hash `e1cc0def…`
still verifies. This is the I-6 mechanism: a locked prereg is never re-locked, ambiguities are
resolved out loud.

## What was found

`HYPOTHESIS.md` §Method 5 specifies a cost sweep `c ∈ {0,5,10,20,40}` in "**bps of notional** per
round trip," and §Gates G4 requires C2 to survive `c = 20`.

"bps of notional" is **ambiguous for an option position**, and the two readings differ by an order
of magnitude:

| reading | denominator | what `c = 20` costs a 30-day ATM seller |
|---|---|---|
| **A — variance notional** (what `src/vrp.py` currently implements) | variance units | eats **1.05%** of gross P&L |
| **B — premium notional** (what you actually pay for the option) | option premium | eats a large fraction of gross P&L |

Measured, at IV 0.50 / RV 0.45: gross variance P&L is 0.1900 per unit variance notional, and
subtracting `20bp/1e4 = 0.0020` removes **1.05%** of it. Under reading A the gate is nearly
non-binding — it would pass almost anything, which **inverts its purpose**. G4 is supposed to be
the hard gate that separates C1 from C2.

## The clarification (binding, pre-registered here, before results)

1. **Both cost bases will be computed and reported.** Neither may be omitted from `RESULT.md`.
2. **C2 requires passing G4 under the STRICTER basis (B, premium notional).** Passing only under
   basis A does **not** satisfy G4. This is the conservative reading and it is fixed now, before
   any result is known.
3. Basis A is retained in the output for continuity with the locked text, labelled
   `net_mean_pnl_by_cost_variance_notional`.
4. This addendum does not and cannot change G1, G2, G3 or G5.

## The observed spread, and why it matters more than the sweep

Live chain (snapshot 2026-10-29, 938 quotable BTC options): **median relative bid-ask 3.85%**
(p25 2.09%, p75 10.00%). A 30-day ATM option with 50% IV has a premium of roughly **5.73% of spot**,
so a 3.85% relative spread is about **22 bp of spot** — for a round trip the seller pays the spread
roughly twice, once in and once out.

**This is far larger than any point in the locked sweep `{0,5,10,20,40}` bps.** The prereg's sweep
was written before the spread prior was measured carefully; it is too optimistic by construction.
That is recorded here rather than used to move the goalposts: the sweep stays as locked, and the
spread observation is reported alongside it as context. **If C2 passes the locked sweep but fails
at the observed 22 bp of spot, the honest verdict is C2 FAIL**, and that must be stated in
`RESULT.md` with this addendum cited.

## Why not just fix the prereg

Because the prereg is the one artifact that must not move after locking (I-6). A spec that turned
out to be ambiguous is a **finding about the spec**, and it belongs in an addendum with a
timestamp, not in a silent edit. The next study's prereg should define cost basis explicitly —
that lesson is logged as `V-06`.
