"""Analyze DOE case relationships with run-config-driven component selection.

The script loads one Excel results sheet and can generate three plot families:
1) plot 1: cost-gap vs global normalized Euclidean layout distance and/or
   cost-gap vs per-technology normalized deviation/value (subplots),
2) plot 2: case ID vs normalized component scales,
3) plot 3: case ID vs total costs.

Technology components for scale-based analysis are resolved from a run-config:
- Included from ``optimization.variable_technology_specs``
- Excluded from ``optimization.fixed_technologies_with_values``
- Expected column naming in the results sheet: ``<technology>_scale``

Rows are filtered by ``termination_condition`` depending on the selected plot.
Distance-derived tables and summary statistics are generated only when plot 1
global-distance view is enabled.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#INPUT_FILE = Path("C:\D\models\BPtMeOH_comparison_thesis\results\BO_case_results_mentawai_Tuapejat_base_2026.04.23_133329.xlsx")
# INPUT_SHEET = "BO_case_results"
# OUTPUT_DIR = Path("C:\D\models\BPtMeOH_comparison_thesis\results\distance-analysis-result")
# RUN_CONFIG_FILE = Path("C:\D\models\BPtMeOH_comparison_thesis\config\run_configs\main_mentawai.json")
#DOE case path: "C:\D\models\BPtMeOH_comparison_thesis\results\doe cases BAP2H2P Final 3000 base.xlsx"
#Updated analysis:
#./results/distance-analysis-result/BO_case_results_mentawai_Tuapejat_base_2026.05.15_171706_200trials.xlsx
#./results/distance-analysis-result/BO_case_results_mentawai_Tuapejat_base_2026.05.15_171706_500trials.xlsx
#results/BO_case_results_Master_Thesis_johannesburg_base_2026.06.12_211247.xlsx
#results/BO_case_results_Master_Thesis_johannesburg_base_2026.06.13_184743.xlsx
#results/BO_case_results_Master_Thesis_johannesburg_base_2026.06.13_225901.xlsx
#results/BO_case_results_Master_Thesis_johannesburg_base_2026.06.14_184651.xlsx
#results/BO_case_results_Master_Thesis_johannesburg_base_2026.06.15_080130.xlsx
#results/BO_case_results_Master_Thesis_johannesburg_base_2026.06.15_193708.xlsx
#2014awe0.2,120trials: results/BO_case_results_Master_Thesis_johannesburg_base_2026.06.16_031253.xlsx
#results/BO_case_results_Master_Thesis_johannesburg_base_2026.06.19_154430.xlsx
#results/BO_case_results_Master_Thesis_johannesburg_base_2026.07.21_041409.xlsx
#results/BO_case_results_Master_Thesis_johannesburg_base_2026.08.17_074240.xlsx

#C:\D\models\BPtMeOH_comparison_thesis\results\BO_case_results_Master_Thesis_johannesburg_base_2026.09.01_204326FinalFinal.xlsx
INPUT_FILE = Path("Data\\Level 1 & 2 Final\\Level 2\\GPSampler run\\final\\BO_case_results_Master_Thesis_johannesburg_base_2026.09.01_204326FinalFinal.xlsx")
INPUT_SHEET = "BO_case_results"
OUTPUT_DIR = Path("Figures\\Chapter 4\\distance-analysis-result")
RUN_CONFIG_FILE = Path("Data\\Level 1 & 2 Final\\master_thesis_BO.json")

# Plot toggles.
PLOTS_TO_DRAW = ["case_vs_total_cost", "lcom_vs_component", "case_vs_scales"] #"distance_cost_gap", "case_vs_scales", "case_vs_total_cost", "lcom_vs_component"
PLOT1_VIEW_MODE = "both"  # "global_distance" | "per_technology" | "both"
PLOT1_COST_GAP_MODE = "relative"  # "relative" | "absolute"
PLOT1_PER_TECH_X_MODE = "minmax_value"  # "delta_to_optimum" | "minmax_value"
PLOT2_VIEW_MODE = "component_subplots"  # "component_subplots" | "aggregate" | "both"

# Plot 3 (case vs objective) labeling. The objective value is LCOM in current runs.
PLOT3_TITLE = "Case ID vs LCOM"
PLOT3_Y_LABEL = "LCOM"
# Unit shown on the LCOM axis label for the case-vs-LCOM plot, e.g. "$/ton".
PLOT3_Y_UNIT = "$/ton"

# LCOM vs single-component sizing plot (absolute sizing only).
LCOM_VS_COMPONENT_TECH = "electrolyzer_lvl2"
LCOM_Y_LABEL = "LCOM"
# Units for the LCOM (y) and component-sizing (x) axis labels.
LCOM_Y_UNIT = "$/ton"
LCOM_COMPONENT_UNIT = "MW"
# Y-axis scaling to reveal variation across trials.
# "linear" | "log". Log scale compresses the large-LCOM outliers.
LCOM_Y_SCALE = "log"
# Optional upper LCOM cap (in y-axis units) to zoom into low-LCOM trials.
# Set to a number (e.g. 1000.0) to clip, or None to keep all trials.
LCOM_Y_MAX: float | None = None

# Output image format(s) for saved figures. Provide any subset of {"png", "svg"}.
OUTPUT_IMAGE_FORMATS: list[str] = ["svg"]
FIGURE_DPI = 300

# Subplot technology selection.
# Use "all" or a list like ["pv", "bess", "electrolyzer_lvl1"].
SUBPLOT_TECHNOLOGIES: str | list[str] = ["electrolyzer_lvl2", "pv", "reformer_auto", "wt", "bess"]

VALID_PLOTS = {"distance_cost_gap", "case_vs_scales", "case_vs_total_cost", "lcom_vs_component"}
VALID_PLOT1_VIEW_MODE = {"global_distance", "per_technology", "both"}
VALID_PLOT1_COST_GAP_MODE = {"relative", "absolute"}
VALID_PLOT1_PER_TECH_X_MODE = {"delta_to_optimum", "minmax_value"}
VALID_PLOT2_VIEW_MODE = {"component_subplots", "aggregate", "both"}
VALID_IMAGE_FORMATS = {"png", "svg"}
PLOT2_ALLOWED_STATUSES = {"optimal", "infeasible"}


def _find_column(columns: Iterable[str], preferred_names: list[str]) -> str | None:
    """Return the first matching column name (case-insensitive)."""
    lowered = {str(col).strip().lower(): str(col) for col in columns}
    for name in preferred_names:
        match = lowered.get(name.lower())
        if match is not None:
            return match
    return None


def _unique_preserve_order(values: Iterable[str]) -> list[str]:
    """Return de-duplicated strings while preserving first-seen order."""
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        output.append(value)
    return output


def _format_list(values: list[str]) -> str:
    """Render list values for compact human-readable summary output."""
    if not values:
        return "<none>"
    return ", ".join(values)


def validate_runtime_configuration() -> list[str]:
    """Validate top-level toggles and return de-duplicated plot selection."""
    selected_plots = list(dict.fromkeys(PLOTS_TO_DRAW))
    if not selected_plots:
        raise ValueError("`PLOTS_TO_DRAW` is empty. Select at least one plot.")

    invalid_plots = [plot for plot in selected_plots if plot not in VALID_PLOTS]
    if invalid_plots:
        raise ValueError(
            f"Invalid plot names in `PLOTS_TO_DRAW`: {invalid_plots}. "
            f"Valid options: {sorted(VALID_PLOTS)}."
        )

    if PLOT1_VIEW_MODE not in VALID_PLOT1_VIEW_MODE:
        raise ValueError(
            f"Invalid `PLOT1_VIEW_MODE`: {PLOT1_VIEW_MODE!r}. "
            f"Valid options: {sorted(VALID_PLOT1_VIEW_MODE)}."
        )

    if PLOT1_COST_GAP_MODE not in VALID_PLOT1_COST_GAP_MODE:
        raise ValueError(
            f"Invalid `PLOT1_COST_GAP_MODE`: {PLOT1_COST_GAP_MODE!r}. "
            f"Valid options: {sorted(VALID_PLOT1_COST_GAP_MODE)}."
        )

    if PLOT1_PER_TECH_X_MODE not in VALID_PLOT1_PER_TECH_X_MODE:
        raise ValueError(
            f"Invalid `PLOT1_PER_TECH_X_MODE`: {PLOT1_PER_TECH_X_MODE!r}. "
            f"Valid options: {sorted(VALID_PLOT1_PER_TECH_X_MODE)}."
        )

    if PLOT2_VIEW_MODE not in VALID_PLOT2_VIEW_MODE:
        raise ValueError(
            f"Invalid `PLOT2_VIEW_MODE`: {PLOT2_VIEW_MODE!r}. "
            f"Valid options: {sorted(VALID_PLOT2_VIEW_MODE)}."
        )

    if not isinstance(OUTPUT_IMAGE_FORMATS, list) or not OUTPUT_IMAGE_FORMATS:
        raise ValueError(
            "`OUTPUT_IMAGE_FORMATS` must be a non-empty list of image format strings."
        )
    normalized_formats = _unique_preserve_order(
        [str(fmt).strip().lower() for fmt in OUTPUT_IMAGE_FORMATS if str(fmt).strip() != ""]
    )
    invalid_formats = [fmt for fmt in normalized_formats if fmt not in VALID_IMAGE_FORMATS]
    if invalid_formats:
        raise ValueError(
            f"Invalid image formats in `OUTPUT_IMAGE_FORMATS`: {invalid_formats}. "
            f"Valid options: {sorted(VALID_IMAGE_FORMATS)}."
        )

    if isinstance(SUBPLOT_TECHNOLOGIES, str):
        if SUBPLOT_TECHNOLOGIES != "all":
            raise ValueError(
                "`SUBPLOT_TECHNOLOGIES` must be 'all' or a list of technology keys."
            )
    elif isinstance(SUBPLOT_TECHNOLOGIES, list):
        if not SUBPLOT_TECHNOLOGIES:
            raise ValueError(
                "`SUBPLOT_TECHNOLOGIES` list is empty. Use 'all' or provide at least one key."
            )
        invalid_values = [
            value for value in SUBPLOT_TECHNOLOGIES
            if not isinstance(value, str) or str(value).strip() == ""
        ]
        if invalid_values:
            raise ValueError(
                "`SUBPLOT_TECHNOLOGIES` must contain non-empty string keys only."
            )
    else:
        raise ValueError(
            "`SUBPLOT_TECHNOLOGIES` must be either 'all' or a list of strings."
        )

    return selected_plots


def load_run_config_json(config_path: Path) -> dict[str, Any]:
    """Load and parse run-config JSON from disk."""
    if not config_path.exists():
        raise FileNotFoundError(f"Run config file not found: {config_path}")

    try:
        run_config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Run config is not valid JSON: {config_path}") from exc

    if not isinstance(run_config, dict):
        raise ValueError("Run config root must be a JSON object.")
    return run_config


def extract_technology_scope_from_run_config(
    run_config: dict[str, Any],
) -> tuple[list[str], list[str]]:
    """Return included/excluded technology keys from run-config optimization settings."""
    optimization_cfg = run_config.get("optimization")
    if not isinstance(optimization_cfg, dict):
        raise ValueError("Run config must contain an object at `optimization`.")

    variable_specs = optimization_cfg.get("variable_technology_specs")
    fixed_values = optimization_cfg.get("fixed_technologies_with_values")

    if not isinstance(variable_specs, dict):
        raise ValueError(
            "Run config must contain object `optimization.variable_technology_specs`."
        )
    if not isinstance(fixed_values, dict):
        raise ValueError(
            "Run config must contain object `optimization.fixed_technologies_with_values`."
        )

    included_techs = _unique_preserve_order(
        [
            str(tech).strip()
            for tech in variable_specs.keys()
            if str(tech).strip() not in ["", "None"]
        ]
    )
    excluded_techs = _unique_preserve_order(
        [
            str(tech).strip()
            for tech in fixed_values.keys()
            if str(tech).strip() not in ["", "None"]
        ]
    )

    included_lower = {name.lower() for name in included_techs}
    excluded_lower = {name.lower() for name in excluded_techs}
    overlap = sorted(included_lower.intersection(excluded_lower))
    if overlap:
        raise ValueError(
            "Run config has overlapping technology keys between "
            "`variable_technology_specs` and `fixed_technologies_with_values`: "
            f"{overlap}"
        )

    if not included_techs:
        raise ValueError(
            "Run config `optimization.variable_technology_specs` does not contain any technologies."
        )

    return included_techs, excluded_techs


def resolve_design_columns_from_run_config(
    df_columns: Iterable[str],
    included_techs: list[str],
    excluded_techs: list[str],
) -> tuple[list[str], list[str], dict[str, str]]:
    """Resolve final design scale columns from run-config technology keys."""
    available_cols = [str(col) for col in df_columns]
    lower_to_original = {col.strip().lower(): col for col in available_cols}
    available_scale_cols = [col for col in available_cols if col.strip().lower().endswith("_scale")]

    excluded_lower = {name.lower() for name in excluded_techs}
    effective_techs = [name for name in included_techs if name.lower() not in excluded_lower]

    missing_expected_cols: list[str] = []
    design_cols: list[str] = []
    tech_to_col: dict[str, str] = {}

    for tech_name in effective_techs:
        expected_col = f"{tech_name}_scale"
        match_col = lower_to_original.get(expected_col.lower())
        if match_col is None:
            missing_expected_cols.append(expected_col)
            continue
        design_cols.append(match_col)
        tech_to_col[tech_name] = match_col

    if missing_expected_cols:
        raise ValueError(
            "Missing expected scale columns derived from run config "
            f"`variable_technology_specs`: {missing_expected_cols}. "
            f"Available `_scale` columns in Excel: {available_scale_cols}."
        )

    if not design_cols:
        raise ValueError(
            "No design columns resolved from run config after applying fixed-technology exclusions."
        )

    return effective_techs, design_cols, tech_to_col


def resolve_subplot_technology_selection(
    subplot_technologies: str | list[str],
    available_technologies: list[str],
) -> list[str]:
    """Resolve and validate selected technologies for subplot rendering."""
    available_map = {name.lower(): name for name in available_technologies}

    if subplot_technologies == "all":
        selected_technologies = available_technologies.copy()
    else:
        requested_raw = _unique_preserve_order(
            [str(value).strip() for value in subplot_technologies if str(value).strip() != ""]
        )
        invalid = [value for value in requested_raw if value.lower() not in available_map]
        if invalid:
            raise ValueError(
                "Unknown technologies in `SUBPLOT_TECHNOLOGIES`: "
                f"{invalid}. Available included technologies: {available_technologies}."
            )
        selected_technologies = [available_map[value.lower()] for value in requested_raw]

    if not selected_technologies:
        raise ValueError("No subplot technologies resolved after validation.")

    return selected_technologies


def load_rmse_dataframe(file_path: Path, sheet_name: str) -> pd.DataFrame:
    """Load the source sheet and drop fully empty rows.

    Parameters
    ----------
    file_path : Path
        Path to the source Excel workbook.
    sheet_name : str
        Name of the worksheet to load.

    Returns
    -------
    pd.DataFrame
        Raw dataframe with stripped column names and empty rows removed.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df.columns = [str(col).strip() for col in df.columns]
    return df.dropna(how="all").copy()


