# ADDENDUM 03 — the post-run decomposition: three effects, not one

**Written after the run.** `runs/vrp.json` exists. This does **not** alter the verdict, and it does
not touch `docs/HYPOTHESIS.md` (`e1cc0def…` still verifies). It corrects the *explanation* of a
verdict that is already FAIL on G2 and G3.

Artifact: `runs/vrp_decomp.json` (newly persisted, because the committed `runs/vrp.json` stored
aggregates only and the decomposition below was not checkable from it — that was a real gap).

---

## What the post-mortem claimed, and what the data supports

The claim was that PK/GK "win 65.6%/62.8% of windows with a positive average volatility spread and
still suffer negative gross variance P&L" **because of Jensen's inequality**: variance payoffs are
quadratic, so dispersion in RV produces a negative penalty.

**Part of that is right, and one part is wrong.**

| est | E[IV] | E[RV] | sd(RV) | vol-pt gap | P&L linear-only | P&L with dispersion | dispersion effect |
|---|---|---|---|---|---|---|---|
| CC | 0.4929 | 0.4380 | 0.1374 | **+0.0549** | +0.2105 | +0.1670 | **−0.0435** |
| PK | 0.4929 | 0.4773 | 0.1368 | **+0.0156** | +0.0624 | +0.0254 | **−0.0370** |
| GK | 0.4929 | 0.4900 | 0.1415 | **+0.0029** | +0.0119 | −0.0283 | **−0.0402** |

Reading this table:

1. **The convexity/dispersion effect is real and roughly constant** at **−0.037 to −0.044** across
   all three estimators. It is a genuine second-order penalty, exactly as described, and it is what
   pushes GK from `+0.0119` to `−0.0283`.
2. **But it is NOT what makes PK negative.** Under PK the variance P&L computed with *zero*
   dispersion is still **+0.0624** — and only becomes negative somewhere between the mean-based and
   the per-period form. The dominant driver for PK is that **E[RV] is close to E[IV]**: at
   `0.4773` vs `0.4929` the raw gap is only +1.56 vol points, and convexity eats it.
3. **A third effect was unmodelled by the post-mortem:** the per-period P&L is
   `mean((IV²−RV²)/IV²)`, which weights each period by `1/IV²`. It is **not** equal to
   `(E[IV²]−E[RV²])/E[IV²]`. The gap:

   | est | per-period mean (as reported) | mean-based identity | `1/IV²` weighting effect |
   |---|---|---|---|
   | CC | **+0.1119** | +0.1670 | **−0.0551** |
   | PK | **−0.0238** | +0.0254 | **−0.0492** |
   | GK | **−0.0747** | −0.0283 | **−0.0464** |

   The `−0.046 to −0.055` weighting effect is **larger than the Jensen effect** and is the actual
   arithmetic reason PK flips sign. It is economically meaningful, not an artifact: periods with
   *low* IV get a larger weight, and those are the periods where the seller collected least for the
   variance sold.

**Corrected statement of the mechanism.** Negative gross variance P&L arises from three additive
terms, in order of size: (a) **E[RV] ≈ E[IV]** once intraday ranges are counted — the estimator
collapse, −3.9 to −5.2 vol points from CC; (b) the **`1/IV²` weighting** of the per-period payoff;
(c) **dispersion of RV** (the Jensen term). The post-mortem credited (c) with the whole reversal.
(c) is real; it is not the main term.

## What this changes

- **Nothing about the verdict.** C1 fails G2, C2 fails G3 and G4, unchanged.
- **The lesson is sharper.** The headline is not "quadratic payoffs eat linear spreads." It is
  **"the premium E[IV]−E[RV] is itself near zero once RV is measured with intraday data"** — PK
  leaves +1.56 vol points, GK +0.29. Everything downstream is arithmetic on a premium that is
  already ≈0.
- **A reporting defect is now fixed:** `runs/vrp.json` did not persist the per-period series, so
  the decomposition above could not be computed from the committed artifact. `runs/vrp_decomp.json`
  now holds it. The next prereg must state *which* estimator of the payoff is the gate —
  per-period mean, mean-based identity, or cumulative — because they differ by up to 0.055 in
  variance-P&L units, which is 100% of the result at these magnitudes.
