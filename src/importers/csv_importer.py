"""CSV importer implementation."""

from pathlib import Path

import pandas as pd

from src.importers.base import DataImporter


class CsvImporter(DataImporter):
    """Read comma-separated campaign files."""

    extensions = (".csv",)

    def read(self, path: Path) -> pd.DataFrame:
        """Read a CSV file using pandas automatic type inference."""
        return pd.read_csv(path)