def prepare_numeric_dataframe(df: pd.DataFrame, numeric_cols: list[str]) -> pd.DataFrame:
    """Convert selected columns to numeric and keep only complete numeric rows.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    numeric_cols : list[str]
        Columns that must be numeric for downstream calculations.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with valid numeric values for `numeric_cols`.
    """
    prepared = df.copy()
    for col in numeric_cols:
        prepared[col] = pd.to_numeric(prepared[col], errors="coerce")
    return prepared.dropna(subset=numeric_cols).copy()


def add_normalized_status_column(df: pd.DataFrame, termination_col: str) -> pd.DataFrame:
    """Attach normalized termination status column."""
    enriched = df.copy()
    enriched["_termination_condition_norm"] = (
        enriched[termination_col].fillna("").astype(str).str.strip().str.lower()
    )
    return enriched


def compute_ranges(df: pd.DataFrame, design_cols: list[str]) -> pd.Series:
    """Compute max-min ranges and remove zero-range variables.

    Parameters
    ----------
    df : pd.DataFrame
        DOE dataframe with design columns.
    design_cols : list[str]
        Candidate columns for distance normalization.

    Returns
    -------
    pd.Series
        Positive ranges indexed by column name.
    """
    # Each variable is normalized by its observed DOE spread (max - min).
    ranges = df[design_cols].max() - df[design_cols].min()
    return ranges[ranges > 0].copy()


