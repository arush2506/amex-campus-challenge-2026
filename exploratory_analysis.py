"""
Exploratory Data Analysis - American Express Campus Challenge 2026
Reproduces the key findings that shaped the modelling strategy.

Usage:
    python src/exploratory_analysis.py
    (expects data/campus_challenge_r1_data.csv)
"""

import pandas as pd
import numpy as np

FEATURES = [f"f{i}" for i in range(1, 24)]


def main():
    df = pd.read_csv("data/campus_challenge_r1_data.csv")

    # 1) Winsorisation: many features capped at their upper percentiles ----------
    print("=" * 70)
    print("1) CAPPING CHECK  (99th percentile == max  =>  top 1% is clamped)")
    print("=" * 70)
    for c in ["f1", "f6", "f7"]:
        q99, mx = df[c].quantile(0.99), df[c].max()
        capped = np.isclose(q99, mx)   # top-1% clamped to a single ceiling value
        print(f"  {c}: 99%={q99:,.0f}  max={mx:,.0f}  -> top-1%-capped={capped}")

    # 2) f5 is a correlational island (flag as noise before spending a submission)
    print("\n" + "=" * 70)
    print("2) IS f5 ('total spend') A REAL SIGNAL?")
    print("=" * 70)
    corr = df.corr(numeric_only=True).drop(index="id", columns="id")
    f5_max = corr["f5"].drop("f5").abs().max()
    print(f"  f5's strongest correlation with any other feature: {f5_max:.3f}")
    print("  -> near-zero: f5 behaves like noise. (Confirmed later: scored 0.388.)")

    # 3) Correlation clusters mirror the economic groupings ----------------------
    print("\n" + "=" * 70)
    print("3) CORRELATION CLUSTERS  (|r| >= 0.5)  ->  match economic levers")
    print("=" * 70)
    seen = set()
    for a in corr.columns:
        for b in corr.columns:
            if a < b and abs(corr.loc[a, b]) >= 0.5:
                print(f"  {a:>4} <-> {b:<4}  r={corr.loc[a, b]:+.2f}")

    # 4) Risk-score direction --------------------------------------------------
    print("\n" + "=" * 70)
    print("4) RISK DIRECTION  (f11 vs collection calls f3)")
    print("=" * 70)
    r = df[["f11", "f3"]].dropna().corr().iloc[0, 1]
    print(f"  corr(risk f11, collection calls f3) = {r:+.2f}  -> higher f11 = riskier")


if __name__ == "__main__":
    main()
