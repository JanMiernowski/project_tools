"""
Tests for offers listing endpoint with sorting (User Story 4.4 - Sortowanie w API).

The tests focus on controller behavior using FastAPI test client:
- Accepting query parameters sort_by and order
- Returning offers sorted by total price in descending order
"""
from __future__ import annotations

from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Listing, Location, Building, Owner, Features


@pytest.mark.asyncio
async def test_get_offers_sorted_by_price_desc(
    test_client: AsyncClient,
    test_session_with_commit: AsyncSession,
) -> None:
    """GET /offers?sort_by=price&order=desc returns offers sorted from most expensive."""
    # Arrange: create shared related entities
    location = Location(city="Warszawa")
    building = Building(year_built=2000)
    owner = Owner(owner_type="agency")
    features = Features(has_parking=True)

    test_session_with_commit.add_all([location, building, owner, features])
    await test_session_with_commit.commit()

    # Reload to get primary keys
    await test_session_with_commit.refresh(location)
    await test_session_with_commit.refresh(building)
    await test_session_with_commit.refresh(owner)
    await test_session_with_commit.refresh(features)

    # Arrange: create listings with different total prices
    listings = [
        Listing(
            location_id=location.location_id,
            building_id=building.building_id,
            owner_id=owner.owner_id,
            features_id=features.features_id,
            area=Decimal("50.0"),
            price_total_zl=Decimal("500000"),
            price_sqm_zl=Decimal("10000"),
        ),
        Listing(
            location_id=location.location_id,
            building_id=building.building_id,
            owner_id=owner.owner_id,
            features_id=features.features_id,
            area=Decimal("60.0"),
            price_total_zl=Decimal("600000"),
            price_sqm_zl=Decimal("10000"),
        ),
        Listing(
            location_id=location.location_id,
            building_id=building.building_id,
            owner_id=owner.owner_id,
            features_id=features.features_id,
            area=Decimal("40.0"),
            price_total_zl=Decimal("400000"),
            price_sqm_zl=Decimal("10000"),
        ),
    ]

    test_session_with_commit.add_all(listings)
    await test_session_with_commit.commit()

    # Act: call the endpoint with sorting parameters
    response = await test_client.get("/offers?sort_by=price&order=desc")

    # Assert: endpoint returns 200 and offers sorted from most to least expensive
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

    prices = [Decimal(item["price_total_zl"]) for item in data]
    assert prices == sorted(prices, reverse=True)


