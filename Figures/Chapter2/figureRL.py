import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_mdp_diagram():
    """
    Generates a publication-ready Markov Decision Process (MDP) Agent-Environment 
    interaction diagram in vector SVG format for a Master's Thesis.
    
    Color palette: Academic Navy Blue line styling (#1B365D).
    """
    # Configure publication-quality typography
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica', 'Arial', 'Liberation Sans']
    plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern for standard academic math typesetting

    # Academic Color Scheme
    NAVY = '#1B365D'        # Navy blue for lines, arrows, box borders, and typography
    BOX_BG = '#FFFFFF'      # Pure white box fill

    # Canvas Setup
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=300)
    ax.set_xlim(0, 9.8)
    ax.set_ylim(0, 4.8)
    ax.axis('off')

    # Line Weights (distinguishing vector quantities S, A from scalar reward R)
    LW_BOLD = 2.4   # State (S_t) and Action (A_t)
    LW_REG  = 1.5   # Reward (R_t)

    # -------------------------------------------------------------------------
    # 1. Boxes (Agent & Environment)
    # -------------------------------------------------------------------------
    # Agent Box (Top)
    agent_x, agent_y, agent_w, agent_h = 4.4, 3.2, 2.4, 1.1
    agent_box = patches.FancyBboxPatch(
        (agent_x, agent_y), agent_w, agent_h,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        ec=NAVY, fc=BOX_BG, lw=2.2, zorder=5
    )
    ax.add_patch(agent_box)
    ax.text(agent_x + agent_w / 2.0, agent_y + agent_h / 2.0, "Agent",
            fontsize=21, fontweight='normal', color=NAVY,
            ha='center', va='center', zorder=6)

    # Environment Box (Bottom)
    env_x, env_y, env_w, env_h = 3.8, 0.5, 3.4, 1.1
    env_box = patches.FancyBboxPatch(
        (env_x, env_y), env_w, env_h,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        ec=NAVY, fc=BOX_BG, lw=2.2, zorder=5
    )
    ax.add_patch(env_box)
    ax.text(env_x + env_w / 2.0, env_y + env_h / 2.0, "Environment",
            fontsize=21, fontweight='normal', color=NAVY,
            ha='center', va='center', zorder=6)

    # Key Anchor Coordinates
    agent_left_upper = (agent_x, agent_y + 0.85)
    agent_left_lower = (agent_x, agent_y + 0.28)
    agent_right_out   = (agent_x + agent_w, agent_y + 0.55)

    env_right_in     = (env_x + env_w, env_y + 0.55)
    env_left_upper   = (env_x, env_y + 0.85)
    env_left_lower   = (env_x, env_y + 0.28)

    # -------------------------------------------------------------------------
    # 2. Action Arrow (Right side: Agent -> Environment)
    # -------------------------------------------------------------------------
    x_action_turn = 8.5

    # Orthogonal Path: Right -> Down -> Left into Environment
    ax.plot([agent_right_out[0], x_action_turn], [agent_right_out[1], agent_right_out[1]], color=NAVY, lw=LW_BOLD, zorder=3)
    ax.plot([x_action_turn, x_action_turn], [agent_right_out[1], env_right_in[1]], color=NAVY, lw=LW_BOLD, zorder=3)
    ax.plot([x_action_turn, env_right_in[0] + 0.15], [env_right_in[1], env_right_in[1]], color=NAVY, lw=LW_BOLD, zorder=3)

    # Arrowhead pointing into Environment box
    ax.annotate('', xy=env_right_in, xytext=(env_right_in[0] + 0.2, env_right_in[1]),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=LW_BOLD, mutation_scale=20),
                zorder=4)

    # Action Labels
    ax.text(x_action_turn + 0.25, 2.65, "action", fontsize=17, color=NAVY, ha='left', va='center')
    ax.text(x_action_turn + 0.25, 2.05, r"$A_t$", fontsize=20, color=NAVY, ha='left', va='center')

    # -------------------------------------------------------------------------
    # 3. Vertical Dashed Boundary Line (Step boundary: t+1 -> t)
    # -------------------------------------------------------------------------
    x_dashed = 2.7
    ax.plot([x_dashed, x_dashed], [0.35, 1.8], color=NAVY, lw=1.4, linestyle='--', zorder=2)

    # -------------------------------------------------------------------------
    # 4. Reward Flow (Environment upper left -> Dashed Line -> Agent lower left)
    # -------------------------------------------------------------------------
    x_turn_reward = 1.9

    # Environment output to dashed line with arrowhead at dashed line
    ax.plot([env_left_upper[0], x_dashed + 0.15], [env_left_upper[1], env_left_upper[1]], color=NAVY, lw=LW_REG, zorder=3)
    ax.annotate('', xy=(x_dashed, env_left_upper[1]), xytext=(x_dashed + 0.2, env_left_upper[1]),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=LW_REG, mutation_scale=16),
                zorder=4)
    ax.text((env_left_upper[0] + x_dashed) / 2.0, env_left_upper[1] + 0.18, r"$R_{t+1}$",
            fontsize=18, color=NAVY, ha='center', va='bottom')

    # From dashed line -> Left -> Turn Up -> Turn Right into Agent
    ax.plot([x_dashed, x_turn_reward], [env_left_upper[1], env_left_upper[1]], color=NAVY, lw=LW_REG, zorder=3)
    ax.plot([x_turn_reward, x_turn_reward], [env_left_upper[1], agent_left_lower[1]], color=NAVY, lw=LW_REG, zorder=3)
    ax.plot([x_turn_reward, agent_left_lower[0] - 0.15], [agent_left_lower[1], agent_left_lower[1]], color=NAVY, lw=LW_REG, zorder=3)

    # Arrowhead into Agent
    ax.annotate('', xy=agent_left_lower, xytext=(agent_left_lower[0] - 0.2, agent_left_lower[1]),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=LW_REG, mutation_scale=16),
                zorder=4)

    # -------------------------------------------------------------------------
    # 5. State Flow (Environment lower left -> Dashed Line -> Agent upper left)
    # -------------------------------------------------------------------------
    x_turn_state = 0.85

    # Environment output to dashed line with arrowhead at dashed line
    ax.plot([env_left_lower[0], x_dashed + 0.15], [env_left_lower[1], env_left_lower[1]], color=NAVY, lw=LW_BOLD, zorder=3)
    ax.annotate('', xy=(x_dashed, env_left_lower[1]), xytext=(x_dashed + 0.2, env_left_lower[1]),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=LW_BOLD, mutation_scale=20),
                zorder=4)
    ax.text((env_left_lower[0] + x_dashed) / 2.0, env_left_lower[1] + 0.18, r"$S_{t+1}$",
            fontsize=18, color=NAVY, ha='center', va='bottom')

    # From dashed line -> Left -> Turn Up -> Turn Right into Agent
    ax.plot([x_dashed, x_turn_state], [env_left_lower[1], env_left_lower[1]], color=NAVY, lw=LW_BOLD, zorder=3)
    ax.plot([x_turn_state, x_turn_state], [env_left_lower[1], agent_left_upper[1]], color=NAVY, lw=LW_BOLD, zorder=3)
    ax.plot([x_turn_state, agent_left_upper[0] - 0.15], [agent_left_upper[1], agent_left_upper[1]], color=NAVY, lw=LW_BOLD, zorder=3)

    # Arrowhead into Agent
    ax.annotate('', xy=agent_left_upper, xytext=(agent_left_upper[0] - 0.2, agent_left_upper[1]),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=LW_BOLD, mutation_scale=20),
                zorder=4)

    # -------------------------------------------------------------------------
    # 6. Left Side Labels (Positioned precisely to avoid any line overlap)
    # -------------------------------------------------------------------------
    # State Labels (To the left of x_turn_state = 0.85)
    ax.text(x_turn_state - 0.25, 3.0, "state", fontsize=17, color=NAVY, ha='right', va='center')
    ax.text(x_turn_state - 0.25, 2.4, r"$S_t$", fontsize=20, color=NAVY, ha='right', va='center')

    # Reward Labels (Centered between x_turn_state = 0.85 and x_turn_reward = 1.9)
    x_mid_reward = (x_turn_state + x_turn_reward) / 2.0
    ax.text(x_mid_reward, 2.7, "reward", fontsize=17, color=NAVY, ha='center', va='center')
    ax.text(x_mid_reward, 2.1, r"$R_t$", fontsize=20, color=NAVY, ha='center', va='center')

    plt.tight_layout()

    # Save SVG vector graphic and PNG preview
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(script_dir, "MDP_process_diagram.svg")
    png_path = os.path.join(script_dir, "MDP_process_diagram_preview.png")

    plt.savefig(svg_path, format='svg', bbox_inches='tight', transparent=True)
    plt.savefig(png_path, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    print(f"MDP Process Diagram created:\n- SVG: {svg_path}\n- PNG Preview: {png_path}")

if __name__ == "__main__":
    generate_mdp_diagram()
