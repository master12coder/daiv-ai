"""Test Pandit Ji correction system."""

import pytest
import tempfile
from pathlib import Path
from jyotish.learn.corrections import PanditCorrection, PanditCorrectionStore


@pytest.fixture
def temp_store():
    """Create a temporary correction store."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield PanditCorrectionStore(data_dir=tmpdir)


class TestPanditCorrections:
    def test_add_and_retrieve_correction(self, temp_store):
        correction = PanditCorrection(
            pandit_name="Test Pandit",
            chart_name="Rajesh",
            category="gemstone",
            ai_said="Wear pukhraj",
            pandit_said="Avoid pukhraj for Mithuna lagna",
            pandit_reasoning="Jupiter is maraka for Mithuna",
            planets_involved=["Jupiter"],
            houses_involved=[7],
            lagna="Mithuna",
        )
        cid = temp_store.add_correction(correction)
        assert len(cid) > 0

        retrieved = temp_store.get_correction(cid)
        assert retrieved is not None
        assert retrieved.pandit_said == "Avoid pukhraj for Mithuna lagna"
        assert retrieved.status == "pending"

    def test_list_corrections(self, temp_store):
        for i in range(3):
            c = PanditCorrection(chart_name=f"Chart {i}", category="gemstone")
            temp_store.add_correction(c)
        results = temp_store.list_corrections()
        assert len(results) == 3

    def test_filter_by_status(self, temp_store):
        c1 = PanditCorrection(chart_name="A", status="pending")
        c2 = PanditCorrection(chart_name="B", status="validated")
        temp_store.add_correction(c1)
        temp_store.add_correction(c2)

        pending = temp_store.list_corrections(status="pending")
        assert len(pending) == 1
        assert pending[0].chart_name == "A"

    def test_validate_correction(self, temp_store):
        c = PanditCorrection(chart_name="Test")
        cid = temp_store.add_correction(c)

        temp_store.validate_correction(cid)
        updated = temp_store.get_correction(cid)
        assert updated.status == "validated"
        assert updated.confidence == 0.3

    def test_dispute_correction(self, temp_store):
        c = PanditCorrection(chart_name="Test", confidence=0.5)
        cid = temp_store.add_correction(c)

        temp_store.dispute_correction(cid)
        updated = temp_store.get_correction(cid)
        assert updated.status == "disputed"
        assert updated.confidence == 0.3  # 0.5 - 0.2

    def test_confidence_bounds(self, temp_store):
        c = PanditCorrection(chart_name="Test", confidence=0.0)
        cid = temp_store.add_correction(c)

        # Disputing below 0 should clamp to 0
        temp_store.dispute_correction(cid)
        updated = temp_store.get_correction(cid)
        assert updated.confidence == 0.0

    def test_get_stats(self, temp_store):
        temp_store.add_correction(PanditCorrection(chart_name="A", status="pending"))
        temp_store.add_correction(PanditCorrection(chart_name="B", status="validated"))
        temp_store.add_correction(PanditCorrection(chart_name="C", status="validated"))

        stats = temp_store.get_stats()
        assert stats["total"] == 3
        assert stats["pending"] == 1
        assert stats["validated"] == 2

    def test_get_relevant_rules(self, temp_store):
        c = PanditCorrection(
            chart_name="Test", lagna="Mithuna",
            category="gemstone", status="validated",
            confidence=0.8,
            planets_involved=["Jupiter"],
            pandit_said="Jupiter is maraka",
        )
        temp_store.add_correction(c)

        rules = temp_store.get_relevant_rules(lagna="Mithuna", category="gemstone")
        assert len(rules) == 1
        assert rules[0].pandit_said == "Jupiter is maraka"

    def test_get_prompt_additions(self, temp_store):
        c = PanditCorrection(
            chart_name="Test", lagna="Mithuna",
            category="gemstone", status="validated",
            confidence=0.8,
            pandit_said="Jupiter is maraka for Mithuna",
            pandit_reasoning="7th lord",
        )
        temp_store.add_correction(c)

        prompt = temp_store.get_prompt_additions(lagna="Mithuna")
        assert "Jupiter is maraka" in prompt
        assert "Pandit Ji" in prompt

    def test_nonexistent_correction(self, temp_store):
        assert temp_store.get_correction("nonexistent") is None
