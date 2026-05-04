"""Reusable cleaning functions for OCD patient records."""

from __future__ import annotations

import pandas as pd


NUMERIC_COLUMNS = [
    "Age",
    "Duration of Symptoms (months)",
    "Y-BOCS Score (Obsessions)",
    "Y-BOCS Score (Compulsions)",
]


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from column names without mutating the input frame."""
    cleaned_df = df.copy()
    cleaned_df.columns = cleaned_df.columns.str.strip()
    return cleaned_df


def normalize_categorical_values(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize common categorical values used by downstream analysis."""
    cleaned_df = df.copy()
    object_columns = cleaned_df.select_dtypes(include="object").columns

    for column in object_columns:
        cleaned_df[column] = cleaned_df[column].astype("string").str.strip()

    yes_no_columns = ["Family History of OCD"]
    for column in yes_no_columns:
        if column in cleaned_df.columns:
            cleaned_df[column] = cleaned_df[column].str.title()

    return cleaned_df


def drop_duplicate_patients(df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicate patient records when a patient identifier is available."""
    if "Patient ID" not in df.columns:
        return df.copy()
    return df.drop_duplicates(subset=["Patient ID"]).copy()


def coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert analytical numeric columns to numeric dtype."""
    cleaned_df = df.copy()
    for column in NUMERIC_COLUMNS:
        if column in cleaned_df.columns:
            cleaned_df[column] = pd.to_numeric(cleaned_df[column], errors="coerce")
    return cleaned_df


def clean_patient_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run the standard raw-to-clean patient data preparation steps."""
    cleaned_df = standardize_column_names(df)
    cleaned_df = normalize_categorical_values(cleaned_df)
    cleaned_df = coerce_numeric_columns(cleaned_df)
    return drop_duplicate_patients(cleaned_df)
