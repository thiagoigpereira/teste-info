"""Importer registry and resolution helpers."""

from pathlib import Path

from src.importers.base import DataImporter
from src.importers.csv_importer import CsvImporter
from src.importers.excel_importer import ExcelImporter


class ImporterFactory:
    """Resolve importers by file extension."""

    def __init__(self, importers: list[DataImporter] | None = None) -> None:
        """Create a factory with default CSV and XLSX importers."""
        self._importers = importers or [CsvImporter(), ExcelImporter()]

    def get_importer(self, path: Path) -> DataImporter | None:
        """Return the first importer that supports the path."""
        for importer in self._importers:
            if importer.supports(path):
                return importer
        return None
