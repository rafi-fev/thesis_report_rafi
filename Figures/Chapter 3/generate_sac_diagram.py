import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

def draw_cylinder(ax, x_center, y_bottom, width, height, cap_height, ec, fc, lw=2.2, zorder=5):
    """
    Draws a stylized, clean 3D database cylinder for the Replay Buffer.
    """
    r_w = width / 2.0
    r_h = cap_height / 2.0
    
    # Lower body & bottom curved base
    body_path_data = [
        (Path.MOVETO, (x_center - r_w, y_bottom + r_h)),
        (Path.LINETO, (x_center - r_w, y_bottom + height - r_h)),
        (Path.CURVE4, (x_center - r_w, y_bottom + height + r_h)),
        (Path.CURVE4, (x_center + r_w, y_bottom + height + r_h)),
        (Path.CURVE4, (x_center + r_w, y_bottom + height - r_h)),
        (Path.LINETO, (x_center + r_w, y_bottom + r_h)),
        (Path.CURVE4, (x_center + r_w, y_bottom - r_h)),
        (Path.CURVE4, (x_center - r_w, y_bottom - r_h)),
        (Path.CURVE4, (x_center - r_w, y_bottom + r_h)),
        (Path.CLOSEPOLY, (x_center - r_w, y_bottom + r_h)),
    ]
    codes, verts = zip(*body_path_data)
    path = Path(verts, codes)
    patch_body = patches.PathPatch(path, facecolor=fc, edgecolor=ec, lw=lw, zorder=zorder)
    ax.add_patch(patch_body)
    
    # Top elliptical surface
    top_cap = patches.Ellipse(
        (x_center, y_bottom + height - r_h),
        width=width, height=cap_height,
        facecolor=fc, edgecolor=ec, lw=lw, zorder=zorder + 1
    )
    ax.add_patch(top_cap)


