import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path


def setup_typography():
    """Configures publication typography with sans-serif fonts and LaTeX math."""
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica', 'Arial', 'Liberation Sans']
    plt.rcParams['mathtext.fontset'] = 'cm'


def draw_header_card(ax, x, y, w, h, title, banner_bg, border_color, fill_bg, header_h=0.68):
    """Draws a card with a colored header banner, body fill, and border."""
    # Outer container
    card = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.01,rounding_size=0.12",
        ec=border_color, fc=fill_bg, lw=1.8, zorder=2
    )
    ax.add_patch(card)

    # Top banner with rounded top
    banner = patches.FancyBboxPatch(
        (x, y + h - header_h), w, header_h,
        boxstyle="round,pad=0.01,rounding_size=0.12",
        ec=banner_bg, fc=banner_bg, lw=1.0, zorder=3
    )
    ax.add_patch(banner)

    # Square off bottom of banner
    banner_bottom = patches.Rectangle(
        (x, y + h - header_h), w, header_h * 0.5,
        facecolor=banner_bg, edgecolor=banner_bg, lw=0, zorder=3
    )
    ax.add_patch(banner_bottom)

    # Header Title
    ax.text(x + w / 2.0, y + h - header_h / 2.0, title,
            fontsize=11.5, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4)


def draw_upper_level_bo(ax, x, y, w, h):
    """
    Renders Upper-Level Bayesian Optimization block with formal text and equations.
    """
    DARK_PURPLE = '#41098B'
    BG_PURPLE   = '#F6F2FC'
    INNER_BG    = '#FFFFFF'
    BORDER_SUB  = '#DDD6FE'

    draw_header_card(ax, x, y, w, h, "Upper-Level: Bayesian Optimization", DARK_PURPLE, DARK_PURPLE, BG_PURPLE)

    # Block 1: Objective & Sizing Vector
    b1_y = y + h - 1.45
    b1_h = 0.65
    box1 = patches.FancyBboxPatch(
        (x + 0.25, b1_y), w - 0.50, b1_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        ec=BORDER_SUB, fc=INNER_BG, lw=1.1, zorder=4
    )
    ax.add_patch(box1)
    ax.text(x + 0.45, b1_y + b1_h / 2.0, r"$\min_{\mathbf{x}}\ \mathrm{LCOM}(\mathbf{x})$",
            fontsize=10.0, fontweight='bold', color=DARK_PURPLE, ha='left', va='center', zorder=5)
    ax.text(x + w - 0.45, b1_y + b1_h / 2.0, "Global Capacity Sizing",
            fontsize=8.8, fontweight='bold', color='#6B21A8', ha='right', va='center', zorder=5)

    # Block 2: Decision Variables Breakdown
    b2_y = y + h - 2.30
    b2_h = 0.72
    box2 = patches.FancyBboxPatch(
        (x + 0.25, b2_y), w - 0.50, b2_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        ec=BORDER_SUB, fc=INNER_BG, lw=1.1, zorder=4
    )
    ax.add_patch(box2)
    ax.text(x + 0.45, b2_y + 0.48, r"$\mathbf{x} = \left[ P_\mathrm{PV},\ P_\mathrm{WT},\ E_\mathrm{BESS},\ P_\mathrm{ATR},\ E_{\mathrm{H}_2\mathrm{SS}},\ E_\mathrm{BGSS},\ P_\mathrm{AWE},\ \dot{m}_\mathrm{MeOH},\ \dot{m}_\mathrm{Dist},\ P_\mathrm{Gen} \right]^\top$",
            fontsize=8.2, color='#0F172A', ha='left', va='center', zorder=5)
    ax.text(x + 0.45, b2_y + 0.18, r"10-dimensional bounded design space: $\mathbf{x}_\mathrm{min} \leq \mathbf{x} \leq \mathbf{x}_\mathrm{max}$",
            fontsize=8.0, color='#475569', ha='left', va='center', zorder=5)

    # Block 3: Surrogate Modeling
    b3_y = y + h - 3.10
    b3_h = 0.68
    box3 = patches.FancyBboxPatch(
        (x + 0.25, b3_y), w - 0.50, b3_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        ec=BORDER_SUB, fc=INNER_BG, lw=1.1, zorder=4
    )
    ax.add_patch(box3)
    ax.text(x + 0.45, b3_y + 0.45, r"Gaussian Process Surrogate: $f(\mathbf{x}) \sim \mathcal{GP}\left(\mu(\mathbf{x}),\ k(\mathbf{x}, \mathbf{x}')\right)$",
            fontsize=8.6, fontweight='bold', color=DARK_PURPLE, ha='left', va='center', zorder=5)
    ax.text(x + 0.45, b3_y + 0.18, r"Matérn $3/2$ kernel with iterative posterior updates $\mathcal{D}_n = \{(\mathbf{x}_i, y_i)\}_{i=1}^n$",
            fontsize=7.8, color='#475569', ha='left', va='center', zorder=5)

    # Block 4: Acquisition Policy
    b4_y = y + 0.20
    b4_h = 0.55
    box4 = patches.FancyBboxPatch(
        (x + 0.25, b4_y), w - 0.50, b4_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        ec=BORDER_SUB, fc=INNER_BG, lw=1.1, zorder=4
    )
    ax.add_patch(box4)
    ax.text(x + 0.45, b4_y + b4_h / 2.0, r"Next Evaluation Query: $\mathbf{x}_{n+1} = \arg\max_{\mathbf{x}}\ \alpha(\mathbf{x} \mid \mathcal{D}_n)$",
            fontsize=8.8, fontweight='bold', color='#B9052D', ha='left', va='center', zorder=5)
    ax.text(x + w - 0.45, b4_y + b4_h / 2.0, "(Expected Improvement)",
            fontsize=8.0, color='#6B21A8', ha='right', va='center', zorder=5)


