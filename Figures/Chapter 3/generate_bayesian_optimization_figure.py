import os
import numpy as np
import matplotlib.pyplot as plt


def matern32_kernel(x1, x2, length_scale=3.2, sigma_f=1.35):
    """
    Matérn 3/2 kernel function for Gaussian Process regression.
    k(r) = sigma_f^2 * (1 + sqrt(3)*r/l) * exp(-sqrt(3)*r/l)
    """
    r = np.abs(x1 - x2.T)
    sqrt3_r = np.sqrt(3.0) * r / length_scale
    return (sigma_f ** 2) * (1.0 + sqrt3_r) * np.exp(-sqrt3_r)


def generate_bayesian_optimization_figure():
    """
    Generates a publication-grade vector SVG figure representing Gaussian Process
    regression in Bayesian Optimization, adhering strictly to FEV corporate visual guidelines.
    """
    # -------------------------------------------------------------------------
    # 1. Publication Typography & LaTeX Styling Configuration
    # -------------------------------------------------------------------------
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica', 'Arial', 'Liberation Sans']
    plt.rcParams['mathtext.fontset'] = 'cm'

    # -------------------------------------------------------------------------
    # 2. Strict FEV Corporate Color Definitions
    # -------------------------------------------------------------------------
    FEV_DARK_PURPLE = '#41098B'  # RGB(65, 9, 139)  - GP Surrogate / Algorithm
    FEV_DARK_RED    = '#B9052D'  # RGB(185, 5, 45)  - Optimum Query Point / Focus
    FEV_DARK_TEAL   = '#005666'  # RGB(0, 86, 102)  - Data Accents
    FEV_BLACK       = '#0F172A'  # Slate Dark       - True Objective Function
    FEV_GRAY_TEXT   = '#1E293B'  # Axes & Labels
    FEV_GRID_COLOR  = '#F1F5F9'  # Soft Gridlines

    # Tints
    BG_PURPLE_LIGHT = '#F4EEFB'  # Soft purple tint for confidence band
    BG_PURPLE_LINE  = '#C4B5FD'  # Soft purple boundary line for std interval

    # -------------------------------------------------------------------------
    # 3. Mathematical Ground Truth & Gaussian Process Surrogate Simulation
    # -------------------------------------------------------------------------
    # Dense domain
    X = np.linspace(0, 20, 1000).reshape(-1, 1)
    y = (np.sin(X) / 2.0 - ((10.0 - X) ** 2) / 50.0 + 2.0).ravel()

    # The 5 sequential queries of Bayesian Optimization + initial observation
    # Points queried: x = [0.0, 2.36, 3.00, 6.25, 8.55]
    X_train = np.array([0.0, 2.36, 3.00, 6.25, 8.55]).reshape(-1, 1)
    y_train = (np.sin(X_train) / 2.0 - ((10.0 - X_train) ** 2) / 50.0 + 2.0).ravel()

    # Optimum candidate query (x = 7.55, y = 2.36 - global peak)
    x_opt = 7.55
    y_opt = float(np.sin(x_opt) / 2.0 - ((10.0 - x_opt) ** 2) / 50.0 + 2.0)

    # GP Regression with Matérn 3/2 Kernel
    length_scale = 3.2
    sigma_f = 1.35
    noise_var = 1e-6

    K = matern32_kernel(X_train, X_train, length_scale, sigma_f) + noise_var * np.eye(len(X_train))
    K_s = matern32_kernel(X_train, X, length_scale, sigma_f)
    
    L = np.linalg.cholesky(K)
    alpha = np.linalg.solve(L.T, np.linalg.solve(L, y_train))
    mu = (K_s.T @ alpha).ravel()

    v = np.linalg.solve(L, K_s)
    sigma2 = (sigma_f ** 2) - np.sum(v ** 2, axis=0)
    sigma = np.sqrt(np.maximum(sigma2, 0.0))

    # -------------------------------------------------------------------------
    # 4. Canvas & Layout Setup (Single/1.5-column Thesis Size: 8.5 x 4.6 in)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 4.6), dpi=300)

    # Shaded GP Uncertainty Region (Surrogate Confidence Band: \mu \pm \sigma)
    ax.fill_between(
        X.ravel(),
        mu - sigma,
        mu + sigma,
        color=FEV_DARK_PURPLE,
        alpha=0.17,
        label=r'Surrogate uncertainty $\mu(x) \pm \sigma(x)$',
        zorder=2
    )
    # Subtle uncertainty boundary lines
    ax.plot(X.ravel(), mu - sigma, color=BG_PURPLE_LINE, linewidth=0.75, linestyle=':', zorder=3)
    ax.plot(X.ravel(), mu + sigma, color=BG_PURPLE_LINE, linewidth=0.75, linestyle=':', zorder=3)

    # True Objective Function f(x)
    ax.plot(
        X.ravel(),
        y,
        color=FEV_BLACK,
        linewidth=2.2,
        label=r'True objective $f(x)$',
        zorder=4
    )

    # GP Surrogate Mean mu(x)
    ax.plot(
        X.ravel(),
        mu,
        color=FEV_DARK_PURPLE,
        linewidth=2.0,
        label=r'GP regressor mean $\mu(x)$',
        zorder=5
    )

    # Queried Points (Black markers with crisp white border)
    ax.scatter(
        X_train.ravel(),
        y_train,
        color='#000000',
        edgecolors='#FFFFFF',
        linewidth=1.2,
        s=62,
        label=r'Queried points $(x_i, y_i)$',
        zorder=7
    )

    # Current Optimum Point (FEV Dark Red with double accent ring)
    ax.scatter(
        [x_opt],
        [y_opt],
        color=FEV_DARK_RED,
        edgecolors='#FFFFFF',
        linewidth=1.5,
        s=120,
        label=r'Current optimum $(x^+, y^+)$',
        zorder=8
    )
    # Highlight accent ring around optimum
    ax.scatter(
        [x_opt],
        [y_opt],
        color='none',
        edgecolors=FEV_DARK_RED,
        linewidth=1.5,
        linestyle='--',
        s=230,
        zorder=8
    )

    # -------------------------------------------------------------------------
    # 5. Styling, Grid, Axis Labels & Typography
    # -------------------------------------------------------------------------
    ax.set_title(
        'Bayesian Optimization: Gaussian Process Surrogate After Five Queries',
        fontsize=12.2,
        fontweight='bold',
        color=FEV_BLACK,
        pad=12
    )

    ax.set_xlabel(r'Input parameter $x$', fontsize=10.5, color=FEV_GRAY_TEXT, labelpad=8)
    ax.set_ylabel(r'Objective value $y$', fontsize=10.5, color=FEV_GRAY_TEXT, labelpad=8)

    ax.set_xlim(-0.3, 20.3)
    ax.set_ylim(-1.15, 2.95)

    ax.tick_params(axis='both', which='major', labelsize=9.5, colors='#334155', length=4.5, width=1.0)
    ax.grid(True, linestyle='--', alpha=0.7, color='#E2E8F0', zorder=1)

    # Clean Card Legend with Crisp Border
    legend = ax.legend(
        loc='upper right',
        frameon=True,
        framealpha=0.96,
        facecolor='#FFFFFF',
        edgecolor='#CBD5E1',
        fontsize=9.0,
        fancybox=True,
        borderpad=0.75,
        labelspacing=0.45
    )
    legend.get_frame().set_linewidth(1.0)

    # Axis spines styling
    for spine in ax.spines.values():
        spine.set_color('#64748B')
        spine.set_linewidth(1.1)

    plt.tight_layout()

    # -------------------------------------------------------------------------
    # 6. Save Vector SVG and High-Res PNG Preview
    # -------------------------------------------------------------------------
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(script_dir, "bayesian_optimization_queries.svg")
    png_path = os.path.join(script_dir, "bayesian_optimization_queries_preview.png")

    plt.savefig(svg_path, format='svg', bbox_inches='tight', transparent=False)
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[SUCCESS] Figure generated successfully:")
    print(f"  - Vector SVG: {svg_path}")
    print(f"  - Preview PNG: {png_path}")


if __name__ == '__main__':
    generate_bayesian_optimization_figure()
