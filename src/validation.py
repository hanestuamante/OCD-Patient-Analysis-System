"""Data validation rules for the OCD patient dataset."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


REQUIRED_COLUMNS = {
    "Patient ID",
    "Age",
    "Gender",
    "Ethnicity",
    "Marital Status",
    "Education Level",
    "OCD Diagnosis Date",
    "Duration of Symptoms (months)",
    "Family History of OCD",
    "Obsession Type",
    "Compulsion Type",
    "Y-BOCS Score (Obsessions)",
    "Y-BOCS Score (Compulsions)",
}

NUMERIC_RANGES = {
    "Age": (0, 120),
    "Duration of Symptoms (months)": (0, 1200),
    "Y-BOCS Score (Obsessions)": (0, 40),
    "Y-BOCS Score (Compulsions)": (0, 40),
}


@dataclass
class ValidationReport:
    """Structured validation result for CLI and automated workflows."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Return True when no blocking validation errors were found."""
        return not self.errors

    def raise_for_errors(self) -> None:
        """Raise a ValueError with all blocking validation errors."""
        if self.errors:
            raise ValueError("Data validation failed: " + " | ".join(self.errors))


def validate_required_columns(df: pd.DataFrame) -> list[str]:
    """Validate that all required analytical columns exist."""
    missing_columns = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if not missing_columns:
        return []
    return [f"Missing required columns: {', '.join(missing_columns)}"]


def validate_numeric_ranges(df: pd.DataFrame) -> list[str]:
    """Validate clinically expected numeric ranges for key fields."""
    errors = []
    for column, (lower_bound, upper_bound) in NUMERIC_RANGES.items():
        if column not in df.columns:
            continue

        numeric_values = pd.to_numeric(df[column], errors="coerce")
        non_numeric_mask = numeric_values.isna() & df[column].notna()
        if non_numeric_mask.any():
            errors.append(
                f"{column} has {int(non_numeric_mask.sum())} non-numeric values."
            )

        invalid_mask = ~numeric_values.between(lower_bound, upper_bound)
        invalid_mask = invalid_mask & numeric_values.notna()
        if invalid_mask.any():
            errors.append(
                f"{column} has {int(invalid_mask.sum())} values outside "
                f"[{lower_bound}, {upper_bound}]."
            )
    return errors


def validate_missingness(
    df: pd.DataFrame,
    warning_threshold: float = 0.05,
) -> list[str]:
    """Warn when required fields exceed the missingness threshold."""
    warnings = []
    available_required_columns = [col for col in REQUIRED_COLUMNS if col in df]
    missing_rates = df[available_required_columns].isna().mean()

    for column, rate in missing_rates.items():
        if rate > warning_threshold:
            warnings.append(f"{column} missing rate is {rate:.1%}.")
    return warnings


def validate_patient_data(df: pd.DataFrame) -> ValidationReport:
    """Run the complete validation suite for raw OCD patient data."""
    validation_df = df.copy()
    validation_df.columns = validation_df.columns.str.strip()

    report = ValidationReport()
    report.errors.extend(validate_required_columns(validation_df))
    report.errors.extend(validate_numeric_ranges(validation_df))
    report.warnings.extend(validate_missingness(validation_df))
    return report
