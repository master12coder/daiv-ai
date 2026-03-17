"""Main CLI entry point — auto-registers commands from product plugins."""
from __future__ import annotations

import logging
import sys

import click
from rich.console import Console

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.compute.geo import resolve_or_manual
from jyotish_engine.models.chart import ChartData

logger = logging.getLogger(__name__)
console = Console()


def _load_chart_from_args(
    name: str | None = None,
    dob: str | None = None,
    tob: str | None = None,
    place: str | None = None,
    gender: str = "Male",
    chart: str | None = None,
) -> ChartData:
    """Load chart from either saved JSON or compute from birth details."""
    if chart:
        import json
        from pathlib import Path

        path = Path(chart)
        if not path.exists():
            console.print(f"[red]Chart file not found: {chart}[/red]")
            sys.exit(1)
        data = json.loads(path.read_text())
        return ChartData.model_validate(data)

    if not all([name, dob, tob]):
        console.print("[red]Provide --name, --dob, --tob (and --place or --chart)[/red]")
        sys.exit(1)

    return compute_chart(
        name=name, dob=dob, tob=tob, place=place, gender=gender,
    )


@click.group()
@click.version_option(version="1.0.0", prog_name="jyotish")
def main() -> None:
    """Vedic AI Framework — AI-powered Vedic astrology."""
    logging.basicConfig(level=logging.WARNING)


# ── Chart command ──────────────────────────────────────────────────────────