def draw_lower_level_milp(ax, x, y, w, h):
    """
    Renders Lower-Level Exact MILP Dispatch block with formal text and equations.
    """
    DARK_TEAL  = '#005666'
    BG_TEAL    = '#EBF5F7'
    INNER_BG   = '#FFFFFF'
    BORDER_SUB = '#BAE6FD'

    draw_header_card(ax, x, y, w, h, "Lower-Level: Exact MILP Dispatch Strategy", DARK_TEAL, DARK_TEAL, BG_TEAL)

    # Block 1: Objective Formulation
    b1_y = y + h - 1.45
    b1_h = 0.65
    box1 = patches.FancyBboxPatch(
        (x + 0.25, b1_y), w - 0.50, b1_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        ec=BORDER_SUB, fc=INNER_BG, lw=1.1, zorder=4
    )
    ax.add_patch(box1)
    ax.text(x + 0.45, b1_y + b1_h / 2.0, r"$\min_{\mathbf{u}}\ \sum_{t=1}^{8760} C_t(\mathbf{u}_t \mid \mathbf{x})$",
            fontsize=10.0, fontweight='bold', color=DARK_TEAL, ha='left', va='center', zorder=5)
    ax.text(x + w - 0.45, b1_y + b1_h / 2.0, "Operational Cost Minimization",
            fontsize=8.8, fontweight='bold', color='#0E7490', ha='right', va='center', zorder=5)

    # Block 2: Operational Dispatch Decision Vector
    b2_y = y + h - 2.30
    b2_h = 0.72
    box2 = patches.FancyBboxPatch(
        (x + 0.25, b2_y), w - 0.50, b2_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        ec=BORDER_SUB, fc=INNER_BG, lw=1.1, zorder=4
    )
    ax.add_patch(box2)
    ax.text(x + 0.45, b2_y + 0.48, r"Hourly Dispatch Vector: $\mathbf{u}_t = \left[ P_{t,\mathrm{grid}},\ P_{t,\mathrm{curt}},\ P_{t,\mathrm{ch}},\ P_{t,\mathrm{dis}},\ \dot{m}_{t,\mathrm{H}_2},\ \dot{m}_{t,\mathrm{MeOH}} \right]^\top$",
            fontsize=8.2, color='#0F172A', ha='left', va='center', zorder=5)
    ax.text(x + 0.45, b2_y + 0.18, r"Hourly simulation over full annual horizon: $t \in \{1, 2, \dots, 8760\ \mathrm{h}\}$",
            fontsize=8.0, color='#475569', ha='left', va='center', zorder=5)

    # Block 3: Physical System Constraints
    b3_y = y + h - 3.10
    b3_h = 0.68
    box3 = patches.FancyBboxPatch(
        (x + 0.25, b3_y), w - 0.50, b3_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        ec=BORDER_SUB, fc=INNER_BG, lw=1.1, zorder=4
    )
    ax.add_patch(box3)
    ax.text(x + 0.45, b3_y + 0.45, r"Linear System Constraints: $\mathbf{A}\mathbf{u} \leq \mathbf{b}(\mathbf{x}),\quad \mathbf{A}_\mathrm{eq}\mathbf{u} = \mathbf{b}_\mathrm{eq}(\mathbf{x})$",
            fontsize=8.6, fontweight='bold', color=DARK_TEAL, ha='left', va='center', zorder=5)
    ax.text(x + 0.45, b3_y + 0.18, r"Energy & mass balances, unit ramping, component capacities & SOC bounds",
            fontsize=7.8, color='#475569', ha='left', va='center', zorder=5)

    # Block 4: Solution Method
    b4_y = y + 0.20
    b4_h = 0.55
    box4 = patches.FancyBboxPatch(
        (x + 0.25, b4_y), w - 0.50, b4_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        ec=BORDER_SUB, fc=INNER_BG, lw=1.1, zorder=4
    )
    ax.add_patch(box4)
    ax.text(x + 0.45, b4_y + b4_h / 2.0, r"Exact MILP Solver Solution $\to \mathbf{u}^*,\ \mathrm{OPEX}^*$",
            fontsize=8.8, fontweight='bold', color='#005666', ha='left', va='center', zorder=5)
    ax.text(x + w - 0.45, b4_y + b4_h / 2.0, "(Global Optimality Guaranteed)",
            fontsize=8.0, color='#0E7490', ha='right', va='center', zorder=5)


