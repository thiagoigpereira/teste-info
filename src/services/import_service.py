"""Services responsible for discovering and importing source files."""

from datetime import datetime, timezone
import logging
from pathlib import Path

import pandas as pd

from src.importers.factory import ImporterFactory

logger = logging.getLogger(__name__)


class ImportService:
    """Import campaign files from configured folders."""

    def __init__(self, factory: ImporterFactory | None = None) -> None:
        """Initialize with an importer factory."""
        self.factory = factory or ImporterFactory()

    def import_directories(self, source_dirs: dict[Path, str]) -> pd.DataFrame:
        """Read all supported files from source directories."""
        frames: list[pd.DataFrame] = []
        for directory, source_type in source_dirs.items():
            if not directory.exists():
                logger.warning("Source directory does not exist: %s", directory)
                continue

            for path in sorted(item for item in directory.iterdir() if item.is_file()):
                importer = self.factory.get_importer(path)
                if importer is None:
                    logger.warning("Unsupported file ignored: %s", path)
                    continue

                try:
                    frame = importer.read(path)
                except Exception:
                    logger.exception("Error importing file: %s", path)
                    continue

                frame = frame.copy()
                frame["source_file"] = path.name
                frame["source_type"] = source_type
                frame["imported_at"] = datetime.now(timezone.utc).isoformat()
                frames.append(frame)
                logger.info("Processed file %s with %s records", path, len(frame))

        if not frames:
            logger.warning("No supported campaign files were imported")
            return pd.DataFrame()
        return pd.concat(frames, ignore_index=True, sort=False)
