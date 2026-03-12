"""Standardization helpers for canonical units."""

from __future__ import annotations

from typing import Optional

import numpy as np

from .. import kernel
from .._private.exceptions import NoStandardsError
from .._private.forms import digest_form
from .._private.parsers import digest_parser
from .._private.quantity_or_unit import QuantityOrUnit, UnitLike
from ..forms import dict_is_unit
from .comparison import are_compatible
from .conversion import convert
from .introspection import get_dimensionality, get_form


from smonitor import signal


def _standard_units_lstsq(solution: np.ndarray, standards: dict, 
                          matrix: Optional[np.ndarray] = None, 
                          units: Optional[list] = None) -> Optional[UnitLike]:
    """ Auxiliary function for get_standard_units.
        Returns standard units by using least squares method.
    """

    if matrix is None:
        matrix_list = []
        standard_units = []
        for aux_unit, aux_dim_array in standards.items():
            standard_units.append(convert(aux_unit, to_type="unit"))
            matrix_list.append(aux_dim_array)
        matrix = np.array(matrix_list)
    else:
        standard_units = units

    x, _, _, _ = np.linalg.lstsq(matrix.T, solution, rcond=None)


    x = x.round(4)

    if np.allclose(np.dot(matrix.T, x), solution):
        output: UnitLike = 1
        for u, exponent in zip(standard_units, x):
            if not np.isclose(0.0, exponent):
                output *= u ** exponent

        return convert(output, to_form="string", to_type="unit")

    return None


@signal(tags=["standardization"])
def get_standard_units(
    quantity_or_unit: Optional[QuantityOrUnit] = None,
    dimensionality: Optional[dict] = None,
    form: Optional[str] = None,
    parser: Optional[str] = None,
) -> UnitLike:
    """ Returns standard unit of the quantity or unit passed.

        Parameters
        ----------
        quantity_or_unit: Any
            A quantity or unit

        Returns
        -------
        str
            The standard unit.

        Raises
        ------
        NoStandardsError
            If no standard units were defined.
    """

    form = digest_form(form)
    parser = digest_parser(parser)

    if quantity_or_unit is not None:
        dimensionality = get_dimensionality(quantity_or_unit)
    else:
        if dimensionality is None:
            dimensionality = {}
        for unit in kernel.order_fundamental_units:
            dimensionality.setdefault(unit, 0)

    solution = np.array(
        [dimensionality[unit] for unit in kernel.order_fundamental_units],
        dtype=float,
    )
    solution_key = tuple(solution.tolist())
    n_dims_solution = len(kernel.order_fundamental_units) - np.sum(
        np.isclose(solution, 0.0)
    )

    cached_output = kernel.standard_units_by_dimensionality_cache.get(solution_key)
    if cached_output is not None:
        return convert(cached_output, to_form=form, parser=parser, to_type="unit")

    output: Optional[UnitLike] = None

    if n_dims_solution == 0:
        if len(kernel.adimensional_standards) == 0:
            raise NoStandardsError

        for standard_unit, _ in kernel.adimensional_standards.items():
            if quantity_or_unit is None or are_compatible(quantity_or_unit, standard_unit):
                output = standard_unit
                break

    elif n_dims_solution == 1:
        for standard_unit, dim_array in kernel.dimensional_fundamental_standards.items():
            if np.allclose(solution, dim_array):
                output = standard_unit
                break

        if output is None:
            if len(kernel.tentative_base_standards) == 0:
                raise NoStandardsError

            output = _standard_units_lstsq(solution, kernel.tentative_base_standards, kernel.tentative_base_standards_matrix, kernel.tentative_base_standards_units)

    else:
        for standard_units, dim_array in kernel.dimensional_combinations_standards.items():
            if np.allclose(solution, dim_array):
                return standard_units

        if len(kernel.dimensional_fundamental_standards) == 0:
            raise NoStandardsError

        output = _standard_units_lstsq(solution, kernel.dimensional_fundamental_standards, kernel.dimensional_fundamental_standards_matrix, kernel.dimensional_fundamental_standards_units)

        if output is None:
            if len(kernel.tentative_base_standards) == 0:
                raise NoStandardsError

            output = _standard_units_lstsq(solution, kernel.tentative_base_standards, kernel.tentative_base_standards_matrix, kernel.tentative_base_standards_units)

    if output is None:
        raise NoStandardsError

    if isinstance(output, str):
        kernel.standard_units_by_dimensionality_cache[solution_key] = output
    else:
        kernel.standard_units_by_dimensionality_cache[solution_key] = convert(
            output, to_form="string", parser=parser, to_type="unit"
        )

    output = convert(output, to_form=form, parser=parser, to_type="unit")

    return output


@signal(tags=["standardization"])
def standardize(
    quantity_or_unit: QuantityOrUnit, to_form: Optional[str] = None
) -> QuantityOrUnit:
    """ Concert a quantity or unit to standard units.

        Parameters
        ----------
        quantity_or_unit : QuantityOrUnit
            The quantity or a unit that will be converted.

        to_form : str, optional.
            The form to transform to

        Returns
        -------
        QuantityOrUnit
            The quantity ot unit converted to standard units.

        Raises
        ------
        NoStandardsError
            If no standard units were defined.

    """

    to_form = digest_form(to_form)

    form_in = get_form(quantity_or_unit)

    if dict_is_unit[form_in](quantity_or_unit):
        return get_standard_units(quantity_or_unit, form=to_form)

    standard = get_standard_units(quantity_or_unit, form=to_form)
    return convert(quantity_or_unit, to_unit=standard, to_form=to_form)


__all__ = ["get_standard_units", "standardize"]
