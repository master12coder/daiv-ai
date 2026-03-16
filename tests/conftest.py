"""Shared test fixtures."""

import pytest
from jyotish.compute.chart import compute_chart, ChartData


@pytest.fixture
def manish_chart() -> ChartData:
    """Reference chart: Manish Chaurasia — verified data."""
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
    """Generic sample chart for testing."""
    return compute_chart(
        name="Test Person",
        dob="15/08/1990",
        tob="06:30",
        lat=26.9124,
        lon=75.7873,
        tz_name="Asia/Kolkata",
        gender="Male",
    )
