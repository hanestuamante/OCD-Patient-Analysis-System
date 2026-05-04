"""End-to-end data preparation pipeline used by CLI, notebooks, and Streamlit."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.cleaning import clean_patient_data
from src.data_loader import OCDDataLoader
from src.features import build_features
from src.validation import validate_patient_data


def prepare_patient_data(
    csv_path: str | Path | None = None,
    validate: bool = True,
) -> pd.DataFrame:
    """Load, validate, clean, and feature-engineer patient data."""
    loader = OCDDataLoader()
    raw_df = loader.load_raw_data(csv_path)

    if validate:
        validation_report = validate_patient_data(raw_df)
        validation_report.raise_for_errors()

    cleaned_df = clean_patient_data(raw_df)
    return build_features(cleaned_df)
