"""Unit tests for the consolidation pipeline."""

from pathlib import Path
import tempfile
import unittest

import pandas as pd

from src.config.settings import AppSettings
from src.services.consolidation_service import ConsolidationService


class ConsolidationPipelineTest(unittest.TestCase):
    """Validate import, consolidate, and export behavior with CSV input."""

    def test_run_all_creates_consolidated_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_dir = root / "input"
            manual_dir = root / "manual"
            processed_dir = root / "processed"
            output_dir = root / "output"
            input_dir.mkdir()
            manual_dir.mkdir()

            pd.DataFrame({"Reach": [100], "Engagement": [12]}).to_csv(
                input_dir / "campaign.csv", index=False
            )
            pd.DataFrame({"Alcance": [50], "Engajamento": [6]}).to_csv(
                manual_dir / "manual.csv", index=False
            )

            service = ConsolidationService(
                settings=AppSettings(
                    input_dir=input_dir,
                    manual_dir=manual_dir,
                    processed_dir=processed_dir,
                    output_dir=output_dir,
                    column_mapping_path=root / "unused.json",
                ),
                mapping={"alcance": ["reach", "alcance"], "engajamento": ["engagement", "engajamento"]},
            )

            paths = service.run_all()

            self.assertTrue((output_dir / "consolidated.csv").exists())
            self.assertTrue((output_dir / "consolidated.xlsx").exists())
            self.assertEqual(paths, [output_dir / "consolidated.csv", output_dir / "consolidated.xlsx"])
            consolidated = pd.read_csv(output_dir / "consolidated.csv")
            self.assertEqual(len(consolidated), 2)
            self.assertIn("source_file", consolidated.columns)
            self.assertIn("source_type", consolidated.columns)


if __name__ == "__main__":
    unittest.main()
