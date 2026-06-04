"""
Command-line interface for TRS Isomorphic Search.

Provides CLI commands for validation, template listing, and testing.
"""

import json
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .models import SystemGraph, ValidationReport
from .validator import validate_isomorphism
from .templates import get_template, list_templates

app = typer.Typer(
    name="trs-iso",
    help="TRS Alliance Structural Integrity Verification Engine",
    no_args_is_help=True,
)

console = Console()


@app.command()
def validate(
    graph: str = typer.Option(
        ...,
        "--graph",
        "-g",
        help="Path to input system graph JSON file",
    ),
    template: str = typer.Option(
        "agent_lattice",
        "--template",
        "-t",
        help="Template name or path to template JSON file",
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file for validation report (JSON)",
    ),
) -> None:
    """
    Validate system graph against a reference template.

    Exit codes:
    - 0: PASS (Residual Risk = 0.00)
    - 1: FAIL (Residual Risk = 1.00)
    """
    try:
        # Load input graph
        graph_path = Path(graph)
        if not graph_path.exists():
            console.print(f"[red]Error: Graph file not found: {graph}[/red]")
            sys.exit(1)

        with open(graph_path, "r") as f:
            graph_data = json.load(f)
        input_graph = SystemGraph.model_validate(graph_data)

        # Load template
        template_graph = None

        # Try loading as file first
        template_path = Path(template)
        if template_path.exists():
            with open(template_path, "r") as f:
                template_data = json.load(f)
            template_graph = SystemGraph.model_validate(template_data)
        else:
            # Try loading from built-in templates
            template_graph = get_template(template)
            if template_graph is None:
                console.print(
                    f"[red]Error: Template not found: {template}[/red]\n"
                    f"[yellow]Available templates: {', '.join(list_templates().keys())}[/yellow]"
                )
                sys.exit(1)

        # Perform validation
        report = validate_isomorphism(input_graph, template_graph)

        # Display results
        status_color = "[green]PASS[/green]" if report.status == "PASS" else "[red]FAIL[/red]"
        console.print(
            Panel(
                f"Status: {status_color}\n"
                f"System ID: {report.system_id}\n"
                f"Risk Score: {report.residual_risk_score:.2f}\n"
                f"Message: {report.message}",
                title="Validation Report",
                expand=False,
            )
        )

        # Output to file if requested
        if output:
            output_path = Path(output)
            with open(output_path, "w") as f:
                json.dump(report.model_dump(mode="json"), f, indent=2, default=str)
            console.print(f"\n[blue]Report saved to: {output_path}[/blue]")

        # Exit with appropriate code
        exit_code = 0 if report.status == "PASS" else 1
        sys.exit(exit_code)

    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON format: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


@app.command()
def templates() -> None:
    """
    List all available reference templates.
    """
    template_list = list_templates()

    if not template_list:
        console.print("[yellow]No templates available[/yellow]")
        return

    table = Table(title="Available Templates")
    table.add_column("Template Name", style="cyan")
    table.add_column("Description", style="magenta")

    for name, description in template_list.items():
        table.add_row(name, description)

    console.print(table)


@app.command()
def version() -> None:
    """
    Show version information.
    """
    from . import __version__

    console.print(f"trs-isomorphic-search version {__version__}")


if __name__ == "__main__":
    app()
