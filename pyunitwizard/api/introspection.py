"""Introspection helpers for PyUnitWizard quantities and units."""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, Any, Dict, Optional

from .. import kernel
from .._private.exceptions import NotImplementedFormError
from .._private.quantity_or_unit import QuantityOrUnit
from .._private.smonitor.emitter import emit_probe_miss
from ..forms import (
    dict_dimensionality,
    dict_get_unit,
    dict_is_form,
    dict_is_quantity,
    dict_is_unit,
    dict_translate_unit,
)

if TYPE_CHECKING:  # pragma: no cover - circular import guard
    from .conversion import convert


from smonitor import signal

_TYPE_TO_FORM_CACHE: Dict[type, str] = {}
_DIMENSIONALITY_CACHE: Dict[tuple[str, str], Dict[str, int]] = {}


@lru_cache(maxsize=256)
def _target_unit_from_string(target_unit: str, form: str, parser: Optional[str]):
    from .construction import unit

    return unit(target_unit, form=form, parser=parser)


@lru_cache(maxsize=256)
def _target_unit_from_pint_registry(target_unit: str, registry):
    return registry.Unit(target_unit)


def _register_detected_form(form: str) -> str:
    if form != "string" and form not in kernel.loaded_libraries:
        from pyunitwizard.configure import load_library

        load_library(form)
    return form


@signal(tags=["introspection"], exception_level="DEBUG")
def get_form(
    quantity_or_unit: QuantityOrUnit, raise_exception: bool = True
) -> Optional[str]:
    """Returns the form of a quantity as a string.

    Parameters
    ---------
    quantity_or_unit : QuantityOrUnit
        A quanitity or a unit

    raise_exception : bool, default=True
        Whether to raise NotImplementedFormError if the form is not found.

    Returns
    -------
    {"string", "pint", "openmm.unit", "unyt", None}
        The form of the quantity
    """

    obj_type = type(quantity_or_unit)
    if obj_type in _TYPE_TO_FORM_CACHE:
        return _TYPE_TO_FORM_CACHE[obj_type]

    if isinstance(quantity_or_unit, str):
        _TYPE_TO_FORM_CACHE[obj_type] = "string"
        return "string"

    # Fast class name detection to avoid loading all libraries or calling many functions
    type_str = str(obj_type)
    if "pint" in type_str:
        _TYPE_TO_FORM_CACHE[obj_type] = "pint"
        return _register_detected_form("pint")
    if "openmm" in type_str:
        _TYPE_TO_FORM_CACHE[obj_type] = "openmm.unit"
        return _register_detected_form("openmm.unit")
    if "unyt" in type_str:
        _TYPE_TO_FORM_CACHE[obj_type] = "unyt"
        return _register_detected_form("unyt")
    if "astropy" in type_str:
        _TYPE_TO_FORM_CACHE[obj_type] = "astropy.units"
        return _register_detected_form("astropy.units")
    if "physipy" in type_str:
        _TYPE_TO_FORM_CACHE[obj_type] = "physipy"
        return _register_detected_form("physipy")
    if "quantities" in type_str:
        _TYPE_TO_FORM_CACHE[obj_type] = "quantities"
        return _register_detected_form("quantities")

    for form_name, aux_is_form in dict_is_form.items():
        if aux_is_form(quantity_or_unit):
            _TYPE_TO_FORM_CACHE[obj_type] = form_name
            return _register_detected_form(form_name)

    if raise_exception:
        raise NotImplementedFormError(type(quantity_or_unit))
    return None


@signal(tags=["introspection"], exception_level="DEBUG")
def is_quantity(quantity_or_unit: QuantityOrUnit, parser: Optional[str] = None) -> bool:
    """Check whether an object is a quantity

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
            form = get_form(quantity_or_unit, raise_exception=False)
            if form is None:
                emit_probe_miss(
                    probe_input, "pyunitwizard.api.introspection.is_quantity"
                )
                return False
            output = dict_is_quantity[form](quantity_or_unit)
        except Exception:
            emit_probe_miss(probe_input, "pyunitwizard.api.introspection.is_quantity")
            return False

    if not output:
        emit_probe_miss(probe_input, "pyunitwizard.api.introspection.is_quantity")

    return output


@signal(tags=["introspection"], exception_level="DEBUG")
def is_unit(quantity_or_unit: QuantityOrUnit, parser: Optional[str] = None) -> bool:
    """Check whether an object is a unit

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


