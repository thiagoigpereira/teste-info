"""Pipeline orchestration for importing and consolidating campaigns."""

from pathlib import Path
import logging

import pandas as pd

from src.config.column_mapping import ColumnMapping
from src.config.settings import AppSettings
from src.exporters.file_exporter import FileExporter
from src.services.import_service import ImportService
from src.transformers.column_mapper import ColumnMapper

logger = logging.getLogger(__name__)


class ConsolidationService:
    """Coordinate import, transformation, and export pipeline steps."""

    def __init__(self, settings: AppSettings, mapping: ColumnMapping) -> None:
        """Create the service with configuration dependencies."""
        self.settings = settings
        self.mapper = ColumnMapper(mapping)
        self.import_service = ImportService()
        self.exporter = FileExporter()

    def import_files(self) -> Path:
        """Import input and manual files into a raw processed CSV file."""
        self._ensure_directories()
        raw_data = self.import_service.import_directories(
            {
                self.settings.input_dir: "campaign",
                self.settings.manual_dir: "manual",
            }
        )
        raw_data.to_csv(self.settings.raw_import_path, index=False)
        logger.info("Raw import saved to %s with %s records", self.settings.raw_import_path, len(raw_data))
        return self.settings.raw_import_path

    def consolidate(self) -> Path:
        """Normalize raw imported data into the canonical consolidated dataset."""
        self._ensure_directories()
        if not self.settings.raw_import_path.exists():
            logger.info("Raw import file not found; importing files before consolidation")
            self.import_files()

        raw_data = pd.read_csv(self.settings.raw_import_path)
        consolidated = self.mapper.transform(raw_data)
        consolidated.to_csv(self.settings.processed_consolidated_path, index=False)
        logger.info(
            "Consolidated dataset saved to %s with %s records",
            self.settings.processed_consolidated_path,
            len(consolidated),
        )
        return self.settings.processed_consolidated_path

    def export(self) -> list[Path]:
        """Export the consolidated dataset as CSV and XLSX."""
        self._ensure_directories()
        if not self.settings.processed_consolidated_path.exists():
            logger.info("Consolidated file not found; consolidating before export")
            self.consolidate()

        consolidated = pd.read_csv(self.settings.processed_consolidated_path)
        paths = self.exporter.export(consolidated, self.settings.output_dir, "consolidated")
        logger.info("Exported consolidated files: %s", paths)
        return paths

    def run_all(self) -> list[Path]:
        """Run import, consolidate, and export in sequence."""
        self.import_files()
        self.consolidate()
        return self.export()

    def _ensure_directories(self) -> None:
        """Create required runtime directories."""
        for directory in (
            self.settings.input_dir,
            self.settings.manual_dir,
            self.settings.processed_dir,
            self.settings.output_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)
