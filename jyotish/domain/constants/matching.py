"""Compatibility matching constants (Vasya, Yoni, Bhakoot)."""

from __future__ import annotations

# Vasya: sign_index -> list of sign_indices that are vasya to it
VASYA_TABLE: dict[int, list[int]] = {
    0: [4, 7],           # Aries -> Leo, Scorpio
    1: [3, 5],           # Taurus -> Cancer, Virgo
    2: [5],              # Gemini -> Virgo
    3: [7, 8],           # Cancer -> Scorpio, Sagittarius
    4: [6],              # Leo -> Libra
    5: [2, 11],          # Virgo -> Gemini, Pisces
    6: [5, 9],           # Libra -> Virgo, Capricorn
    7: [3],              # Scorpio -> Cancer
    8: [11],             # Sagittarius -> Pisces
    9: [0, 10],          # Capricorn -> Aries, Aquarius
    10: [0],             # Aquarius -> Aries
    11: [8, 9],          # Pisces -> Sagittarius, Capricorn
}

# Yoni: animals and their enemies for yoni matching
YONI_ENEMIES: dict[str, str] = {
    "Horse": "Buffalo",
    "Buffalo": "Horse",
    "Elephant": "Lion",
    "Lion": "Elephant",
    "Dog": "Deer",
    "Deer": "Dog",
    "Cat": "Rat",
    "Rat": "Cat",
    "Serpent": "Mongoose",
    "Mongoose": "Serpent",
    "Monkey": "Goat",
    "Goat": "Monkey",
    "Tiger": "Cow",
    "Cow": "Tiger",
}

# Bhakoot: unfavorable sign distances (from boy to girl and girl to boy)
BHAKOOT_NEGATIVE_COMBOS = {
    (2, 12), (12, 2),   # 2/12 axis
    (6, 8), (8, 6),     # 6/8 axis
    (5, 9), (9, 5),     # 5/9 axis (some traditions consider this negative)
}
