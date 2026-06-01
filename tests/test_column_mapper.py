"""Unit tests for column mapping."""

import unittest

import pandas as pd

from src.transformers.column_mapper import ColumnMapper


class ColumnMapperTest(unittest.TestCase):
    """Validate configurable column normalization behavior."""

    def test_maps_aliases_and_adds_missing_columns(self) -> None:
        mapper = ColumnMapper(
            {
                "alcance": ["reach", "alcance"],
                "impressoes": ["impressions", "impressões"],
                "engajamento": ["engagement"],
            }
        )
        data = pd.DataFrame(
            {
                "Reach": [10],
                "Impressões": [20],
                "source_file": ["example.csv"],
            }
        )

        result = mapper.transform(data)

        self.assertEqual(result.loc[0, "alcance"], 10)
        self.assertEqual(result.loc[0, "impressoes"], 20)
        self.assertTrue(pd.isna(result.loc[0, "engajamento"]))
        self.assertEqual(result.loc[0, "source_file"], "example.csv")


if __name__ == "__main__":
    unittest.main()
