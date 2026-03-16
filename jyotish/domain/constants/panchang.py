"""Panchang constants: tithi, karana, yoga, muhurta, and time slots."""

from __future__ import annotations

TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya",
]

KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja",
    "Vanija", "Vishti",  # Repeating karanas
    "Shakuni", "Chatushpada", "Nagava", "Kimstughna",  # Fixed karanas
]

# Panchang Yoga (not planetary yoga)
PANCHANG_YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti",
]

# Muhurta: favorable nakshatras per purpose
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
    0: 8, 1: 2, 2: 7, 3: 5, 4: 6, 5: 4, 6: 3,
}

# Yamaghanda time slots per day
YAMAGHANDA_SLOT: dict[int, int] = {
    0: 5, 1: 4, 2: 3, 3: 2, 4: 1, 5: 7, 6: 6,
}

# Gulika time slots per day
GULIKA_SLOT: dict[int, int] = {
    0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1,
}
