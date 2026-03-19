#!/usr/bin/env python3
"""Generate and save charts for the Chaurasia family.

Computes chart, dashas, yogas, gemstones for each family member.
Saves JSON to output/family/ and prints summary table.
"""
from __future__ import annotations

from pathlib import Path

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.compute.dasha import find_current_dasha
from jyotish_engine.compute.yoga import detect_all_yogas
from jyotish_products.interpret.context import build_lordship_context


FAMILY = [
    {"name": "Manish Chaurasia", "dob": "13/03/1989", "tob": "12:17",
     "lat": 25.3176, "lon": 83.0067, "gender": "Male"},
    {"name": "Vaishali Chaurasia", "dob": "20/08/1992", "tob": "12:00",
     "lat": 25.3176, "lon": 83.0067, "gender": "Female"},
    {"name": "Abhay Chaurasia", "dob": "22/07/1985", "tob": "08:00",
     "lat": 25.3176, "lon": 83.0067, "gender": "Male"},
    {"name": "Shashank Chaurasia", "dob": "15/01/1993", "tob": "10:00",
     "lat": 25.3176, "lon": 83.0067, "gender": "Male"},
    {"name": "Dhitya", "dob": "07/01/2020", "tob": "14:05",
     "lat": 25.3176, "lon": 83.0067, "gender": "Female"},
    {"name": "Devina", "dob": "01/04/2021", "tob": "17:59",
     "lat": 25.3176, "lon": 83.0067, "gender": "Female"},
    {"name": "Krisha", "dob": "01/04/2021", "tob": "18:00",
     "lat": 25.3176, "lon": 83.0067, "gender": "Female"},
]

OUTPUT_DIR = Path("output/family")


def main() -> None:
    """Generate all family charts."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"{'Name':<25} {'Lagna':<12} {'Moon Nak':<15} {'MD':<10} {'AD':<10} {'Rec. Stones'}")
    print("=" * 100)

    for member in FAMILY:
        chart = compute_chart(
            name=member["name"], dob=member["dob"], tob=member["tob"],
            lat=member["lat"], lon=member["lon"],
            tz_name="Asia/Kolkata", gender=member["gender"],
        )

        md, ad, _pd = find_current_dasha(chart)
        yogas = detect_all_yogas(chart)
        ctx = build_lordship_context(chart.lagna_sign)

        rec_stones = [s["stone"] for s in ctx.get("recommended_stones", [])]

        # Save JSON
        safe_name = member["name"].lower().replace(" ", "_")
        path = OUTPUT_DIR / f"{safe_name}.json"
        path.write_text(chart.model_dump_json(indent=2))

        # Print summary
        moon = chart.planets["Moon"]
        yoga_count = sum(1 for y in yogas if y.is_present)
        stones_str = ", ".join(rec_stones[:3]) if rec_stones else "—"

        print(
            f"{member['name']:<25} {chart.lagna_sign:<12} "
            f"{moon.nakshatra:<15} {md.lord:<10} {ad.lord:<10} {stones_str}"
        )

    print(f"\nCharts saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
