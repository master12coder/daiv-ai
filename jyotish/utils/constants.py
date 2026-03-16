"""All astrological constants in one place."""

from __future__ import annotations

# ── Signs (Rashis) ──────────────────────────────────────────────────────────
SIGNS = [
    "Mesha", "Vrishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrischika",
    "Dhanu", "Makara", "Kumbha", "Meena",
]

SIGNS_EN = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGNS_HI = [
    "मेष", "वृषभ", "मिथुन", "कर्क",
    "सिंह", "कन्या", "तुला", "वृश्चिक",
    "धनु", "मकर", "कुम्भ", "मीन",
]

# Element per sign index
SIGN_ELEMENTS = [
    "Fire", "Earth", "Air", "Water",
    "Fire", "Earth", "Air", "Water",
    "Fire", "Earth", "Air", "Water",
]

# ── Planets (Grahas) ───────────────────────────────────────────────────────
PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

PLANETS_HI = [
    "सूर्य", "चन्द्र", "मंगल", "बुध",
    "बृहस्पति", "शुक्र", "शनि", "राहु", "केतु",
]

# Swiss Ephemeris planet indices
import swisseph as swe
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

# ── Sign Lordships ─────────────────────────────────────────────────────────
SIGN_LORDS = {
    0: "Mars",       # Mesha / Aries
    1: "Venus",      # Vrishabha / Taurus
    2: "Mercury",    # Mithuna / Gemini
    3: "Moon",       # Karka / Cancer
    4: "Sun",        # Simha / Leo
    5: "Mercury",    # Kanya / Virgo
    6: "Venus",      # Tula / Libra
    7: "Mars",       # Vrischika / Scorpio
    8: "Jupiter",    # Dhanu / Sagittarius
    9: "Saturn",     # Makara / Capricorn
    10: "Saturn",    # Kumbha / Aquarius
    11: "Jupiter",   # Meena / Pisces
}

# ── Nakshatras ─────────────────────────────────────────────────────────────
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Moola", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

NAKSHATRAS_HI = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा",
    "आर्द्रा", "पुनर्वसु", "पुष्य", "अश्लेषा", "मघा",
    "पूर्वा फाल्गुनी", "उत्तरा फाल्गुनी", "हस्त", "चित्रा", "स्वाती",
    "विशाखा", "अनुराधा", "ज्येष्ठा", "मूला", "पूर्वाषाढ़ा",
    "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वा भाद्रपद",
    "उत्तरा भाद्रपद", "रेवती",
]

# Nakshatra lords (Vimshottari dasha sequence)
NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu",
    "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury", "Ketu", "Venus",
    "Sun", "Moon", "Mars", "Rahu", "Jupiter",
    "Saturn", "Mercury",
]

# Nakshatra ganas: D=Deva, M=Manushya, R=Rakshasa
NAKSHATRA_GANAS = [
    "Deva", "Manushya", "Rakshasa", "Manushya", "Deva",
    "Manushya", "Deva", "Deva", "Rakshasa", "Rakshasa",
    "Manushya", "Manushya", "Deva", "Rakshasa", "Deva",
    "Rakshasa", "Deva", "Rakshasa", "Rakshasa", "Manushya",
    "Manushya", "Deva", "Rakshasa", "Rakshasa", "Manushya",
    "Manushya", "Deva",
]

# Nakshatra animals for Yoni matching (14 animal types)
NAKSHATRA_ANIMALS = [
    "Horse", "Elephant", "Goat", "Serpent", "Serpent",
    "Dog", "Cat", "Goat", "Cat", "Rat",
    "Rat", "Cow", "Buffalo", "Tiger", "Buffalo",
    "Tiger", "Deer", "Deer", "Dog", "Monkey",
    "Mongoose", "Monkey", "Lion", "Horse", "Lion",
    "Cow", "Elephant",
]

# Nakshatra Nadi: Aadi(A), Madhya(M), Antya(N)
NAKSHATRA_NADIS = [
    "Aadi", "Aadi", "Aadi", "Madhya", "Madhya",
    "Madhya", "Antya", "Antya", "Antya", "Aadi",
    "Aadi", "Aadi", "Madhya", "Madhya", "Madhya",
    "Antya", "Antya", "Antya", "Aadi", "Aadi",
    "Aadi", "Madhya", "Madhya", "Madhya", "Antya",
    "Antya", "Antya",
]

# ── Vimshottari Dasha ──────────────────────────────────────────────────────
DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

DASHA_YEARS: dict[str, int] = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

DASHA_TOTAL_YEARS = 120

# ── Dignity ────────────────────────────────────────────────────────────────
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

# ── Planetary Friendships ──────────────────────────────────────────────────
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

# ── Combustion Limits (degrees from Sun) ──────────────────────────────────
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

# ── Special Aspects ────────────────────────────────────────────────────────
# Standard aspect: every planet aspects the 7th house from its position
# Special (additional) aspects:
SPECIAL_ASPECTS: dict[str, list[int]] = {
    "Mars": [4, 8],       # 4th and 8th house aspects (in addition to 7th)
    "Jupiter": [5, 9],    # 5th and 9th house aspects
    "Saturn": [3, 10],    # 3rd and 10th house aspects
    "Rahu": [5, 9],       # Same as Jupiter
    "Ketu": [5, 9],       # Same as Jupiter
}

