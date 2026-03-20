"""Avakhada Chakra computation — 18 classical birth qualities.

Computes the complete Avakhada Chakra from a pre-computed birth chart.
All values are derived from the Moon's nakshatra, pada, and sign, plus
the lagna and panchang data already embedded in ChartData.

Sources:
  - Brihat Parasara Hora Shastra (gana, nadi, nakshatra lords)
  - Classical Jyotish matching texts (Paya, Tatva, Yunja, Vashya)
  - Paya method verified: Rohini(4) → 4%4=0 → Iron ✓ (InstaAstro cross-check)
  - Tatva verified: Rohini Pada 2 → Earth ✓ (InstaAstro cross-check)
"""

from __future__ import annotations

from daivai_engine.constants import (
    KARANA_NAMES,
    NAKSHATRA_ANIMALS,
    NAKSHATRA_GANAS,
    NAKSHATRA_LORDS,
    NAKSHATRA_NADIS,
    SIGN_ELEMENTS,
    SIGN_LORDS,
    SIGN_VARNA,
    TITHI_NAMES,
)
from daivai_engine.models.avakhada import AvakhadaChakra
from daivai_engine.models.chart import ChartData


# ---------------------------------------------------------------------------
# Name alphabet table: [nakshatra_index (0-26)][pada_index (0-3)] = syllable
# Source: Standard Vedic naming convention (108 padas x 1 syllable each)
# Verified: Rohini (index 3), pada 2 → index 1 → "Va" ✓
# ---------------------------------------------------------------------------
_NAME_ALPHABETS: list[list[str]] = [
    ["Chu", "Che", "Cho", "La"],      # 0 Ashwini
    ["Li", "Lu", "Le", "Lo"],          # 1 Bharani
    ["A", "I", "U", "E"],              # 2 Krittika
    ["O", "Va", "Vi", "Vu"],           # 3 Rohini
    ["Ve", "Vo", "Ka", "Ki"],          # 4 Mrigashira
    ["Ku", "Gha", "Na", "Cha"],        # 5 Ardra
    ["Ke", "Ko", "Ha", "Hi"],          # 6 Punarvasu
    ["Hu", "He", "Ho", "Da"],          # 7 Pushya
    ["Di", "Du", "De", "Do"],          # 8 Ashlesha
    ["Ma", "Mi", "Mu", "Me"],          # 9 Magha
    ["Mo", "Ta", "Ti", "Tu"],          # 10 Purva Phalguni
    ["Te", "To", "Pa", "Pi"],          # 11 Uttara Phalguni
    ["Pu", "Sha", "Na", "Tha"],        # 12 Hasta
    ["Pe", "Po", "Ra", "Ri"],          # 13 Chitra
    ["Ru", "Re", "Ro", "Ta"],          # 14 Swati
    ["Ti", "Tu", "Te", "To"],          # 15 Vishakha
    ["Na", "Ni", "Nu", "Ne"],          # 16 Anuradha
    ["No", "Ya", "Yi", "Yu"],          # 17 Jyeshtha
    ["Ye", "Yo", "Bha", "Bhi"],        # 18 Moola
    ["Bhu", "Dha", "Pha", "Da"],       # 19 Purva Ashadha
    ["Be", "Bo", "Ja", "Ji"],          # 20 Uttara Ashadha
    ["Khi", "Khu", "Khe", "Kho"],      # 21 Shravana
    ["Ga", "Gi", "Gu", "Ge"],          # 22 Dhanishta
    ["Go", "Sa", "Si", "Su"],          # 23 Shatabhisha
    ["Se", "So", "Da", "Di"],          # 24 Purva Bhadrapada
    ["Du", "Tha", "Jha", "Na"],        # 25 Uttara Bhadrapada
    ["De", "Do", "Cha", "Chi"],        # 26 Revati
]

# Vashya (creature type) per sign index (0 = Aries … 11 = Pisces)
_VASHYA: list[str] = [
    "Chatushpad",   # 0  Mesha (Aries)
    "Chatushpad",   # 1  Vrishabha (Taurus)
    "Manav",        # 2  Mithuna (Gemini)
    "Jalachara",    # 3  Karka (Cancer)
    "Vanchar",      # 4  Simha (Leo)
    "Manav",        # 5  Kanya (Virgo)
    "Manav",        # 6  Tula (Libra)
    "Keet",         # 7  Vrischika (Scorpio)
    "Chatushpad",   # 8  Dhanu (Sagittarius)
    "Chatushpad",   # 9  Makara (Capricorn)
    "Manav",        # 10 Kumbha (Aquarius)
    "Jalachara",    # 11 Meena (Pisces)
]

