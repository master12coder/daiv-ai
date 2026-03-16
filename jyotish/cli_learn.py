"""Learning CLI commands — correct, learn-audio, rules, events, dashboard."""

from __future__ import annotations

import sys
import uuid
from pathlib import Path

import click
from rich.markdown import Markdown

from jyotish.cli_utils import console, load_chart_from_file


@click.command()
@click.option("--chart-name", "chart_name", required=True, help="Chart name")
@click.option("--category", required=True, help="Category (gemstone/house_reading/dasha/remedy)")
@click.option("--ai-said", "ai_said", required=True, help="What the AI said")
@click.option("--pandit-said", "pandit_said", required=True, help="What Pandit Ji said")
@click.option("--reasoning", default="", help="Pandit Ji's reasoning")
@click.option("--pandit", default="Pandit Ji", help="Pandit name")
def correct(
    chart_name: str, category: str, ai_said: str,
    pandit_said: str, reasoning: str, pandit: str,
) -> None:
    """Add a Pandit Ji correction."""
    from jyotish.learn.corrections import PanditCorrection, PanditCorrectionStore

    store = PanditCorrectionStore()
    correction = PanditCorrection(
        pandit_name=pandit, chart_name=chart_name, category=category,
        ai_said=ai_said, pandit_said=pandit_said, pandit_reasoning=reasoning,
        correction_type="override",
    )
    cid = store.add_correction(correction)
    console.print(f"[green]Correction added: {cid}[/green]")
    console.print("Status: pending (validate to learn from it)")


@click.command(name="learn-audio")
@click.option("--file", "audio_file", required=True, help="Audio file path")
@click.option("--chart-name", "chart_name", required=True, help="Chart name")
@click.option("--pandit", default="Pandit Ji", help="Pandit name")
@click.option("--method", default="groq", type=click.Choice(["groq", "local"]))
def learn_audio(audio_file: str, chart_name: str, pandit: str, method: str) -> None:
    """Process Pandit Ji audio recording for corrections."""
    from jyotish.learn.audio_processor import process_audio_session
    from jyotish.learn.corrections import PanditCorrectionStore

    try:
        result, corrections = process_audio_session(audio_file, chart_name, pandit, method)
    except Exception as e:
        console.print(f"[red]Error processing audio: {e}[/red]")
        sys.exit(1)

    console.print(f"[green]Transcribed {result.duration_seconds:.0f}s of audio[/green]")
    console.print(f"Extracted {len(corrections)} potential corrections")

    if corrections:
        store = PanditCorrectionStore()
        for c in corrections:
            cid = store.add_correction(c)
            console.print(f"  [{cid}] {c.pandit_said[:60]}...")


@click.command()
@click.option("--lagna", default=None, help="Filter by lagna")
@click.option("--category", default=None, help="Filter by category")
def rules(lagna: str | None, category: str | None) -> None:
    """Show learned rules from Pandit Ji corrections."""
    from jyotish.learn.rule_extractor import RuleExtractor

    extractor = RuleExtractor()
    learned = extractor.extract_rules()

    if lagna:
        learned = [r for r in learned if r.lagna == lagna or not r.lagna]
    if category:
        learned = [r for r in learned if r.category == category]

    if not learned:
        console.print("[yellow]No learned rules yet. Add and validate corrections first.[/yellow]")
        return

    lines = ["# Learned Rules"]
    for r in learned:
        lines.append(f"## [{r.category}] {r.lagna or 'General'}")
        lines.append(f"**Rule:** {r.rule_text}")
        lines.append(f"**Confidence:** {r.confidence} | **Sources:** {r.occurrence_count}")
        lines.append("")

    console.print(Markdown("\n".join(lines)))


@click.group()
def events() -> None:
    """Life event tracking commands."""


@events.command(name="add")
@click.option("--chart", "chart_file", required=True, help="Chart JSON file")
@click.option("--type", "event_type", required=True, help="Event type (marriage/career/health/education/financial/child)")
@click.option("--date", "event_date", required=True, help="Event date (YYYY-MM or DD/MM/YYYY)")
@click.option("--desc", "description", required=True, help="Event description")
def events_add(chart_file: str, event_type: str, event_date: str, description: str) -> None:
    """Add a life event to the database."""
    from jyotish.learn.life_events_db import LifeEventsDB

    chart_data = load_chart_from_file(chart_file)

    db = LifeEventsDB()
    try:
        # Ensure chart exists in DB (get or create)
        chart_id = db.get_or_create_chart_from_data(chart_data)

        # Add event
        event_id = db.add_event_simple(
            chart_id=chart_id,
            event_type=event_type,
            event_date=event_date,
            description=description,
        )
        console.print(f"[green]Event added: {event_id}[/green]")
        console.print(f"  Type: {event_type}")
        console.print(f"  Date: {event_date}")
        console.print(f"  Description: {description}")
    finally:
        db.close()


@events.command(name="list")
@click.option("--chart", "chart_file", required=True, help="Chart JSON file")
def events_list(chart_file: str) -> None:
    """List life events for a chart."""
    from jyotish.learn.life_events_db import LifeEventsDB

    chart_data = load_chart_from_file(chart_file)
    db = LifeEventsDB()
    try:
        chart_id = db.get_chart_id(chart_data.name)
        if chart_id is None:
            console.print("[yellow]No events found for this chart.[/yellow]")
            return

        event_list = db.get_events_as_dicts(chart_id)
        if not event_list:
            console.print("[yellow]No events recorded.[/yellow]")
            return

        lines = [f"# Life Events — {chart_data.name}", ""]
        lines.append("| # | Type | Date | Description |")
        lines.append("|---|------|------|-------------|")
        for i, ev in enumerate(event_list, 1):
            lines.append(f"| {i} | {ev['event_type']} | {ev['event_date']} | {ev['description']} |")

        console.print(Markdown("\n".join(lines)))
    finally:
        db.close()


@click.command()
@click.option("--category", default=None, help="Filter by category")
@click.option("--format", "fmt", default="terminal", type=click.Choice(["terminal", "json"]))
def dashboard(category: str | None, fmt: str) -> None:
    """Show prediction accuracy dashboard."""
    from jyotish.learn.prediction_tracker import PredictionTracker
    import json as json_mod

    tracker = PredictionTracker()
    try:
        dash = tracker.get_accuracy_dashboard()
    finally:
        tracker.close()

    if fmt == "json":
        click.echo(json_mod.dumps(dash, indent=2))
        return

    lines = ["# Prediction Accuracy Dashboard", ""]
    lines.append(f"**Total predictions:** {dash['total_predictions']}")
    lines.append(f"**Pending:** {dash['pending']}")
    lines.append(f"**Overall accuracy:** {dash['overall_accuracy']}%")
    lines.append("")

    cats = dash.get("categories", {})
    if cats:
        lines.append("| Category | Confirmed | Total Decided | Accuracy |")
        lines.append("|----------|-----------|---------------|----------|")
        for cat, data in cats.items():
            if category and cat != category:
                continue
            lines.append(
                f"| {cat} | {data['confirmed']} | {data['total_decided']} | {data['accuracy']}% |"
            )
    else:
        lines.append("No decided predictions yet. Track predictions with `jyotish predict track`.")

    console.print(Markdown("\n".join(lines)))