# ── Houses ─────────────────────────────────────────────────────────────────
KENDRAS = [1, 4, 7, 10]        # Quadrants
TRIKONAS = [1, 5, 9]           # Trines
DUSTHANAS = [6, 8, 12]         # Malefic houses
UPACHAYAS = [3, 6, 10, 11]     # Growth houses
MARAKAS = [2, 7]               # Death-inflicting houses
TRISHADAYAS = [3, 6, 11]       # Houses of effort

# ── Avastha (Planetary Age States) ─────────────────────────────────────────
# Based on degree range in odd/even signs
AVASTHAS = ["Bala", "Kumara", "Yuva", "Vriddha", "Mruta"]

# ── Varna (Caste for matching) ─────────────────────────────────────────────
# Based on sign element
SIGN_VARNA = {
    "Water": "Brahmin",    # Cancer, Scorpio, Pisces
    "Fire": "Kshatriya",   # Aries, Leo, Sagittarius
    "Earth": "Vaishya",    # Taurus, Virgo, Capricorn
    "Air": "Shudra",       # Gemini, Libra, Aquarius
}

VARNA_RANK = {"Brahmin": 4, "Kshatriya": 3, "Vaishya": 2, "Shudra": 1}

# ── Vasya (Compatibility) ──────────────────────────────────────────────────
# sign_index -> list of sign_indices that are vasya to it
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

# ── Yoni Compatibility ─────────────────────────────────────────────────────
# Animals and their enemies for yoni matching
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

# ── Bhakoot (Moon sign distance) ───────────────────────────────────────────
# Unfavorable sign distances (from boy to girl and girl to boy)
BHAKOOT_NEGATIVE_COMBOS = {
    (2, 12), (12, 2),   # 2/12 axis
    (6, 8), (8, 6),     # 6/8 axis
    (5, 9), (9, 5),     # 5/9 axis (some traditions consider this negative)
}

# ── Day-Planet Mapping ─────────────────────────────────────────────────────
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
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
}

DAY_NAMES_HI = {
    0: "रविवार",
    1: "सोमवार",
    2: "मंगलवार",
    3: "बुधवार",
    4: "गुरुवार",
    5: "शुक्रवार",
    6: "शनिवार",
}

# ── Tithi Names ────────────────────────────────────────────────────────────
TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya",
]

# ── Karana Names ───────────────────────────────────────────────────────────
KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja",
    "Vanija", "Vishti",  # Repeating karanas
    "Shakuni", "Chatushpada", "Nagava", "Kimstughna",  # Fixed karanas
]

# ── Yoga Names (Panchang Yoga, not planetary yoga) ─────────────────────────
PANCHANG_YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti",
]

# ── Muhurta: Favorable nakshatras per purpose ─────────────────────────────
MUHURTA_FAVORABLE_NAKSHATRAS: dict[str, list[str]] = {
    "marriage": [
        "Rohini", "Mrigashira", "Magha", "Uttara Phalguni", "Hasta",
        "Swati", "Anuradha", "Moola", "Uttara Ashadha", "Shravana",
        "Dhanishta", "Uttara Bhadrapada", "Revati",
    ],
    "business": [
        "Ashwini", "Rohini", "Punarvasu", "Pushya", "Hasta",
        "Chitra", "Swati", "Anuradha", "Shravana", "Dhanishta", "Revati",
    ],
    "travel": [
        "Ashwini", "Mrigashira", "Punarvasu", "Pushya", "Hasta",
        "Anuradha", "Shravana", "Revati",
    ],
    "property": [
        "Rohini", "Uttara Phalguni", "Uttara Ashadha",
        "Uttara Bhadrapada", "Pushya", "Shravana",
    ],
}

# Rahu Kaal time slots per day (eighths of day from sunrise)
# Day index (0=Sun..6=Sat) -> which eighth of daylight is Rahu Kaal
RAHU_KAAL_SLOT: dict[int, int] = {
    0: 8,   # Sunday: 8th slot
    1: 2,   # Monday: 2nd slot
    2: 7,   # Tuesday: 7th slot
    3: 5,   # Wednesday: 5th slot
    4: 6,   # Thursday: 6th slot
    5: 4,   # Friday: 4th slot
    6: 3,   # Saturday: 3rd slot
}

# Yamaghanda time slots per day
YAMAGHANDA_SLOT: dict[int, int] = {
    0: 5,   # Sunday
    1: 4,   # Monday
    2: 3,   # Tuesday
    3: 2,   # Wednesday
    4: 1,   # Thursday
    5: 7,   # Friday
    6: 6,   # Saturday
}

# Gulika time slots per day
GULIKA_SLOT: dict[int, int] = {
    0: 7,   # Sunday
    1: 6,   # Monday
    2: 5,   # Tuesday
    3: 4,   # Wednesday
    4: 3,   # Thursday
    5: 2,   # Friday
    6: 1,   # Saturday
}
