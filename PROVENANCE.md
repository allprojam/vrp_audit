# PROVENANCE — every claim binds to a file:line

Rule **A-22**: no figure is quoted without a resolvable pointer.
`python3 src/check_provenance.py` verifies this mechanically and exits non-zero on failure (A-23).

Format: `| claim | value | path:line | token |
|---|---|---|
| DVOL history capped at 1000 points | 1000 daily points max | docs/HYPOTHESIS.md:30 | 1000 daily points |
| DVOL coverage start | 2024-02-03 | docs/HYPOTHESIS.md:30 | 2024-02-03 |
| No historical bid/ask archive exists | snapshot only | docs/HYPOTHESIS.md:37 | no historical bid/ask |
| Options chain snapshot counts | 937 with both bid+ask | docs/HYPOTHESIS.md:32 | 937 |
| Effective sample size rule | n/30 | docs/HYPOTHESIS.md:58 | n/30 |
| C2 requires surviving 20 bps | 20 bps | docs/HYPOTHESIS.md:77 | 20 bps |
| Minimum acceptable n_eff | n_eff < 30 | docs/HYPOTHESIS.md:91 | n_eff |
| 20bp eats 1.05% of gross variance P&L | 1.05% | docs/ADDENDUM_01.md:18 | 1.05% |
| gross variance P&L at IV .50/RV .45 | 0.1900 | docs/ADDENDUM_01.md:21 | 0.1900 |
| 30d ATM premium as % of spot | 5.73% | docs/ADDENDUM_01.md:39 | 5.73% |
| 3.85% relative spread in spot terms | 22 bp of spot | docs/ADDENDUM_01.md:40 | 22 bp of spot |
| Observed spread vs G4 gate | 19.2x over | docs/ADDENDUM_02.md:41 | 19.2 |
| G3 fail rate, plausible premium | 0% | docs/ADDENDUM_02.md:20 | 0% |
| G3 fail rate, thin premium | 22% | docs/ADDENDUM_02.md:21 | 22% |
| Round-trip cost at observed spread | 1.34 | docs/ADDENDUM_02.md:58 | 1.34 |
| RESULTS — mean VRP, CC | +0.0549 vol pts | docs/RESULT.md:26 | 0.0549 |
| RESULTS — mean VRP, PK | +0.0156 vol pts | docs/RESULT.md:27 | 0.0156 |
| RESULTS — mean VRP, GK | +0.0029 vol pts | docs/RESULT.md:28 | 0.0029 |
| RESULTS — nominal n | 971 | docs/RESULT.md:21 | 971 |
| RESULTS — effective n | 32 | docs/RESULT.md:21 | 32 |
| RESULTS — IV>RV, CC | 70.6% | docs/RESULT.md:26 | 70.6% |
| RESULTS — IV>RV, PK | 65.6% | docs/RESULT.md:27 | 65.6% |
| RESULTS — IV>RV, GK | 62.8% | docs/RESULT.md:28 | 62.8% |
| RESULTS — worst period, CC | -2.249 | docs/RESULT.md:26 | 2.249 |
| RESULTS — mdd/mean, CC | 501.7 | docs/RESULT.md:88 | 501.7 |
| RESULTS — net at observed spread, CC | -1.2504 | docs/RESULT.md:77 | 1.2504 |
| RESULTS — net at observed spread, PK | -1.3861 | docs/RESULT.md:78 | 1.3861 |
| RESULTS — net at observed spread, GK | -1.4370 | docs/RESULT.md:79 | 1.4370 |
| RESULTS — premium as fraction of spot | 5.65% | docs/RESULT.md:72 | 5.65% |
| RESULTS — P&L linear-only, CC | +0.2105 | docs/ADDENDUM_03.md:22 | 0.2105 |
| RESULTS — P&L with dispersion, CC | +0.1670 | docs/ADDENDUM_03.md:22 | 0.1670 |
| RESULTS — dispersion (Jensen) effect, CC | -0.0435 | docs/ADDENDUM_03.md:22 | 0.0435 |
| RESULTS — 1/IV^2 weighting effect, CC | -0.0551 | docs/ADDENDUM_03.md:41 | 0.0551 |
| RESULTS — E[RV] under GK | 0.4900 | docs/ADDENDUM_03.md:24 | 0.4900 |
| OCT29 — single-day RV, CC | 23.2% | docs/ADDENDUM_04.md:48 | 23.2% |
| OCT29 — single-day RV, PK | 53.4% | docs/ADDENDUM_04.md:49 | 53.4% |
| OCT29 — single-day RV, GK | 61.2% | docs/ADDENDUM_04.md:50 | 61.2% |
| OCT29 — DVOL at snapshot | 41.8% | docs/ADDENDUM_04.md:51 | 41.8% |
| OCT29 — GK/CC ratio | 2.63x | docs/ADDENDUM_04.md:54 | 2.63 |
| OCT29 — UTC daily move | -1.21% | docs/ADDENDUM_04.md:33 | 1.21% |
| OCT29 — intraday range | 4.76% | docs/ADDENDUM_04.md:53 | 4.76% |
| OCT29 — stale committed DVOL close | 37.94 | docs/ADDENDUM_04.md:23 | 37.94 |

## Superseded — never cite as current (A-21)

| stale figure | stale value | current value | source of truth |
|---|---|---|---|
| | | | |

## Withdrawn — no source exists anywhere in the project

| claim | status |
|---|---|
| | |
