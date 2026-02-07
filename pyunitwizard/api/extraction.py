"""Value and unit extraction helpers."""

from __future__ import annotations

from typing import Optional, Tuple, Union

import numpy as np

from .._private.quantity_or_unit import QuantityLike, UnitLike
from ..forms import dict_change_value
from .introspection import get_form


from smonitor import signal

@signal(tags=["extraction"])
def get_value(
    quantity: QuantityLike,
    to_unit: Optional[str] = None,
    parser: Optional[str] = None,
    standardized: Optional[bool] = False,
) -> Union[np.ndarray, float, int]:
    """ Returns the value of a quantity.

        Parameters
        ----------
        to_unit : str, optional
            Name of the unit to which the quantity will be converted (i.e kcal/mol).

        parser : {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser to use.

        Returns
        -------
        np.ndarray or float or int
            An array with the quantity value or a a float or an int if it's a scalar.

    """

    from .conversion import convert
    from .standardization import standardize

    if standardized:
        quantity = standardize(quantity)
        to_unit = None

    return convert(quantity, to_unit=to_unit, parser=parser, to_type="value")


@signal(tags=["extraction"])
def get_unit(
    quantity: QuantityLike,
    to_form: Optional[str] = None,
    parser: Optional[str] = None,
    standardized: Optional[bool] = False,
) -> UnitLike:
    """ Returns the unit of a quantity.

        Parameters
        ----------
        to_unit : str, optional
            Name of the unit to which the quantity will be converted (i.e kcal/mol).

         form : {"unyt", "pint", "openmm.unit", "astropy.units", "string"}, optional
            If passed the unit will be converted to that form. This is the type that will be returned

        parser : {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser to use.

        Returns
        -------
        UnitLike
            The unit.

    """

    from .conversion import convert
    from .standardization import standardize

    if standardized:
        quantity = standardize(quantity)

    return convert(quantity, to_form=to_form, parser=parser, to_type="unit")


@signal(tags=["extraction"])
def get_value_and_unit(
    quantity: QuantityLike,
    to_unit: Optional[str] = None,
    to_form: Optional[str] = None,
    parser: Optional[str] = None,
    standardized: Optional[bool] = False,
) -> Tuple[Union[np.ndarray, float, int], UnitLike]:
    """ Returns the value and unit of a quantity.

        Parameters
        ----------
        to_unit : str, optional
            Name of the unit to which the quantity will be converted (i.e kcal/mol).

        parser : {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser to use.

        Returns
        -------
        np.ndarray or float or int
        UnitLike
            The value and unit of the input quantity.

    """

    from .conversion import convert
    from .standardization import standardize

    if standardized:
        quantity = standardize(quantity)
        to_unit = None

    value = convert(quantity, to_unit=to_unit, parser=parser, to_type="value")
    unit = convert(
        quantity, to_unit=to_unit, to_form=to_form, parser=parser, to_type="unit"
    )

    return value, unit


def change_value(quantity: QuantityLike, value: Union[np.ndarray, float, int]) -> QuantityLike:
    """Return the quantity with a new value preserving its unit."""

    form = get_form(quantity)
    return dict_change_value[form](quantity, value)


__all__ = [
    "change_value",
    "get_unit",
    "get_value",
    "get_value_and_unit",
]
