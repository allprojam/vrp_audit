# RESULT — BTC variance risk premium: existence vs harvestability

Prereg `docs/HYPOTHESIS.md`, sha256 `e1cc0def…`, frozen 2026-10-29T20:50:51Z before results.
Verify: `python3 src/prereg.py verify docs/HYPOTHESIS.md` → **OK**.
Addenda **01** (cost denominator) and **02** (G3 threshold, spot/premium conversion), both written
before this run. Code `src/vrp.py`. Results `runs/vrp.json`.

## VERDICT

| claim | verdict | basis |
|---|---|---|
| **C1** a premium exists | **CONDITIONAL — fails estimator robustness (G2)** | CC passes; PK and GK do not survive the variance-P&L test |
| **C2** harvestable at retail | **FAIL** | fails G3 on every estimator; deeply negative at the observed spread |

**C2 FAIL is unambiguous and was the expected outcome.** C1 is the finding that matters and it is
not a clean pass: the premium exists in *vol points* and shrinks toward zero as the estimator
improves.

## Results

`n` nominal **971**, `n_eff` **32** (non-overlapping), window 2024-02-03 → 2026-10-29. G5 met
(`n_eff ≥ 30`), barely.

| est | mean IV−RV (vol pts) | median | IV>RV | mean variance P&L | cum P&L | worst period | mdd/mean |
|---|---|---|---|---|---|---|---|
| **CC** (close-to-close) | **+0.0549** | +0.0870 | 70.6% | **+0.1119** | +108.61 | −2.249 | 501.7 |
| **PK** (Parkinson) | **+0.0156** | +0.0479 | 65.6% | **−0.0238** | −23.11 | −2.927 | n/a |
| **GK** (Garman-Klass) | **+0.0029** | +0.0359 | 62.8% | **−0.0747** | −72.55 | −3.148 | n/a |

### The central finding: the premium evaporates as the estimator improves

| estimator | mean VRP (vol pts) | vs CC |
|---|---|---|
| CC | +0.0549 | — |
| PK | +0.0156 | **−72%** |
| GK | +0.0029 | **−95%** |

CC uses only closes, so it misses intraday extremes and gap risk — precisely the variance a seller
is short. The prereg (G2) fails C1 outright if the premium appears under CC but not PK/GK. **That
is what happened.** The "premium" is largely an artifact of under-measuring realized volatility.

### G1 passes while the trade loses money — a spec defect, disclosed

For PK and GK, `mean(IV − RV) > 0` (G1 passes) while `mean((IV²−RV²)/IV²) < 0` (the variance trade
loses). Both are correct; they measure different things. G1 is defined in **vol points** (linear);
the P&L is **quadratic** in vol. A single spike at RV = 1.20 against IV = 0.50 loses 4.76 in
variance units and erases ~25 benign periods at +0.19. **G1/G2 as written do not gate the quantity
that determines profit.** This is the third gate in this prereg that does not bite where intended
(see V-07, V-11); recorded as **V-13**, not patched, because the verdict is already FAIL.

## Gates, as written

| gate | CC | PK | GK |
|---|---|---|---|
| **G1** existence | PASS | PASS | PASS |
| **G2** not just CC | — | **FAIL** (premium collapses) | **FAIL** |
| **G3** tail ≤ 50% of cumulative | **FAIL** | FAIL | FAIL |
| **G4** survives 20 bp premium basis | PASS (+0.0411) | **FAIL** (−0.0946) | **FAIL** (−0.1455) |
| **G5** `n_eff ≥ 30` | PASS (32) | PASS | PASS |

- **C1 = G1 ∧ G2 ∧ G5 → FAIL** (G2 fails).
- **C2 = G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5 → FAIL.**

## The decisive number: cost at the observed spread

Premium is **5.65% of spot** on average, so the live chain's median relative bid-ask
(**3.85% of premium**) is a round trip of `2 × 0.0385 / 0.0565` in variance-P&L units:

| est | gross mean P&L | net at observed spread |
|---|---|---|
| CC | +0.1119 | **−1.2504** |
| PK | −0.0238 | **−1.3861** |
| GK | −0.0747 | **−1.4370** |

**C2 is not marginal. It is off by roughly an order of magnitude**, on every estimator, before any
tail loss. This confirms the ADDENDUM_02 correction: the locked sweep `{0,5,10,20,40}` bp explores a
region where costs are ~19× too low, and even the CC cell that "passes" G4 at 20 bp is positive only
because the sweep never reaches the real spread.

## Tail

`mdd / mean` for CC is **501.7** — the worst drawdown is ~502× one period's average premium. The
prereg's G3 threshold (50% of cumulative) failed for every estimator, and per ADDENDUM_02 it barely
bites in general (0% fail on a plausible premium). The stricter diagnostic shows the tail is
enormous. Worst individual 30-day periods: CC −2.249, PK −2.927, GK −3.148 in variance units,
against a benign period worth ~+0.19. **A single spike costs 12–17 benign periods.**

## What this means

1. **The premium is real but small, and mostly measurement artifact.** IV does exceed realized vol
   (G1 passes everywhere, IV>RV in 63–71% of periods, median positive on all three). But the margin
   shrinks by 95% once realized vol is measured properly. On GK — the honest estimator — it is
   +0.29 vol points, which is **inside any plausible transaction cost**.
2. **The retail harvest is impossible at observed spreads**, by ~10×, with or without the tail.
3. **This is a successful study.** C1 conditional, C2 failed, decided by pre-registered gates, with
   the answer unchanged by the two pre-run addenda.

## Provenance

All figures above are registered in `PROVENANCE.md` and pass `python3 src/check_provenance.py`.

## Corrections to earlier expectations

The pre-run expectation was "**C1 PASS, C2 FAIL**". C2 FAIL was right. **C1 was predicted too
confidently** — the estimator-degradation (−85% and −95%) was not anticipated in the prereg, and
G2 caught it only because it was pre-committed. Without G2 this would have been reported as a clean
C1 PASS on the CC estimator alone.

**Lesson for the next prereg:** define gates on the quantity that determines P&L (variance units),
not on an intermediate proxy (vol points). See `V-13`.
