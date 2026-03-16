"""Multi-source validation logic for Pandit Ji corrections."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from jyotish.learn.corrections import PanditCorrection, PanditCorrectionStore


@dataclass
class ValidationResult:
    correction_id: str
    is_valid: bool
    new_status: str
    confidence_delta: float
    source: str
    notes: str


class MultiSourceValidator:
    """Validates corrections against multiple sources.

    Validation sources:
    1. Second pandit opinion
    2. Life event confirmation
    3. Cross-reference with classical texts (manual)
    4. DrikPanchang/computational verification
    """

    def __init__(self, store: PanditCorrectionStore | None = None):
        self._store = store or PanditCorrectionStore()

    def validate_by_second_opinion(
        self,
        correction_id: str,
        second_pandit_agrees: bool,
        pandit_name: str = "",
        notes: str = "",
    ) -> ValidationResult:
        """Validate using a second pandit's opinion."""
        if second_pandit_agrees:
            self._store.update_status(correction_id, "validated", 0.3)
            return ValidationResult(
                correction_id=correction_id,
                is_valid=True,
                new_status="validated",
                confidence_delta=0.3,
                source=f"second_pandit:{pandit_name}",
                notes=notes or "Second pandit agrees",
            )
        else:
            self._store.update_status(correction_id, "disputed", -0.2)
            return ValidationResult(
                correction_id=correction_id,
                is_valid=False,
                new_status="disputed",
                confidence_delta=-0.2,
                source=f"second_pandit:{pandit_name}",
                notes=notes or "Second pandit disagrees",
            )

    def validate_by_life_event(
        self,
        correction_id: str,
        event_matches: bool,
        event_description: str = "",
    ) -> ValidationResult:
        """Validate using a life event confirmation."""
        if event_matches:
            self._store.update_status(correction_id, "validated", 0.3)
            return ValidationResult(
                correction_id=correction_id,
                is_valid=True,
                new_status="validated",
                confidence_delta=0.3,
                source="life_event",
                notes=f"Confirmed by event: {event_description}",
            )
        else:
            self._store.update_status(correction_id, "disputed", -0.2)
            return ValidationResult(
                correction_id=correction_id,
                is_valid=False,
                new_status="disputed",
                confidence_delta=-0.2,
                source="life_event",
                notes=f"Contradicted by event: {event_description}",
            )

    def validate_by_computation(
        self,
        correction_id: str,
        computation_agrees: bool,
        notes: str = "",
    ) -> ValidationResult:
        """Validate using computational verification (DrikPanchang, etc.)."""
        if computation_agrees:
            self._store.update_status(correction_id, "validated", 0.2)
            return ValidationResult(
                correction_id=correction_id,
                is_valid=True,
                new_status="validated",
                confidence_delta=0.2,
                source="computation",
                notes=notes or "Computational verification passed",
            )
        else:
            self._store.update_status(correction_id, "disputed", -0.1)
            return ValidationResult(
                correction_id=correction_id,
                is_valid=False,
                new_status="disputed",
                confidence_delta=-0.1,
                source="computation",
                notes=notes or "Computational verification failed",
            )

    def get_validation_summary(self) -> dict[str, int]:
        """Get a summary of validation status across all corrections."""
        return self._store.get_stats()
