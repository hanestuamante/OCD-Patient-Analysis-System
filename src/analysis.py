"""Statistical, clustering, and insight-generation utilities."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


CLUSTER_FEATURES = ["Age", "Total_Score", "Family_History_Bin"]


@dataclass(frozen=True)
class ClusterResult:
    """Container for clustering outputs used by reports and apps."""

    data: pd.DataFrame
    model: KMeans
    scaler: StandardScaler


def perform_clustering(
    df: pd.DataFrame,
    n_clusters: int = 4,
    features: list[str] | None = None,
) -> ClusterResult:
    """Segment patients with K-Means over severity and demographic features."""
    model_features = features or CLUSTER_FEATURES
    clustered_df = df.copy()
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(clustered_df[model_features])

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clustered_df["Cluster"] = model.fit_predict(x_scaled)
    return ClusterResult(data=clustered_df, model=model, scaler=scaler)


def run_anova(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
) -> tuple[float, float]:
    """Run one-way ANOVA across groups for a numeric outcome."""
    groups = [
        group[value_col].dropna().values
        for _, group in df.groupby(group_col)
        if group[value_col].notna().any()
    ]
    if len(groups) < 2:
        raise ValueError("ANOVA requires at least two non-empty groups.")

    f_stat, p_value = stats.f_oneway(*groups)
    return float(f_stat), float(p_value)


def get_association_rules(
    df: pd.DataFrame,
    min_support: float = 0.05,
    min_lift: float = 1.0,
) -> pd.DataFrame:
    """Calculate association rules between obsession and compulsion types."""
    encoded_symptoms = pd.get_dummies(
        df[["Obsession Type", "Compulsion Type"]],
        dtype=bool,
    )
    frequent_itemsets = apriori(
        encoded_symptoms,
        min_support=min_support,
        use_colnames=True,
    )

    if frequent_itemsets.empty:
        return pd.DataFrame()

    return association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=min_lift,
    )


def summarize_key_metrics(df: pd.DataFrame) -> dict[str, float]:
    """Return executive-level health metrics for the current cohort."""
    return {
        "patient_count": float(len(df)),
        "avg_total_ybocs": float(df["Total_Score"].mean()),
        "extreme_rate": float((df["Severity"] == "Extreme").mean()),
        "family_history_rate": float(df["Family_History_Bin"].mean()),
    }


def build_cluster_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate each patient segment into interpretable cluster profiles."""
    return (
        df.groupby("Cluster")
        .agg(
            patient_count=("Cluster", "size"),
            avg_age=("Age", "mean"),
            avg_total_ybocs=("Total_Score", "mean"),
            family_history_rate=("Family_History_Bin", "mean"),
            extreme_rate=("Severity", lambda values: (values == "Extreme").mean()),
        )
        .round(3)
        .sort_values("avg_total_ybocs", ascending=False)
        .reset_index()
    )


def generate_strategic_insights(df: pd.DataFrame) -> list[str]:
    """Translate analytical results into business and clinical actions."""
    profiles = build_cluster_profiles(df)
    highest_risk = profiles.iloc[0]
    extreme_rate = (df["Severity"] == "Extreme").mean()

    return [
        (
            f"Prioritize Cluster {int(highest_risk['Cluster'])}: this segment "
            f"has the highest average Y-BOCS score "
            f"({highest_risk['avg_total_ybocs']:.1f}) and should receive the "
            "first outreach in stepped-care triage."
        ),
        (
            f"Use severity distribution as an operational capacity signal: "
            f"{extreme_rate:.1%} of patients are classified as Extreme, which "
            "can inform clinician staffing and follow-up cadence."
        ),
        (
            "Monitor family-history concentration by segment to identify "
            "groups where early screening and psychoeducation may create the "
            "highest prevention ROI."
        ),
    ]


class OCDAnalysis:
    """Backward-compatible facade for existing notebooks and scripts."""

    @staticmethod
    def perform_clustering(
        df: pd.DataFrame,
        n_clusters: int = 4,
    ) -> tuple[pd.DataFrame, KMeans]:
        """Return the legacy `(dataframe, model)` clustering tuple."""
        result = perform_clustering(df, n_clusters=n_clusters)
        return result.data, result.model

    run_anova = staticmethod(run_anova)
    get_association_rules = staticmethod(get_association_rules)
