#!/usr/bin/env python3
"""Standalone daily transit script — shows today's transits for a chart."""

from daivai_engine.compute.chart import compute_chart
from daivai_engine.compute.panchang import compute_panchang
from daivai_engine.compute.transit import compute_transits
from daivai_engine.utils.datetime_utils import now_ist


# Default: Manish's chart
chart = compute_chart(
    name="Manish Chaurasia",
    dob="13/03/1989",
    tob="12:17",
    lat=25.3176,
    lon=83.0067,
    tz_name="Asia/Kolkata",
    gender="Male",
)

today = now_ist()
date_str = today.strftime("%d/%m/%Y")

print(f"=== Daily Transit Report — {date_str} ===")
print(f"Chart: {chart.name} | Lagna: {chart.lagna_sign}")
print()

# Panchang
panchang = compute_panchang(date_str, chart.latitude, chart.longitude, chart.timezone_name)
print(f"Vara: {panchang.vara} ({panchang.vara_hi})")
print(f"Tithi: {panchang.tithi_name} ({panchang.paksha})")
print(f"Nakshatra: {panchang.nakshatra_name}")
print(f"Rahu Kaal: {panchang.rahu_kaal}")
print()

# Transits
transit_data = compute_transits(chart, today)
print("Planet Transits:")
print(f"{'Planet':10s} {'Sign':14s} {'House':6s} {'Retro':6s}")
print("-" * 40)
for t in transit_data.transits:
    r = "[R]" if t.is_retrograde else ""
    print(f"{t.name:10s} {t.sign:14s} {t.natal_house_activated:5d}  {r}")
print()

print("Major Transits:")
for mt in transit_data.major_transits:
    print(f"  • {mt}")
