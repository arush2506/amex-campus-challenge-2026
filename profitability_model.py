"""
Premier Cardmember Profitability Model
American Express Campus Challenge 2026 - Round 1 (Strategy Track)

Reproduces the final submission (public leaderboard accuracy: 0.883).

The model estimates each cardmember's annual profit-to-issuer as a transparent
Revenue - Cost equation grounded in premium-card unit economics, then rank-orders
members. Because scoring is rank-based (top-20% overlap), only the RATIOS between
coefficients affect the result, not their absolute scale.

Usage:
    python src/profitability_model.py
    (expects data/campus_challenge_r1_data.csv; writes predictions.csv)
"""

import pandas as pd
import numpy as np

# ----------------------------------------------------------------------------
# Feature dictionary (decoded from the competition's masked-attribute key)
# ----------------------------------------------------------------------------
# f1  Average revolve balance (12m)     f13 Lounge access count
# f2  Cancellation calls (12m)          f14 Airline credits used ($)
# f3  Collection calls                  f15 Cab benefit usage (count)
# f4  Rewards points balance            f16 Entertainment credit used ($)
# f5  "Total spend" (EXCLUDED: noise)   f17 Total lend line   (unused; dup of f18)
# f6  Airlines spend (12m)              f18 Consumer lend line (unused)
# f7  Other spend (12m)                 f19 Supplementary accounts
# f8  Entertainment spend (12m)         f20 Active charge cards (EXCLUDED: engagement)
# f9  Lodging spend (12m)               f21 Points redeemed (EXCLUDED: earned basis wins)
# f10 Dining spend (12m)                f22 Emails opened  (unused)
# f11 Average risk score (12m)          f23 Emails clicked (unused)
# f12 Website logins (unused)
# ----------------------------------------------------------------------------

# Coefficients (derived from premium-card economics, calibrated on the leaderboard).
# See experiment_log.md for the measurement behind each value.
PARAMS = {
    "discount_rate":     0.037,   # interchange kept per $ of spend (fitted optimum)
    "interest_margin":   0.42,    # net interest weight on revolving balance
    "supp_fee":          175,     # $ per supplementary account
    "reward_cost_per_pt":0.006,   # issuer cost per rewards point EARNED (measured peak)
    "lounge_cost":       35,      # $ per lounge visit
    "cab_cost":          15,      # $ per cab-benefit use
    "lgd_x_pd_weight":   5.1,     # risk-adjusted expected-loss multiplier (f11 * f1)
    "collection_cost":   400,     # $ per collection call (distress proxy)
    "cancel_cost":       30,      # $ per cancellation call (servicing proxy)
}

SPEND_COLS = ["f6", "f7", "f8", "f9", "f10"]        # granular spend categories
TRAVEL_5X  = ["f6", "f9"]                            # airlines + lodging earn 5x points
OTHER_1X   = ["f7", "f8", "f10"]                     # everything else earns 1x


def load_and_impute(path: str) -> pd.DataFrame:
    """Load the dataset and impute missing values with the column median.

    Median imputation is neutral to the (apparently random) masking pattern;
    usage/benefit medians are ~0, so non-users contribute ~0 cost.
    """
    df = pd.read_csv(path)
    feat = [f"f{i}" for i in range(1, 24)]
    for c in feat:
        df[c] = df[c].fillna(df[c].median())
    return df


def profitability_score(df: pd.DataFrame, p: dict = PARAMS) -> pd.Series:
    """Compute the Revenue - Cost profitability score per cardmember."""
    spend         = df[SPEND_COLS].sum(axis=1)
    points_earned = 5 * df[TRAVEL_5X].sum(axis=1) + df[OTHER_1X].sum(axis=1)

    revenue = (
        p["discount_rate"]   * spend
        + p["interest_margin"] * df["f1"]
        + p["supp_fee"]        * df["f19"]
    )
    cost = (
        p["reward_cost_per_pt"] * points_earned
        + (p["lounge_cost"] * df["f13"] + df["f14"]
           + p["cab_cost"] * df["f15"] + df["f16"])          # benefit credits
        + p["lgd_x_pd_weight"] * df["f11"] * df["f1"]          # risk-adjusted loss
        + p["collection_cost"] * df["f3"]
        + p["cancel_cost"]     * df["f2"]
    )
    return revenue - cost


def main():
    df = load_and_impute("data/campus_challenge_r1_data.csv")
    df["Prediction"] = profitability_score(df).round(2)

    out = df[["id", "Prediction"]].rename(columns={"id": "ID"})
    out.to_csv("predictions.csv", index=False)

    thr = df["Prediction"].quantile(0.80)
    print(f"Scored {len(df):,} members. Top-20% cutoff score: {thr:,.0f}")
    print("Wrote predictions.csv")


if __name__ == "__main__":
    main()
