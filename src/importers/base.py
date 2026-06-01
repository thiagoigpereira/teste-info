"""Base interfaces for data importers."""

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class DataImporter(ABC):
    """Interface implemented by all file importers."""

    extensions: tuple[str, ...]

    def supports(self, path: Path) -> bool:
        """Return True when this importer can read the provided file."""
        return path.suffix.lower() in self.extensions

    @abstractmethod
    def read(self, path: Path) -> pd.DataFrame:
        """Read a file and return a DataFrame."""