def minmax_normalize_series(series: pd.Series) -> pd.Series:
    """Return a [0, 1] min-max normalized series.

    Constant series are mapped to 0.0.
    """
    if series.empty:
        return pd.Series(dtype=float, index=series.index)

    min_value = series.min()
    max_value = series.max()
    if pd.isna(min_value) or pd.isna(max_value):
        return pd.Series(np.nan, index=series.index, dtype=float)
    if float(max_value) > float(min_value):
        return (series - float(min_value)) / (float(max_value) - float(min_value))
    return pd.Series(0.0, index=series.index, dtype=float)


def minmax_normalize_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Min-max normalize multiple columns independently."""
    normalized = pd.DataFrame(index=df.index)
    for col in columns:
        normalized[col] = minmax_normalize_series(df[col].astype(float))
    return normalized


def add_cost_gap_metrics(
    df: pd.DataFrame,
    global_opt_row: pd.Series,
    cost_col: str,
) -> pd.DataFrame:
    """Add absolute and relative cost-gap metrics relative to one optimum row."""
    result = df.copy()
    result["abs_cost_gap"] = result[cost_col] - float(global_opt_row[cost_col])
    denominator = abs(float(global_opt_row[cost_col]))
    if denominator > 0:
        # Relative gap is expressed in percent of absolute optimum magnitude.
        result["rel_cost_gap"] = result["abs_cost_gap"] / denominator * 100.0
    else:
        result["rel_cost_gap"] = np.nan
    return result


def compute_metrics(
    df: pd.DataFrame,
    global_opt_row: pd.Series,
    cost_col: str,
    valid_design_cols: list[str],
    ranges: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute layout distance and cost-gap metrics for all DOE rows.

    Parameters
    ----------
    df : pd.DataFrame
        Clean DOE dataframe.
    global_opt_row : pd.Series
        Row representing the global optimum case.
    cost_col : str
        Column containing total cost values.
    valid_design_cols : list[str]
        Design columns with non-zero ranges.
    ranges : pd.Series
        Normalization ranges for `valid_design_cols`.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        - Dataframe with `layout_distance`, `abs_cost_gap`, `rel_cost_gap`.
        - Squared normalized contribution dataframe per design variable.
    """
    result = add_cost_gap_metrics(df=df, global_opt_row=global_opt_row, cost_col=cost_col)

    design_data = result[valid_design_cols].astype(float)
    global_opt_design = global_opt_row[valid_design_cols].astype(float)
    ranges_float = ranges.astype(float)

    # Normalized variable-wise difference:
    # (x_i,j - x_opt,j) / (max_j - min_j)
    normalized_diff = (design_data - global_opt_design) / ranges_float
    # Squared normalized contribution per variable j.
    squared_contrib = normalized_diff.pow(2)

    # Euclidean distance in normalized design space:
    # d_i = sqrt(sum_j(((x_i,j - x_opt,j) / range_j)^2))
    result["layout_distance"] = np.sqrt(squared_contrib.sum(axis=1))
    return result, squared_contrib


