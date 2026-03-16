#!/usr/bin/env python3
"""Quick chart test script — verify computation works."""

from jyotish.compute.chart import compute_chart
from jyotish.interpret.formatter import format_chart_terminal

print("Computing chart for Manish Chaurasia...")
chart = compute_chart(
    name="Manish Chaurasia",
    dob="13/03/1989",
    tob="12:17",
    lat=25.3176,
    lon=83.0067,
    tz_name="Asia/Kolkata",
    gender="Male",
)

print(format_chart_terminal(chart))

# Verify key values
assert chart.lagna_sign == "Mithuna", f"Expected Mithuna, got {chart.lagna_sign}"
assert chart.planets["Moon"].nakshatra == "Rohini", f"Expected Rohini, got {chart.planets['Moon'].nakshatra}"
print("\n✓ All assertions passed!")
