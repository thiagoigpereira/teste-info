"""Excel importer implementation."""

from pathlib import Path

import pandas as pd

from src.importers.base import DataImporter


class ExcelImporter(DataImporter):
    """Read all sheets from an XLSX campaign workbook."""

    extensions = (".xlsx",)

    def read(self, path: Path) -> pd.DataFrame:
        """Read every worksheet and keep the source sheet name."""
        sheets = pd.read_excel(path, sheet_name=None, engine="openpyxl")
        frames: list[pd.DataFrame] = []
        for sheet_name, frame in sheets.items():
            sheet_frame = frame.copy()
            sheet_frame["source_sheet"] = sheet_name
            frames.append(sheet_frame)
        if not frames:
            return pd.DataFrame()
        return pd.concat(frames, ignore_index=True, sort=False)
