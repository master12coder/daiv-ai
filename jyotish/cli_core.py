"""Core CLI commands — chart, report, save, export, ashtakavarga, kp."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.markdown import Markdown

from jyotish.cli_utils import console, compute_or_load, save_chart_to_file


@click.command()
@click.option("--name", required=True, help="Full name")
@click.option("--dob", required=True, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", required=True, help="Time of birth (HH:MM)")
@click.option("--place", required=True, help="Place of birth")
@click.option("--gender", default="Male", help="Gender (Male/Female)")
@click.option("--format", "fmt", default="terminal", type=click.Choice(["terminal", "json"]))
def chart(name: str, dob: str, tob: str, place: str, gender: str, fmt: str) -> None:
    """Compute a Vedic birth chart."""
    from jyotish.interpret.formatter import format_chart_terminal, format_chart_json

    try:
        chart_data = compute_or_load(name=name, dob=dob, tob=tob, place=place, gender=gender)
    except Exception as e:
        console.print(f"[red]Error computing chart: {e}[/red]")
        sys.exit(1)

    if fmt == "json":
        click.echo(format_chart_json(chart_data))
    else:
        console.print(Markdown(format_chart_terminal(chart_data)))


@click.command()
@click.option("--name", default=None, help="Full name")
@click.option("--dob", default=None, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", default=None, help="Time of birth (HH:MM)")
@click.option("--place", default=None, help="Place of birth")
@click.option("--gender", default="Male", help="Gender")
@click.option("--chart", "chart_file", default=None, help="Saved chart JSON file")
@click.option("--llm", default=None, help="LLM backend (ollama/groq/claude/openai/none)")
@click.option("--output", default=None, help="Output file path")
@click.option("--events", "events_file", default=None, help="Life events JSON file")
@click.option("--format", "fmt", default="markdown", type=click.Choice(["markdown", "json"]))
def report(
    name: str | None, dob: str | None, tob: str | None, place: str | None,
    gender: str, chart_file: str | None, llm: str | None,
    output: str | None, events_file: str | None, fmt: str,
) -> None:
    """Generate full chart report with interpretation."""
    from jyotish.interpret.interpreter import interpret_chart, interpret_with_events
    from jyotish.interpret.formatter import format_report_markdown, format_chart_terminal
    from jyotish.interpret.llm_backend import get_backend

    try:
        chart_data = compute_or_load(name=name, dob=dob, tob=tob, place=place,
                                     gender=gender, chart_file=chart_file)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

    backend = get_backend(llm) if llm else get_backend("none")

    if backend.name() == "none":
        content = format_chart_terminal(chart_data)
    else:
        try:
            if events_file:
                event_data = json.loads(Path(events_file).read_text())
                content = interpret_with_events(chart_data, event_data, backend)
            else:
                interpretations = interpret_chart(chart_data, backend)
                content = format_report_markdown(chart_data, interpretations)
        except Exception as e:
            console.print(f"[yellow]LLM failed: {e}. Falling back to computation.[/yellow]")
            content = format_chart_terminal(chart_data)

    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(content, encoding="utf-8")
        console.print(f"[green]Report saved to {output}[/green]")
    else:
        console.print(Markdown(content))


@click.command()
@click.option("--name", required=True, help="Full name")
@click.option("--dob", required=True, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", required=True, help="Time of birth (HH:MM)")
@click.option("--place", required=True, help="Place of birth")
@click.option("--gender", default="Male", help="Gender")
@click.option("-o", "--output", required=True, help="Output JSON file path")
def save(name: str, dob: str, tob: str, place: str, gender: str, output: str) -> None:
    """Compute and save chart for later reuse."""
    try:
        chart_data = compute_or_load(name=name, dob=dob, tob=tob, place=place, gender=gender)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

    save_chart_to_file(chart_data, output)
    console.print(f"[green]Chart saved to {output}[/green]")
    console.print(f"Lagna: {chart_data.lagna_sign} ({chart_data.lagna_sign_en})")


@click.command(name="export")
@click.option("--name", default=None, help="Full name")
@click.option("--dob", default=None, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", default=None, help="Time of birth (HH:MM)")
@click.option("--place", default=None, help="Place of birth")
@click.option("--gender", default="Male", help="Gender")
@click.option("--chart", "chart_file", default=None, help="Saved chart JSON")
@click.option("--format", "fmt", default="json", type=click.Choice(["json", "markdown"]))
@click.option("--output", default=None, help="Output file path")
def export_cmd(
    name: str | None, dob: str | None, tob: str | None, place: str | None,
    gender: str, chart_file: str | None, fmt: str, output: str | None,
) -> None:
    """Export chart as JSON or Markdown."""
    from jyotish.deliver.json_export import export_chart_json
    from jyotish.deliver.markdown_report import generate_markdown_report

    chart_data = compute_or_load(name=name, dob=dob, tob=tob, place=place,
                                 gender=gender, chart_file=chart_file)

    if fmt == "json":
        content = export_chart_json(chart_data, output)
    else:
        content = generate_markdown_report(chart_data, output_path=output)

    if output:
        console.print(f"[green]Exported to {output}[/green]")
    else:
        click.echo(content)


@click.command(name="ashtakavarga")
@click.option("--name", default=None, help="Full name")
@click.option("--dob", default=None, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", default=None, help="Time of birth (HH:MM)")
@click.option("--place", default=None, help="Place of birth")
@click.option("--chart", "chart_file", default=None, help="Saved chart JSON")
def ashtakavarga_cmd(
    name: str | None, dob: str | None, tob: str | None,
    place: str | None, chart_file: str | None,
) -> None:
    """Compute Ashtakavarga bindu table."""
    from jyotish.compute.ashtakavarga import compute_ashtakavarga
    from jyotish.domain.constants.signs import SIGNS

    chart_data = compute_or_load(name=name, dob=dob, tob=tob, place=place, chart_file=chart_file)
    result = compute_ashtakavarga(chart_data)

    lines = [f"# Ashtakavarga — {chart_data.name}", ""]
    lines.append(f"## Sarvashtakavarga (Total: {result.total})")
    lines.append("| Sign | Bindus |")
    lines.append("|------|--------|")
    for i, b in enumerate(result.sarva):
        lines.append(f"| {SIGNS[i]} | {b} |")

    console.print(Markdown("\n".join(lines)))


@click.command(name="kp")
@click.option("--name", default=None, help="Full name")
@click.option("--dob", default=None, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", default=None, help="Time of birth (HH:MM)")
@click.option("--place", default=None, help="Place of birth")
@click.option("--chart", "chart_file", default=None, help="Saved chart JSON")
def kp_cmd(
    name: str | None, dob: str | None, tob: str | None,
    place: str | None, chart_file: str | None,
) -> None:
    """Compute KP sub-lord positions."""
    from jyotish.compute.kp import compute_kp_positions

    chart_data = compute_or_load(name=name, dob=dob, tob=tob, place=place, chart_file=chart_file)
    positions = compute_kp_positions(chart_data)

    lines = [f"# KP Sub-Lord Positions — {chart_data.name}", ""]
    lines.append("| Planet | Nakshatra | Star Lord | Sub Lord | Sub-Sub Lord |")
    lines.append("|--------|-----------|-----------|----------|--------------|")
    for p in positions:
        lines.append(f"| {p.name} | {p.nakshatra} | {p.nakshatra_lord} | {p.sub_lord} | {p.sub_sub_lord} |")

    console.print(Markdown("\n".join(lines)))
