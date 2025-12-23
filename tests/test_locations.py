"""
Tests for location details endpoint.
"""
from decimal import Decimal
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Location


@pytest.mark.asyncio
async def test_get_location_details_success(
    test_client: AsyncClient,
    test_session_with_commit: AsyncSession,
) -> None:
    """Endpoint GET /locations/{location_id} returns location details for existing location."""
    # Arrange: create a sample location in the test database
    location = Location(
        city="Warszawa",
        locality="Śródmieście",
        city_district="Śródmieście Północne",
        street="Marszałkowska",
        full_address="Marszałkowska 1, 00-001 Warszawa",
        latitude=Decimal("52.2297"),
        longitude=Decimal("21.0122"),
    )
    test_session_with_commit.add(location)
    await test_session_with_commit.commit()
    await test_session_with_commit.refresh(location)

    # Act: call the endpoint
    response = await test_client.get(f"/locations/{location.location_id}")

    # Assert: endpoint returns 200 and correct data
    assert response.status_code == 200

    data = response.json()

    # Check presence of all required fields
    expected_fields = {
        "location_id",
        "city",
        "locality",
        "city_district",
        "street",
        "full_address",
        "latitude",
        "longitude",
    }
    assert set(data.keys()) == expected_fields

    # Check values
    assert data["location_id"] == location.location_id
    assert data["city"] == location.city
    assert data["locality"] == location.locality
    assert data["city_district"] == location.city_district
    assert data["street"] == location.street
    assert data["full_address"] == location.full_address
    # SQLModel serializes Decimal as string in JSON, convert for comparison
    assert abs(float(location.latitude) - float(data["latitude"])) < 1e-6
    assert abs(float(location.longitude) - float(data["longitude"])) < 1e-6


@pytest.mark.asyncio
async def test_get_location_details_not_found(
    test_client: AsyncClient,
) -> None:
    """Endpoint returns 404 when location does not exist."""
    # Act: call the endpoint with non-existing ID
    non_existing_id = 999999
    response = await test_client.get(f"/locations/{non_existing_id}")

    # Assert: 404 with proper error message
    assert response.status_code == 404

    data = response.json()
    # Standard FastAPI HTTPException shape: {"detail": "..."}
    assert "detail" in data
    assert data["detail"] == "Location not found"

@pytest.mark.asyncio
async def test_list_locations_returns_all_fields(
    test_client: AsyncClient,
    test_session_with_commit: AsyncSession,
) -> None:
    """Endpoint GET /locations/ returns list of locations with all fields."""
    # Arrange: create a few sample locations
    locations = [
        Location(
            city="Warszawa",
            locality="Śródmieście",
            city_district="Śródmieście Północne",
            street="Marszałkowska",
            full_address="Marszałkowska 1, 00-001 Warszawa",
            latitude=52.2297,
            longitude=21.0122,
        ),
        Location(
            city="Kraków",
            locality="Stare Miasto",
            city_district="Śródmieście",
            street="Floriańska",
            full_address="Floriańska 1, 31-019 Kraków",
            latitude=50.0647,
            longitude=19.945,
        ),
    ]
    test_session_with_commit.add_all(locations)
    await test_session_with_commit.commit()

    # Act: call the endpoint without parameters
    response = await test_client.get("/locations/")

    # Assert: endpoint returns 200 and list of locations
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(locations)

    # Check presence of all required fields for each location
    expected_fields = {
        "location_id",
        "city",
        "locality",
        "city_district",
        "street",
        "full_address",
        "latitude",
        "longitude",
    }

    for item in data:
        assert set(item.keys()) == expected_fields


@pytest.mark.asyncio
async def test_list_locations_default_pagination_limit_100(
    test_client: AsyncClient,
    test_session_with_commit: AsyncSession,
) -> None:
    """Endpoint GET /locations/ returns at most 100 locations by default."""
    # Arrange: create more than 100 locations
    locations = [
        Location(
            city=f"City {i}",
            locality=f"Locality {i}",
            city_district=f"District {i}",
            street=f"Street {i}",
            full_address=f"Street {i} 1",
            latitude=50.0 + i * 0.01,
            longitude=20.0 + i * 0.01,
        )
        for i in range(150)
    ]
    test_session_with_commit.add_all(locations)
    await test_session_with_commit.commit()

    # Act: call the endpoint without limit parameter
    response = await test_client.get("/locations/")

    # Assert: only 100 locations are returned
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100


@pytest.mark.asyncio
async def test_list_locations_skip_and_limit(
    test_client: AsyncClient,
    test_session_with_commit: AsyncSession,
) -> None:
    """Endpoint GET /locations/ supports skip and limit parameters for pagination."""
    # Arrange: create a few locations with predictable order
    locations = [
        Location(
            city=f"City {i}",
            locality=f"Locality {i}",
            city_district=f"District {i}",
            street=f"Street {i}",
            full_address=f"Street {i} 1",
            latitude=50.0 + i * 0.01,
            longitude=20.0 + i * 0.01,
        )
        for i in range(10)
    ]
    test_session_with_commit.add_all(locations)
    await test_session_with_commit.commit()
    for i in range(4):
        await test_session_with_commit.refresh(locations[i])

    # Act: skip first 2 and take next 2
    response = await test_client.get("/locations/?skip=2&limit=2")

    # Assert
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    # Ensure pagination is consistent with insertion order (by primary key)
    returned_ids = [item["location_id"] for item in data]
    assert returned_ids == [
        locations[2].location_id,
        locations[3].location_id,
    ]
