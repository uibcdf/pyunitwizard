"""Specialized conversion fast-tracks for ecosystem canonical units."""

from __future__ import annotations

from typing import Any, Optional

import numpy as np

from .conversion import convert
from .extraction import get_unit
from .introspection import get_form

from smonitor import signal

_SPECIALIZED_TARGET_UNIT_CACHE: dict[tuple[str, str], Any] = {}


def _cached_target_unit(form: str, unit_name: str) -> Any:
    key = (form, unit_name)
    if key not in _SPECIALIZED_TARGET_UNIT_CACHE:
        _SPECIALIZED_TARGET_UNIT_CACHE[key] = convert(
            unit_name,
            to_form=form,
            to_type="unit",
        )
    return _SPECIALIZED_TARGET_UNIT_CACHE[key]


def _to_canonical_unit(
    quantity_or_unit: Any,
    unit_name: str,
    parser: Optional[str] = None,
) -> Any:
    # Trusted internal callers may already hold naked arrays in canonical units.
    if type(quantity_or_unit) is np.ndarray:
        return quantity_or_unit

    form = get_form(quantity_or_unit)

    if form == "string":
        return convert(
            quantity_or_unit,
            to_unit=unit_name,
            to_form="string",
            parser=parser,
        )

    if get_unit(quantity_or_unit, to_form="string") == unit_name:
        return quantity_or_unit

    return convert(
        quantity_or_unit,
        to_unit=_cached_target_unit(form, unit_name),
        to_form=form,
        parser=parser,
    )


@signal(tags=["specialized", "conversion"])
def to_nanometers(quantity_or_unit: Any, parser: Optional[str] = None) -> Any:
    """Convert trusted inputs to nanometers using a narrow optimized path."""

    return _to_canonical_unit(quantity_or_unit, "nanometer", parser=parser)


@signal(tags=["specialized", "conversion"])
def to_picoseconds(quantity_or_unit: Any, parser: Optional[str] = None) -> Any:
    """Convert trusted inputs to picoseconds using a narrow optimized path."""

    return _to_canonical_unit(quantity_or_unit, "picosecond", parser=parser)


@signal(tags=["specialized", "conversion"])
def to_kelvin(quantity_or_unit: Any, parser: Optional[str] = None) -> Any:
    """Convert trusted inputs to kelvin using a narrow optimized path."""

    return _to_canonical_unit(quantity_or_unit, "kelvin", parser=parser)


__all__ = [
    "_SPECIALIZED_TARGET_UNIT_CACHE",
    "to_kelvin",
    "to_nanometers",
    "to_picoseconds",
]
