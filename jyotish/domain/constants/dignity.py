"""Planetary dignity constants: exaltation, debilitation, own signs, mooltrikona."""

from __future__ import annotations

# Sign index where each planet is exalted
EXALTATION: dict[str, int] = {
    "Sun": 0,       # Aries
    "Moon": 1,      # Taurus
    "Mars": 9,      # Capricorn
    "Mercury": 5,   # Virgo
    "Jupiter": 3,   # Cancer
    "Venus": 11,    # Pisces
    "Saturn": 6,    # Libra
    "Rahu": 1,      # Taurus (traditional)
    "Ketu": 7,      # Scorpio (traditional)
}

# Exact exaltation degree within the sign
EXALTATION_DEGREE: dict[str, float] = {
    "Sun": 10.0,
    "Moon": 3.0,
    "Mars": 28.0,
    "Mercury": 15.0,
    "Jupiter": 5.0,
    "Venus": 27.0,
    "Saturn": 20.0,
    "Rahu": 20.0,
    "Ketu": 20.0,
}

# Sign index where each planet is debilitated (opposite of exaltation)
DEBILITATION: dict[str, int] = {
    "Sun": 6,       # Libra
    "Moon": 7,      # Scorpio
    "Mars": 3,      # Cancer
    "Mercury": 11,  # Pisces
    "Jupiter": 9,   # Capricorn
    "Venus": 5,     # Virgo
    "Saturn": 0,    # Aries
    "Rahu": 7,      # Scorpio
    "Ketu": 1,      # Taurus
}

# Own signs for each planet
OWN_SIGNS: dict[str, list[int]] = {
    "Sun": [4],         # Leo
    "Moon": [3],        # Cancer
    "Mars": [0, 7],     # Aries, Scorpio
    "Mercury": [2, 5],  # Gemini, Virgo
    "Jupiter": [8, 11], # Sagittarius, Pisces
    "Venus": [1, 6],    # Taurus, Libra
    "Saturn": [9, 10],  # Capricorn, Aquarius
    "Rahu": [10],       # Aquarius (co-lord)
    "Ketu": [7],        # Scorpio (co-lord)
}

# Mooltrikona signs and degree ranges
MOOLTRIKONA: dict[str, tuple[int, float, float]] = {
    "Sun": (4, 0.0, 20.0),       # Leo 0-20
    "Moon": (1, 3.0, 30.0),      # Taurus 3-30
    "Mars": (0, 0.0, 12.0),      # Aries 0-12
    "Mercury": (5, 15.0, 20.0),  # Virgo 15-20
    "Jupiter": (8, 0.0, 10.0),   # Sagittarius 0-10
    "Venus": (6, 0.0, 15.0),     # Libra 0-15
    "Saturn": (10, 0.0, 20.0),   # Aquarius 0-20
}
