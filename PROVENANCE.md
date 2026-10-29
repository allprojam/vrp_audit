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

## Superseded — never cite as current (A-21)

| stale figure | stale value | current value | source of truth |
|---|---|---|---|
| | | | |

## Withdrawn — no source exists anywhere in the project

| claim | status |
|---|---|
| | |
