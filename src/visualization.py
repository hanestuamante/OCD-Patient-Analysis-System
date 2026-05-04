"""Consistent plotting utilities for reports and Streamlit dashboards."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns


REPORT_FIGURE_DIR = Path("reports/figures")
PLOT_STYLE = "whitegrid"
PALETTE = {
    "primary": "#2563EB",
    "accent": "#DC2626",
    "neutral": "#334155",
    "highlight": "#16A34A",
}


def configure_plot_style() -> None:
    """Apply a consistent visual style across generated figures."""
    sns.set_theme(style=PLOT_STYLE, context="talk")
    plt.rcParams.update(
        {
            "axes.titleweight": "bold",
            "axes.labelcolor": PALETTE["neutral"],
            "figure.dpi": 120,
            "savefig.bbox": "tight",
        }
    )


class OCDVisualizer:
    """Generate reusable figures for the OCD patient analytics project."""

    def __init__(
        self,
        df: pd.DataFrame,
        report_dir: str | Path = REPORT_FIGURE_DIR,
    ) -> None:
        """Create a visualizer with a target output directory."""
        self.df = df
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        configure_plot_style()

    def plot_marital_impact(self) -> Path:
        """Save point plot of total Y-BOCS score by marital status."""
        figure_path = self.report_dir / "marital_impact.png"
        plt.figure(figsize=(10, 6))
        sns.pointplot(
            data=self.df,
            x="Marital Status",
            y="Total_Score",
            capsize=0.1,
            color=PALETTE["accent"],
        )
        plt.title("Average Y-BOCS Score by Marital Status")
        plt.xlabel("Marital Status")
        plt.ylabel("Average Total Y-BOCS Score")
        plt.savefig(figure_path)
        plt.close()
        return figure_path

    def plot_education_duration(self) -> Path:
        """Save violin plot of symptom duration by education level."""
        figure_path = self.report_dir / "education_duration.png"
        plt.figure(figsize=(12, 7))
        sns.violinplot(
            data=self.df,
            x="Education Level",
            y="Duration of Symptoms (months)",
            inner="quartile",
            color=PALETTE["primary"],
        )
        plt.title("Symptom Duration Distribution by Education Level")
        plt.xlabel("Education Level")
        plt.ylabel("Duration of Symptoms (months)")
        plt.xticks(rotation=20, ha="right")
        plt.savefig(figure_path)
        plt.close()
        return figure_path

    def plot_cluster_profile(self) -> Path:
        """Save scatter plot of patient clusters by age and severity."""
        figure_path = self.report_dir / "cluster_distribution.png"
        plt.figure(figsize=(12, 8))
        sns.scatterplot(
            data=self.df,
            x="Age",
            y="Total_Score",
            hue="Cluster",
            palette="viridis",
            s=70,
        )
        plt.title("OCD Patient Segments by Age and Y-BOCS Severity")
        plt.xlabel("Age")
        plt.ylabel("Total Y-BOCS Score")
        plt.savefig(figure_path)
        plt.close()
        return figure_path

    def save_network_graph(self, rules: pd.DataFrame, top_n: int = 20) -> Path:
        """Save symptom association network from Apriori rules."""
        figure_path = self.report_dir / "symptom_network.png"
        graph = nx.DiGraph()

        if rules.empty:
            graph.add_node("No rules found")
        else:
            top_rules = rules.sort_values("lift", ascending=False).head(top_n)
            for _, row in top_rules.iterrows():
                antecedent = next(iter(row["antecedents"]))
                consequent = next(iter(row["consequents"]))
                graph.add_edge(antecedent, consequent, weight=row["lift"])

        plt.figure(figsize=(12, 8))
        position = nx.spring_layout(graph, k=1.5, seed=42)
        nx.draw_networkx(
            graph,
            position,
            node_size=2500,
            node_color="#BFDBFE",
            edge_color="#64748B",
            font_size=9,
            alpha=0.9,
            arrows=True,
        )
        plt.title("Obsession-Compulsion Association Network")
        plt.axis("off")
        plt.savefig(figure_path)
        plt.close()
        return figure_path
