from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.database import get_db
from models.models import Location
from schemas.locations import LocationResponse

router = APIRouter(prefix="/locations")


@router.get(
    "/",
    response_model=list[LocationResponse],
    summary="List locations",
    description="Returns a paginated list of locations.",
)
async def list_locations(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, description="Maximum number of records to return"),
) -> list[LocationResponse]:
    """
    Endpoint returning a paginated list of locations.

    Default pagination: skip=0, limit=100.
    """
    stmt = (
        select(Location)
        .order_by(Location.location_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    locations: list[Location] = list(result.scalars().all())

    return [
        LocationResponse(
            location_id=location.location_id,
            city=location.city,
            locality=location.locality,
            city_district=location.city_district,
            street=location.street,
            full_address=location.full_address,
            latitude=float(location.latitude) if location.latitude is not None else None,
            longitude=float(location.longitude)
            if location.longitude is not None
            else None,
        )
        for location in locations
    ]


@router.get(
    "/{location_id}",
    response_model=LocationResponse,
    summary="Get location details",
    description="Returns full details of a specific location by its ID",
)
async def get_location_details(
    location_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LocationResponse:
    """
    Endpoint returning full details of a single location.

    Raises 404 if location does not exist.
    """
    stmt = select(Location).where(Location.location_id == location_id)
    result = await db.execute(stmt)
    location: Location | None = result.scalar_one_or_none()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return LocationResponse(
        location_id=location.location_id,
        city=location.city,
        locality=location.locality,
        city_district=location.city_district,
        street=location.street,
        full_address=location.full_address,
        latitude=float(location.latitude) if location.latitude is not None else None,
        longitude=float(location.longitude) if location.longitude is not None else None,
    )


