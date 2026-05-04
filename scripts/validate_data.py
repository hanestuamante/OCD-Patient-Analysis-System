"""Validate raw OCD patient data before analysis runs."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.validation import validate_patient_data


def parse_args() -> argparse.Namespace:
    """Parse validation CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Validate the raw OCD patient CSV schema and data quality."
    )
    parser.add_argument(
        "csv_path",
        type=Path,
        help="Path to the raw CSV file to validate.",
    )
    return parser.parse_args()


def main() -> None:
    """Run validation and print a concise data quality report."""
    args = parse_args()
    df = pd.read_csv(args.csv_path)
    report = validate_patient_data(df)

    if report.errors:
        print("Validation errors:")
        for error in report.errors:
            print(f"- {error}")

    if report.warnings:
        print("Validation warnings:")
        for warning in report.warnings:
            print(f"- {warning}")

    if report.is_valid:
        print("Validation passed.")
    else:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