def choose_identifier_column(df: pd.DataFrame) -> str:
    """Pick the best available identifier column for plotting/reporting output."""
    preferred = ["case_id", "case", "id", "Unnamed: 1", "Unnamed: 0"]
    match = _find_column(df.columns, preferred)
    if match is not None:
        return match
    return str(df.columns[0])


def sort_by_case_identifier(df: pd.DataFrame, case_col: str) -> pd.DataFrame:
    """Sort rows by numeric case ID when possible, with stable fallback order."""
    sorted_df = df.copy()
    sorted_df["_case_label"] = sorted_df[case_col].astype(str).str.strip()
    sorted_df["_case_numeric"] = pd.to_numeric(sorted_df["_case_label"], errors="coerce")
    sorted_df["_case_numeric_missing"] = sorted_df["_case_numeric"].isna()
    sorted_df["_source_order"] = np.arange(len(sorted_df))

    sorted_df = sorted_df.sort_values(
        by=["_case_numeric_missing", "_case_numeric", "_case_label", "_source_order"],
        kind="mergesort",
    ).copy()
    sorted_df = sorted_df.reset_index(drop=True)
    sorted_df["_x_position"] = np.arange(len(sorted_df), dtype=float)
    return sorted_df


def apply_sparse_case_ticks(ax: plt.Axes, sorted_df: pd.DataFrame, max_ticks: int = 20) -> None:
    """Apply sparse, rotated case-ID ticks to avoid overlapping labels."""
    if sorted_df.empty:
        return

    total_cases = len(sorted_df)
    if total_cases <= max_ticks:
        index_positions = np.arange(total_cases)
    else:
        index_positions = np.unique(np.linspace(0, total_cases - 1, num=max_ticks, dtype=int))

    tick_positions = sorted_df.iloc[index_positions]["_x_position"].to_numpy()
    tick_labels = sorted_df.iloc[index_positions]["_case_label"].tolist()
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha="right")


def format_component_label(column_name: str) -> str:
    """Format scale-column names for axis labels."""
    return column_name.replace("_scale", "").replace("_", " ").title()


def resolve_output_formats() -> list[str]:
    """Return the de-duplicated, normalized list of configured image formats."""
    return _unique_preserve_order(
        [str(fmt).strip().lower() for fmt in OUTPUT_IMAGE_FORMATS if str(fmt).strip() != ""]
    )


def save_figure(fig: plt.Figure, output_stem: Path) -> list[Path]:
    """Save a figure to every configured image format and return written paths.

    Parameters
    ----------
    fig : plt.Figure
        Figure to persist.
    output_stem : Path
        Target path without a file extension. One file per configured format
        is written using the format as the file suffix.

    Returns
    -------
    list[Path]
        Paths of the files written.
    """
    written: list[Path] = []
    for fmt in resolve_output_formats():
        output_path = output_stem.with_suffix(f".{fmt}")
        fig.savefig(output_path, dpi=FIGURE_DPI, format=fmt)
        written.append(output_path)
    return written


def make_distance_cost_gap_plot(
    df: pd.DataFrame,
    global_opt_index: int,
    output_stem: Path,
    cost_gap_mode: str,
) -> list[Path]:
    """Create and save the layout distance versus cost-gap plot."""
    if cost_gap_mode == "relative":
        y_col = "rel_cost_gap"
        y_label = "Relative cost gap (%)"
        title = "Layout Distance vs Relative Cost Gap"
    else:
        y_col = "abs_cost_gap"
        y_label = "Absolute cost gap"
        title = "Layout Distance vs Absolute Cost Gap"

    plt.figure(figsize=(10, 6))
    plt.scatter(
        df["layout_distance"],
        df[y_col],
        s=36,
        alpha=0.75,
        color="tab:blue",
        edgecolors="white",
        linewidths=0.5,
        label="BO trials",
    )
    plt.scatter(
        df.loc[global_opt_index, "layout_distance"],
        df.loc[global_opt_index, y_col],
        s=140,
        color="red",
        marker="*",
        edgecolors="black",
        linewidths=0.8,
        label="Global optimum",
        zorder=5,
    )
    plt.xlabel("Layout distance (normalized Euclidean)")
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    written = save_figure(plt.gcf(), output_stem)
    plt.close()
    return written


def make_plot1_per_technology_subplots(
    df: pd.DataFrame,
    global_opt_index: int,
    component_cols: list[str],
    cost_gap_mode: str,
    x_mode: str,
    output_stem: Path,
) -> list[Path]:
    """Plot plot-1 per-technology view as subplots (optimal-only rows)."""
    if cost_gap_mode == "relative":
        y_col = "rel_cost_gap"
        y_label = "Relative cost gap (%)"
    else:
        y_col = "abs_cost_gap"
        y_label = "Absolute cost gap"

    if x_mode == "delta_to_optimum":
        x_label = "Normalized deviation from optimum"
        title_suffix = "Component Deviation vs Cost Gap"
    else:
        x_label = "Min-max normalized scale value"
        title_suffix = "Component Scale vs Cost Gap"

    num_components = len(component_cols)
    fig_height = max(4.0, 2.8 * num_components)
    fig, axes = plt.subplots(num_components, 1, figsize=(12, fig_height), sharey=True)
    axes_array = np.atleast_1d(axes)

    y_values = df[y_col].astype(float)
    opt_y = float(df.loc[global_opt_index, y_col])

    for idx, component_col in enumerate(component_cols):
        axis = axes_array[idx]
        series = df[component_col].astype(float)
        min_value = float(series.min())
        max_value = float(series.max())
        span = max_value - min_value
        opt_value = float(df.loc[global_opt_index, component_col])

        if x_mode == "delta_to_optimum":
            if span > 0:
                x_values = (series - opt_value) / span
            else:
                x_values = pd.Series(0.0, index=series.index, dtype=float)
            opt_x = 0.0
        else:
            if span > 0:
                x_values = (series - min_value) / span
                opt_x = (opt_value - min_value) / span
            else:
                x_values = pd.Series(0.0, index=series.index, dtype=float)
                opt_x = 0.0

        axis.scatter(
            x_values,
            y_values,
            s=34,
            alpha=0.8,
            color="tab:blue",
            edgecolors="white",
            linewidths=0.5,
            label="BO trials" if idx == 0 else None,
            zorder=3,
        )
        axis.scatter(
            opt_x,
            opt_y,
            s=140,
            color="red",
            marker="*",
            edgecolors="black",
            linewidths=0.8,
            label="Global optimum" if idx == 0 else None,
            zorder=5,
        )
        axis.axvline(
            opt_x,
            color="red",
            linestyle="--",
            alpha=0.35,
            linewidth=0.9,
        )

        if x_mode == "minmax_value":
            axis.set_xlim(-0.05, 1.05)
        axis.set_ylabel(y_label)
        axis.set_title(format_component_label(component_col))
        axis.grid(True, linestyle="--", alpha=0.35)

    handles, labels = axes_array[0].get_legend_handles_labels()
    if handles:
        axes_array[0].legend(loc="upper right")

    axes_array[-1].set_xlabel(x_label)
    fig.suptitle(f"Plot 1 Per-Technology: {title_suffix} (Optimal Cases)")
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    written = save_figure(fig, output_stem)
    plt.close(fig)
    return written