@main.command()
@click.option("--name", required=True, help="Full name")
@click.option("--dob", required=True, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", required=True, help="Time of birth (HH:MM)")
@click.option("--place", default=None, help="Place of birth")
@click.option("--gender", default="Male", help="Gender (Male/Female)")
def chart(name: str, dob: str, tob: str, place: str | None, gender: str) -> None:
    """Compute and display a Vedic birth chart."""
    from jyotish_engine.compute.yoga import detect_all_yogas
    from jyotish_engine.compute.dosha import detect_all_doshas
    from jyotish_engine.compute.dasha import compute_mahadashas
    from rich.table import Table
    from rich.panel import Panel

    chart_data = compute_chart(name=name, dob=dob, tob=tob, place=place, gender=gender)

    # Header
    console.print(Panel(
        f"Vedic Birth Chart — {chart_data.name}",
        style="bold cyan",
    ))
    console.print(
        f"DOB: {chart_data.dob}  TOB: {chart_data.tob}  "
        f"Place: {chart_data.place} "
        f"Lagna: {chart_data.lagna_sign} ({chart_data.lagna_sign_en}) — "
        f"{chart_data.lagna_degree:.1f}°"
    )

    # Planets table
    table = Table(title="Planetary Positions")
    for col in ["Planet", "Sign", "House", "Degree", "Nakshatra", "Pada", "Dignity", "R", "C"]:
        table.add_column(col)

    for p in chart_data.planets.values():
        table.add_row(
            p.name, p.sign, str(p.house),
            f"{p.degree_in_sign:.1f}°", p.nakshatra, str(p.pada),
            p.dignity,
            "R" if p.is_retrograde else "",
            "C" if p.is_combust else "",
        )
    console.print(table)

    # Yogas
    yogas = detect_all_yogas(chart_data)
    if yogas:
        console.print("\n[bold]Yogas Detected[/bold]")
        for y in yogas:
            prefix = "[+]" if y.effect == "benefic" else "[-]" if y.effect == "malefic" else "[~]"
            console.print(f"{prefix} {y.name} ({y.name_hindi}) — {y.description}")

    # Doshas
    doshas = detect_all_doshas(chart_data)
    if doshas:
        console.print("\n[bold]Doshas[/bold]")
        for d in doshas:
            console.print(f"{'⚠️' if d.is_present else '✓'} {d.name} — {d.description}")

    # Dasha
    dashas = compute_mahadashas(chart_data)
    console.print("\n[bold]Vimshottari Mahadasha[/bold]")
    from datetime import datetime

    now = datetime.now()
    for md in dashas:
        marker = " ← CURRENT" if md.start <= now <= md.end else ""
        console.print(
            f"  {md.planet:8s} {md.start.strftime('%Y-%m-%d')} to "
            f"{md.end.strftime('%Y-%m-%d')}{marker}"
        )


# ── Save command ───────────────────────────────────────────────────────────

@main.command()
@click.option("--name", required=True, help="Full name")
@click.option("--dob", required=True, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", required=True, help="Time of birth (HH:MM)")
@click.option("--place", default=None, help="Place of birth")
@click.option("--gender", default="Male", help="Gender")
@click.option("-o", "--output", required=True, help="Output JSON file path")
def save(name: str, dob: str, tob: str, place: str | None, gender: str, output: str) -> None:
    """Compute and save chart as JSON for later reuse."""
    from pathlib import Path

    chart_data = compute_chart(name=name, dob=dob, tob=tob, place=place, gender=gender)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(chart_data.model_dump_json(indent=2))
    console.print(f"Chart saved to {output}")
    console.print(f"Lagna: {chart_data.lagna_sign} ({chart_data.lagna_sign_en})")


# ── Report command ─────────────────────────────────────────────────────────

@main.command()
@click.option("--name", default=None, help="Full name")
@click.option("--dob", default=None, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", default=None, help="Time of birth (HH:MM)")
@click.option("--place", default=None, help="Place of birth")
@click.option("--gender", default="Male", help="Gender")
@click.option("--chart", default=None, help="Saved chart JSON path")
@click.option("--llm", default="none", help="LLM backend (groq/ollama/claude/openai/none)")
@click.option("--output", "-o", default=None, help="Save report to file")
def report(
    name: str | None, dob: str | None, tob: str | None,
    place: str | None, gender: str, chart: str | None,
    llm: str, output: str | None,
) -> None:
    """Generate full chart report with interpretation."""
    chart_data = _load_chart_from_args(name, dob, tob, place, gender, chart)

    # Show chart first (same as chart command)
    from click import Context

    ctx = click.get_current_context()
    ctx.invoke(
        chart.__wrapped__ if hasattr(chart, "__wrapped__") else chart,
        name=chart_data.name, dob=chart_data.dob, tob=chart_data.tob,
        place=chart_data.place, gender=chart_data.gender,
    )

    if llm != "none":
        try:
            from jyotish_products.interpret.renderer import interpret_chart

            result = interpret_chart(chart_data, backend_name=llm)
            console.print("\n[bold cyan]AI Interpretation[/bold cyan]")
            console.print(result)
        except ImportError:
            console.print("[yellow]LLM backend not available. Install jyotish-products.[/yellow]")
    else:
        console.print("\n[dim]Skipping LLM interpretation (--llm none)[/dim]")


# ── Daily command ──────────────────────────────────────────────────────────

@main.command()
@click.option("--name", default=None)
@click.option("--dob", default=None)
@click.option("--tob", default=None)
@click.option("--place", default=None)
@click.option("--gender", default="Male")
@click.option("--chart", default=None, help="Saved chart JSON path")
def daily(
    name: str | None, dob: str | None, tob: str | None,
    place: str | None, gender: str, chart: str | None,
) -> None:
    """Get today's personalized daily suggestion."""
    chart_data = _load_chart_from_args(name, dob, tob, place, gender, chart)

    from jyotish_engine.compute.daily import compute_daily_suggestion
    from rich.table import Table
    from rich.panel import Panel

    suggestion = compute_daily_suggestion(chart_data)

    console.print(Panel(f"Daily Suggestion — {chart_data.name}", style="bold cyan"))
    console.print(f"{suggestion.date}\n")

    table = Table()
    table.add_column("Item")
    table.add_column("Value")
    table.add_row("Day", suggestion.vara)
    table.add_row("Nakshatra", suggestion.nakshatra)
    table.add_row("Tithi", suggestion.tithi)
    table.add_row("Color", suggestion.recommended_color)
    table.add_row("Mantra", suggestion.recommended_mantra)
    table.add_row("Rahu Kaal", suggestion.rahu_kaal)
    table.add_row("Day Rating", f"{'⭐' * suggestion.day_rating} ({suggestion.day_rating}/10)")
    table.add_row("Health Focus", suggestion.health_focus)
    console.print(table)

    if suggestion.good_for:
        console.print("\n[bold green]Good For Today[/bold green]")
        for item in suggestion.good_for:
            console.print(f" • {item}")

    if suggestion.avoid:
        console.print("\n[bold red]Avoid Today[/bold red]")
        for item in suggestion.avoid:
            console.print(f" • {item}")


# ── Transit command ────────────────────────────────────────────────────────

@main.command()
@click.option("--name", default=None)
@click.option("--dob", default=None)
@click.option("--tob", default=None)
@click.option("--place", default=None)
@click.option("--gender", default="Male")
@click.option("--chart", default=None, help="Saved chart JSON path")
@click.option("--months", default=6, help="Forecast period in months")
def transit(
    name: str | None, dob: str | None, tob: str | None,
    place: str | None, gender: str, chart: str | None, months: int,
) -> None:
    """Show current transits for a chart."""
    chart_data = _load_chart_from_args(name, dob, tob, place, gender, chart)

    from jyotish_engine.compute.transit import compute_transits
    from rich.table import Table
    from rich.panel import Panel

    transits = compute_transits(chart_data)

    console.print(Panel(
        f"Transits — {chart_data.name} — {transits.date}",
        style="bold cyan",
    ))
    console.print(f"Natal Lagna: {chart_data.lagna_sign} Forecast period: {months} month(s)\n")

    table = Table()
    for col in ["Planet", "Sign", "Natal House", "Retrograde"]:
        table.add_column(col)
    for t in transits.planets:
        table.add_row(t.planet, t.sign, str(t.natal_house), "R" if t.is_retrograde else "")
    console.print(table)


# ── Muhurta command ────────────────────────────────────────────────────────

@main.command()
@click.option("--purpose", required=True, help="Purpose (marriage, business_start, travel, etc.)")
@click.option("--chart", required=True, help="Saved chart JSON path")
@click.option("--from", "from_date", required=True, help="Start date (DD/MM/YYYY)")
@click.option("--to", "to_date", required=True, help="End date (DD/MM/YYYY)")
def muhurta(purpose: str, chart: str, from_date: str, to_date: str) -> None:
    """Find auspicious dates (muhurta)."""
    chart_data = _load_chart_from_args(chart=chart)

    from jyotish_engine.compute.muhurta import find_muhurta
    from jyotish_engine.compute.datetime_utils import parse_birth_datetime
    from rich.table import Table
    from rich.panel import Panel

    tz = chart_data.timezone_name
    start = parse_birth_datetime(from_date, "00:00", tz)
    end = parse_birth_datetime(to_date, "23:59", tz)
    purpose_clean = purpose.replace("_", " ").replace("-", " ")

    results = find_muhurta(
        purpose=purpose_clean,
        lat=chart_data.latitude, lon=chart_data.longitude,
        tz_name=tz, start_date=start, end_date=end,
    )

    console.print(Panel(
        f"Muhurta for {purpose_clean.title()} — {chart_data.place}",
        style="bold cyan",
    ))
    console.print(f"Search: {from_date} to {to_date}\n")

    table = Table()
    for col in ["#", "Date", "Day", "Nakshatra", "Tithi", "Score", "Reasons"]:
        table.add_column(col)
    for i, r in enumerate(results[:10], 1):
        table.add_row(
            str(i), r.date, r.day, r.nakshatra, r.tithi,
            f"{r.score:.1f}", "; ".join(r.reasons),
        )
    console.print(table)


# ── Pooja command ──────────────────────────────────────────────────────────

@main.command()
@click.option("--name", default=None)
@click.option("--dob", default=None)
@click.option("--tob", default=None)
@click.option("--place", default=None)
@click.option("--gender", default="Male")
@click.option("--chart", default=None, help="Saved chart JSON path")
def pooja(
    name: str | None, dob: str | None, tob: str | None,
    place: str | None, gender: str, chart: str | None,
) -> None:
    """Generate personalized weekly pooja plan."""
    chart_data = _load_chart_from_args(name, dob, tob, place, gender, chart)

    try:
        from jyotish_products.interpret.pooja_planner import generate_weekly_plan

        plan = generate_weekly_plan(chart_data)
        console.print(plan)
    except ImportError:
        console.print("[yellow]Pooja planner requires jyotish-products.[/yellow]")


# ── Events command ─────────────────────────────────────────────────────────

@main.group()
def events() -> None:
    """Life event tracking commands."""


@events.command("add")
@click.option("--chart", required=True, help="Saved chart JSON path")
@click.option("--type", "event_type", required=True, help="Event type")
@click.option("--date", "event_date", required=True, help="Event date")
@click.option("--desc", default="", help="Description")
def events_add(chart: str, event_type: str, event_date: str, desc: str) -> None:
    """Add a life event."""
    chart_data = _load_chart_from_args(chart=chart)

    try:
        from jyotish_products.store.events import LifeEventsDB

        db = LifeEventsDB()
        event_id = db.add_event(
            chart_id=chart_data.name,
            event_type=event_type,
            event_date=event_date,
            description=desc,
        )
        console.print(f"Event added: {event_id}")
        console.print(f"  Type: {event_type}")
        console.print(f"  Date: {event_date}")
        console.print(f"  Description: {desc}")
    except ImportError:
        console.print("[yellow]Events require jyotish-products.[/yellow]")


# ── Dashboard command ──────────────────────────────────────────────────────

@main.command()
def dashboard() -> None:
    """Show prediction accuracy dashboard."""
    from rich.panel import Panel

    try:
        from jyotish_products.store.predictions import PredictionTracker

        tracker = PredictionTracker()
        stats = tracker.get_stats()
        console.print(Panel("Prediction Accuracy Dashboard", style="bold cyan"))
        console.print(
            f"Total predictions: {stats.get('total', 0)} "
            f"Pending: {stats.get('pending', 0)} "
            f"Overall accuracy: {stats.get('accuracy', 0):.1f}%"
        )
        if stats.get("total", 0) == 0:
            console.print("\nNo decided predictions yet. Track predictions with jyotish predict track.")
    except ImportError:
        console.print("[yellow]Dashboard requires jyotish-products.[/yellow]")


if __name__ == "__main__":
    main()
