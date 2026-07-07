"""
Generate the EDA figures used in the README.

Usage:
    python src/make_figures.py
    (expects data/campus_challenge_r1_data.csv; writes PNGs to figures/)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

FEATURES = [f"f{i}" for i in range(1, 24)]


def main():
    df = pd.read_csv("data/campus_challenge_r1_data.csv")
    corr = df[FEATURES].corr()

    sns.set_style("white")

    # 1) Full correlation heatmap ------------------------------------------------
    plt.figure(figsize=(14, 12))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                vmin=-1, vmax=1, square=True, linewidths=0.5,
                annot_kws={"size": 7}, cbar_kws={"shrink": 0.8})
    plt.title("Correlation Heatmap of American Express Dataset", fontsize=16, pad=12)
    plt.tight_layout()
    plt.savefig("figures/correlation_heatmap.png", dpi=130, bbox_inches="tight")
    plt.close()

    # 2) Lower-triangle heatmap (cleaner read) ----------------------------------
    mask = np.triu(np.ones_like(corr, dtype=bool))
    plt.figure(figsize=(13, 11))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                vmin=-1, vmax=1, square=True, linewidths=0.5,
                annot_kws={"size": 7}, cbar_kws={"shrink": 0.8})
    plt.title("Feature Correlation Heatmap (lower triangle)", fontsize=16, pad=12)
    plt.tight_layout()
    plt.savefig("figures/correlation_heatmap_triangle.png", dpi=130, bbox_inches="tight")
    plt.close()

    # 3) Most-connected features (total absolute correlation) -------------------
    connectivity = (corr.abs().sum(axis=1) - 1).sort_values(ascending=False)
    top = connectivity.head(15)
    plt.figure(figsize=(10, 5))
    plt.bar(top.index, top.values, color="#1f77b4")
    plt.ylabel("Total Absolute Correlation")
    plt.title("Most Connected Features", fontsize=15)
    plt.tight_layout()
    plt.savefig("figures/most_connected_features.png", dpi=130, bbox_inches="tight")
    plt.close()

    print("Wrote 3 figures to figures/")
    print("\nMost connected features (total |correlation|):")
    for name, val in top.items():
        print(f"  {name:>4}: {val:.2f}")


if __name__ == "__main__":
    main()
