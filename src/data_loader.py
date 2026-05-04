"""Data access utilities for the OCD patient analytics project."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from src.cleaning import clean_patient_data
from src.features import build_features


DEFAULT_DATABASE_URL = "mysql+pymysql://root:@127.0.0.1/ocd_analysis"
DEFAULT_TABLE_NAME = "ocd_patient_dataset"


class OCDDataLoader:
    """Load OCD patient data from CSV files or a SQL database."""

    def __init__(
        self,
        database_url: str | None = None,
        table_name: str = DEFAULT_TABLE_NAME,
    ) -> None:
        """Create a loader using environment-aware database defaults.

        Args:
            database_url: SQLAlchemy database URL. If omitted, the loader reads
                `OCD_DATABASE_URL`, then falls back to a local MySQL URL.
            table_name: Source table used by `load_from_database`.
        """
        self.database_url = (
            database_url
            or os.getenv("OCD_DATABASE_URL")
            or DEFAULT_DATABASE_URL
        )
        self.table_name = table_name

    def load_from_database(self) -> pd.DataFrame:
        """Read the configured OCD patient table from the database."""
        engine = create_engine(self.database_url)
        query = f"SELECT * FROM {self.table_name}"
        return pd.read_sql(query, engine)

    def load_from_csv(self, file_path: str | Path) -> pd.DataFrame:
        """Read patient data from a CSV file.

        Args:
            file_path: Path to a local CSV file.

        Returns:
            Raw patient dataset as a pandas DataFrame.
        """
        return pd.read_csv(file_path)

    def load_raw_data(self, csv_path: str | Path | None = None) -> pd.DataFrame:
        """Load raw data from CSV when provided, otherwise from the database."""
        if csv_path:
            return self.load_from_csv(csv_path)
        return self.load_from_database()

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return cleaned and feature-engineered data for legacy notebooks."""
        return build_features(clean_patient_data(df))