def make_case_vs_scales_component_subplots(
    df_sorted: pd.DataFrame,
    component_norm_cols: dict[str, str],
    output_stem: Path,
) -> list[Path]:
    """Plot case ID vs normalized scales with one subplot per component."""
    components = list(component_norm_cols.keys())
    num_components = len(components)
    fig_height = max(4.0, 2.4 * num_components)
    fig, axes = plt.subplots(num_components, 1, figsize=(12, fig_height), sharex=True)
    axes_array = np.atleast_1d(axes)

    x_values = df_sorted["_x_position"].to_numpy()
    status_series = df_sorted["_termination_condition_norm"]
    optimal_mask = status_series.eq("optimal").to_numpy()
    infeasible_mask = status_series.eq("infeasible").to_numpy()

    for idx, component in enumerate(components):
        axis = axes_array[idx]
        norm_col = component_norm_cols[component]
        y_values = df_sorted[norm_col].to_numpy(dtype=float)

        # Keep a light line to show ordering, then status-specific markers.
        axis.plot(x_values, y_values, color="0.75", linewidth=0.9, alpha=0.85)
        if optimal_mask.any():
            axis.scatter(
                x_values[optimal_mask],
                y_values[optimal_mask],
                s=34,
                alpha=0.8,
                color="tab:blue",
                edgecolors="white",
                linewidths=0.5,
                label="Optimal" if idx == 0 else None,
                zorder=3,
            )
        if infeasible_mask.any():
            axis.scatter(
                x_values[infeasible_mask],
                y_values[infeasible_mask],
                s=40,
                alpha=0.9,
                color="tab:orange",
                marker="x",
                linewidths=1.2,
                label="Infeasible" if idx == 0 else None,
                zorder=4,
            )

        axis.set_ylabel(format_component_label(component))
        axis.set_ylim(-0.05, 1.05)
        axis.grid(True, linestyle="--", alpha=0.35)

    axes_array[0].set_title("Case ID vs Normalized Component Scales")
    handles, labels = axes_array[0].get_legend_handles_labels()
    if handles:
        axes_array[0].legend(loc="upper right")

    axes_array[-1].set_xlabel("Case ID")
    apply_sparse_case_ticks(axes_array[-1], df_sorted)
    fig.tight_layout()
    written = save_figure(fig, output_stem)
    plt.close(fig)
    return written


def make_case_vs_scales_aggregate_plot(
    df_sorted: pd.DataFrame,
    aggregate_col: str,
    output_stem: Path,
) -> list[Path]:
    """Plot case ID versus aggregate normalized scaling index."""
    x_values = df_sorted["_x_position"].to_numpy()
    y_values = df_sorted[aggregate_col].to_numpy(dtype=float)
    status_series = df_sorted["_termination_condition_norm"]
    optimal_mask = status_series.eq("optimal").to_numpy()
    infeasible_mask = status_series.eq("infeasible").to_numpy()

    fig, axis = plt.subplots(figsize=(12, 6))
    axis.plot(x_values, y_values, color="0.75", linewidth=0.9, alpha=0.85)
    if optimal_mask.any():
        axis.scatter(
            x_values[optimal_mask],
            y_values[optimal_mask],
            s=34,
            alpha=0.8,
            color="tab:blue",
            edgecolors="white",
            linewidths=0.5,
            label="Optimal",
            zorder=3,
        )
    if infeasible_mask.any():
        axis.scatter(
            x_values[infeasible_mask],
            y_values[infeasible_mask],
            s=40,
            alpha=0.9,
            color="tab:orange",
            marker="x",
            linewidths=1.2,
            label="Infeasible",
            zorder=4,
        )

    axis.set_xlabel("Case ID")
    axis.set_ylabel("Aggregate normalized scale index")
    axis.set_title("Case ID vs Aggregate Normalized Scaling")
    axis.set_ylim(-0.05, 1.05)
    axis.grid(True, linestyle="--", alpha=0.35)
    axis.legend(loc="upper right")
    apply_sparse_case_ticks(axis, df_sorted)
    fig.tight_layout()
    written = save_figure(fig, output_stem)
    plt.close(fig)
    return written


def _label_with_unit(base_label: str, unit: str | None) -> str:
    """Append a unit in square brackets to an axis label when a unit is provided."""
    unit_text = "" if unit is None else str(unit).strip()
    if unit_text == "":
        return base_label
    return f"{base_label} [{unit_text}]"


def make_case_vs_total_cost_plot(
    df_sorted: pd.DataFrame,
    cost_col: str,
    output_stem: Path,
    y_label: str,
    title: str,
    y_unit: str | None = None,
) -> list[Path]:
    """Plot case ID versus the objective value for optimal cases only."""
    x_values = df_sorted["_x_position"].to_numpy()
    y_values = df_sorted[cost_col].to_numpy(dtype=float)

    fig, axis = plt.subplots(figsize=(12, 6))
    axis.plot(x_values, y_values, color="0.75", linewidth=0.9, alpha=0.85)
    axis.scatter(
        x_values,
        y_values,
        s=34,
        alpha=0.8,
        color="tab:blue",
        edgecolors="white",
        linewidths=0.5,
        label="BO trials",
        zorder=3,
    )

    min_idx = int(np.argmin(y_values))
    axis.scatter(
        x_values[min_idx],
        y_values[min_idx],
        s=140,
        color="red",
        marker="*",
        edgecolors="black",
        linewidths=0.8,
        label=f"Minimum {y_label}",
        zorder=5,
    )

    axis.set_xlabel("Case ID")
    axis.set_ylabel(_label_with_unit(y_label, y_unit))
    axis.set_title(title)
    axis.grid(True, linestyle="--", alpha=0.35)
    axis.legend(loc="best")
    apply_sparse_case_ticks(axis, df_sorted)
    fig.tight_layout()
    written = save_figure(fig, output_stem)
    plt.close(fig)
    return written


