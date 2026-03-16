"""Planet (Graha) constants."""

from __future__ import annotations

import swisseph as swe

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

PLANETS_HI = [
    "सूर्य", "चन्द्र", "मंगल", "बुध",
    "बृहस्पति", "शुक्र", "शनि", "राहु", "केतु",
]

# Swiss Ephemeris planet indices
SWE_PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE,  # True Node
}
# Ketu = Rahu + 180°

# Planetary friendships
NATURAL_FRIENDS: dict[str, list[str]] = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"],
    "Rahu": ["Mercury", "Venus", "Saturn"],
    "Ketu": ["Mars", "Jupiter"],
}

NATURAL_ENEMIES: dict[str, list[str]] = {
    "Sun": ["Saturn", "Venus"],
    "Moon": ["Rahu", "Ketu"],
    "Mars": ["Mercury"],
    "Mercury": ["Moon"],
    "Jupiter": ["Mercury", "Venus"],
    "Venus": ["Sun", "Moon"],
    "Saturn": ["Sun", "Moon", "Mars"],
    "Rahu": ["Sun", "Moon", "Mars"],
    "Ketu": ["Mercury", "Venus"],
}

NATURAL_NEUTRALS: dict[str, list[str]] = {
    "Sun": ["Mercury"],
    "Moon": ["Mars", "Jupiter", "Venus", "Saturn"],
    "Mars": ["Venus", "Saturn"],
    "Mercury": ["Mars", "Jupiter", "Saturn"],
    "Jupiter": ["Saturn"],
    "Venus": ["Mars", "Jupiter"],
    "Saturn": ["Jupiter"],
    "Rahu": ["Jupiter"],
    "Ketu": ["Saturn", "Moon", "Sun"],
}

# Combustion limits (degrees from Sun)
COMBUSTION_LIMITS: dict[str, float] = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": 14.0,   # 12.0 when retrograde
    "Jupiter": 11.0,
    "Venus": 10.0,     # 8.0 when retrograde
    "Saturn": 15.0,
}

COMBUSTION_LIMITS_RETROGRADE: dict[str, float] = {
    "Mercury": 12.0,
    "Venus": 8.0,
}

# Special (additional) aspects beyond the standard 7th-house aspect
SPECIAL_ASPECTS: dict[str, list[int]] = {
    "Mars": [4, 8],       # 4th and 8th house aspects
    "Jupiter": [5, 9],    # 5th and 9th house aspects
    "Saturn": [3, 10],    # 3rd and 10th house aspects
    "Rahu": [5, 9],       # Same as Jupiter
    "Ketu": [5, 9],       # Same as Jupiter
}

# Day-planet mapping
DAY_PLANET = {
    0: "Sun",      # Sunday
    1: "Moon",     # Monday
    2: "Mars",     # Tuesday
    3: "Mercury",  # Wednesday
    4: "Jupiter",  # Thursday
    5: "Venus",    # Friday
    6: "Saturn",   # Saturday
}

DAY_NAMES = {
    0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
    4: "Thursday", 5: "Friday", 6: "Saturday",
}

DAY_NAMES_HI = {
    0: "रविवार", 1: "सोमवार", 2: "मंगलवार", 3: "बुधवार",
    4: "गुरुवार", 5: "शुक्रवार", 6: "शनिवार",
}
