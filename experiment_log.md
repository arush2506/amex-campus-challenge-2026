# Experiment Log — reverse-engineering the profitability function

Ten scored submissions, used as controlled single-variable experiments. Every score —
including drops — is a measurement. Offline analysis (free) was exhausted before spending
each (scarce) submission.

| # | Hypothesis under test | Change (one variable) | Score | Δ | Learning |
|---|---|---|---|---|---|
| 1 | A revenue−cost economics equation ranks profitability well | Baseline (category spend) | 0.823 | — | Strong start; economic structure is sound (random ≈ 0.20) |
| 2 | `f5` "total spend" is the real spend signal | Spend base = `f5` | 0.388 | −0.435 | **Falsified.** `f5` is noise (matches its ~0 correlations) |
| 3 | Premier members are transactors → spend matters more | Spend weight 0.024→0.040 | 0.832 | +0.009 | ✅ Direction confirmed |
| 4 | Even heavier spend is better | Spend weight →0.070 | 0.767 | −0.065 | **Overshoot.** Quadratic fit locates optimum ≈ 0.037 |
| 5 | `f20` "# cards held" is engagement, not fee revenue | Remove `f20` fee term | 0.847 | +0.015 | ✅ Structural fix (taxonomy-driven) |
| 6 | Rewards cost per point is higher than assumed | Reward cost 0.006→0.012 | 0.826 | −0.021 | **Falsified.** Cost is not higher |
| 7 | Rewards cost is ~zero | Reward cost →0 | 0.819 | −0.028 | **Falsified.** Peak confirmed at ≈0.006 |
| 8 | Rewards cost hits at redemption, not accrual | Cost basis = `f21` redeemed | 0.756 | −0.091 | **Falsified.** Swap algebra: ejected redeemers were ~54 pts more accurate → they belong in top 20% |
| 9 | Clean revolvers are undervalued (risk-adjusted) | Interest (0.18,0.9)→(0.30,3.0) | 0.876 | +0.029 | ✅ **Largest single gain** |
| 10 | Continue along the validated interest ray | →(0.42, 5.1) | **0.883** | +0.007 | ✅ Near the summit; structure locally optimal |

## Analytical techniques used
- **Exploratory data analysis** — distributions, winsorisation detection, missingness pattern.
- **Correlation / multicollinearity analysis** — clusters validated the economic groupings; `f5` flagged as noise pre-emptively; redundant risk measure (`f3` vs `f11`) removed.
- **Sensitivity analysis** — identified that ~4 of 10 coefficients control almost the entire ranking, focusing the search.
- **Response-surface fitting** — a quadratic through three leaderboard points located the spend-weight optimum.
- **Error autopsy** — profiling the members swapped between a better and worse submission to infer what the hidden formula values.
- **Controlled experimentation** — one change per submission; drops treated as information, not failure.
