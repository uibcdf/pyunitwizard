"""Factory helpers for creating quantities and units."""

from __future__ import annotations

from typing import Optional, Union

from .._private.exceptions import (
    ArgumentError as BadCallError,
    NotImplementedMethodError,
)
from .._private.forms import digest_form
from .._private.quantity_or_unit import ArrayLike, QuantityLike, UnitLike
from ..forms import dict_make_quantity
from .introspection import is_quantity, is_unit


def quantity(
    value: Union[int, float, ArrayLike],
    unit: Optional[UnitLike] = None,
    form: Optional[str] = None,
    parser: Optional[str] = None,
    standardized: Optional[bool] = False,
) -> QuantityLike:
    """ Returns a quantity.

        Parameters
        ----------
        value : int, float or arraylike
            The value of the quantity. Can be a scalar or an array like type.

        unit : UnitLike
            Unit in of the quantity in any of the accepted form.

        form : {"unyt", "pint", "openmm.unit", "astropy.units", "string"}, optional
            Output form of the quantity.

        parser : {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser to use.

        standardized : bool, optional
            Return a standardized quantity, default=False.

        Returns
        -------
        QuantityLike
            The quantity.
    """

    from .conversion import convert
    from .standardization import standardize

    output = None

    form = digest_form(form)

    if type(value) is str:
        if unit is None:
            output = convert(value, to_form=form, parser=parser)
            if not is_quantity(output):
                raise BadCallError("value")
        elif type(unit) is str:
            output = convert(value + " " + unit, to_form=form, parser=parser)
        elif is_unit(unit):
            unit = convert(unit, to_form="string", parser=parser)
            output = convert(value + " " + unit, to_form=form, parser=parser)
    else:
        if unit is None:
            raise BadCallError("unit")

        unit = convert(unit, to_form=form, parser=parser, to_type="unit")

        try:
            output = dict_make_quantity[form](value, unit)
        except Exception as exc:
            raise NotImplementedMethodError() from exc

    if standardized:
        output = standardize(output)

    return output


def unit(unit: str, form: Optional[str] = None, parser: Optional[str] = None) -> UnitLike:
    """ Returns a unit.

        Parameters
        ----------
        unit : str
            Name of the unit (i.e kcal/mol).

        form : {"unyt", "pint", "openmm.unit", "astropy.units", "string"}, optional
            The form of the unit. This is the type that will be returned

        parser : {"unyt", "pint", "openmm.unit", "astropy.units"}, optional
            The parser to use.

        Returns
        -------
        Unitlike
            The unit.
    """

    from .conversion import convert

    return convert(unit, to_form=form, parser=parser, to_type="unit")


__all__ = ["quantity", "unit"]
