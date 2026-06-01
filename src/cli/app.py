"""Typer CLI for the campaign report automation pipeline."""

from pathlib import Path

import typer

from src.config.column_mapping import load_column_mapping
from src.config.logging_config import configure_logging
from src.config.settings import load_settings
from src.services.consolidation_service import ConsolidationService

app = typer.Typer(help="Automação de consolidação de dados de campanhas de marketing.")


def _build_service(env_file: Path = Path(".env")) -> ConsolidationService:
    """Load settings, logging, and service dependencies."""
    settings = load_settings(env_file)
    configure_logging(settings.log_path)
    mapping = load_column_mapping(settings.column_mapping_path)
    return ConsolidationService(settings=settings, mapping=mapping)


@app.command("import")
def import_command(env_file: Path = typer.Option(Path(".env"), help="Arquivo .env.")) -> None:
    """Import source files into the processed raw dataset."""
    path = _build_service(env_file).import_files()
    typer.echo(f"Importação concluída: {path}")


@app.command("consolidate")
def consolidate_command(env_file: Path = typer.Option(Path(".env"), help="Arquivo .env.")) -> None:
    """Normalize imported data into the consolidated dataset."""
    path = _build_service(env_file).consolidate()
    typer.echo(f"Consolidação concluída: {path}")


@app.command("export")
def export_command(env_file: Path = typer.Option(Path(".env"), help="Arquivo .env.")) -> None:
    """Export the consolidated dataset as CSV and XLSX."""
    paths = _build_service(env_file).export()
    typer.echo("Exportação concluída:")
    for path in paths:
        typer.echo(f"- {path}")


@app.command("run-all")
def run_all_command(env_file: Path = typer.Option(Path(".env"), help="Arquivo .env.")) -> None:
    """Run import, consolidation, and export steps."""
    paths = _build_service(env_file).run_all()
    typer.echo("Pipeline completo executado:")
    for path in paths:
        typer.echo(f"- {path}")
