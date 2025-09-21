"""Comparison visualization functions for benchmarking."""

import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append("/Users/pragathi.vetrivelmurugan/AI-Analyst/backend/app")
from ..utils.helpers import format_currency


class ComparisonVisualizer:
    """Visualizer for comparison and benchmark charts."""

    def __init__(self):
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

    def create_scorecard(self, target_data, benchmarks, output_path):
        """Create a scorecard showing target company performance vs benchmarks."""
        if not target_data or not benchmarks:
            return False

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis("off")

        # Title
        company_name = target_data.get("company_overview", {}).get(
            "name", "Target Company"
        )
        fig.suptitle(
            f"{company_name} Performance Scorecard",
            fontsize=20,
            fontweight="bold",
            y=0.95,
        )

        # Create scorecard sections
        y_position = 0.85
        row_height = 0.15

        scorecard_metrics = [
            ("Revenue Performance", "revenue"),
            ("Customer Acquisition Cost", "cac"),
            ("LTV/CAC Ratio", "ltv_cac_ratio"),
            ("Gross Margin", "gross_margin_pct"),
        ]

        for i, (label, metric_key) in enumerate(scorecard_metrics):
            if metric_key not in benchmarks:
                continue

            # Get target value
            target_value = self._get_metric_value(target_data, metric_key)
            if target_value is None:
                continue

            # Get benchmark data
            benchmark_data = benchmarks[metric_key]
            median_value = benchmark_data["median"]
            p25_value = benchmark_data["p25"]
            p75_value = benchmark_data["p75"]

            # Determine performance level
            if metric_key == "cac":  # Lower is better for CAC
                if target_value <= p25_value:
                    performance = "Excellent"
                    color = "#2ecc71"
                elif target_value <= median_value:
                    performance = "Good"
                    color = "#f39c12"
                elif target_value <= p75_value:
                    performance = "Average"
                    color = "#e67e22"
                else:
                    performance = "Needs Improvement"
                    color = "#e74c3c"
            else:  # Higher is better for other metrics
                if target_value >= p75_value:
                    performance = "Excellent"
                    color = "#2ecc71"
                elif target_value >= median_value:
                    performance = "Good"
                    color = "#f39c12"
                elif target_value >= p25_value:
                    performance = "Average"
                    color = "#e67e22"
                else:
                    performance = "Needs Improvement"
                    color = "#e74c3c"

            # Draw scorecard row
            y_pos = y_position - (i * row_height)

            # Metric label
            ax.text(0.05, y_pos, label, fontsize=14, fontweight="bold", va="center")

            # Target value
            formatted_target = (
                format_currency(target_value)
                if metric_key in ["revenue", "cac"]
                else f"{target_value:.2f}"
            )
            if metric_key == "gross_margin_pct":
                formatted_target = f"{target_value:.1f}%"

            ax.text(
                0.35,
                y_pos,
                formatted_target,
                fontsize=12,
                va="center",
                fontweight="bold",
            )

            # Benchmark comparison
            formatted_median = (
                format_currency(median_value)
                if metric_key in ["revenue", "cac"]
                else f"{median_value:.2f}"
            )
            if metric_key == "gross_margin_pct":
                formatted_median = f"{median_value:.1f}%"

            ax.text(
                0.55, y_pos, f"Median: {formatted_median}", fontsize=11, va="center"
            )

            # Performance indicator
            rect = plt.Rectangle(
                (0.75, y_pos - 0.03),
                0.2,
                0.06,
                facecolor=color,
                alpha=0.7,
                edgecolor="black",
            )
            ax.add_patch(rect)
            ax.text(
                0.85,
                y_pos,
                performance,
                fontsize=11,
                va="center",
                ha="center",
                fontweight="bold",
                color="white",
            )

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return True

    def create_fundraise_analysis(self, target_data, competitor_data, output_path):
        """Create fundraise analysis visualization."""
        if not target_data:
            return False

        target_fundraise = (
            target_data.get("fundraise")
            if target_data.get("fundraise") is not None
            else {}
        )
        if not target_fundraise:
            print("No fundraise data available for target company")
            return False

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # Left plot: Fundraise timeline
        self._plot_fundraise_timeline(ax1, target_fundraise)

        # Right plot: Valuation comparison
        self._plot_valuation_comparison(ax2, target_data, competitor_data)

        plt.suptitle("Fundraise Analysis", fontsize=16, fontweight="bold")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return True

    def create_traction_comparison(self, target_data, competitor_data, output_path):
        """Create traction comparison visualization."""
        if not target_data:
            return False

        target_traction = (
            target_data.get("traction")
            if target_data.get("traction") is not None
            else {}
        )
        if not target_traction:
            print("No traction data available for target company")
            return False

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        # Plot various traction metrics
        self._plot_orders_comparison(ax1, target_data, competitor_data)
        self._plot_repeat_rate_comparison(ax2, target_data, competitor_data)
        self._plot_gmv_comparison(ax3, target_data, competitor_data)
        self._plot_aov_comparison(ax4, target_data, competitor_data)

        plt.suptitle("Traction Metrics Comparison", fontsize=16, fontweight="bold")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return True

    def _get_metric_value(self, company_data, metric_key):
        """Extract metric value from company data."""
        if metric_key == "revenue":
            return company_data.get("financials", {}).get("revenue", {}).get("amount")
        elif metric_key == "cac":
            return company_data.get("financials", {}).get("cac", {}).get("amount")
        elif metric_key == "ltv_cac_ratio":
            # Calculate from financials
            financials = company_data.get("financials", {})
            ltv = (
                financials.get("ltv", {}).get("amount")
                if financials.get("ltv")
                else None
            )
            cac = (
                financials.get("cac", {}).get("amount")
                if financials.get("cac")
                else None
            )
            return ltv / cac if ltv and cac and cac > 0 else None
        elif metric_key == "gross_margin_pct":
            return company_data.get("financials", {}).get("gross_margin_pct")
        return None

    def _plot_fundraise_timeline(self, ax, fundraise_data):
        """Plot fundraise timeline."""
        # This is a simplified version - in real implementation you'd parse fundraise history
        round_name = fundraise_data.get("round", "Current Round")
        amount_raised_data = (
            fundraise_data.get("amount_raised")
            if fundraise_data.get("amount_raised") is not None
            else {}
        )
        amount = (
            amount_raised_data.get("amount", 0)
            if isinstance(amount_raised_data, dict)
            else 0
        )

        ax.bar([round_name], [amount], color="#3498db", alpha=0.7)
        ax.set_title("Fundraise Amount", fontweight="bold")
        ax.set_ylabel("Amount Raised")
        ax.tick_params(axis="x", rotation=45)

    def _plot_valuation_comparison(self, ax, target_data, competitor_data):
        """Plot valuation comparison."""
        target_valuation = (
            target_data.get("fundraise", {})
            .get("post_money_valuation", {})
            .get("amount", 0)
        )

        valuations = [target_valuation]
        labels = [target_data.get("company_overview", {}).get("name", "Target")]

        # Add competitor valuations if available
        for comp in competitor_data[:5]:  # Limit to top 5 competitors
            comp_data = comp.get("data") if comp.get("data") is not None else {}
            comp_val = (
                comp_data.get("fundraise", {})
                .get("post_money_valuation", {})
                .get("amount")
            )
            if comp_val:
                valuations.append(comp_val)
                comp_name = comp_data.get("company_overview", {}).get(
                    "name", "Competitor"
                )
                labels.append(comp_name)

        colors = ["#e74c3c"] + ["#3498db"] * (len(valuations) - 1)
        ax.bar(labels, valuations, color=colors, alpha=0.7)
        ax.set_title("Valuation Comparison", fontweight="bold")
        ax.set_ylabel("Valuation")
        ax.tick_params(axis="x", rotation=45)

    def _plot_orders_comparison(self, ax, target_data, competitor_data):
        """Plot orders fulfilled comparison."""
        target_orders = target_data.get("traction", {}).get("orders_fulfilled_total", 0)

        orders = [target_orders if target_orders is not None else 0]
        labels = [target_data.get("company_overview", {}).get("name", "Target")]

        for comp in competitor_data[:5]:
            comp_data = comp.get("data") if comp.get("data") is not None else {}
            comp_orders = comp_data.get("traction", {}).get("orders_fulfilled_total")
            if comp_orders is not None:
                orders.append(comp_orders)
                comp_name = comp_data.get("company_overview", {}).get("name", "Comp")
                labels.append(comp_name)

        colors = ["#e74c3c"] + ["#3498db"] * (len(orders) - 1)
        ax.bar(labels, orders, color=colors, alpha=0.7)
        ax.set_title("Orders Fulfilled", fontweight="bold")
        ax.set_ylabel("Total Orders")
        ax.tick_params(axis="x", rotation=45)

    def _plot_repeat_rate_comparison(self, ax, target_data, competitor_data):
        """Plot repeat rate comparison."""
        target_rate = target_data.get("traction", {}).get("repeat_rate_pct", 0)

        rates = [target_rate if target_rate is not None else 0]
        labels = [target_data.get("company_overview", {}).get("name", "Target")]

        for comp in competitor_data[:5]:
            comp_data = comp.get("data") if comp.get("data") is not None else {}
            comp_rate = comp_data.get("traction", {}).get("repeat_rate_pct")
            if comp_rate is not None:
                rates.append(comp_rate)
                comp_name = comp_data.get("company_overview", {}).get("name", "Comp")
                labels.append(comp_name)

        colors = ["#e74c3c"] + ["#3498db"] * (len(rates) - 1)
        ax.bar(labels, rates, color=colors, alpha=0.7)
        ax.set_title("Repeat Rate %", fontweight="bold")
        ax.set_ylabel("Repeat Rate (%)")
        ax.tick_params(axis="x", rotation=45)

    def _plot_gmv_comparison(self, ax, target_data, competitor_data):
        """Plot GMV comparison."""
        target_gmv = target_data.get("financials", {}).get("gmv", {}).get("amount", 0)

        gmvs = [target_gmv if target_gmv is not None else 0]
        labels = [target_data.get("company_overview", {}).get("name", "Target")]

        for comp in competitor_data[:5]:
            comp_data = comp.get("data") if comp.get("data") is not None else {}
            comp_gmv = comp_data.get("financials", {}).get("gmv", {}).get("amount")
            if comp_gmv is not None:
                gmvs.append(comp_gmv)
                comp_name = comp_data.get("company_overview", {}).get("name", "Comp")
                labels.append(comp_name)

        colors = ["#e74c3c"] + ["#3498db"] * (len(gmvs) - 1)
        ax.bar(labels, gmvs, color=colors, alpha=0.7)
        ax.set_title("GMV Comparison", fontweight="bold")
        ax.set_ylabel("GMV")
        ax.tick_params(axis="x", rotation=45)

    def _plot_aov_comparison(self, ax, target_data, competitor_data):
        """Plot AOV comparison."""
        target_aov = target_data.get("financials", {}).get("aov", {}).get("amount", 0)

        aovs = [target_aov if target_aov is not None else 0]
        labels = [target_data.get("company_overview", {}).get("name", "Target")]

        for comp in competitor_data[:5]:
            comp_data = comp.get("data") if comp.get("data") is not None else {}
            comp_aov = comp_data.get("financials", {}).get("aov", {}).get("amount")
            if comp_aov is not None:
                aovs.append(comp_aov)
                comp_name = comp_data.get("company_overview", {}).get("name", "Comp")
                labels.append(comp_name)

        colors = ["#e74c3c"] + ["#3498db"] * (len(aovs) - 1)
        ax.bar(labels, aovs, color=colors, alpha=0.7)
        ax.set_title("AOV Comparison", fontweight="bold")
        ax.set_ylabel("Average Order Value")
        ax.tick_params(axis="x", rotation=45)


# Global instance
comparison_visualizer = ComparisonVisualizer()
