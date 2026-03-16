"""Companion CLI commands — daily, pooja, transit, muhurta, panchang, match."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.markdown import Markdown

from jyotish.cli_utils import console, compute_or_load, load_chart_from_file


@click.command()
@click.option("--chart", "chart_file", default=None, help="Saved chart JSON")
@click.option("--name", default=None, help="Full name")
@click.option("--dob", default=None, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", default=None, help="Time of birth (HH:MM)")
@click.option("--place", default=None, help="Place of birth")
@click.option("--gender", default="Male", help="Gender")
def daily(
    chart_file: str | None, name: str | None, dob: str | None,
    tob: str | None, place: str | None, gender: str,
) -> None:
    """Get today's personalized daily suggestion."""
    from jyotish.compute.daily import compute_daily_suggestion

    chart_data = compute_or_load(name=name, dob=dob, tob=tob, place=place,
                                 gender=gender, chart_file=chart_file)
    suggestion = compute_daily_suggestion(chart_data)

    lines = [f"# Daily Suggestion — {chart_data.name}", f"**{suggestion.date}**", ""]
    lines.append(f"| Item | Value |")
    lines.append(f"|------|-------|")
    lines.append(f"| Day | {suggestion.vara} ({suggestion.vara_planet} day) |")
    lines.append(f"| Nakshatra | {suggestion.nakshatra} |")
    lines.append(f"| Tithi | {suggestion.tithi} |")
    lines.append(f"| Color | {suggestion.recommended_color} |")
    lines.append(f"| Mantra | {suggestion.recommended_mantra} |")
    lines.append(f"| Rahu Kaal | {suggestion.rahu_kaal} |")
    lines.append(f"| Day Rating | {'⭐' * suggestion.day_rating} ({suggestion.day_rating}/10) |")
    lines.append(f"| Health Focus | {suggestion.health_focus} |")
    lines.append("")

    lines.append("## Good For Today")
    for g in suggestion.good_for:
        lines.append(f"- {g}")
    lines.append("")

    lines.append("## Avoid Today")
    for a in suggestion.avoid:
        lines.append(f"- {a}")
    lines.append("")

    if suggestion.transit_impacts:
        lines.append("## Transit Impacts")
        for t in suggestion.transit_impacts:
            marker = "✅" if t.is_favorable else "⚠️"
            lines.append(f"- {marker} {t.description}")

    console.print(Markdown("\n".join(lines)))


