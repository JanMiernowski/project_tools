from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.database import get_db
from models.models import Location

router = APIRouter(prefix="/locations")


@router.get(
    "/",
    response_model=list[Location],
    summary="List locations",
    description="Returns a paginated list of locations.",
)
async def list_locations(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, description="Maximum number of records to return"),
) -> list[Location]:
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

    return locations


@router.get(
    "/{location_id}",
    response_model=Location,
    summary="Get location details",
    description="Returns full details of a specific location by its ID",
)
async def get_location_details(
    location_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Location:
    """
    Endpoint returning full details of a single location.

    Raises 404 if location does not exist.
    """
    stmt = select(Location).where(Location.location_id == location_id)
    result = await db.execute(stmt)
    location: Location | None = result.scalar_one_or_none()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location


