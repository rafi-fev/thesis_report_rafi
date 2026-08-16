# Figure Quality Baseline & Best Practices

This document defines the publication-grade visual and typographic standards for all figures, block diagrams, and system architectures across the thesis.

For automated assistance and recreation workflows, refer to the project skill at [.agents/skills/publication-grade-svg-figure/SKILL.md](file:///Users/mrafiindrajaya/Desktop/Github%20Projects/thesis_report_rafi/.agents/skills/publication-grade-svg-figure/SKILL.md).

---

## 1. Typography & Font Hierarchy

Follow major academic publisher conventions (IEEE, Nature, Elsevier):

* **Typeface**: **Sans-serif** (`Helvetica`, `Arial`, `DejaVu Sans`, `Liberation Sans`). 
  * *Note*: Do not use Serif fonts inside figures, even when the manuscript text is Serif. Sans-serif preserves legibility when figures are scaled to column widths.
* **Font Size Hierarchy (at final printed scale)**:
  * **11–12 pt (Bold)**: Card/Panel headlines and major module titles (e.g., *Actor*, *Critic*, *Plant*).
  * **9–10 pt (Medium/Bold)**: Sub-block headers, port labels, and primary equations (e.g., $\pi_\theta(a|s)$).
  * **8–9 pt (Regular)**: Descriptions, signal flow annotations, and parameter values.
  * **6–8 pt (Regular)**: Subscripts, superscripts, and minor tick labels (*absolute minimum readable size: 6 pt*).

---

## 2. Mathematical & Variable Notation (ISO 80000-2)

* **Variables & Parameters**: Always *Italic* (e.g., $s$, $a$, $r$, $t$, $T$, $P$, $\theta$, $\gamma$).
* **Subscripts / Labels**:
  * *Italic* if the subscript is a variable or index: $s_t$, $a_i$, $x_k$.
  * **Upright (Roman)** if the subscript is a word, abbreviation, or state name: $T_\mathrm{in}$, $P_\mathrm{out}$, $Q_\mathrm{target}$, $E_\mathrm{kin}$.
* **Operators & Functions**: Always **Upright** (e.g., $\min$, $\max$, $\exp$, $\sin$, $\Delta$, $\mathrm{d}t$).
* **Units**: Always **Upright** with a space after the number (e.g., $50\ \mathrm{bar}$, $350\ \mathrm{K}$, $100\ \mathrm{kW}$).

---

## 3. FEV Color Scheme & Tint Hierarchy

Use the primary FEV colors for borders, focal icons, and headers. Use light pastel tint fills ($5\%\text{--}12\%$ saturation) for card backgrounds to maintain high text contrast and modern card-based hierarchy:

| Module / Role | Color Name | RGB Code | Hex Code | Light Fill Tint (Hex) |
| :--- | :--- | :--- | :--- | :--- |
| **Critic / Q-Networks / Algorithms** | Dark Purple | `RGB(65, 9, 139)` | `#41098B` | `#F6F2FC` |
| **Actor / Policy / Action Flows** | Dark Red | `RGB(185, 5, 45)` | `#B9052D` | `#FDF2F4` |
| **Replay Buffer / Data Storage** | Dark Teal | `RGB(0, 86, 102)` | `#005666` | `#EBF5F7` |
| **Environment / Process / Physical Plant**| Dark Green | `RGB(33, 118, 45)` | `#21762D` | `#EFF7F0` |
| **Flow Arrows / Labels / Primary Text** | Black | `RGB(0, 0, 0)` | `#000000` | `#FFFFFF` |
| **Neutral Sub-cards & Accents** | Slate Gray | `RGB(100, 116, 139)` | `#64748B` | `#F1F5F9` |

---

## 4. Geometry, Cards & Connectors

* **Card Borders**: Rounded rectangle styling (`rounding_size=0.10` to `0.15` in Matplotlib; `rx="8"` in SVG) with a border stroke width of `1.8` to `2.2 pt`.
* **Flow Arrows**: Stroke width `1.8` to `2.0 pt` with clean proportional arrowheads. Prefer orthogonal routing (right-angle paths) over diagonal overlaps.
* **Format**: Always deliver figures in clean, vector **`.svg`** format alongside a $300\text{ DPI}$ preview `.png`.

---

## 5. Python / Matplotlib Boilerplate

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Typography setup
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica', 'Arial']
plt.rcParams['mathtext.fontset'] = 'cm'

# Canvas (in inches)
fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
ax.set_xlim(0, 6.5)
ax.set_ylim(0, 4.5)
ax.axis('off')

# Example FEV Card
card = patches.FancyBboxPatch((0.5, 1.0), 2.2, 2.5,
                              boxstyle="round,pad=0.03,rounding_size=0.1",
                              ec='#B9052D', fc='#FDF2F4', lw=1.8)
ax.add_patch(card)

# Labels & Equations
ax.text(1.6, 3.1, "Actor Module", fontsize=11, fontweight='bold', color='#B9052D', ha='center')
ax.text(1.6, 2.3, r"$\pi_\theta(a_t \mid s_t)$", fontsize=10, color='#000000', ha='center')
ax.text(1.6, 1.6, "Action distribution", fontsize=8, color='#4B5563', ha='center')

plt.savefig("figure.svg", format='svg', bbox_inches='tight')
plt.close()
```