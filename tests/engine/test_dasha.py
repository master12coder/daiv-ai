"""Test Vimshottari Dasha computation."""

from datetime import datetime

import pytz

from daivai_engine.compute.dasha import (
    compute_antardashas,
    compute_mahadashas,
    find_current_dasha,
)


class TestDashaComputation:
    def test_first_dasha_lord_is_moon(self, manish_chart):
        """Moon in Rohini -> nakshatra lord is Moon -> first dasha is Moon."""
        mds = compute_mahadashas(manish_chart)
        assert mds[0].lord == "Moon"

    def test_dasha_sequence(self, manish_chart):
        """Verify dasha sequence from Moon: Moon→Mars→Rahu→Jupiter→Saturn→Mercury→Ketu→Venus→Sun."""
        mds = compute_mahadashas(manish_chart)
        expected = ["Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun"]
        actual = [md.lord for md in mds]
        assert actual == expected

    def test_nine_mahadashas(self, manish_chart):
        mds = compute_mahadashas(manish_chart)
        assert len(mds) == 9

    def test_current_dasha_march_2026(self, manish_chart):
        """On 15/03/2026, should be in Jupiter Mahadasha."""
        target = pytz.timezone("Asia/Kolkata").localize(datetime(2026, 3, 15))
        md, ad, pd = find_current_dasha(manish_chart, target)
        assert md.lord == "Jupiter"

    def test_dasha_periods_contiguous(self, manish_chart):
        """Each dasha should start where the previous one ended."""
        mds = compute_mahadashas(manish_chart)
        for i in range(1, len(mds)):
            diff = abs((mds[i].start - mds[i - 1].end).total_seconds())
            assert diff < 60, f"Gap between {mds[i - 1].lord} and {mds[i].lord}: {diff}s"

    def test_antardasha_count(self, manish_chart):
        """Each Mahadasha should have 9 Antardashas."""
        mds = compute_mahadashas(manish_chart)
        for md in mds:
            ads = compute_antardashas(md)
            assert len(ads) == 9

    def test_antardasha_starts_with_md_lord(self, manish_chart):
        """First Antardasha should be of the Mahadasha lord."""
        mds = compute_mahadashas(manish_chart)
        for md in mds:
            ads = compute_antardashas(md)
            assert ads[0].lord == md.lord

    def test_first_dasha_is_partial(self, manish_chart):
        """First dasha should be partial (balance of dasha at birth)."""
        mds = compute_mahadashas(manish_chart)
        # Moon dasha is 10 years total. Partial should be less.
        duration_days = (mds[0].end - mds[0].start).days
        assert duration_days < 10 * 365.25  # Less than full 10 years
        assert duration_days > 0  # But positive
