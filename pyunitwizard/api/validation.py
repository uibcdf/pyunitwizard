"""Validation helpers for PyUnitWizard."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import numpy as np

from .comparison import are_equal, _compatible_dimensionalities
from .extraction import get_unit, get_value
from .introspection import get_dimensionality, is_quantity, is_unit


from smonitor import signal

@signal(tags=["validation"])
def check(
    quantity_or_unit: Any,
    dimensionality: Optional[Dict[str, int]] = None,
    value_type: Optional[Any] = None,
    shape: Optional[Tuple[int, ...]] = None,
    unit: Optional[str] = None,
    dtype_name: Optional[str] = None,
) -> bool:
    """ Check if a quantity or unit has the specified dimensionality,
        value_type, shape, unit or data type.

        Parameters
        ---------
        quantity_or_unit: Any
            A quantity or unit object. If any other object is passed False will be returned.

        dimensionality: dict
            A dictionary specifying the dimensionality of the quantity or unit.

        value_type: Any
            The type of the quantity. Can be int, float, np.ndarray.

        shape: tuple of int
            For non scalar quantities. A tuple with the shape of the array.

        unit: str
            Name of the unit.

        dtype_name : str
            For non scalar quantities. The dtype of the array (i.e float64).

        Returns
        -------
        bool
            True if the quantity or unit has the specified parameters.
    """

    if is_quantity(quantity_or_unit):
        if unit is not None:
            aux_unit = get_unit(quantity_or_unit)
            if not are_equal(aux_unit, unit):
                return False
        if value_type is not None:
            aux_value = get_value(quantity_or_unit)
            if not isinstance(aux_value, value_type):
                return False
        if shape is not None:
            value = get_value(quantity_or_unit)
            if np.shape(value) != tuple(shape):
                return False
        if dimensionality is not None:
            aux_dimensionality = get_dimensionality(quantity_or_unit)
            if not _compatible_dimensionalities(aux_dimensionality, dimensionality):
                return False
        if dtype_name is not None:
            aux_value = get_value(quantity_or_unit)
            try:
                aux_dtype_name = aux_value.dtype.name  # type: ignore[attr-defined]
                if aux_dtype_name != dtype_name:
                    return False
            except Exception:
                return False

    elif is_unit(quantity_or_unit):
        if unit is not None:
            if not are_equal(quantity_or_unit, unit):
                return False
        if dimensionality is not None:
            aux_dimensionality = get_dimensionality(quantity_or_unit)
            if not _compatible_dimensionalities(aux_dimensionality, dimensionality):
                return False
    else:
        return False

    return True


@signal(tags=["validation"])
def ensure_quantity(
    value: Any,
    dimensionality: Optional[Dict[str, int]] = None,
    to_unit: Optional[str] = None,
    standardized: bool = True,
    parser: Optional[str] = None,
    caller: Optional[str] = None,
) -> Any:
    """ Return ``value`` as a validated quantity, or raise.

        This is the canonical "digest a length/mass/time/... argument" helper:
        it accepts any PyUnitWizard-recognized quantity form (a unit-bearing
        string, or a pint/openmm/astropy/unyt quantity), optionally checks its
        physical dimensionality, and returns it standardized (or in ``to_unit``).
        Bare numbers are rejected, so a value meant as one unit is never silently
        reinterpreted as another.

        Parameters
        ----------
        value : Any
            A quantity, or a unit-bearing string (e.g. ``"3.5 angstroms"``).
            Bare numbers (int/float/array/list) are rejected.
        dimensionality : dict, optional
            Required dimensionality, e.g. ``{'[L]': 1}`` for a length. If given
            and the quantity does not match, an ``ArgumentError`` is raised.
        to_unit : str, optional
            If given, the quantity is returned in this unit instead of the
            configured standard unit.
        standardized : bool, default True
            When True (and ``to_unit`` is None) the quantity is returned in the
            configured standard units. When False (and ``to_unit`` is None) the
            quantity is returned unchanged (still validated).
        parser : str, optional
            Parser used for string quantities.
        caller : str, optional
            Name of the calling function, used to enrich error messages.

        Returns
        -------
        Any
            The validated quantity, standardized or converted to ``to_unit``.

        Raises
        ------
        ArgumentError
            If ``value`` is not a quantity, or its dimensionality does not match.
    """

    from ..parse import parse
    from .standardization import standardize
    from .conversion import convert
    from .._private.exceptions import ArgumentError

    if isinstance(value, str):
        value = parse(value, parser=parser)

    if not is_quantity(value):
        raise ArgumentError(
            argument="value", value=value, caller=caller,
            message="expected a quantity with explicit units; bare numbers are not accepted",
        )

    if dimensionality is not None and not check(value, dimensionality=dimensionality):
        raise ArgumentError(
            argument="value", value=value, caller=caller,
            message=f"expected a quantity with dimensionality {dimensionality}",
        )

    if to_unit is not None:
        return standardize(value, to_unit=to_unit) if standardized else convert(value, to_unit=to_unit)

    return standardize(value) if standardized else value


__all__ = ["check", "ensure_quantity"]
