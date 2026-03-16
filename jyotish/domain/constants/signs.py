"""Sign (Rashi) constants."""

from __future__ import annotations

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

# Sign lordships
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

# Varna (caste for matching) based on sign element
SIGN_VARNA = {
    "Water": "Brahmin",    # Cancer, Scorpio, Pisces
    "Fire": "Kshatriya",   # Aries, Leo, Sagittarius
    "Earth": "Vaishya",    # Taurus, Virgo, Capricorn
    "Air": "Shudra",       # Gemini, Libra, Aquarius
}

VARNA_RANK = {"Brahmin": 4, "Kshatriya": 3, "Vaishya": 2, "Shudra": 1}
