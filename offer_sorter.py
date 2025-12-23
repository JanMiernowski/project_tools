"""
Compatibility wrapper for `OfferSorter`.

Tests import `OfferSorter` from `offer_sorter`, while the implementation
resides in `sorter.py`. This module re-exports the class to keep the tests
simple and focused on behavior.
"""
from __future__ import annotations

from sorter import OfferSorter

__all__ = ["OfferSorter"]


