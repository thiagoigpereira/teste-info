"""Column mapping configuration loader."""

import json
from pathlib import Path
from typing import TypeAlias

from pydantic import RootModel, field_validator

ColumnMapping: TypeAlias = dict[str, list[str]]


class ColumnMappingConfig(RootModel[ColumnMapping]):
    """Pydantic model for canonical columns and accepted aliases."""

    @field_validator("root")
    @classmethod
    def validate_mapping(cls, value: ColumnMapping) -> ColumnMapping:
        """Ensure every canonical column has at least one alias."""
        if not value:
            raise ValueError("column mapping must not be empty")
        for canonical, aliases in value.items():
            if not aliases:
                raise ValueError(f"column '{canonical}' must define aliases")
        return value


def load_column_mapping(path: str | Path) -> ColumnMapping:
    """Read and validate a JSON column mapping file."""
    mapping_path = Path(path)
    with mapping_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    return ColumnMappingConfig.model_validate(payload).root
