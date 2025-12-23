"""
Sorting utilities for real estate offers.

The `OfferSorter` class provides a single entry point for sorting a list of
offer-like objects (currently plain dictionaries) by various criteria.

Supported sort fields:
- price          – total price of the offer
- price_per_sqm  – price per square meter
- date_added     – date when the offer was added
- area           – area (metrąż)

The implementation is intentionally domain-agnostic and operates on mappings,
to keep it easy to reuse with different data sources and models.
"""
from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Literal, Mapping, Any, Sequence


SortDirection = Literal["asc", "desc"]


class SortField(str, Enum):
    """Supported sort fields for offers."""

    PRICE = "price"
    PRICE_PER_SQM = "price_per_sqm"
    DATE_ADDED = "date_added"
    AREA = "area"


class OfferSorter:
    """Utility class responsible for sorting offer collections."""

    @staticmethod
    def sort_offers(
        offers: Sequence[Mapping[str, Any]],
        sort_by: str | None = None,
        direction: SortDirection = "asc",
    ) -> list[Mapping[str, Any]]:
        """
        Sort a collection of offers by a given criterion.

        The function does not mutate the original list and always returns
        a new list instance.

        If `sort_by` is None or unsupported, the offers are returned unchanged.
        """
        if not offers:
            return []

        # Default behavior for "Najtrafniejsze" – for now, return list unchanged.
        if not sort_by:
            return list(offers)

        try:
            sort_field = SortField(sort_by)
        except ValueError:
            # Unknown sort field – do not attempt to sort.
            return list(offers)

        reverse = direction == "desc"

        return sorted(
            offers,
            key=lambda offer: OfferSorter._build_sort_key(offer, sort_field),
            reverse=reverse,
        )

    @staticmethod
    def _build_sort_key(
        offer: Mapping[str, Any],
        sort_field: SortField,
    ) -> Any:
        """Compute a comparable key used for sorting a single offer."""
        if sort_field is SortField.PRICE:
            return OfferSorter._normalize_price_value(offer.get("price"))

        if sort_field is SortField.PRICE_PER_SQM:
            return OfferSorter._calculate_price_per_sqm(offer)

        if sort_field is SortField.DATE_ADDED:
            return offer.get("date_added")

        if sort_field is SortField.AREA:
            return offer.get("area")

        # Fallback – should not happen with a closed enum, but keeps behavior safe.
        return 0

    @staticmethod
    def _normalize_price_value(value: Any) -> Decimal:
        """
        Normalize a price-like value to Decimal.

        Supports existing Decimal instances and numeric types; missing values
        are treated as zero to keep sorting stable.
        """
        if isinstance(value, Decimal):
            return value

        if value is None:
            return Decimal("0")

        return Decimal(str(value))

    @staticmethod
    def _calculate_price_per_sqm(offer: Mapping[str, Any]) -> Decimal:
        """
        Calculate price per square meter for an offer.

        If the offer already exposes `price_per_sqm`, that value is normalized
        and used directly. Otherwise, it is derived from `price` and `area`.
        """
        direct_value = offer.get("price_per_sqm")
        if direct_value is not None:
            return OfferSorter._normalize_price_value(direct_value)

        total_price = offer.get("price")
        area = offer.get("area")

        if total_price is None or area is None:
            return Decimal("0")

        price_dec = OfferSorter._normalize_price_value(total_price)

        if isinstance(area, Decimal):
            area_dec = area
        else:
            area_dec = Decimal(str(area))

        if area_dec == 0:
            return Decimal("0")

        return price_dec / area_dec


__all__ = ["OfferSorter"]