def make_lcom_vs_component_plot(
    df: pd.DataFrame,
    global_opt_index: int,
    component_col: str,
    cost_col: str,
    y_label: str,
    output_stem: Path,
    y_unit: str | None = None,
    component_unit: str | None = None,
    y_scale: str = "linear",
    y_max: float | None = None,
) -> list[Path]:
    """Plot objective (LCOM) versus one component's absolute sizing.

    The y-axis can use a log scale and/or an upper LCOM cap to better reveal the
    spread across trials whose LCOM values otherwise compress against large outliers.
    """
    component_label = format_component_label(component_col)

    plot_df = df
    clipped_count = 0
    if y_max is not None:
        mask = df[cost_col].astype(float) <= float(y_max)
        clipped_count = int((~mask).sum())
        plot_df = df[mask].copy()
        if plot_df.empty:
            raise ValueError(
                f"`LCOM_Y_MAX` ({y_max}) removed all rows; nothing to plot."
            )

    y_values = plot_df[cost_col].astype(float)
    absolute_values = plot_df[component_col].astype(float)

    opt_in_view = global_opt_index in plot_df.index
    opt_y = float(df.loc[global_opt_index, cost_col])
    opt_abs = float(df.loc[global_opt_index, component_col])

    fig, axis = plt.subplots(figsize=(9, 6))
    axis.scatter(
        absolute_values,
        y_values,
        s=36,
        alpha=0.75,
        color="tab:blue",
        edgecolors="white",
        linewidths=0.5,
        label="BO trials",
    )
    if opt_in_view:
        axis.scatter(
            opt_abs,
            opt_y,
            s=140,
            color="red",
            marker="*",
            edgecolors="black",
            linewidths=0.8,
            label=f"Minimum {y_label}",
            zorder=5,
        )

    if y_scale == "log":
        axis.set_yscale("log")

    axis.set_xlabel(_label_with_unit(f"{component_label} sizing", component_unit))
    axis.set_ylabel(_label_with_unit(y_label, y_unit))
    axis.grid(True, which="both", linestyle="--", alpha=0.4)
    axis.legend(loc="best")

    title = f"{y_label} vs {component_label} Sizing (Optimal Cases)"
    if y_max is not None:
        title = f"{title}\n{y_label} <= {y_max:g} {y_unit or ''}".rstrip()
    fig.suptitle(title)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    written = save_figure(fig, output_stem)
    plt.close(fig)
    return written


