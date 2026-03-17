"""Shared test fixtures — all tests import from here."""
from __future__ import annotations

import pytest

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.models.chart import ChartData


@pytest.fixture
def manish_chart() -> ChartData:
    """Reference chart: Manish Chaurasia — verified data.

    Known values:
        Lagna = Mithuna (Gemini)
        Moon = Rohini Pada 2
        Jupiter = maraka (7th lord)
        Mercury = lagnesh
        Current MD = Jupiter (maraka)
    """
    return compute_chart(
        name="Manish Chaurasia",
        dob="13/03/1989",
        tob="12:17",
        lat=25.3176,
        lon=83.0067,
        tz_name="Asia/Kolkata",
        gender="Male",
    )


@pytest.fixture
def sample_chart() -> ChartData:
    """Secondary test chart for cross-validation."""
    return compute_chart(
        name="Test Person",
        dob="01/01/2000",
        tob="06:00",
        lat=28.6139,
        lon=77.2090,
        tz_name="Asia/Kolkata",
        gender="Female",
    )
