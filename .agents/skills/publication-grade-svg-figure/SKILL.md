---
name: publication-grade-svg-figure
description: Design, generate, and reverse-engineer publication-grade vector SVG figures, system architectures, and flowcharts adhering to FEV corporate color palettes, academic typography standards, and scientific math conventions.
---

# Publication-Grade SVG Figure Design & Engineering

## Use This Skill When

- Creating new vector (`.svg`) architectural diagrams, system flowcharts, or block diagrams for papers, reports, or the thesis.
- Recreating/reverse-engineering raster figures (PNG, JPG, WebP) or online reference diagrams into clean, publication-grade vector figures.
- Standardizing font sizes, line weights, color palettes, and mathematical notation across all figures in the project.

## Do Not Use This Skill When

- Generating raw experimental data plots (use standard `matplotlib`/`seaborn` plotting workflows with consistent thesis styling instead).
- Drafting non-visual textual prose or bibliographies.

---

## 1. Core Visual Standards

### A. FEV Corporate Color Palette

Use the primary FEV colors for borders, focal elements, and headers. Use soft tint fills ($5\%\text{--}12\%$ saturation) for background containers and cards to maintain high contrast and modern card-based visual hierarchy:

| Role / Element | Name | RGB | Hex Code | Light Fill Tint (Hex) |
| :--- | :--- | :--- | :--- | :--- |
| **Critic / Control / Algorithms** | Dark Purple | `RGB(65, 9, 139)` | `#41098B` | `#F6F2FC` |
| **Actor / Policy / Critical Actions** | Dark Red | `RGB(185, 5, 45)` | `#B9052D` | `#FDF2F4` |
| **Storage / Buffers / Data Repositories** | Dark Teal | `RGB(0, 86, 102)` | `#005666` | `#EBF5F7` |
| **Environment / Process / Physical Plant** | Dark Green | `RGB(33, 118, 45)` | `#21762D` | `#EFF7F0` |
| **Flow Lines / Main Text / Borders** | Black / Neutral Dark | `RGB(0, 0, 0)` | `#000000` | `#F9FAFB` |
| **Sub-containers / Accents** | Medium Neutral Gray | `RGB(100, 116, 139)` | `#64748B` | `#F1F5F9` |

### B. Typography & Text Hierarchy

Adhere strictly to academic publishing standards (IEEE, Nature, Elsevier):

1. **Typeface**: Clean, standard **Sans-serif** (`Helvetica`, `Arial`, `DejaVu Sans`, or `Liberation Sans`). Do **not** use Serif fonts inside figures, even if the thesis body text is Serif.
2. **Standard Point Size Hierarchy** (at final printed scale):
   - **Figure / Block Title**: `10–12 pt` (Bold, `#000000` or Primary Color)
   - **Subsystem Header / Box Name**: `9–10 pt` (Bold or Semi-Bold)
   - **Body Text / Port Labels / Flow Annotations**: `8–9 pt` (Regular, `#000000`)
   - **Subscripts / Superscripts / Auxiliary Notes**: `6–8 pt` (**Never** below `6 pt`)
3. **Contrast**: Ensure all text has a contrast ratio $\ge 4.5:1$ against its background container.

### C. Mathematical & Variable Notation (ISO 80000-2)

- **Variables & Physical Parameters**: Always in *Italics* ($s, a, r, t, T, P, \theta, \gamma$).
- **Labels & State Subscripts**: Always **Upright / Roman** ($T_\mathrm{in}$, $P_\mathrm{out}$, $Q_\mathrm{target}$, $s_{t+1}$).
- **Functions & Operators**: Always **Upright / Roman** ($\sin, \exp, \min, \max, \ln, \Delta, \mathrm{d}t$).
- **Units**: Always **Upright / Roman** preceded by a non-breaking space ($10\ \mathrm{kW}$, $50\ \mathrm{bar}$, $300\ \mathrm{K}$).
- **Vectors / Tensors**: **Bold Upright** ($\mathbf{s}_t, \mathbf{a}_t$) or **Bold Italic** ($\boldsymbol{s}_t$).

---

## 2. Diagram Geometry & Layout Rules

1. **Canvas Dimensioning**:
   - Match physical column width directly in generator scripts:
     - Single-column figure: width $\approx 3.4\text{ in}$ ($86\text{ mm}$)
     - 1.5-column / Centered thesis figure: width $\approx 5.0\text{--}5.5\text{ in}$ ($127\text{--}140\text{ mm}$)
     - Full-width / Two-column span: width $\approx 6.8\text{--}7.2\text{ in}$ ($173\text{--}183\text{ mm}$)
2. **Container Boxes (Cards)**:
   - Use rounded corners (`boxstyle="round,pad=0.04,rounding_size=0.15"` in Matplotlib or `rx="8" ry="8"` in SVG).
   - Border line width: `1.5` to `2.2 pt`.
   - Card fill: Use soft pastel tints ($5\%\text{--}10\%$ opacity equivalent); never use solid dark background fills for large containers.