def main() -> None:
    """Run the configured plotting and analysis workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    selected_plots = validate_runtime_configuration()

    draw_plot1 = "distance_cost_gap" in selected_plots
    draw_plot2 = "case_vs_scales" in selected_plots
    draw_plot3 = "case_vs_total_cost" in selected_plots
    draw_plot_lcom = "lcom_vs_component" in selected_plots
    draw_plot1_global = draw_plot1 and PLOT1_VIEW_MODE in {"global_distance", "both"}
    draw_plot1_per_tech = draw_plot1 and PLOT1_VIEW_MODE in {"per_technology", "both"}

    run_config = load_run_config_json(RUN_CONFIG_FILE)
    included_techs, excluded_techs = extract_technology_scope_from_run_config(run_config)

    df_raw = load_rmse_dataframe(INPUT_FILE, INPUT_SHEET)
    if df_raw.empty:
        raise ValueError("Input sheet is empty after dropping fully empty rows.")

    termination_col = _find_column(df_raw.columns, ["termination_condition"])
    if termination_col is None and (draw_plot1 or draw_plot2 or draw_plot3 or draw_plot_lcom):
        raise ValueError("Missing required column: `termination_condition`.")

    cost_col = _find_column(df_raw.columns, ["objective_value", "objective_value"])
    if cost_col is None and (draw_plot1 or draw_plot3 or draw_plot_lcom):
        raise ValueError("Could not find a cost column (`total_cost` or `total_costs`).")

    case_col = choose_identifier_column(df_raw)
    df_status = add_normalized_status_column(df_raw, termination_col) if termination_col else df_raw.copy()

    df_optimal_raw = df_status[df_status["_termination_condition_norm"] == "optimal"].copy()
    df_plot2_raw = df_status[
        df_status["_termination_condition_norm"].isin(PLOT2_ALLOWED_STATUSES)
    ].copy()

    if draw_plot1 and df_optimal_raw.empty:
        raise ValueError("No `optimal` rows available for `distance_cost_gap` plotting.")
    if draw_plot3 and df_optimal_raw.empty:
        raise ValueError("No `optimal` rows available for `case_vs_total_cost` plotting.")
    if draw_plot_lcom and df_optimal_raw.empty:
        raise ValueError("No `optimal` rows available for `lcom_vs_component` plotting.")
    if draw_plot2 and df_plot2_raw.empty:
        raise ValueError(
            "No rows with termination status in {'optimal', 'infeasible'} "
            "available for `case_vs_scales` plotting."
        )

    design_techs: list[str] = []
    design_cols: list[str] = []
    tech_to_col: dict[str, str] = {}
    selected_subplot_techs: list[str] = []
    subplot_cols: list[str] = []
    if draw_plot1 or draw_plot2 or draw_plot_lcom:
        design_techs, design_cols, tech_to_col = resolve_design_columns_from_run_config(
            df_columns=df_raw.columns,
            included_techs=included_techs,
            excluded_techs=excluded_techs,
        )
        selected_subplot_techs = resolve_subplot_technology_selection(
            subplot_technologies=SUBPLOT_TECHNOLOGIES,
            available_technologies=design_techs,
        )
        subplot_cols = [tech_to_col[technology] for technology in selected_subplot_techs]

    lcom_component_col: str | None = None
    if draw_plot_lcom:
        lcom_tech_key = str(LCOM_VS_COMPONENT_TECH).strip()
        tech_to_col_lower = {key.lower(): col for key, col in tech_to_col.items()}
        lcom_component_col = tech_to_col_lower.get(lcom_tech_key.lower())
        if lcom_component_col is None:
            raise ValueError(
                f"`LCOM_VS_COMPONENT_TECH` ({LCOM_VS_COMPONENT_TECH!r}) is not a resolved "
                f"design technology. Available: {_format_list(list(tech_to_col.keys()))}."
            )

    generated_files: list[Path] = []
    summary_lines = [
        "=== Layout Distance and Case Plot Summary ===",
        f"Input file: {INPUT_FILE}",
        f"Sheet: {INPUT_SHEET}",
        f"Run config file: {RUN_CONFIG_FILE}",
        f"Selected plots: {', '.join(selected_plots)}",
        f"Plot 1 view mode: {PLOT1_VIEW_MODE}",
        f"Plot 1 cost-gap mode: {PLOT1_COST_GAP_MODE}",
        f"Plot 1 per-tech x mode: {PLOT1_PER_TECH_X_MODE}",
        f"Plot 2 view mode: {PLOT2_VIEW_MODE}",
        f"Output image formats: {_format_list(resolve_output_formats())}",
        f"Case identifier column: {case_col}",
        f"Termination status column: {termination_col}",
        f"Included technologies from run config: {_format_list(included_techs)}",
        f"Excluded technologies from run config: {_format_list(excluded_techs)}",
    ]

    if draw_plot1 or draw_plot2 or draw_plot_lcom:
        summary_lines.extend(
            [
                f"Resolved design technologies: {_format_list(design_techs)}",
                f"Resolved design columns: {_format_list(design_cols)}",
                f"Selected subplot technologies: {_format_list(selected_subplot_techs)}",
                f"Selected subplot columns: {_format_list(subplot_cols)}",
            ]
        )
    else:
        summary_lines.append(
            "Design columns were not resolved because plot 1 and plot 2 are both disabled."
        )

    summary_lines.extend(["", "Termination status counts (normalized):"])
    status_counts = df_status["_termination_condition_norm"].value_counts(dropna=False)
    for status, count in status_counts.items():
        status_label = status if status else "<blank>"
        summary_lines.append(f"- {status_label}: {int(count)}")

    if draw_plot1:
        numeric_cols = [cost_col, *design_cols]
        df_plot1 = prepare_numeric_dataframe(df_optimal_raw, numeric_cols=numeric_cols)
        if df_plot1.empty:
            raise ValueError(
                "No numeric-valid optimal rows for plot 1 after cleaning required columns."
            )

        global_opt_index = int(df_plot1[cost_col].idxmin())
        global_opt = df_plot1.loc[global_opt_index]
        df_plot1_cost_gap = add_cost_gap_metrics(
            df=df_plot1,
            global_opt_row=global_opt,
            cost_col=cost_col,
        )

        if draw_plot1_per_tech:
            plot1_per_tech_stem = OUTPUT_DIR / (
                f"plot1_per_technology_{PLOT1_PER_TECH_X_MODE}_vs_"
                f"{'rel' if PLOT1_COST_GAP_MODE == 'relative' else 'abs'}_cost_gap"
            )
            plot1_per_tech_files = make_plot1_per_technology_subplots(
                df=df_plot1_cost_gap,
                global_opt_index=global_opt_index,
                component_cols=subplot_cols,
                cost_gap_mode=PLOT1_COST_GAP_MODE,
                x_mode=PLOT1_PER_TECH_X_MODE,
                output_stem=plot1_per_tech_stem,
            )
            generated_files.extend(plot1_per_tech_files)
            summary_lines.extend(
                [
                    "",
                    "Plot 1 per-technology mode:",
                    f"- Components plotted: {len(subplot_cols)}",
                    f"- X-mode: {PLOT1_PER_TECH_X_MODE}",
                ]
            )

        if draw_plot1_global:
            ranges = compute_ranges(df_plot1, design_cols)
            valid_design_cols = list(ranges.index)
            if not valid_design_cols:
                raise ValueError("All design variables have zero range; distance cannot be computed.")

            df_metrics, squared_contrib = compute_metrics(
                df=df_plot1,
                global_opt_row=global_opt,
                cost_col=cost_col,
                valid_design_cols=valid_design_cols,
                ranges=ranges,
            )

            if PLOT1_COST_GAP_MODE == "relative":
                plot1_stem = OUTPUT_DIR / "layout_distance_vs_rel_cost_gap"
            else:
                plot1_stem = OUTPUT_DIR / "layout_distance_vs_abs_cost_gap"
            plot1_files = make_distance_cost_gap_plot(
                df_metrics,
                global_opt_index=global_opt_index,
                output_stem=plot1_stem,
                cost_gap_mode=PLOT1_COST_GAP_MODE,
            )
            generated_files.extend(plot1_files)

            p75_dist = float(df_metrics["layout_distance"].quantile(0.75))
            p10_dist = float(df_metrics["layout_distance"].quantile(0.10))

            # "Far but cheap": close in cost, far in design space.
            near_opt_struct_diff = df_metrics[
                (df_metrics["rel_cost_gap"] <= 5.0) & (df_metrics["layout_distance"] >= p75_dist)
            ].copy()
            # "Near but expensive": similar layout, much worse economics.
            struct_sim_poor_cost = df_metrics[
                (df_metrics["layout_distance"] <= p10_dist) & (df_metrics["rel_cost_gap"] >= 25.0)
            ].copy()
            # "Near and cheap": similar layout and similar economics.
            very_close_opt = df_metrics[
                (df_metrics["layout_distance"] <= p10_dist) & (df_metrics["rel_cost_gap"] <= 5.0)
            ].copy()

            near_opt_path = OUTPUT_DIR / "near_optimal_but_structurally_different.csv"
            struct_sim_path = OUTPUT_DIR / "structurally_similar_but_poor_cost.csv"
            very_close_path = OUTPUT_DIR / "very_close_to_optimum.csv"
            near_opt_struct_diff.to_csv(near_opt_path, index=False)
            struct_sim_poor_cost.to_csv(struct_sim_path, index=False)
            very_close_opt.to_csv(very_close_path, index=False)
            generated_files.extend([near_opt_path, struct_sim_path, very_close_path])

            identifier_col = choose_identifier_column(df_metrics)
            far_but_cheap = near_opt_struct_diff.sort_values("layout_distance", ascending=False)
            top10_far_but_cheap = far_but_cheap.head(10).copy()
            if top10_far_but_cheap.empty:
                top10_far_but_cheap = df_metrics.sort_values(
                    by=["rel_cost_gap", "layout_distance"], ascending=[True, False]
                ).head(10)

            contribution_df = squared_contrib.loc[top10_far_but_cheap.index].copy()
            contribution_df = contribution_df.rename(columns=lambda c: f"{c}_sq_norm_contrib")
            contribution_df.insert(
                0,
                identifier_col,
                df_metrics.loc[top10_far_but_cheap.index, identifier_col],
            )
            contribution_df["layout_distance"] = df_metrics.loc[
                top10_far_but_cheap.index, "layout_distance"
            ].values
            contribution_df["rel_cost_gap"] = df_metrics.loc[top10_far_but_cheap.index, "rel_cost_gap"].values

            contribution_path = OUTPUT_DIR / "top10_far_but_cheap_contributions.csv"
            metrics_path = OUTPUT_DIR / "rmse_with_layout_distance_and_cost_gaps.csv"
            ranges_path = OUTPUT_DIR / "normalization_ranges.csv"
            contribution_df.to_csv(contribution_path, index=False)
            df_metrics.to_csv(metrics_path, index=False)
            ranges.to_csv(ranges_path, header=["range"])
            generated_files.extend([contribution_path, metrics_path, ranges_path])

            within_1 = int((df_metrics["rel_cost_gap"] <= 1.0).sum())
            within_3 = int((df_metrics["rel_cost_gap"] <= 3.0).sum())
            within_5 = int((df_metrics["rel_cost_gap"] <= 5.0).sum())
            example_cols = [
                col
                for col in [identifier_col, cost_col, "layout_distance", "abs_cost_gap", "rel_cost_gap"]
                if col in df_metrics.columns
            ]
            example_rows = df_metrics.sort_values("rel_cost_gap").head(8)[example_cols]

            summary_lines.extend(
                [
                    "",
                    "Distance-cost analysis (optimal rows only, global distance view):",
                    f"- Total valid optimal cases in distance analysis: {len(df_metrics)}",
                    f"- Global optimum index: {global_opt_index}",
                    f"- Global optimum {identifier_col}: {df_metrics.loc[global_opt_index, identifier_col]}",
                    f"- Global optimum {cost_col}: {df_metrics.loc[global_opt_index, cost_col]:,.6f}",
                    "",
                    "Counts within relative optimum cost gap thresholds:",
                    f"- <= 1%: {within_1}",
                    f"- <= 3%: {within_3}",
                    f"- <= 5%: {within_5}",
                    "",
                    (
                        "Far-but-cheap count "
                        "(rel_cost_gap <= 5% and layout_distance >= 75th percentile): "
                        f"{len(near_opt_struct_diff)}"
                    ),
                    "",
                    "Normalization ranges used:",
                ]
            )
            for col_name, col_range in ranges.items():
                summary_lines.append(f"- {col_name}: {col_range:.6f}")
            summary_lines.extend(
                [
                    "",
                    "Example rows (best relative cost gap):",
                    example_rows.to_string(index=False),
                ]
            )
        else:
            summary_lines.extend(
                [
                    "",
                    "Distance-cost analysis artifacts were skipped because "
                    "`PLOT1_VIEW_MODE` does not include `global_distance`.",
                ]
            )
    else:
        summary_lines.extend(
            [
                "",
                "Plot 1 artifacts were skipped because `distance_cost_gap` is not selected "
                "in `PLOTS_TO_DRAW`.",
            ]
        )

    if draw_plot2:
        df_plot2 = prepare_numeric_dataframe(df_plot2_raw, numeric_cols=subplot_cols)
        if df_plot2.empty:
            raise ValueError(
                "No numeric-valid rows for plot 2 after cleaning selected subplot design columns."
            )

        df_plot2_sorted = sort_by_case_identifier(df_plot2, case_col=case_col)
        normalized_components = minmax_normalize_columns(df_plot2_sorted, subplot_cols)
        component_norm_cols: dict[str, str] = {}
        for design_col in subplot_cols:
            norm_col = f"{design_col}_norm"
            df_plot2_sorted[norm_col] = normalized_components[design_col].values
            component_norm_cols[design_col] = norm_col

        if PLOT2_VIEW_MODE in {"component_subplots", "both"}:
            plot2_components_stem = OUTPUT_DIR / "case_id_vs_normalized_scales_components"
            plot2_components_files = make_case_vs_scales_component_subplots(
                df_sorted=df_plot2_sorted,
                component_norm_cols=component_norm_cols,
                output_stem=plot2_components_stem,
            )
            generated_files.extend(plot2_components_files)

        if PLOT2_VIEW_MODE in {"aggregate", "both"}:
            aggregate_raw = df_plot2_sorted[list(component_norm_cols.values())].sum(axis=1)
            df_plot2_sorted["aggregate_normalized_scale"] = minmax_normalize_series(aggregate_raw)
            plot2_aggregate_stem = OUTPUT_DIR / "case_id_vs_aggregate_normalized_scale"
            plot2_aggregate_files = make_case_vs_scales_aggregate_plot(
                df_sorted=df_plot2_sorted,
                aggregate_col="aggregate_normalized_scale",
                output_stem=plot2_aggregate_stem,
            )
            generated_files.extend(plot2_aggregate_files)

    if draw_plot3:
        df_plot3 = prepare_numeric_dataframe(df_optimal_raw, numeric_cols=[cost_col])
        if df_plot3.empty:
            raise ValueError(
                "No numeric-valid optimal rows for plot 3 after cleaning total cost column."
            )
        df_plot3_sorted = sort_by_case_identifier(df_plot3, case_col=case_col)
        plot3_stem = OUTPUT_DIR / "case_id_vs_lcom_optimal"
        plot3_files = make_case_vs_total_cost_plot(
            df_plot3_sorted,
            cost_col=cost_col,
            output_stem=plot3_stem,
            y_label=PLOT3_Y_LABEL,
            title=PLOT3_TITLE,
            y_unit=PLOT3_Y_UNIT,
        )
        generated_files.extend(plot3_files)

    if draw_plot_lcom:
        df_lcom = prepare_numeric_dataframe(
            df_optimal_raw, numeric_cols=[cost_col, lcom_component_col]
        )
        if df_lcom.empty:
            raise ValueError(
                "No numeric-valid optimal rows for `lcom_vs_component` after cleaning columns."
            )
        lcom_opt_index = int(df_lcom[cost_col].idxmin())
        lcom_stem = OUTPUT_DIR / (
            f"lcom_vs_{lcom_component_col}_absolute"
        )
        lcom_files = make_lcom_vs_component_plot(
            df=df_lcom,
            global_opt_index=lcom_opt_index,
            component_col=lcom_component_col,
            cost_col=cost_col,
            y_label=LCOM_Y_LABEL,
            output_stem=lcom_stem,
            y_unit=LCOM_Y_UNIT,
            component_unit=LCOM_COMPONENT_UNIT,
            y_scale=LCOM_Y_SCALE,
            y_max=LCOM_Y_MAX,
        )
        generated_files.extend(lcom_files)

    unique_generated_files = list(dict.fromkeys(generated_files))
    summary_lines.extend(["", "Output files:"])
    for output_file in unique_generated_files:
        summary_lines.append(f"- {output_file}")

    summary_text = "\n".join(summary_lines)
    print(summary_text)
    summary_path = OUTPUT_DIR / "summary.txt"
    summary_path.write_text(summary_text, encoding="utf-8")


if __name__ == "__main__":
    main()
