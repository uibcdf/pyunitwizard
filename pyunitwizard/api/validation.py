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


__all__ = ["check"]
