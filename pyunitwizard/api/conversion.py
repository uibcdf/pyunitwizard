"""Conversion helpers bridging between different quantity backends."""

from __future__ import annotations

from typing import Any, Optional, Union

import numpy as np

from .._private.exceptions import ArgumentError as BadCallError
from .._private.forms import digest_to_form
from .._private.parsers import digest_parser
from .._private.quantity_or_unit import QuantityOrUnit
from ..forms import (
    dict_convert,
    dict_get_unit,
    dict_get_value,
    dict_translate_quantity,
    dict_translate_unit,
)
from ..parse import parse as _parse
from .introspection import get_form, is_unit


from smonitor import signal
from depdigest import dep_digest

@signal(tags=["conversion"], exception_level="DEBUG")
@dep_digest('unyt', when={'to_form': 'unyt'})
@dep_digest('openmm.unit', when={'to_form': 'openmm.unit'})
@dep_digest('astropy.units', when={'to_form': 'astropy.units'})
def convert(
    quantity_or_unit: Any,
    to_unit: Optional[str] = None,
    to_form: Optional[str] = None,
    parser: Optional[str] = None,
    to_type: Optional[str] = "quantity",
) -> Union[QuantityOrUnit, float, np.ndarray]:
    """ Converts a quantity or unit to a different unit and/or to a different
        form and/or type.

        Parameters
        ----------
        to_unit : str, optional
            The unit to convert to.

        to_form : {"unyt", "pint", "openmm.unit", "astropy.units", "string"}, optional
            The form to convert to.

        parser : {"pint", "openmm.unit", "astropy.units"}, optional
            The parser to use if a string is passed.

        to_type : {"quantity", "unit", "value"}, optional
            The type to convert to.

        Returns
        -------
        QuantityOrUnit or ArrayLike or float
            The converted quantity or unit. If to_type is passed the return value can
            be a float or a numpy array.
    """

    output = None

    form_in = get_form(quantity_or_unit)
    to_form = digest_to_form(to_form, form_in)
    parser = digest_parser(parser)

    if to_type not in ["unit", "value", "quantity"]:
        raise BadCallError("to_type")

    if isinstance(to_unit, str):
        to_unit = _parse(to_unit, parser=parser, to_form=to_form)
        to_unit = dict_get_unit[to_form](to_unit)

    if form_in == "string":
        if to_form == "string":
            output = _parse(quantity_or_unit, parser=parser, to_form=parser)

            if to_unit is not None:
                output = dict_convert[parser](output, to_unit)
            if to_type == "unit":
                if is_unit(output):
                    output = output
                else:
                    output = dict_get_unit[parser](output)
                output = dict_translate_quantity[parser]["string"](output)
            elif to_type == "value":
                output = dict_get_value[parser](output)
                output = str(output)
            else:
                output = dict_translate_quantity[parser]["string"](output)
        else:
            output = _parse(quantity_or_unit, parser=parser, to_form=to_form)

            if to_unit is not None:
                output = dict_convert[to_form](output, to_unit)
            if to_type == "unit":
                if is_unit(output):
                    output = output
                else:
                    output = dict_get_unit[to_form](output)
            elif to_type == "value":
                output = dict_get_value[to_form](output)
    else:
        if to_form == "string":
            output = quantity_or_unit

            if to_unit is not None:
                output = dict_convert[form_in](output, to_unit)

            if to_type == "unit":
                if is_unit(output):
                    output = output
                else:
                    output = dict_get_unit[form_in](output)
                output = dict_translate_unit[form_in]["string"](output)
            elif to_type == "value":
                output = dict_get_value[form_in](output)
                output = str(output)
            else:
                output = dict_translate_quantity[form_in]["string"](output)
        else:
            if form_in == to_form:
                output = quantity_or_unit
            else:
                if is_unit(quantity_or_unit):
                    output = dict_translate_unit[form_in][to_form](quantity_or_unit)
                else:
                    output = dict_translate_quantity[form_in][to_form](quantity_or_unit)

            if to_unit is not None:
                to_unit = convert(to_unit, to_form=to_form)
                output = dict_convert[to_form](output, to_unit)

            if to_type == "unit":
                if is_unit(output):
                    output = output
                else:
                    output = dict_get_unit[to_form](output)
            elif to_type == "value":
                output = dict_get_value[to_form](output)

    return output


@signal(tags=["conversion"], exception_level="DEBUG")
def to_string(
    quantity_or_unit: Any,
    to_unit: Optional[str] = None,
    parser: Optional[str] = None,
) -> str:
    """Return a quantity converted to the string form."""

    return convert(
        quantity_or_unit,
        to_unit=to_unit,
        to_form="string",
        parser=parser,
        to_type="quantity",
    )


__all__ = ["convert", "to_string"]
