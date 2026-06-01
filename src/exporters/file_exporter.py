"""Export consolidated campaign datasets."""

from pathlib import Path

import pandas as pd


class FileExporter:
    """Write consolidated data in supported output formats."""

    def export(self, data: pd.DataFrame, output_dir: Path, basename: str) -> list[Path]:
        """Export a DataFrame as CSV and XLSX files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        csv_path = output_dir / f"{basename}.csv"
        xlsx_path = output_dir / f"{basename}.xlsx"

        data.to_csv(csv_path, index=False)
        data.to_excel(xlsx_path, index=False, engine="openpyxl")
        return [csv_path, xlsx_path]
