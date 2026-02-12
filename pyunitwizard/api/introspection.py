"""Introspection helpers for PyUnitWizard quantities and units."""

from __future__ import annotations

from typing import Dict, Optional, TYPE_CHECKING

from .._private.exceptions import NotImplementedFormError
from .._private.quantity_or_unit import QuantityOrUnit
from .._private.smonitor.emitter import emit_probe_miss
from ..forms import dict_is_form, dict_is_quantity, dict_is_unit, dict_dimensionality
from .. import kernel

if TYPE_CHECKING:  # pragma: no cover - circular import guard
    from .conversion import convert


from smonitor import signal

_TYPE_TO_FORM_CACHE: Dict[type, str] = {}

@signal(tags=["introspection"], exception_level="DEBUG")
def get_form(quantity_or_unit: QuantityOrUnit) -> str:
    """ Returns the form of a quantity as a string.

        Parameters
        ---------
        quantity_or_unit : QuantityOrUnit
            A quanitity or a unit

        Returns
        -------
        {"string", "pint", "openmm.unit", "unyt"}
            The form of the quantity
    """

    obj_type = type(quantity_or_unit)
    if obj_type in _TYPE_TO_FORM_CACHE:
        return _TYPE_TO_FORM_CACHE[obj_type]

    for form_name, aux_is_form in dict_is_form.items():
        if aux_is_form(quantity_or_unit):
            _TYPE_TO_FORM_CACHE[obj_type] = form_name
            return form_name

    raise NotImplementedFormError(type(quantity_or_unit))


@signal(tags=["introspection"], exception_level="DEBUG")
def is_quantity(quantity_or_unit: QuantityOrUnit, parser: Optional[str] = None) -> bool:
    """ Check whether an object is a quantity

        Parameters
        ---------
        quantity_or_unit : QuantityOrUnit
            A quanitity or a unit

        parser :  {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser for string quantities

        Returns
        -------
        bool
            False if it's not a quantity
    """

    from .conversion import convert  # Local import to avoid circular dependency

    probe_input = quantity_or_unit

    if isinstance(quantity_or_unit, str):
        try:
            quantity_or_unit = convert(
                quantity_or_unit, to_form=kernel.default_form, parser=parser
            )
            output = dict_is_quantity[kernel.default_form](quantity_or_unit)
        except Exception:
            emit_probe_miss(probe_input, "pyunitwizard.api.introspection.is_quantity")
            return False
    else:
        try:
            form = get_form(quantity_or_unit)
            output = dict_is_quantity[form](quantity_or_unit)
        except Exception:
            emit_probe_miss(probe_input, "pyunitwizard.api.introspection.is_quantity")
            return False

    if not output:
        emit_probe_miss(probe_input, "pyunitwizard.api.introspection.is_quantity")

    return output


@signal(tags=["introspection"], exception_level="DEBUG")
def is_unit(quantity_or_unit: QuantityOrUnit, parser: Optional[str] = None) -> bool:
    """ Check whether an object is a unit

        Parameters
        ---------
        quantity_or_unit : QuantityOrUnit
            A quantity or a unit

        parser :  {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser for string quantities

        Returns
        -------
        bool
            False if it's not a unit
    """

    from .conversion import convert  # Local import to avoid circular dependency
    from .extraction import get_value

    probe_input = quantity_or_unit

    if isinstance(quantity_or_unit, str):
        try:
            quantity_or_unit = convert(quantity_or_unit, parser=parser)
            output = get_value(quantity_or_unit) == 1
        except Exception:
            emit_probe_miss(probe_input, "pyunitwizard.api.introspection.is_unit")
            return False
    else:
        try:
            form = get_form(quantity_or_unit)
            output = dict_is_unit[form](quantity_or_unit)
        except Exception:
            emit_probe_miss(probe_input, "pyunitwizard.api.introspection.is_unit")
            return False

    if not output:
        emit_probe_miss(probe_input, "pyunitwizard.api.introspection.is_unit")

    return output


@signal(tags=["introspection"])
def get_dimensionality(quantity_or_unit: QuantityOrUnit) -> Dict[str, int]:
    """ Returns the dimensionality of the quantity or unit.

        Parmeters
        ---------
        quantity_or_unit : QuantityOrUnit
            A quantity or a unit

        Returns
        -------
        dict
            A dictionary with the dimensionality of the unit.
    """

    from .conversion import convert

    dim = None

    if isinstance(quantity_or_unit, str):
        if is_quantity(quantity_or_unit):
            quantity_or_unit = convert(quantity_or_unit, to_type="quantity")
        elif is_unit(quantity_or_unit):
            quantity_or_unit = convert(quantity_or_unit, to_type="unit")

    form = get_form(quantity_or_unit)
    dim = dict_dimensionality[form](quantity_or_unit)

    return dim


def is_dimensionless(quantity_or_unit: QuantityOrUnit) -> bool:
    """ Check wheter a quantity or unit is dimensionless.

        Parameters
        ----------
        quantity_or_unit : QuantityOrUnit
            A quantity or a unit

        Returns
        -------
        bool
            Whether the quantity or unit is dimensionless.
    """

    dim = get_dimensionality(quantity_or_unit)
    for exponent in dim.values():
        if exponent != 0:
            return False
    return True


__all__ = [
    "get_form",
    "is_quantity",
    "is_unit",
    "get_dimensionality",
    "is_dimensionless",
]