@signal(tags=["introspection"], exception_level="DEBUG")
def has_unit(
    quantity_or_unit: QuantityOrUnit,
    target_unit: Any,
    parser: Optional[str] = None,
) -> Optional[bool]:
    """Check whether an object already uses an exact target unit.

    This predicate inspects only unit metadata and never extracts or converts
    the magnitude. String quantities return ``None`` because answering for
    them requires parsing the input rather than inspecting existing metadata.

    Parameters
    ----------
    quantity_or_unit : QuantityOrUnit
        Quantity or unit whose current unit is inspected.
    target_unit : str or UnitLike
        Exact unit expected on the input object.
    parser : str, optional
        Parser used once when caching a string target unit.

    Returns
    -------
    bool or None
        ``True`` for an exact unit match, ``False`` for a different unit, and
        ``None`` when the input is textual and cannot be inspected cheaply.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> quantity = puw.quantity(1.0, "nanometer")
    >>> puw.has_unit(quantity, "nm")
    True
    """

    if isinstance(quantity_or_unit, str):
        return None

    object_type = type(quantity_or_unit)
    form = _TYPE_TO_FORM_CACHE.get(object_type)
    if form is None:
        form = get_form(quantity_or_unit)

    source_unit = (
        quantity_or_unit
        if dict_is_unit[form](quantity_or_unit)
        else dict_get_unit[form](quantity_or_unit)
    )

    if isinstance(target_unit, str) and form == "pint":
        registry = getattr(source_unit, "_REGISTRY", None)
        if registry is not None:
            try:
                target_unit = _target_unit_from_pint_registry(target_unit, registry)
            except (AttributeError, TypeError, ValueError):
                return None
    elif isinstance(target_unit, str):
        try:
            target_unit = _target_unit_from_string(target_unit, form, parser)
        except Exception:
            return None
    else:
        target_form = get_form(target_unit)
        if not dict_is_unit[target_form](target_unit):
            target_unit = dict_get_unit[target_form](target_unit)
        if target_form != form:
            target_unit = dict_translate_unit[target_form][form](target_unit)

    try:
        comparison = source_unit == target_unit
        return bool(comparison)
    except (TypeError, ValueError):
        if form != "pint":
            return None
        registry = getattr(source_unit, "_REGISTRY", None)
        if registry is None:
            return None
        try:
            normalized_target = _target_unit_from_pint_registry(
                str(target_unit), registry
            )
            return bool(source_unit == normalized_target)
        except (AttributeError, TypeError, ValueError):
            return None


@signal(tags=["introspection"])
def get_dimensionality(quantity_or_unit: QuantityOrUnit) -> Dict[str, int]:
    """Return dimensional exponents for a quantity or unit.

    Parameters
    ----------
    quantity_or_unit : QuantityOrUnit
        Quantity or unit to inspect. String values are parsed when possible.

    Returns
    -------
    dict
        Mapping of fundamental dimensions to integer exponents.

    Raises
    ------
    NotImplementedFormError
        If the input form is not supported by current runtime adapters.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> puw.get_dimensionality("1 nanometer")
    """

    from .conversion import convert
    from .extraction import get_unit

    if isinstance(quantity_or_unit, str):
        if is_quantity(quantity_or_unit):
            quantity_or_unit = convert(quantity_or_unit, to_type="quantity")
        elif is_unit(quantity_or_unit):
            quantity_or_unit = convert(quantity_or_unit, to_type="unit")

    form = get_form(quantity_or_unit)
    unit = (
        quantity_or_unit
        if dict_is_unit[form](quantity_or_unit)
        else get_unit(quantity_or_unit)
    )
    cache_key = (form, str(unit))

    if cache_key in _DIMENSIONALITY_CACHE:
        return dict(_DIMENSIONALITY_CACHE[cache_key])

    dim = dict_dimensionality[form](quantity_or_unit)
    _DIMENSIONALITY_CACHE[cache_key] = dict(dim)

    return dict(dim)


@signal(tags=["introspection"])
def is_dimensionless(quantity_or_unit: QuantityOrUnit) -> bool:
    """Check wheter a quantity or unit is dimensionless.

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
    "_DIMENSIONALITY_CACHE",
    "_TYPE_TO_FORM_CACHE",
    "get_form",
    "is_quantity",
    "is_unit",
    "has_unit",
    "get_dimensionality",
    "is_dimensionless",
]