def draw_system_outcomes(ax, x, y, w, h):
    """
    Renders System Outcomes & LCOM block with formal equations and metrics.
    """
    DARK_GREEN = '#21762D'
    BG_GREEN   = '#EFF7F0'
    INNER_BG   = '#FFFFFF'
    BORDER_SUB = '#BBF7D0'

    draw_header_card(ax, x, y, w, h, "System Outcomes: Techno-Economic Evaluation", DARK_GREEN, DARK_GREEN, BG_GREEN, header_h=0.55)

    # Formula Box
    f_y = y + 0.18
    f_h = h - 0.82
    fbox = patches.FancyBboxPatch(
        (x + 0.25, f_y), w - 0.50, f_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        ec=BORDER_SUB, fc=INNER_BG, lw=1.2, zorder=4
    )
    ax.add_patch(fbox)

    formula_str = r"$\mathrm{LCOM}(\mathbf{x}) = \frac{\mathrm{CAPEX}(\mathbf{x}) + \mathrm{OPEX}^*(\mathbf{u}^* \mid \mathbf{x})}{M_\mathrm{MeOH}} \quad \left[\frac{\mathrm{EUR}}{\mathrm{kg\ MeOH}}\right]$"
    ax.text(x + w / 2.0, f_y + f_h * 0.65, formula_str,
            fontsize=9.8, fontweight='bold', color='#0F172A', ha='center', va='center', zorder=5)

    ax.text(x + w / 2.0, f_y + f_h * 0.25, r"$\mathrm{CAPEX}(\mathbf{x})$: Annualized investment  $\mid$  $\mathrm{OPEX}^*$: Optimal annual operations  $\mid$  $M_\mathrm{MeOH}$: Net yield",
            fontsize=7.8, color='#334155', ha='center', va='center', zorder=5)


