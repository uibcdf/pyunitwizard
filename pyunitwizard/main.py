"""Compatibility module that re-exports the public API from :mod:`pyunitwizard.api`."""

from __future__ import annotations

from .api.comparison import (
    are_close,
    are_compatible,
    are_equal,
    compatibility,
    similarity,
)
from .api.construction import quantity, unit
from .api.conversion import convert, to_string
from .api.extraction import change_value, get_unit, get_value, get_value_and_unit
from .api.introspection import (
    get_dimensionality,
    get_form,
    is_dimensionless,
    is_quantity,
    is_unit,
)
from .api.standardization import get_standard_units, standardize
from .api.validation import check

__all__ = [
    "are_close",
    "are_compatible",
    "are_equal",
    "change_value",
    "check",
    "compatibility",
    "convert",
    "get_dimensionality",
    "get_form",
    "get_standard_units",
    "get_unit",
    "get_value",
    "get_value_and_unit",
    "is_dimensionless",
    "is_quantity",
    "is_unit",
    "quantity",
    "similarity",
    "standardize",
    "to_string",
    "unit",
]
