"""
Tests for offer sorting (User Story 4.3 - Sortowanie).

The tests describe the expected behavior of the `OfferSorter` class:
- Sort by total price (ascending / descending)
- Sort by price per square meter (ascending / descending)
- Sort by date added (newest first)
- Sort by area (ascending / descending)
- Default sort should be "Najtrafniejsze" (best value for money).

These tests work directly on plain offer data structures to support TDD.
They do not introduce any additional mock classes.
"""
from __future__ import annotations

from datetime import date

from offer_sorter import OfferSorter


def create_offers() -> list[dict]:
    """
    Return a deterministic list of offer dicts for sorting tests.

    The keys intentionally match domain concepts from the user story.
    """
    return [
        {
            "id": 1,
            "price": 500_000,
            "price_per_sqm": 10_000,
            "area": 50,
            "date_added": date(2024, 1, 10),
        },
        {
            "id": 2,
            "price": 450_000,
            "price_per_sqm": 9_000,
            "area": 50,
            "date_added": date(2024, 1, 12),
        },
        {
            "id": 3,
            "price": 600_000,
            "price_per_sqm": 8_000,
            "area": 75,
            "date_added": date(2024, 1, 8),
        },
        {
            "id": 4,
            "price": 400_000,
            "price_per_sqm": 12_500,
            "area": 32,
            "date_added": date(2024, 1, 15),
        },
    ]


def test_sort_by_price_ascending() -> None:
    """Offers are sorted by total price in ascending order when requested."""
    offers = create_offers()

    sorted_offers = OfferSorter.sort_offers(
        offers=offers,
        sort_by="price",
        direction="asc",
    )

    assert [offer["id"] for offer in sorted_offers] == [4, 2, 1, 3]


def test_sort_by_price_descending() -> None:
    """Offers are sorted by total price in descending order when requested."""
    offers = create_offers()

    sorted_offers = OfferSorter.sort_offers(
        offers=offers,
        sort_by="price",
        direction="desc",
    )

    assert [offer["id"] for offer in sorted_offers] == [3, 1, 2, 4]


def test_sort_by_price_per_sqm_ascending() -> None:
    """Offers are sorted by price per square meter in ascending order."""
    offers = create_offers()

    sorted_offers = OfferSorter.sort_offers(
        offers=offers,
        sort_by="price_per_sqm",
        direction="asc",
    )

    assert [offer["id"] for offer in sorted_offers] == [3, 2, 1, 4]


def test_sort_by_price_per_sqm_descending() -> None:
    """Offers are sorted by price per square meter in descending order."""
    offers = create_offers()

    sorted_offers = OfferSorter.sort_offers(
        offers=offers,
        sort_by="price_per_sqm",
        direction="desc",
    )

    assert [offer["id"] for offer in sorted_offers] == [4, 1, 2, 3]


def test_sort_by_date_added_newest_first() -> None:
    """Offers are sorted by date added, newest offers first."""
    offers = create_offers()

    sorted_offers = OfferSorter.sort_offers(
        offers=offers,
        sort_by="date_added",
        # By business requirement, date sorting should default to newest first.
        direction="desc",
    )

    # Check that the newest offer (id=4, 2024-01-15) is first and order is correct.
    assert [offer["id"] for offer in sorted_offers] == [4, 2, 1, 3]


def test_sort_by_area_ascending() -> None:
    """Offers are sorted by area (metrąż) in ascending order."""
    offers = create_offers()

    sorted_offers = OfferSorter.sort_offers(
        offers=offers,
        sort_by="area",
        direction="asc",
    )

    assert [offer["id"] for offer in sorted_offers] == [4, 1, 2, 3]


def test_sort_by_area_descending() -> None:
    """Offers are sorted by area (metrąż) in descending order."""
    offers = create_offers()

    sorted_offers = OfferSorter.sort_offers(
        offers=offers,
        sort_by="area",
        direction="desc",
    )

    assert [offer["id"] for offer in sorted_offers] == [3, 1, 2, 4]


def test_default_sort_returns_offers_unchanged() -> None:
    """
    Default sorting is set to "Najtrafniejsze".

    For now the "Najtrafniejsze" behavior is not defined, so the sorter
    should return offers in the original order when no sort_by is provided.
    """
    offers = create_offers()

    sorted_offers = OfferSorter.sort_offers(offers=offers)

    assert [offer["id"] for offer in sorted_offers] == [1, 2, 3, 4]


