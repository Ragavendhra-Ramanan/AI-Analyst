"""Chart generation functions for visualizations."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch
import sys

sys.path.append("/Users/pragathi.vetrivelmurugan/AI-Analyst/backend/app")
from ..utils.helpers import format_currency


class ChartGenerator:
    """Generator for various chart types."""

    def __init__(self):
        # Set style - try seaborn first, fallback to default
        try:
            plt.style.use("seaborn-v0_8")
        except:
            try:
                plt.style.use("seaborn")
            except:
                plt.style.use("default")
        self.colors = [
            "#3498db",
            "#e74c3c",
            "#2ecc71",
            "#f39c12",
            "#9b59b6",
            "#1abc9c",
            "#e67e22",
        ]

    def create_radar_chart(self, metrics_df, target_company_name, output_path):
        """Create radar chart comparing company metrics."""
        if metrics_df.empty:
            return False

        # Define metrics for radar chart
        radar_metrics = [
            "revenue",
            "cac",
            "ltv_cac_ratio",
            "gross_margin_pct",
            "valuation",
        ]
        available_metrics = []

        for metric in radar_metrics:
            if metric in metrics_df.columns:
                # Check if there are at least 2 non-null values for this metric
                non_null_count = metrics_df[metric].notna().sum()
                if non_null_count >= 2:
                    available_metrics.append(metric)

        print(f"Available metrics for radar chart: {available_metrics}")

        if len(available_metrics) < 3:
            print(
                f"Not enough metrics available for radar chart (need 3, have {len(available_metrics)})"
            )
            return False

        # Normalize metrics to 0-1 scale
        normalized_df = metrics_df.copy()
        for metric in available_metrics:
            metric_series = normalized_df[metric].dropna()
            if len(metric_series) < 2:
                continue

            min_val = metric_series.min()
            max_val = metric_series.max()

            if min_val == max_val:
                # If all values are the same, set to 0.5
                normalized_df[metric] = 0.5
            else:
                if metric == "cac":  # Lower is better for CAC
                    normalized_df[metric] = 1 - (normalized_df[metric] - min_val) / (
                        max_val - min_val
                    )
                else:
                    normalized_df[metric] = (normalized_df[metric] - min_val) / (
                        max_val - min_val
                    )

        # Fill NaN values with 0
        for metric in available_metrics:
            normalized_df[metric] = normalized_df[metric].fillna(0)

        # Create radar chart
        angles = np.linspace(
            0, 2 * np.pi, len(available_metrics), endpoint=False
        ).tolist()
        angles += angles[:1]  # Complete the circle

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection="polar"))

        # Plot each company
        for idx, (_, row) in enumerate(normalized_df.iterrows()):
            values = [
                row[metric] if not np.isnan(row[metric]) else 0
                for metric in available_metrics
            ]
            values += values[:1]  # Complete the circle

            color = (
                "#e74c3c"
                if row["company_name"] == target_company_name
                else self.colors[idx % len(self.colors)]
            )
            linewidth = 3 if row["company_name"] == target_company_name else 2
            alpha = 0.8 if row["company_name"] == target_company_name else 0.6

            ax.plot(
                angles,
                values,
                "o-",
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                label=row["company_name"],
            )
            ax.fill(angles, values, alpha=0.25, color=color)

        # Customize chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(
            [metric.replace("_", " ").title() for metric in available_metrics]
        )
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(["20%", "40%", "60%", "80%", "100%"])
        ax.grid(True)

        plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0))
        plt.title("Company Performance Radar Chart", size=16, fontweight="bold", pad=20)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return True

    def create_heatmap(self, metrics_df, output_path):
        """Create heatmap of normalized metrics."""
        if metrics_df.empty:
            return False

        # Select numeric columns for heatmap
        numeric_cols = [
            "revenue",
            "cac",
            "ltv_cac_ratio",
            "gross_margin_pct",
            "valuation",
            "orders_fulfilled_total",
        ]
        available_cols = [col for col in numeric_cols if col in metrics_df.columns]

        if len(available_cols) < 2:
            print("Not enough numeric metrics for heatmap")
            return False

        # Prepare data for heatmap - ensure numeric types
        heatmap_data = metrics_df[["company_name"] + available_cols].set_index(
            "company_name"
        )

        # Convert to numeric and handle non-numeric values
        for col in available_cols:
            heatmap_data[col] = pd.to_numeric(heatmap_data[col], errors="coerce")

        # Remove rows/columns with all NaN values
        heatmap_data = heatmap_data.dropna(how="all", axis=0)  # Drop rows with all NaN
        heatmap_data = heatmap_data.dropna(
            how="all", axis=1
        )  # Drop columns with all NaN

        if heatmap_data.empty:
            print("No valid data for heatmap after cleaning")
            return False

        # Update available columns after cleaning
        available_cols = [col for col in available_cols if col in heatmap_data.columns]

        if len(available_cols) < 2:
            print("Not enough columns remaining for heatmap after cleaning")
            return False

        # Normalize data
        for col in available_cols:
            col_data = heatmap_data[col].dropna()
            if len(col_data) < 2:
                continue

            min_val = col_data.min()
            max_val = col_data.max()

            if min_val == max_val:
                heatmap_data[col] = 0.5  # Set to middle value if all same
            else:
                if col == "cac":  # Lower is better for CAC
                    heatmap_data[col] = 1 - (heatmap_data[col] - min_val) / (
                        max_val - min_val
                    )
                else:
                    heatmap_data[col] = (heatmap_data[col] - min_val) / (
                        max_val - min_val
                    )

        # Fill any remaining NaN values
        heatmap_data = heatmap_data.fillna(0)

        # Create heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            heatmap_data,
            annot=True,
            cmap="RdYlGn",
            center=0.5,
            fmt=".2f",
            cbar_kws={"label": "Normalized Performance (0-1)"},
        )
        plt.title("Company Performance Heatmap", fontsize=16, fontweight="bold")
        plt.xlabel("Metrics", fontweight="bold")
        plt.ylabel("Companies", fontweight="bold")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return True

    def create_bubble_chart(self, metrics_df, target_company_name, output_path):
        """Create bubble chart with revenue vs valuation."""
        if (
            metrics_df.empty
            or "revenue" not in metrics_df.columns
            or "valuation" not in metrics_df.columns
        ):
            return False

        # Filter data with both revenue and valuation
        bubble_data = metrics_df.dropna(subset=["revenue", "valuation"])

        if bubble_data.empty:
            print("No companies with both revenue and valuation data")
            return False

        plt.figure(figsize=(12, 8))

        for _, row in bubble_data.iterrows():
            color = (
                "#e74c3c" if row["company_name"] == target_company_name else "#3498db"
            )
            size = 1000 if row["company_name"] == target_company_name else 500
            alpha = 0.8 if row["company_name"] == target_company_name else 0.6

            plt.scatter(
                row["revenue"],
                row["valuation"],
                s=size,
                alpha=alpha,
                color=color,
                edgecolors="black",
                linewidth=2,
            )
            plt.annotate(
                row["company_name"],
                (row["revenue"], row["valuation"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=10,
                fontweight="bold",
            )

        plt.xlabel("Revenue (INR)", fontweight="bold", fontsize=12)
        plt.ylabel("Valuation (INR)", fontweight="bold", fontsize=12)
        plt.title("Revenue vs Valuation Bubble Chart", fontsize=16, fontweight="bold")
        plt.grid(True, alpha=0.3)

        # Format axes
        ax = plt.gca()
        ax.ticklabel_format(style="scientific", axis="both", scilimits=(0, 0))

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return True

    def create_quadrant_analysis(self, metrics_df, target_company_name, output_path):
        """Create quadrant analysis chart."""
        if (
            metrics_df.empty
            or "revenue" not in metrics_df.columns
            or "ltv_cac_ratio" not in metrics_df.columns
        ):
            return False

        quadrant_data = metrics_df.dropna(subset=["revenue", "ltv_cac_ratio"])

        if quadrant_data.empty:
            print("No companies with both revenue and LTV/CAC ratio data")
            return False

        fig, ax = plt.subplots(figsize=(12, 10))

        # Calculate median values for quadrant lines
        revenue_median = quadrant_data["revenue"].median()
        ltv_cac_median = quadrant_data["ltv_cac_ratio"].median()

        # Draw quadrant lines
        ax.axvline(x=revenue_median, color="gray", linestyle="--", alpha=0.7)
        ax.axhline(y=ltv_cac_median, color="gray", linestyle="--", alpha=0.7)

        # Plot companies
        for _, row in quadrant_data.iterrows():
            color = (
                "#e74c3c" if row["company_name"] == target_company_name else "#3498db"
            )
            size = 200 if row["company_name"] == target_company_name else 100
            alpha = 0.8 if row["company_name"] == target_company_name else 0.6

            ax.scatter(
                row["revenue"],
                row["ltv_cac_ratio"],
                s=size,
                alpha=alpha,
                color=color,
                edgecolors="black",
                linewidth=2,
            )
            ax.annotate(
                row["company_name"],
                (row["revenue"], row["ltv_cac_ratio"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=10,
                fontweight="bold",
            )

        # Add quadrant labels
        ax.text(
            0.25,
            0.95,
            "High Efficiency\nLow Revenue",
            transform=ax.transAxes,
            ha="center",
            va="top",
            bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.7),
            fontweight="bold",
        )
        ax.text(
            0.75,
            0.95,
            "High Efficiency\nHigh Revenue",
            transform=ax.transAxes,
            ha="center",
            va="top",
            bbox=dict(boxstyle="round", facecolor="lightgreen", alpha=0.7),
            fontweight="bold",
        )
        ax.text(
            0.25,
            0.05,
            "Low Efficiency\nLow Revenue",
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            bbox=dict(boxstyle="round", facecolor="lightcoral", alpha=0.7),
            fontweight="bold",
        )
        ax.text(
            0.75,
            0.05,
            "Low Efficiency\nHigh Revenue",
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.7),
            fontweight="bold",
        )

        ax.set_xlabel("Revenue (INR)", fontweight="bold", fontsize=12)
        ax.set_ylabel("LTV/CAC Ratio", fontweight="bold", fontsize=12)
        ax.set_title(
            "Revenue vs LTV/CAC Quadrant Analysis", fontsize=16, fontweight="bold"
        )
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return True

    def create_distribution_plots(self, metrics_df, target_company_name, output_path):
        """Create distribution plots for key metrics."""
        if metrics_df.empty:
            return False

        # Select metrics for distribution
        distribution_metrics = ["revenue", "cac", "ltv_cac_ratio", "gross_margin_pct"]
        available_metrics = [
            m
            for m in distribution_metrics
            if m in metrics_df.columns and not metrics_df[m].isna().all()
        ]

        if not available_metrics:
            print("No metrics available for distribution plots")
            return False

        n_metrics = len(available_metrics)
        cols = 2
        rows = (n_metrics + 1) // 2

        fig, axes = plt.subplots(rows, cols, figsize=(15, 4 * rows))
        if rows == 1:
            axes = [axes] if cols == 1 else axes
        else:
            axes = axes.flatten()

        for idx, metric in enumerate(available_metrics):
            ax = axes[idx]

            # Create histogram
            data = metrics_df[metric].dropna()
            ax.hist(
                data,
                bins=min(10, len(data)),
                alpha=0.7,
                color="lightblue",
                edgecolor="black",
            )

            # Mark target company
            target_value = (
                metrics_df[metrics_df["company_name"] == target_company_name][
                    metric
                ].iloc[0]
                if not metrics_df[
                    metrics_df["company_name"] == target_company_name
                ].empty
                else None
            )
            if target_value and not np.isnan(target_value):
                ax.axvline(
                    x=target_value,
                    color="red",
                    linestyle="--",
                    linewidth=2,
                    label=f"{target_company_name}",
                )
                ax.legend()

            ax.set_title(
                f"{metric.replace('_', ' ').title()} Distribution", fontweight="bold"
            )
            ax.set_xlabel(metric.replace("_", " ").title())
            ax.set_ylabel("Frequency")
            ax.grid(True, alpha=0.3)

        # Hide unused subplots
        for idx in range(n_metrics, len(axes)):
            axes[idx].set_visible(False)

        plt.suptitle("Metric Distributions", fontsize=16, fontweight="bold")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return True


# Global instance
chart_generator = ChartGenerator()
