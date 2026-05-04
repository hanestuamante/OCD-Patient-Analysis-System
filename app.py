"""Streamlit dashboard for OCD patient segmentation insights."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from src.analysis import (
    build_cluster_profiles,
    get_association_rules,
    perform_clustering,
    run_anova,
    summarize_key_metrics,
)
from src.pipeline import prepare_patient_data
from src.visualization import PALETTE, OCDVisualizer, configure_plot_style


FIGURE_DIR = Path("reports/figures")


st.set_page_config(page_title="OCD Patient Insights", layout="wide")
configure_plot_style()


@st.cache_data(show_spinner=False)
def get_data() -> tuple:
    """Load prepared and clustered patient data for the dashboard."""
    patient_df = prepare_patient_data()
    result = perform_clustering(patient_df)
    rules_df = get_association_rules(result.data)
    return result.data, rules_df


df, rules = get_data()

st.title("OCD Patient Analytics")
st.caption(
    "Patient segmentation, severity profiling, and action-oriented clinical "
    "operations insights."
)

with st.sidebar:
    st.header("Filters")
    selected_clusters = st.multiselect(
        "Cluster",
        options=sorted(df["Cluster"].unique()),
        default=sorted(df["Cluster"].unique()),
    )
    selected_severity = st.multiselect(
        "Severity",
        options=sorted(df["Severity"].unique()),
        default=sorted(df["Severity"].unique()),
    )

filtered_df = df[
    df["Cluster"].isin(selected_clusters)
    & df["Severity"].isin(selected_severity)
]
metrics = summarize_key_metrics(filtered_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Patients", f"{int(metrics['patient_count']):,}")
col2.metric("Avg Y-BOCS", f"{metrics['avg_total_ybocs']:.2f}")
col3.metric("Extreme Rate", f"{metrics['extreme_rate']:.1%}")
col4.metric("Family History", f"{metrics['family_history_rate']:.1%}")

tab_segments, tab_stats, tab_rules = st.tabs(
    ["Segments", "Statistical Evidence", "Symptom Rules"]
)

with tab_segments:
    st.dataframe(
        build_cluster_profiles(filtered_df),
        use_container_width=True,
        hide_index=True,
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=filtered_df,
        x="Age",
        y="Total_Score",
        hue="Cluster",
        palette="viridis",
        ax=ax,
    )
    ax.set_title("Patient Segments by Age and Y-BOCS Severity")
    st.pyplot(fig)

with tab_stats:
    f_stat, p_value = run_anova(
        df,
        group_col="Marital Status",
        value_col="Total_Score",
    )
    stat_col, p_col = st.columns(2)
    stat_col.metric("F-Statistic", f"{f_stat:.2f}")
    p_col.metric("P-Value", f"{p_value:.4f}")

    message = (
        "Statistically significant difference detected across marital-status "
        "groups."
        if p_value < 0.05
        else "No statistically significant difference detected at alpha=0.05."
    )
    st.info(message)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.pointplot(
        data=df,
        x="Marital Status",
        y="Total_Score",
        capsize=0.1,
        color=PALETTE["accent"],
        ax=ax,
    )
    ax.set_title("Average Y-BOCS Score by Marital Status")
    st.pyplot(fig)

with tab_rules:
    visualizer = OCDVisualizer(df)
    network_path = visualizer.save_network_graph(rules)
    st.image(str(network_path), caption="Top obsession-compulsion associations")
    st.dataframe(
        rules.sort_values("lift", ascending=False).head(10)
        if not rules.empty
        else rules,
        use_container_width=True,
    )
