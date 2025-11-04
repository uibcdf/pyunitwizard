"""Comparison helpers for quantities and units."""

from __future__ import annotations

from typing import Dict

import numpy as np

from .._private.quantity_or_unit import QuantityLike, QuantityOrUnit
from ..forms import dict_compatibility
from .introspection import get_dimensionality, get_form, is_dimensionless, is_quantity, is_unit


def similarity(
    quantity_or_unit_1: QuantityOrUnit,
    quantity_or_unit_2: QuantityOrUnit,
    relative_tolerance: float = 1e-08,
) -> bool:
    """Alias for :func:`are_close` using ``relative_tolerance`` as ``rtol``."""

    return are_close(
        quantity_or_unit_1, quantity_or_unit_2, rtol=relative_tolerance
    )


def are_close(
    quantity_1: QuantityLike,
    quantity_2: QuantityLike,
    rtol: float = 1e-05,
    atol: float = 1e-08,
) -> bool:
    """ Compares whether two quantities are similiar within a specified tolerance.

        Parameters
        ----------
        quantity_or_unit_1 : QuantityOrUnit
            A quantity or a unit

        quantity_or_unit_2 : QuantityOrUnit
            A quantity or a unit

        relative_tolerance : float
            The relative tolerance to compare the quantities.

        Returns
        -------
        bool
            Whether the quantities or units are similar.
    """

    from .extraction import get_value, get_value_and_unit

    compatible = are_compatible(quantity_1, quantity_2)

    if compatible:
        value_1, unit_1 = get_value_and_unit(quantity_1)
        value_2 = get_value(quantity_2, to_unit=unit_1)

        if isinstance(value_1, (list, tuple, np.ndarray)):
            return np.allclose(value_1, value_2, rtol=rtol, atol=atol)
        else:
            check_atol = abs(value_1 - value_2) < atol
            check_rtol = abs(value_1 / value_2 - 1.0) < rtol

            return check_atol and check_rtol

    return False


def are_equal(
    quantity_or_unit_1: QuantityOrUnit,
    quantity_or_unit_2: QuantityOrUnit,
    same_form: bool = False,
) -> bool:
    """ Compares whether two quantities are similiar within a specified tolerance.

        Parameters
        ----------
        quantity_or_unit_1 : QuantityOrUnit
            A quantity or a unit

        quantity_or_unit_2 : QuantityOrUnit
            A quantity or a unit

        relative_tolerance : float
            The relative tolerance to compare the quantities.

        Returns
        -------
        bool
            Whether the quantities or units are similar.
    """

    from .conversion import convert
    from .extraction import get_unit, get_value, get_value_and_unit

    if same_form:
        form_1 = get_form(quantity_or_unit_1)
        form_2 = get_form(quantity_or_unit_2)
        if form_1 != form_2:
            return False

    compatible = are_compatible(quantity_or_unit_1, quantity_or_unit_2)

    if compatible:
        if is_quantity(quantity_or_unit_1) and is_quantity(quantity_or_unit_2):
            value_1, unit_1 = get_value_and_unit(quantity_or_unit_1)
            value_2 = get_value(quantity_or_unit_2, to_unit=unit_1)

            if isinstance(value_1, (list, tuple, np.ndarray)):
                return np.all(np.equal(value_1, value_2))
            else:
                return value_1 == value_2

        if is_unit(quantity_or_unit_1) and is_unit(quantity_or_unit_2):
            unit_1 = convert(quantity_or_unit_1)
            unit_2 = convert(quantity_or_unit_2)

            return unit_1 == unit_2

    return False


def compatibility(
    quantity_or_unit_1: QuantityOrUnit, quantity_or_unit_2: QuantityOrUnit
) -> bool:
    """Alias for :func:`are_compatible`."""

    return are_compatible(quantity_or_unit_1, quantity_or_unit_2)


def are_compatible(
    quantity_or_unit_1: QuantityOrUnit,
    quantity_or_unit_2: QuantityOrUnit,
) -> bool:
    """ Check whether two quantities or units are compatible.
        This means that they have the same dimensionalities.

        Parameters
        ----------
        quantity_or_unit_1 : QuantityOrUnit
            A quantity or a unit

        quantity_or_unit_2 : QuantityOrUnit
            A quantity or a unit

        Returns
        -------
        bool
            Whether the quantities or units are compatible.
    """

    from .conversion import convert

    if is_dimensionless(quantity_or_unit_1) and is_dimensionless(quantity_or_unit_2):
        form1 = get_form(quantity_or_unit_1)
        form2 = get_form(quantity_or_unit_2)

        if form1 != form2:
            try:
                tmp = convert(quantity_or_unit_1, to_form=form2)
                is_compatible = dict_compatibility[form2](tmp, quantity_or_unit_2)
            except Exception:
                tmp = convert(quantity_or_unit_2, to_form=form1)
                is_compatible = dict_compatibility[form1](tmp, quantity_or_unit_1)
        else:
            is_compatible = dict_compatibility[form1](
                quantity_or_unit_1, quantity_or_unit_2
            )
    else:
        dim1 = get_dimensionality(quantity_or_unit_1)
        dim2 = get_dimensionality(quantity_or_unit_2)

        is_compatible = _compatible_dimensionalities(dim1, dim2)

    return is_compatible


def _compatible_dimensionalities(
    dim1: Dict[str, int], dim2: Dict[str, int]
) -> bool:
    """ Check whether two dimensionalities are compatible.

        Parameters
        ----------
        dim1 : dict
            Dimensionality dictionary.

        dim2 : dict
            Dimensionality dictionary.

        Returns
        ----------
        bool
            Whether the dimensiomnalities are compatible.

    """

    for dim in ["[L]", "[M]", "[T]", "[K]", "[mol]", "[A]", "[Cd]"]:
        if dim not in dim1:
            dim1[dim] = 0
        if dim not in dim2:
            dim2[dim] = 0

    return dim1 == dim2


__all__ = [
    "are_close",
    "are_compatible",
    "are_equal",
    "compatibility",
    "similarity",
]
