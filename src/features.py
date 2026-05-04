"""Feature engineering functions for OCD patient analysis."""

from __future__ import annotations

import pandas as pd


OBSESSION_SCORE_COLUMN = "Y-BOCS Score (Obsessions)"
COMPULSION_SCORE_COLUMN = "Y-BOCS Score (Compulsions)"
TOTAL_SCORE_COLUMN = "Total_Score"


def classify_ybocs_severity(score: float) -> str:
    """Classify total Y-BOCS score into a clinical severity band."""
    if score <= 7:
        return "Subclinical"
    if score <= 15:
        return "Mild"
    if score <= 23:
        return "Moderate"
    if score <= 31:
        return "Severe"
    return "Extreme"


def add_total_score(df: pd.DataFrame) -> pd.DataFrame:
    """Add combined obsession and compulsion Y-BOCS score."""
    featured_df = df.copy()
    featured_df[TOTAL_SCORE_COLUMN] = (
        featured_df[OBSESSION_SCORE_COLUMN]
        + featured_df[COMPULSION_SCORE_COLUMN]
    )
    return featured_df


def add_severity_band(df: pd.DataFrame) -> pd.DataFrame:
    """Add the Y-BOCS severity band derived from total score."""
    featured_df = df.copy()
    featured_df["Severity"] = featured_df[TOTAL_SCORE_COLUMN].apply(
        classify_ybocs_severity
    )
    return featured_df


def add_family_history_binary(df: pd.DataFrame) -> pd.DataFrame:
    """Add a binary family-history feature for statistical modeling."""
    featured_df = df.copy()
    featured_df["Family_History_Bin"] = (
        featured_df["Family History of OCD"].map({"Yes": 1, "No": 0})
    )
    return featured_df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create all analysis-ready features used by notebooks and apps."""
    featured_df = add_total_score(df)
    featured_df = add_severity_band(featured_df)
    return add_family_history_binary(featured_df)
