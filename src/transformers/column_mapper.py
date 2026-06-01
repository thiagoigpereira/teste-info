"""Column normalization and mapping utilities."""

import logging
import unicodedata

import pandas as pd

from src.config.column_mapping import ColumnMapping

logger = logging.getLogger(__name__)

METADATA_COLUMNS = {"source_file", "source_type", "source_sheet", "imported_at"}


def normalize_name(value: str) -> str:
    """Normalize column names for resilient matching."""
    normalized = unicodedata.normalize("NFKD", str(value))
    without_accents = "".join(char for char in normalized if not unicodedata.combining(char))
    return without_accents.strip().lower().replace(" ", "_").replace("-", "_")


class ColumnMapper:
    """Apply a configurable alias-to-canonical column mapping."""

    def __init__(self, mapping: ColumnMapping) -> None:
        """Build a lookup from aliases to canonical names."""
        self.mapping = mapping
        self._alias_lookup: dict[str, str] = {}
        for canonical, aliases in mapping.items():
            self._alias_lookup[normalize_name(canonical)] = canonical
            for alias in aliases:
                self._alias_lookup[normalize_name(alias)] = canonical

    @property
    def canonical_columns(self) -> list[str]:
        """Return all canonical columns configured for the dataset."""
        return list(self.mapping.keys())

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Rename recognized columns, preserve metadata and add missing columns."""
        transformed = pd.DataFrame(index=data.index)
        recognized_sources: set[str] = set()

        for source_column in data.columns:
            source_name = str(source_column)
            if source_name in METADATA_COLUMNS:
                transformed[source_name] = data[source_column]
                recognized_sources.add(source_name)
                continue

            canonical = self._alias_lookup.get(normalize_name(source_name))
            if canonical is None:
                logger.warning("Unrecognized column ignored: %s", source_name)
                continue

            recognized_sources.add(source_name)
            if canonical in transformed.columns:
                transformed[canonical] = transformed[canonical].combine_first(data[source_column])
                logger.warning(
                    "Duplicate mapped column '%s' merged into canonical '%s'",
                    source_name,
                    canonical,
                )
            else:
                transformed[canonical] = data[source_column]

        for canonical in self.canonical_columns:
            if canonical not in transformed.columns:
                transformed[canonical] = pd.NA
                logger.warning("Missing canonical column added as empty: %s", canonical)

        for metadata_column in METADATA_COLUMNS:
            if metadata_column not in transformed.columns:
                transformed[metadata_column] = pd.NA

        ordered_columns = [
            "source_file",
            "source_type",
            "source_sheet",
            "imported_at",
            *self.canonical_columns,
        ]
        return transformed[ordered_columns]