# Paya: nakshatra_number (1-indexed) % 4  →  metal
_PAYA_MAP: dict[int, str] = {
    0: "Iron",    # Rohini(4), Pushya(8), Chitra(14), Vishakha(16), ...
    1: "Gold",    # Ashwini(1), Mrigashira(5), Magha(10), ...
    2: "Silver",  # Bharani(2), Ardra(6), Purva Phalguni(11), ...
    3: "Copper",  # Krittika(3), Punarvasu(7), Uttara Phalguni(12), ...
}

# Tatva: pada (1-4)  →  element
_TATVA_MAP: dict[int, str] = {
    1: "Fire",   # Dharma pada
    2: "Earth",  # Artha pada
    3: "Air",    # Kama pada
    4: "Water",  # Moksha pada
}


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _paya(nakshatra_number: int) -> str:
    """Paya from 1-indexed nakshatra number via cyclical mod-4 method.

    Verified: Rohini = 4 → 4 % 4 = 0 → Iron (matches InstaAstro).
    """
    return _PAYA_MAP[nakshatra_number % 4]


def _tatva(pada: int) -> str:
    """Tatva from pada (1-4): Pada 1=Fire, 2=Earth, 3=Air, 4=Water."""
    return _TATVA_MAP[pada]


def _yunja(nakshatra_number: int) -> str:
    """Yunja group from 1-indexed nakshatra number.

    Poorva: 1-9  | Madhya: 10-18  | Uttara: 19-27
    """
    if nakshatra_number <= 9:
        return "Poorva"
    if nakshatra_number <= 18:
        return "Madhya"
    return "Uttara"


def _tithi_karan(chart: ChartData) -> tuple[str, str]:
    """Extract Tithi and Karana from the chart's Sun/Moon longitudes."""
    moon_lon = chart.planets["Moon"].longitude
    sun_lon = chart.planets["Sun"].longitude

    diff = (moon_lon - sun_lon) % 360.0
    tithi_idx = min(int(diff / 12.0), 29)
    tithi = TITHI_NAMES[tithi_idx]

    karan_idx = int(diff / 6.0) % 11
    karan = KARANA_NAMES[karan_idx]

    return tithi, karan


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def compute_avakhada(chart: ChartData) -> AvakhadaChakra:
    """Compute the complete Avakhada Chakra for a birth chart.

    Derives all 18 classical birth qualities from the Moon's nakshatra,
    pada, and sign, together with the lagna and panchang information
    already stored in the pre-computed ChartData.

    Args:
        chart: Pre-computed birth chart with planetary positions.

    Returns:
        AvakhadaChakra containing all 18 classical qualities.

    Example (Manish Chaurasia — verified against InstaAstro):
        nakshatra    = Rohini          nakshatra_lord = Moon
        sign         = Vrishabha       sign_lord      = Venus
        charan       = 2               tatva          = Earth
        paya         = Iron            yunja          = Poorva
        gan          = Manushya        nadi           = Madhya
        yoni         = Serpent         varna          = Vaishya
        vashya       = Chatushpad      name_alphabet  = Va
        ascendant    = Mithuna         ascendant_lord = Mercury
    """
    moon = chart.planets["Moon"]

    # 0-indexed nakshatra index and 1-indexed number
    nak_idx: int = moon.nakshatra_index   # 0-26
    nak_num: int = nak_idx + 1            # 1-27
    pada: int = moon.pada                 # 1-4

    tithi, karan = _tithi_karan(chart)

    moon_sign_idx = moon.sign_index
    moon_element = SIGN_ELEMENTS[moon_sign_idx]

    lagna_idx = chart.lagna_sign_index

    return AvakhadaChakra(
        # Nakshatra
        nakshatra=moon.nakshatra,
        nakshatra_lord=NAKSHATRA_LORDS[nak_idx],
        nakshatra_number=nak_num,
        # Moon sign
        sign=moon.sign,
        sign_lord=SIGN_LORDS[moon_sign_idx],
        # Pada
        charan=pada,
        # Derived qualities
        tatva=_tatva(pada),
        paya=_paya(nak_num),
        yunja=_yunja(nak_num),
        # Nakshatra-based qualities
        gan=NAKSHATRA_GANAS[nak_idx],
        nadi=NAKSHATRA_NADIS[nak_idx],
        yoni=NAKSHATRA_ANIMALS[nak_idx],
        varna=SIGN_VARNA[moon_element],
        vashya=_VASHYA[moon_sign_idx],
        # Panchang
        tithi=tithi,
        karan=karan,
        # Lagna
        ascendant=chart.lagna_sign,
        ascendant_lord=SIGN_LORDS[lagna_idx],
        # Name
        name_alphabet=_NAME_ALPHABETS[nak_idx][pada - 1],
    )
