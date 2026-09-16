"""Generate a publication-grade "modeling trilemma" triangle figure.

Three competing objectives sit at the vertices of an equilateral triangle:
    - Physical Model Accuracy   (MINLP / NLP)
    - Computational Tractability (MILP / LP)
    - Operational Uncertainty    (RL / Stochastic / Robust)

Each edge represents the tension (trade-off) between the two adjacent
objectives. Follows the FEV palette and ISO 80000-2 math notation.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch


DARK_PURPLE = "#41098B"   # Physical Model Accuracy
DARK_GREEN  = "#21762D"   # Computational Tractability
DARK_RED    = "#B9052D"   # Operational Uncertainty
BLACK       = "#000000"
GRAY        = "#64748B"
MATH_GRAY   = "#334155"   # darker gray for math (higher contrast)

BG_PURPLE   = "#F6F2FC"
BG_GREEN    = "#EFF7F0"
BG_RED      = "#FDF2F4"
BG_NEUTRAL  = "#FBFCFD"


def _lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _midpoint(p, q):
    return _lerp(p, q, 0.5)


def _blend(hex0, hex1, t):
    c0 = np.array([int(hex0[i:i + 2], 16) for i in (1, 3, 5)])
    c1 = np.array([int(hex1[i:i + 2], 16) for i in (1, 3, 5)])
    c = (c0 * (1 - t) + c1 * t).astype(int)
    return "#%02x%02x%02x" % tuple(c)


def create_figure(output_svg, output_png):
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica", "Arial"]
    plt.rcParams["mathtext.fontset"] = "cm"

    fig, ax = plt.subplots(figsize=(7.2, 6.6), dpi=300)
    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(0, 9.6)
    ax.axis("off")

    # ------------------------------------------------------------------ #
    # Triangle geometry (equilateral)
    # ------------------------------------------------------------------ #
    cx = 5.0
    top = (cx, 8.05)
    bl  = (1.55, 2.15)
    br  = (8.45, 2.15)

    tri_bg = patches.Polygon(
        [top, bl, br], closed=True,
        facecolor=BG_NEUTRAL, edgecolor="none", zorder=1
    )
    ax.add_patch(tri_bg)

    # Solid black edges connecting the three vertices
    edge_specs = [
        (top, bl),
        (top, br),
        (bl,  br),
    ]
    for p, q in edge_specs:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=BLACK, lw=4.8,
                solid_capstyle="round", zorder=3)

    # ------------------------------------------------------------------ #
    # Vertex cards (all identical size)
    # ------------------------------------------------------------------ #
    CW, CH = 3.05, 1.45

    def vertex_card(anchor, ec, fc, title, approach, dx=0.0, dy=0.0):
        x = anchor[0] - CW / 2 + dx
        y = anchor[1] - CH / 2 + dy
        # soft drop shadow
        shadow = FancyBboxPatch(
            (x + 0.07, y - 0.10), CW, CH,
            boxstyle="round,pad=0.02,rounding_size=0.14",
            ec="none", fc="#000000", alpha=0.10, zorder=4,
        )
        ax.add_patch(shadow)
        card = FancyBboxPatch(
            (x, y), CW, CH,
            boxstyle="round,pad=0.02,rounding_size=0.14",
            ec=ec, fc=fc, lw=2.1, zorder=5,
        )
        ax.add_patch(card)
        ccx, ccy = x + CW / 2, y + CH / 2
        ax.text(ccx, ccy + 0.28, title, fontsize=14, fontweight="bold",
                color=ec, ha="center", va="center", linespacing=1.05, zorder=6)
        ax.text(ccx, ccy - 0.44, approach, fontsize=11, color=BLACK,
                ha="center", va="center", zorder=6)

    vertex_card(
        top, DARK_PURPLE, BG_PURPLE,
        "Physical Model\nAccuracy", "e.g. MINLP / NLP", dy=0.60,
    )
    vertex_card(
        bl, DARK_GREEN, BG_GREEN,
        "Computational\nTractability", "e.g. MILP / LP",
        dx=0.0, dy=-0.60,
    )
    vertex_card(
        br, DARK_RED, BG_RED,
        "Operational\nUncertainty", "e.g. RL / Stochastic",
        dx=0.0, dy=-0.60,
    )

    # ------------------------------------------------------------------ #
    # Edge (trade-off) labels: horizontal, placed OUTSIDE the triangle
    # ------------------------------------------------------------------ #
    centroid = ((top[0] + bl[0] + br[0]) / 3, (top[1] + bl[1] + br[1]) / 3)

    # ------------------------------------------------------------------ #
    # Central annotation
    # ------------------------------------------------------------------ #
    # visual centre nudged slightly up from the geometric centroid
    centre = (centroid[0], centroid[1] + 0.35)
    # tri-colour ring echoing the three vertices (each 120-deg arc)
    R = 0.95
    arc_specs = [
        (DARK_PURPLE,  30, 150),   # top
        (DARK_GREEN,  150, 270),   # bottom-left
        (DARK_RED,    270, 390),   # bottom-right
    ]
    for col, a0, a1 in arc_specs:
        ax.add_patch(patches.Arc(
            centre, 2 * R, 2 * R, angle=0, theta1=a0, theta2=a1,
            edgecolor=col, lw=2.8, zorder=5))
    circ = patches.Circle(centre, R - 0.06, facecolor="white",
                          edgecolor="none", zorder=4)
    ax.add_patch(circ)
    ax.text(centre[0], centre[1] + 0.20, "Modeling", fontsize=10.5,
            fontweight="bold", color=BLACK, ha="center", va="center", zorder=6)
    ax.text(centre[0], centre[1] - 0.14, "Trilemma", fontsize=10.5,
            fontweight="bold", color=BLACK, ha="center", va="center", zorder=6)

    plt.tight_layout()
    plt.savefig(output_svg, format="svg", bbox_inches="tight", transparent=False)
    plt.savefig(output_png, format="png", dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_svg}\nSaved: {output_png}")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    create_figure(
        os.path.join(here, "modeling_trilemma_tradeoffs.svg"),
        os.path.join(here, "modeling_trilemma_tradeoffs.png"),
    )