def draw_process_arrows(ax, bo_x, bo_y, bo_w, bo_h, milp_x, milp_y, milp_w, milp_h, out_x, out_y, out_w, out_h):
    """
    Renders connecting flow arrows and the curved feedback loop for the process cycle.
    """
    ARROW_DARK = '#0F172A'
    FEV_RED    = '#B9052D'

    # 1. Forward Arrow: Upper BO -> Lower MILP
    arrow1_y = bo_y + bo_h * 0.52
    ax.annotate(
        '', xy=(milp_x, arrow1_y), xytext=(bo_x + bo_w, arrow1_y),
        arrowprops=dict(arrowstyle='->,head_width=0.45,head_length=0.7', color=ARROW_DARK, lw=2.2),
        zorder=10
    )
    ax.text(
        (bo_x + bo_w + milp_x) / 2.0, arrow1_y + 0.18,
        "Trial capacity sizing\nparameters " + r"$\mathbf{x}$",
        fontsize=8.5, fontweight='bold', color=ARROW_DARK, ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFFFFF', edgecolor='#DDD6FE', lw=1.0),
        zorder=11
    )

    # 2. Forward Arrow: Lower MILP -> System Outcomes
    arrow2_x = out_x + out_w * 0.50
    ax.annotate(
        '', xy=(arrow2_x, out_y + out_h), xytext=(arrow2_x, milp_y),
        arrowprops=dict(arrowstyle='->,head_width=0.45,head_length=0.7', color=ARROW_DARK, lw=2.2),
        zorder=10
    )
    ax.text(
        arrow2_x + 0.20, (milp_y + out_y + out_h) / 2.0,
        "Optimal dispatch " + r"$\mathbf{u}^*$" + "\n& operational cost " + r"$\mathrm{OPEX}^*$",
        fontsize=8.2, fontweight='bold', color=ARROW_DARK, ha='left', va='center',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFFFFF', edgecolor='#BAE6FD', lw=1.0),
        zorder=11
    )

    # 3. Sweeping Curved Feedback Arrow: System Outcomes -> Upper BO
    start_pt = (out_x, out_y + out_h * 0.5)
    target_pt = (bo_x + bo_w * 0.50, bo_y)
    corner_x = target_pt[0]
    corner_y = start_pt[1]
    radius = 0.65

    verts = [
        start_pt,
        (corner_x + radius, corner_y),
        (corner_x, corner_y),
        (corner_x, corner_y + radius),
        target_pt
    ]
    codes = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', edgecolor=FEV_RED, lw=2.2, zorder=10)
    ax.add_patch(patch)

    ax.annotate(
        '', xy=target_pt, xytext=(target_pt[0], target_pt[1] - 0.15),
        arrowprops=dict(arrowstyle='->,head_width=0.45,head_length=0.7', color=FEV_RED, lw=2.2),
        zorder=11
    )

    # Feedback label badge centered cleanly along horizontal segment
    mid_badge_x = (start_pt[0] + corner_x + radius) / 2.0
    ax.text(
        mid_badge_x, start_pt[1] + 0.18,
        r"Feedback update: Return observed $\mathrm{LCOM}(\mathbf{x})$ to update GP surrogate",
        fontsize=8.0, fontweight='bold', color=FEV_RED, ha='center', va='bottom',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#FEF2F2', edgecolor=FEV_RED, lw=1.1),
        zorder=12
    )


def generate_bilevel_figure():
    """Generates the clean text and equation bi-level process cycle figure."""
    setup_typography()

    fig_w, fig_h = 13.6, 7.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis('off')

    # Card dimensions
    bo_x, bo_y, bo_w, bo_h = 0.6, 2.4, 5.6, 4.1
    milp_x, milp_y, milp_w, milp_h = 7.4, 2.4, 5.6, 4.1
    out_x, out_y, out_w, out_h = 7.4, 0.45, 5.6, 1.35

    # 1. Render Component Blocks
    draw_upper_level_bo(ax, bo_x, bo_y, bo_w, bo_h)
    draw_lower_level_milp(ax, milp_x, milp_y, milp_w, milp_h)
    draw_system_outcomes(ax, out_x, out_y, out_w, out_h)

    # 2. Render Process Cycle Arrows
    draw_process_arrows(ax, bo_x, bo_y, bo_w, bo_h, milp_x, milp_y, milp_w, milp_h, out_x, out_y, out_w, out_h)

    plt.tight_layout()

    # Save outputs
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(script_dir, "bilevel_bo_milp_architecture.svg")
    png_path = os.path.join(script_dir, "bilevel_bo_milp_architecture_preview.png")

    plt.savefig(svg_path, format='svg', bbox_inches='tight', transparent=False)
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()

    print("[SUCCESS] Publication-grade Bi-level Process Cycle diagram generated successfully:")
    print(f"  - SVG: {svg_path}")
    print(f"  - PNG: {png_path}")


if __name__ == '__main__':
    generate_bilevel_figure()