3. **Flow Arrows & Connectors**:
   - Connector line width: `1.5` to `2.0 pt`, solid `#000000` or category color.
   - Arrowheads: Proportional and filled (`arrowstyle='->,head_width=0.4,head_length=0.6'`).
   - Route orthogonally (right-angle bends) with rounded corners when possible; avoid awkward diagonals across cards.
   - Text placement: Position labels along arrows with clear white halo/background padding to prevent line collisions.

---

## 3. Reverse-Engineering Workflow (Online/Raster $\to$ Publication SVG)

When recreating a raster diagram (PNG, JPG, WebP) or online paper figure:

1. **Structural Decomposition**:
   - List all top-level functional modules (e.g., Environment, Agent, Buffer, Controller).
   - Trace all signal/data flows (Inputs, Outputs, Feedback loops, Training gradients).
2. **Map to Thesis Visual Standard**:
   - Map functional categories to the FEV Palette (e.g., Policy $\to$ Dark Red `#B9052D`, Value/Critic $\to$ Dark Purple `#41098B`, Buffer $\to$ Dark Teal `#005666`, Physical Plant $\to$ Dark Green `#21762D`).
   - Replace raster text with LaTeX-formatted mathematical symbols ($s_t, a_t, r_{t+1}$).
3. **Draft Python Generation Script**:
   - Write a standalone Python script using `matplotlib.patches`, `matplotlib.path`, and `matplotlib.pyplot`.
   - Export both the crisp vector `.svg` and a high-resolution `.png` preview ($300\text{ DPI}$).
4. **Inspect & Refine**:
   - Verify alignment, label spacing, no overlapping arrows, and consistent font hierarchy.

---

## 4. Standard Python / Matplotlib SVG Template

Use this modular template for generating publication-grade SVGs:

```python
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_publication_figure(output_svg="figure.svg", output_png="figure.png"):
    # 1. Publication Typography Configuration
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica', 'Arial']
    plt.rcParams['mathtext.fontset'] = 'cm'  # LaTeX Computer Modern Math

    # 2. Strict FEV Color Definitions
    DARK_PURPLE = '#41098B'
    DARK_RED    = '#B9052D'
    DARK_TEAL   = '#005666'
    DARK_GREEN  = '#21762D'
    BLACK       = '#000000'

    # Tint Fills
    BG_PURPLE   = '#F6F2FC'
    BG_RED      = '#FDF2F4'
    BG_TEAL     = '#EBF5F7'
    BG_GREEN    = '#EFF7F0'

    # 3. Canvas Setup (in inches)
    fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
    ax.set_xlim(0, 6.5)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    # 4. Draw Cards / Containers
    card_actor = patches.FancyBboxPatch(
        (0.5, 1.0), 2.2, 2.5,
        boxstyle="round,pad=0.03,rounding_size=0.1",
        ec=DARK_RED, fc=BG_RED, lw=1.8, zorder=2
    )
    ax.add_patch(card_actor)

    # 5. Add Hierarchical Typography (12pt Header, 10pt/8pt Body & Math)
    ax.text(1.6, 3.2, "Actor Network", fontsize=11, fontweight='bold',
            color=DARK_RED, ha='center', va='center')
    ax.text(1.6, 2.5, r"$\pi_\theta(a_t \mid s_t)$", fontsize=10,
            color=BLACK, ha='center', va='center')
    ax.text(1.6, 1.8, "Outputs action vector", fontsize=8,
            color='#4B5563', ha='center', va='center')

    # 6. Save Clean Vector SVG & PNG Preview
    plt.tight_layout()
    plt.savefig(output_svg, format='svg', bbox_inches='tight', transparent=False)
    plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_publication_figure()
```

---

## 5. Quality Assurance Checklist

Before finalizing any figure:

- [ ] **Vector Format**: Saved as pure `.svg` (all text/lines are scalable vectors).
- [ ] **Sans-Serif Font**: Text uses `Helvetica`, `Arial`, or `DejaVu Sans`.
- [ ] **Hierarchy**: Headers $\ge 10\text{ pt}$, Body/Labels $8\text{--}9\text{ pt}$, Subscripts $\ge 6\text{ pt}$.
- [ ] **Math Notation**: Variables italicized ($s_t, a_t$), labels/units upright ($T_\mathrm{in}, \mathrm{bar}$).
- [ ] **FEV Palette**: Uses standard FEV primaries with high-contrast light tint fills.
- [ ] **Flow Clarity**: Arrow heads are clean, orthogonal lines preferred, zero text-line collisions.
- [ ] **Self-Contained**: Figure is clear and understandable alongside its caption.
