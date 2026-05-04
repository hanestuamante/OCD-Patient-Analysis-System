"""Command-line orchestrator for the OCD patient analytics pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.analysis import (
    build_cluster_profiles,
    generate_strategic_insights,
    get_association_rules,
    perform_clustering,
    run_anova,
    summarize_key_metrics,
)
from src.pipeline import prepare_patient_data
from src.visualization import OCDVisualizer


def parse_args() -> argparse.Namespace:
    """Parse CLI options for local and reproducible pipeline runs."""
    parser = argparse.ArgumentParser(
        description="Run OCD patient analytics from raw data to report assets."
    )
    parser.add_argument(
        "--csv-path",
        type=Path,
        default=None,
        help="Optional CSV source path. Defaults to OCD_DATABASE_URL/MySQL.",
    )
    parser.add_argument(
        "--clusters",
        type=int,
        default=4,
        help="Number of K-Means clusters to create.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the complete analytical pipeline."""
    args = parse_args()
    print("--- Starting OCD patient analytics pipeline ---")

    patient_df = prepare_patient_data(csv_path=args.csv_path)
    cluster_result = perform_clustering(patient_df, n_clusters=args.clusters)
    clustered_df = cluster_result.data

    f_stat, p_value = run_anova(
        clustered_df,
        group_col="Marital Status",
        value_col="Total_Score",
    )
    rules = get_association_rules(clustered_df)

    visualizer = OCDVisualizer(clustered_df)
    output_paths = [
        visualizer.plot_cluster_profile(),
        visualizer.plot_marital_impact(),
        visualizer.plot_education_duration(),
        visualizer.save_network_graph(rules),
    ]

    metrics = summarize_key_metrics(clustered_df)
    cluster_profiles = build_cluster_profiles(clustered_df)
    insights = generate_strategic_insights(clustered_df)

    print(f"Patients analyzed: {int(metrics['patient_count'])}")
    print(f"Average total Y-BOCS: {metrics['avg_total_ybocs']:.2f}")
    print(f"Extreme severity rate: {metrics['extreme_rate']:.1%}")
    print(f"Family history rate: {metrics['family_history_rate']:.1%}")
    print(f"Marital-status ANOVA: F={f_stat:.2f}, p={p_value:.4f}")
    print("\nCluster profiles:")
    print(cluster_profiles.to_string(index=False))
    print("\nStrategic insights:")
    for insight in insights:
        print(f"- {insight}")
    print("\nReport figures:")
    for path in output_paths:
        print(f"- {path}")
    print("--- Pipeline complete ---")


if __name__ == "__main__":
    main()
