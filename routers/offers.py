from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from models.database import get_db
from models.models import Listing


router = APIRouter()


def apply_ordering(
    stmt: Select,
    sort_by: str | None,
    order: str | None,
) -> Select:
    """
    Apply dynamic ORDER BY clause based on allowed sort fields.

    Currently supported:
    - sort_by=price (mapped to Listing.price_total_zl)
    - order=asc|desc (default: desc)
    """
    if not sort_by:
        return stmt

    # Whitelist of sortable fields
    sortable_fields: dict[str, object] = {
        "price": Listing.price_total_zl,
    }

    sort_column = sortable_fields.get(sort_by)
    if sort_column is None:
        # Unsupported sort field -> return statement unchanged
        return stmt

    sort_order = (order or "desc").lower()
    if sort_order == "asc":
        return stmt.order_by(sort_column.asc())

    # Default to descending order
    return stmt.order_by(sort_column.desc())


@router.get(
    "/offers",
    response_model=list[Listing],
    summary="List offers",
    description="Returns a list of offers with optional sorting.",
)
async def list_offers(
    db: Annotated[AsyncSession, Depends(get_db)],
    sort_by: str | None = Query(
        default=None,
        description="Sort field (currently supported: 'price').",
    ),
    order: str | None = Query(
        default=None,
        description="Sort order: 'asc' or 'desc' (default: 'desc').",
    ),
) -> list[Listing]:
    """
    Endpoint returning a list of offers (listings) with optional sorting.

    Sorting is controlled by:
    - sort_by: logical field name (e.g. 'price')
    - order: 'asc' or 'desc' (default: 'desc')
    """
    stmt = select(Listing)
    stmt = apply_ordering(stmt, sort_by=sort_by, order=order)

    result = await db.execute(stmt)
    offers: list[Listing] = list(result.scalars().all())

    return offers

