"""Provenance — source citation and reasoning for every computation.

Every result in DaivAI must carry its own proof: what text it comes from,
what formula was used, what alternatives exist, and what would invalidate it.

When a Pandit questions any result, this provenance answers:
1. WHAT: The specific rule or formula applied
2. WHY: The classical text and verse that prescribes it
3. HOW: The exact computation with input values
4. ALTERNATIVES: Other texts that interpret this differently
5. INVALIDATION: What conditions would make this result wrong
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class SourceCitation(BaseModel):
    """Reference to a classical text."""

    model_config = ConfigDict(frozen=True)

    text: str  # "BPHS", "Phaladeepika", "Surya Siddhanta", "Jaimini Sutras"
    chapter: str  # "Chapter 46", "Ch.7 v12"
    verse: str | None = None  # Specific verse if known
    topic: str  # "Kalachakra Dasha", "Gajakesari Yoga"


class ComputationProof(BaseModel):
    """Self-contained proof for any computation result.

    This is the 'courtroom exhibit' — when a Pandit questions the result,
    this object contains everything needed to defend or revise it.
    """

    model_config = ConfigDict(frozen=True)

    # WHAT: The rule applied
    rule: str  # "Jupiter in kendra (1/4/7/10) from Moon = Gajakesari"

    # WHY: Classical source
    sources: list[SourceCitation]  # Primary + supporting sources

    # HOW: The exact computation
    computation: str  # "Jupiter sign=1(Taurus), Moon sign=1(Taurus), distance=1 (kendra)"

    # ALTERNATIVES: Other interpretations that exist
    alternatives: list[str]  # ["Some texts require Jupiter to be unafflicted"]

    # INVALIDATION: What would make this wrong
    invalidation: list[str]  # ["If Jupiter is combust, some texts cancel this yoga"]

    # CONFIDENCE: How sure we are
    confidence: str  # "high" (BPHS explicit), "medium" (interpretation), "low" (debated)


# ── Pre-built citations for common sources ────────────────────────────────

BPHS = "Brihat Parashara Hora Shastra"
PHALA = "Phaladeepika"
SURYA = "Surya Siddhanta"
JAIMINI = "Jaimini Upadesa Sutras"
SARAVALI = "Saravali"
MUHURTA_CHINTAMANI = "Muhurta Chintamani"


def cite_bphs(chapter: str, topic: str, verse: str | None = None) -> SourceCitation:
    """Create a BPHS citation."""
    return SourceCitation(text=BPHS, chapter=chapter, verse=verse, topic=topic)


def cite_phala(chapter: str, topic: str, verse: str | None = None) -> SourceCitation:
    """Create a Phaladeepika citation."""
    return SourceCitation(text=PHALA, chapter=chapter, verse=verse, topic=topic)