@click.command()
@click.option("--chart", "chart_file", default=None, help="Saved chart JSON")
@click.option("--name", default=None, help="Full name")
@click.option("--dob", default=None, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", default=None, help="Time of birth (HH:MM)")
@click.option("--place", default=None, help="Place of birth")
@click.option("--gender", default="Male", help="Gender")
def pooja(
    chart_file: str | None, name: str | None, dob: str | None,
    tob: str | None, place: str | None, gender: str,
) -> None:
    """Generate personalized weekly pooja plan."""
    from jyotish.interpret.pooja_planner import generate_weekly_plan

    chart_data = compute_or_load(name=name, dob=dob, tob=tob, place=place,
                                 gender=gender, chart_file=chart_file)
    plan = generate_weekly_plan(chart_data)

    lines = [
        f"# Weekly Pooja Plan — {chart_data.name}",
        f"Lagna: {plan.lagna} ({plan.lagna_en}) | Current Dasha: {plan.current_dasha_lord}",
        "",
    ]

    if plan.special_notes:
        lines.append("## Special Notes")
        for note in plan.special_notes:
            lines.append(f"- {note}")
        lines.append("")

    lines.append("| Day | Planet | Deity | Color | Mantra | Activity | Note |")
    lines.append("|-----|--------|-------|-------|--------|----------|------|")
    for d in plan.days:
        marker = "✅" if d.is_planet_benefic else "⚠️"
        lines.append(
            f"| {d.day} ({d.day_hindi}) | {d.planet} {marker} | {d.deity} | "
            f"{d.color} | {d.mantra} | {d.activity} | {d.lordship_note[:60]} |"
        )

    console.print(Markdown("\n".join(lines)))


@click.command()
@click.option("--chart", "chart_file", default=None, help="Saved chart JSON")
@click.option("--name", default=None, help="Full name")
@click.option("--dob", default=None, help="Date of birth (DD/MM/YYYY)")
@click.option("--tob", default=None, help="Time of birth (HH:MM)")
@click.option("--place", default=None, help="Place of birth")
@click.option("--gender", default="Male", help="Gender")
@click.option("--months", default=1, help="Number of months to show (default 1)")
def transit(
    chart_file: str | None, name: str | None, dob: str | None,
    tob: str | None, place: str | None, gender: str, months: int,
) -> None:
    """Show current transits for a chart."""
    from jyotish.compute.transit import compute_transits

    chart_data = compute_or_load(name=name, dob=dob, tob=tob, place=place,
                                 gender=gender, chart_file=chart_file)
    transit_data = compute_transits(chart_data)

    lines = [
        f"# Transits — {chart_data.name} — {transit_data.target_date}",
        f"Natal Lagna: {transit_data.natal_lagna_sign}",
        f"Forecast period: {months} month(s)",
        "",
        "| Planet | Sign | Natal House | Retrograde |",
        "|--------|------|-------------|------------|",
    ]
    for t in transit_data.transits:
        r = "R" if t.is_retrograde else ""
        lines.append(f"| {t.name} | {t.sign} | {t.natal_house_activated} | {r} |")

    lines.append("")
    lines.append("## Major Transits")
    for mt in transit_data.major_transits:
        lines.append(f"- {mt}")

    console.print(Markdown("\n".join(lines)))


@click.command()
@click.option("--purpose", required=True, help="Purpose (marriage/business_start/travel/property)")
@click.option("--chart", "chart_file", default=None, help="Saved chart JSON")
@click.option("--place", default=None, help="Location for muhurta")
@click.option("--from", "from_date", required=True, help="Start date (DD/MM/YYYY)")
@click.option("--to", "to_date", required=True, help="End date (DD/MM/YYYY)")
def muhurta(
    purpose: str, chart_file: str | None, place: str | None,
    from_date: str, to_date: str,
) -> None:
    """Find auspicious dates (muhurta)."""
    from jyotish.utils.geo import resolve_place
    from jyotish.utils.datetime_utils import parse_birth_datetime
    from jyotish.compute.muhurta import find_muhurta

    # Get location from chart file or --place
    if chart_file:
        chart_data = load_chart_from_file(chart_file)
        lat, lon, tz = chart_data.latitude, chart_data.longitude, chart_data.timezone_name
        loc_name = chart_data.place
    elif place:
        geo = resolve_place(place)
        lat, lon, tz = geo.latitude, geo.longitude, geo.timezone_name
        loc_name = place
    else:
        console.print("[red]Provide --chart or --place for location[/red]")
        sys.exit(1)

    start = parse_birth_datetime(from_date, "00:00", tz)
    end = parse_birth_datetime(to_date, "23:59", tz)

    # Normalize purpose name
    purpose_clean = purpose.replace("_", " ").replace("-", " ")

    candidates = find_muhurta(purpose_clean, lat, lon, start, end, tz)

    lines = [f"# Muhurta for {purpose_clean.title()} — {loc_name}"]
    lines.append(f"Search: {from_date} to {to_date}")
    lines.append("")
    if candidates:
        lines.append("| # | Date | Day | Nakshatra | Tithi | Score | Reasons |")
        lines.append("|---|------|-----|-----------|-------|-------|---------|")
        for i, c in enumerate(candidates, 1):
            reasons = "; ".join(c.reasons[:2])
            lines.append(f"| {i} | {c.date} | {c.day} | {c.nakshatra} | {c.tithi} | {c.score} | {reasons} |")
    else:
        lines.append("No suitable muhurta found in the given range.")

    console.print(Markdown("\n".join(lines)))


@click.command(name="panchang")
@click.option("--place", required=True, help="Place name")
@click.option("--date", "date_str", default=None, help="Date (DD/MM/YYYY), default today")
def panchang_cmd(place: str, date_str: str | None) -> None:
    """Show Panchang for a date and place."""
    from jyotish.utils.geo import resolve_place
    from jyotish.compute.panchang import compute_panchang

    geo = resolve_place(place)

    if date_str is None:
        from jyotish.utils.datetime_utils import now_ist
        date_str = now_ist().strftime("%d/%m/%Y")

    panchang = compute_panchang(date_str, geo.latitude, geo.longitude, geo.timezone_name, place)

    lines = [f"# Panchang — {place} — {date_str}", ""]
    lines.append("| Element | Value |")
    lines.append("|---------|-------|")
    lines.append(f"| Vara | {panchang.vara} ({panchang.vara_hi}) — {panchang.vara_planet} |")
    lines.append(f"| Tithi | {panchang.tithi_name} ({panchang.paksha} Paksha) |")
    lines.append(f"| Nakshatra | {panchang.nakshatra_name} |")
    lines.append(f"| Yoga | {panchang.yoga_name} |")
    lines.append(f"| Karana | {panchang.karana_name} |")
    lines.append(f"| Sunrise | {panchang.sunrise} |")
    lines.append(f"| Sunset | {panchang.sunset} |")
    lines.append(f"| Rahu Kaal | {panchang.rahu_kaal} |")

    console.print(Markdown("\n".join(lines)))


@click.command(name="match")
@click.option("--person1", required=True, help="Person 1 chart JSON")
@click.option("--person2", required=True, help="Person 2 chart JSON")
def match_cmd(person1: str, person2: str) -> None:
    """Ashtakoot (36 guna) matching between two charts."""
    from jyotish.compute.matching import compute_ashtakoot
    from jyotish.deliver.markdown_report import generate_matching_report

    c1 = load_chart_from_file(person1)
    c2 = load_chart_from_file(person2)

    result = compute_ashtakoot(
        person1_nakshatra_index=c1.planets["Moon"].nakshatra_index,
        person1_moon_sign=c1.planets["Moon"].sign_index,
        person2_nakshatra_index=c2.planets["Moon"].nakshatra_index,
        person2_moon_sign=c2.planets["Moon"].sign_index,
    )

    report = generate_matching_report(result, c1.name, c2.name)
    console.print(Markdown(report))
