"""Horizontal bar plot of hyperparameter (component capacity) importance.

Produces a publication-grade figure following the thesis Quality Baseline:
sans-serif typography, FEV color accents, clean layout. Bars run left-to-right,
sorted from most to least important.
"""

import os

import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Typography (Quality Baseline §1, §5)
# ---------------------------------------------------------------------------
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica", "Arial"]
plt.rcParams["mathtext.fontset"] = "cm"

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
importance = {
    "BESS": 0.030551,
    "BGSS": 0.00208,
    "CGH2": 0.00318,
    "AWE": 0.4802,
    "Generator": 0.00333,
    "MeOH reactor": 0.00534,
    "PV": 0.0512,
    "ATR": 0.04323,
    "WT": 0.03074,
}

# Sort ascending so the largest bar sits at the top of the axis.
items = sorted(importance.items(), key=lambda kv: kv[1])
labels = [k for k, _ in items]
values = [v for _, v in items]

# ---------------------------------------------------------------------------
# Colors: highlight the dominant driver, keep the rest in a neutral tint.
# ---------------------------------------------------------------------------
FEV_RED = "#B9052D"       # dominant / focal
SLATE = "#64748B"          # neutral bars
bar_colors = [FEV_RED if v == max(values) else SLATE for v in values]

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.0), dpi=300)

bars = ax.barh(labels, values, color=bar_colors, edgecolor="none", height=0.68)

# Value annotations at the end of each bar.
xmax = max(values)
for bar, v in zip(bars, values):
    ax.text(
        bar.get_width() + xmax * 0.01,
        bar.get_y() + bar.get_height() / 2,
        f"{v:.3f}",
        va="center",
        ha="left",
        fontsize=8,
        color="#000000",
    )

# ---------------------------------------------------------------------------
# Axes styling
# ---------------------------------------------------------------------------
ax.set_xlabel("Relative importance", fontsize=10)
ax.set_xlim(0, xmax * 1.12)
ax.tick_params(axis="y", labelsize=9)
ax.tick_params(axis="x", labelsize=8)

# Clean spines: keep only bottom + left.
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.spines["left"].set_color("#000000")
ax.spines["bottom"].set_color("#000000")

ax.xaxis.grid(True, linestyle="--", linewidth=0.6, color="#CBD5E1", alpha=0.7)
ax.set_axisbelow(True)

ax.set_title("Hyperparameter Importance", fontsize=12, fontweight="bold", pad=10)

fig.tight_layout()

# ---------------------------------------------------------------------------
# Export: vector SVG + 300 DPI PNG preview (Quality Baseline §4)
# ---------------------------------------------------------------------------
out_dir = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(out_dir, "hyperparameter_importance.svg")
png_path = os.path.join(out_dir, "hyperparameter_importance.png")

fig.savefig(svg_path, format="svg", bbox_inches="tight")
fig.savefig(png_path, format="png", dpi=300, bbox_inches="tight")

print(f"Saved: {svg_path}")
print(f"Saved: {png_path}")