def generate_sac_diagram():
    """
    Generates a publication-grade vector SVG diagram of the Soft Actor-Critic (SAC) 
    architecture adapted for the Hybrid BPtMeOH system.
    """
    # Publication Typography: Modern Clean Sans-serif with Computer Modern Math
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica', 'Arial', 'Liberation Sans']
    plt.rcParams['mathtext.fontset'] = 'cm'

    # Color Palette according to exact FEV specifications
    DARK_PURPLE = '#41098B'  # RGB(65,9,139) - Critic & Q-Networks
    DARK_RED    = '#B9052D'  # RGB(185,5,45) - Actor & Policy Network
    DARK_TEAL   = '#005666'  # RGB(0,86,102) - Replay Buffer
    BLACK       = '#000000'  # RGB(0,0,0)    - Flow arrows & labels
    DARK_GREEN  = '#21762D'  # RGB(33,118,45) - Hybrid BPtMeOH Environment

    # Soft tint fills for clean, modern card styling
    BG_PURPLE_LIGHT = '#F6F2FC'
    BG_PURPLE_INNER = '#EBE2F8'
    BG_RED_LIGHT    = '#FDF2F4'
    BG_RED_INNER    = '#F8D8DE'
    BG_TEAL_LIGHT   = '#EBF5F7'
    BG_GREEN_LIGHT  = '#EFF7F0'

    # Canvas Setup
    fig, ax = plt.subplots(figsize=(11.0, 9.8), dpi=300)
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 9.8)
    ax.axis('off')

    # Line Weights & Arrow Props
    LW_FLOW = 2.0
    ARROW_STYLE = dict(arrowstyle='->,head_width=0.45,head_length=0.7', color=BLACK, lw=LW_FLOW)

    # -------------------------------------------------------------------------
    # 1. Replay Buffer (Top Center)
    # -------------------------------------------------------------------------
    rb_cx, rb_bottom, rb_w, rb_h, rb_cap = 5.5, 8.0, 3.6, 1.25, 0.45
    draw_cylinder(ax, rb_cx, rb_bottom, rb_w, rb_h, rb_cap, ec=DARK_TEAL, fc=BG_TEAL_LIGHT, lw=2.2, zorder=5)
    ax.text(rb_cx, rb_bottom + 0.48, "Replay Buffer",
            fontsize=18, fontweight='bold', color=DARK_TEAL, ha='center', va='center', zorder=7)

    # -------------------------------------------------------------------------
    # 2. Actor Module (Middle Left)
    # -------------------------------------------------------------------------
    actor_x, actor_y, actor_w, actor_h = 1.4, 3.2, 3.3, 3.8
    actor_box = patches.FancyBboxPatch(
        (actor_x, actor_y), actor_w, actor_h,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        ec=DARK_RED, fc=BG_RED_LIGHT, lw=2.2, zorder=4
    )
    ax.add_patch(actor_box)
    ax.text(actor_x + actor_w / 2.0, actor_y + actor_h - 0.48, "Actor",
            fontsize=21, fontweight='bold', color=DARK_RED, ha='center', va='center', zorder=6)

    # Policy Network Sub-card inside Actor
    pn_x, pn_y, pn_w, pn_h = actor_x + 0.25, actor_y + 0.55, actor_w - 0.5, 1.9
    pn_box = patches.FancyBboxPatch(
        (pn_x, pn_y), pn_w, pn_h,
        boxstyle="round,pad=0.03,rounding_size=0.1",
        ec=DARK_RED, fc=BG_RED_INNER, lw=1.8, zorder=5
    )
    ax.add_patch(pn_box)
    ax.text(pn_x + pn_w / 2.0, pn_y + pn_h - 0.52, "Policy Network",
            fontsize=15, fontweight='bold', color=DARK_RED, ha='center', va='center', zorder=6)
    ax.text(pn_x + pn_w / 2.0, pn_y + 0.5, r"$\pi_\phi(\mathbf{a} \mid \mathbf{s})$",
            fontsize=19, fontweight='normal', color=DARK_RED, ha='center', va='center', zorder=6)

    # -------------------------------------------------------------------------
    # 3. Critic Module (Middle Right)
    # -------------------------------------------------------------------------
    critic_x, critic_y, critic_w, critic_h = 6.6, 1.8, 3.8, 5.2
    critic_box = patches.FancyBboxPatch(
        (critic_x, critic_y), critic_w, critic_h,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        ec=DARK_PURPLE, fc=BG_PURPLE_LIGHT, lw=2.2, zorder=4
    )
    ax.add_patch(critic_box)
    ax.text(critic_x + critic_w / 2.0, critic_y + critic_h - 0.48, "Critic",
            fontsize=21, fontweight='bold', color=DARK_PURPLE, ha='center', va='center', zorder=6)

    # Main Q-networks Sub-card
    mq_x, mq_y, mq_w, mq_h = critic_x + 0.25, critic_y + 2.8, critic_w - 0.5, 1.65
    mq_box = patches.FancyBboxPatch(
        (mq_x, mq_y), mq_w, mq_h,
        boxstyle="round,pad=0.03,rounding_size=0.1",
        ec=DARK_PURPLE, fc=BG_PURPLE_INNER, lw=1.8, zorder=5
    )
    ax.add_patch(mq_box)
    ax.text(mq_x + mq_w / 2.0, mq_y + mq_h - 0.5, "Main Q-networks",
            fontsize=15, fontweight='bold', color=DARK_PURPLE, ha='center', va='center', zorder=6)
    ax.text(mq_x + mq_w / 2.0, mq_y + 0.45, r"$Q_{\theta_1}(\mathbf{s},\mathbf{a}), \, Q_{\theta_2}(\mathbf{s},\mathbf{a})$",
            fontsize=15, fontweight='normal', color=DARK_PURPLE, ha='center', va='center', zorder=6)

    # Target Q-networks Sub-card
    tq_x, tq_y, tq_w, tq_h = critic_x + 0.25, critic_y + 0.35, critic_w - 0.5, 1.65
    tq_box = patches.FancyBboxPatch(
        (tq_x, tq_y), tq_w, tq_h,
        boxstyle="round,pad=0.03,rounding_size=0.1",
        ec=DARK_PURPLE, fc=BG_PURPLE_INNER, lw=1.8, zorder=5
    )
    ax.add_patch(tq_box)
    ax.text(tq_x + tq_w / 2.0, tq_y + tq_h - 0.5, "Target Q-networks",
            fontsize=15, fontweight='bold', color=DARK_PURPLE, ha='center', va='center', zorder=6)
    ax.text(tq_x + tq_w / 2.0, tq_y + 0.45, r"$Q_{\bar{\theta}_1}(\mathbf{s},\mathbf{a}), \, Q_{\bar{\theta}_2}(\mathbf{s},\mathbf{a})$",
            fontsize=15, fontweight='normal', color=DARK_PURPLE, ha='center', va='center', zorder=6)

    # Soft Update arrow inside Critic
    ax.annotate('', xy=(critic_x + critic_w / 2.0, tq_y + tq_h),
                xytext=(critic_x + critic_w / 2.0, mq_y),
                arrowprops=ARROW_STYLE, zorder=8)
    ax.text(critic_x + critic_w / 2.0 + 0.15, (mq_y + tq_y + tq_h) / 2.0, "Soft Update",
            fontsize=14, color=BLACK, fontweight='bold', ha='left', va='center', zorder=8)

    # -------------------------------------------------------------------------
    # 4. Environment Module (Hybrid BPtMeOH - Bottom Left)
    # -------------------------------------------------------------------------
    env_x, env_y, env_w, env_h = 1.4, 0.7, 3.3, 1.3
    env_box = patches.FancyBboxPatch(
        (env_x, env_y), env_w, env_h,
        boxstyle="round,pad=0.04,rounding_size=0.15",
        ec=DARK_GREEN, fc=BG_GREEN_LIGHT, lw=2.2, zorder=4
    )
    ax.add_patch(env_box)
    ax.text(env_x + env_w / 2.0, env_y + env_h / 2.0, "Hybrid BPtMeOH",
            fontsize=17, fontweight='bold', color=DARK_GREEN, ha='center', va='center', zorder=6)

    # -------------------------------------------------------------------------
    # 5. Inter-Module Arrows & Labels (Color: Black, Clean Layout)
    # -------------------------------------------------------------------------

    # Flow A: Replay Buffer -> Actor (Sample Tuples)
    rb_sample_actor_x = 2.6
    ax.plot([rb_cx - rb_w / 2.0, rb_sample_actor_x], [rb_bottom + 0.5, rb_bottom + 0.5], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.plot([rb_sample_actor_x, rb_sample_actor_x], [rb_bottom + 0.5, actor_y + actor_h], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.annotate('', xy=(rb_sample_actor_x, actor_y + actor_h),
                xytext=(rb_sample_actor_x, actor_y + actor_h + 0.2),
                arrowprops=ARROW_STYLE, zorder=9)
    ax.text(rb_sample_actor_x - 0.18, 7.6, "Sample\nTuples",
            fontsize=13.5, fontweight='bold', color=BLACK, ha='right', va='center', zorder=9)

    # Flow B: Actor -> Replay Buffer (Store Tuples)
    actor_store_x = 3.4
    rb_store_x = 5.0
    rb_base_y = rb_bottom
    ax.plot([actor_store_x, actor_store_x], [actor_y + actor_h, 7.35], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.plot([actor_store_x, rb_store_x], [7.35, 7.35], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.plot([rb_store_x, rb_store_x], [7.35, rb_base_y], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.annotate('', xy=(rb_store_x, rb_base_y),
                xytext=(rb_store_x, rb_base_y - 0.2),
                arrowprops=ARROW_STYLE, zorder=9)
    ax.text((actor_store_x + rb_store_x) / 2.0, 7.45, "Store Tuples",
            fontsize=13.5, fontweight='bold', color=BLACK, ha='center', va='bottom', zorder=9)

    # Flow C: Replay Buffer -> Critic (Sample Tuples)
    rb_sample_critic_x = 8.5
    ax.plot([rb_cx + rb_w / 2.0, rb_sample_critic_x], [rb_bottom + 0.5, rb_bottom + 0.5], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.plot([rb_sample_critic_x, rb_sample_critic_x], [rb_bottom + 0.5, critic_y + critic_h], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.annotate('', xy=(rb_sample_critic_x, critic_y + critic_h),
                xytext=(rb_sample_critic_x, critic_y + critic_h + 0.2),
                arrowprops=ARROW_STYLE, zorder=9)
    ax.text(rb_sample_critic_x + 0.18, 7.6, "Sample\nTuples",
            fontsize=13.5, fontweight='bold', color=BLACK, ha='left', va='center', zorder=9)

    # Flow D: Evaluate Policy (Policy Network -> Main Q-networks)
    y_eval = pn_y + 0.6
    ax.plot([pn_x + pn_w, mq_x], [y_eval, y_eval], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.annotate('', xy=(mq_x, y_eval),
                xytext=(mq_x - 0.2, y_eval),
                arrowprops=ARROW_STYLE, zorder=9)
    ax.text((actor_x + actor_w + critic_x) / 2.0, y_eval + 0.12, "Evaluate Policy",
            fontsize=13.5, fontweight='bold', color=BLACK, ha='center', va='bottom', zorder=9)

    # Flow E: Improve Policy (Main Q-networks -> Policy Network)
    y_improve = mq_y + mq_h - 0.4
    x_improve_drop = pn_x + pn_w / 2.0
    ax.plot([mq_x, x_improve_drop], [y_improve, y_improve], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.plot([x_improve_drop, x_improve_drop], [y_improve, pn_y + pn_h], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.annotate('', xy=(x_improve_drop, pn_y + pn_h),
                xytext=(x_improve_drop, pn_y + pn_h + 0.2),
                arrowprops=ARROW_STYLE, zorder=9)
    ax.text((actor_x + actor_w + critic_x) / 2.0, y_improve + 0.12, "Improve Policy",
            fontsize=13.5, fontweight='bold', color=BLACK, ha='center', va='bottom', zorder=9)

    # Flow F: State s_t (Hybrid BPtMeOH -> Actor)
    x_st = 3.05
    ax.plot([x_st, x_st], [env_y + env_h, actor_y], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.annotate('', xy=(x_st, actor_y),
                xytext=(x_st, actor_y - 0.2),
                arrowprops=ARROW_STYLE, zorder=9)
    ax.text(x_st + 0.22, (env_y + env_h + actor_y) / 2.0, r"$\mathbf{s}_t$",
            fontsize=21, fontweight='bold', color=BLACK, ha='left', va='center', zorder=9)

    # Flow G: Action a_t (Actor -> Hybrid BPtMeOH)
    x_at_turn = 0.7
    y_actor_act = actor_y + 1.4
    y_env_act = env_y + env_h / 2.0
    ax.plot([actor_x, x_at_turn], [y_actor_act, y_actor_act], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.plot([x_at_turn, x_at_turn], [y_actor_act, y_env_act], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.plot([x_at_turn, env_x], [y_env_act, y_env_act], color=BLACK, lw=LW_FLOW, zorder=8)
    ax.annotate('', xy=(env_x, y_env_act),
                xytext=(env_x - 0.2, y_env_act),
                arrowprops=ARROW_STYLE, zorder=9)
    ax.text(x_at_turn - 0.15, (y_actor_act + y_env_act) / 2.0, r"$\mathbf{a}_t$",
            fontsize=21, fontweight='bold', color=BLACK, ha='right', va='center', zorder=9)

    plt.tight_layout()

    # Save SVG vector graphic and PNG preview
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(script_dir, "sac_structure_diagram.svg")
    png_path = os.path.join(script_dir, "sac_structure_diagram_preview.png")

    plt.savefig(svg_path, format='svg', bbox_inches='tight', transparent=True)
    plt.savefig(png_path, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    print(f"SAC Diagram successfully generated:\n- SVG: {svg_path}\n- PNG Preview: {png_path}")

if __name__ == "__main__":
    generate_sac_diagram()
