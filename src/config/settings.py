"""Application settings loaded from environment variables."""

from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os


class AppSettings(BaseModel):
    """Filesystem settings for the campaign consolidation pipeline."""

    input_dir: Path = Field(default=Path("data/input"))
    manual_dir: Path = Field(default=Path("data/manual"))
    processed_dir: Path = Field(default=Path("data/processed"))
    output_dir: Path = Field(default=Path("data/output"))
    column_mapping_path: Path = Field(default=Path("config/column_mapping.json"))

    @property
    def raw_import_path(self) -> Path:
        """Path where the imported raw dataset is persisted."""
        return self.processed_dir / "imported_raw.csv"

    @property
    def processed_consolidated_path(self) -> Path:
        """Path where the normalized consolidated dataset is persisted."""
        return self.processed_dir / "consolidated.csv"

    @property
    def log_path(self) -> Path:
        """Path for the application log file."""
        return self.processed_dir / "campaign_automation.log"


def load_settings(env_file: str | Path = ".env") -> AppSettings:
    """Load application settings from a .env file and process environment."""
    load_dotenv(env_file)
    return AppSettings(
        input_dir=Path(os.getenv("CAMPAIGN_INPUT_DIR", "data/input")),
        manual_dir=Path(os.getenv("CAMPAIGN_MANUAL_DIR", "data/manual")),
        processed_dir=Path(os.getenv("CAMPAIGN_PROCESSED_DIR", "data/processed")),
        output_dir=Path(os.getenv("CAMPAIGN_OUTPUT_DIR", "data/output")),
        column_mapping_path=Path(
            os.getenv("CAMPAIGN_COLUMN_MAPPING", "config/column_mapping.json")
        ),
    )
