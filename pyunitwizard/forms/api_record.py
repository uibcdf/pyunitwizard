"""Adapter for the ``record`` form: PyUnitWizard's inert interchange form.

Every function reads through :class:`pyunitwizard.record.QuantityRecord`, which verifies
the record; computations go through pint and come back as a new, sealed record. See
``pyunitwizard/record.py`` and uibcdf/pyunitwizard#82.
"""

from typing import Any, Dict, Union

import numpy as np

from pyunitwizard._private.quantity_or_unit import ArrayLike
from pyunitwizard.record import QuantityRecord, _canonical_name, _registry

form_name = "record"
parser = False


def _unit_name(unit: Any) -> str:
    return unit if isinstance(unit, str) else _canonical_name(unit)


def is_form(quantity_or_unit: Any) -> bool:
    """``True`` for a :class:`QuantityRecord`."""
    return isinstance(quantity_or_unit, QuantityRecord)


def is_quantity(quantity_or_unit: Any) -> bool:
    """A record always holds a quantity."""
    return isinstance(quantity_or_unit, QuantityRecord)


def is_unit(quantity_or_unit: Any) -> bool:
    """Records hold quantities; there are no unit-only records."""
    return False


def dimensionality(quantity_or_unit: QuantityRecord) -> Dict[str, int]:
    """Dimensionality in PyUnitWizard notation."""
    from .api_pint import dimensionality as _pint_dimensionality

    return _pint_dimensionality(quantity_or_unit.to_quantity(form="pint"))


def compatibility(quantity_or_unit_1: QuantityRecord, quantity_or_unit_2: Any) -> bool:
    """Two records are compatible when their SI dimensions agree."""
    if isinstance(quantity_or_unit_2, QuantityRecord):
        return quantity_or_unit_1.si["exponents"] == quantity_or_unit_2.si["exponents"]
    return False


def make_quantity(value: Union[int, float, ArrayLike], unit_name: Any) -> QuantityRecord:
    """A sealed record from a value and a unit."""
    return QuantityRecord.from_quantity(_registry().Quantity(np.asarray(value), _unit_name(unit_name)))


def get_value(quantity: QuantityRecord):
    """A copy of the values: a Python scalar for 0-d records, an array otherwise."""
    value = np.array(quantity.values, copy=True)
    return value.item() if value.ndim == 0 else value


def get_unit(quantity: QuantityRecord) -> str:
    """The canonical unit name."""
    return quantity.unit


def change_value(quantity: QuantityRecord, value: Union[int, float, ArrayLike]) -> QuantityRecord:
    """A new sealed record with other values, the same unit, field and kind."""
    q = _registry().Quantity(np.asarray(value), quantity.unit)
    return QuantityRecord.from_quantity(q, field=quantity.field, kind=quantity.kind)


def convert(quantity: QuantityRecord, unit_name: Any) -> QuantityRecord:
    """A new sealed record in another unit, keeping field and kind."""
    q = quantity.to_quantity(form="pint", unit=_unit_name(unit_name))
    return QuantityRecord.from_quantity(q, field=quantity.field, kind=quantity.kind)
