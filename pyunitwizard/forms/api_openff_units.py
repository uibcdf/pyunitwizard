"""Optional OpenFF form, native OpenMM translators and unsealed val/unit tools.

Dispatch/parser key: ``openff.units``. Definition checks reuse Pint's verifier;
loading this module alone imports no optional provider.
"""

from __future__ import annotations

import ast
import sys
from typing import Any, Dict, Mapping, Optional

import numpy as np

from pyunitwizard._private.exceptions import RecordError

form_name = "openff.units"
parser = True


def require_openff() -> Any:
    """Return the optional registry or an actionable installation diagnostic."""
    if sys.version_info < (3, 12):
        raise ModuleNotFoundError(
            "openff.units requires Python 3.12–3.14; other PyUnitWizard forms support Python 3.11."
        )
    from depdigest import is_installed

    if not is_installed("openff.units"):
        raise ModuleNotFoundError(
            "Install the optional form with conda install -c conda-forge openff-units=0.4.0; its PyPI upload is yanked."
        )
    import pint

    if not (0, 24) <= tuple(int(v) for v in pint.__version__.split(".")[:2]) < (0, 26):
        raise ModuleNotFoundError(
            "OpenFF 0.4.0 requires Pint >=0.24,<0.26; use the optional OpenFF Conda environment."
        )
    from openff.units import unit

    return unit


def is_form(obj: Any) -> bool:
    """Recognize an object owned by an OpenFF registry."""
    return is_quantity(obj) or is_unit(obj)


def is_quantity(obj: Any) -> bool:
    """Recognize an OpenFF quantity, including generated Pint classes."""
    import pint

    return isinstance(obj, pint.Quantity) and type(obj._REGISTRY).__module__.startswith("openff.units")


def is_unit(obj: Any) -> bool:
    """Recognize an OpenFF unit."""
    import pint

    return isinstance(obj, pint.Unit) and type(obj._REGISTRY).__module__.startswith("openff.units")


def normalize_registry(obj: Any) -> Any:
    """Verify a foreign OpenFF object before same-form fast paths."""
    from .api_pint import normalize_registry as normalize

    return normalize(obj, registry=require_openff())


def quantity_to_pint(quantity: Any) -> Any:
    """Verify definitions and rebuild in PyUnitWizard's Pint registry."""
    from .api_pint import normalize_registry as normalize

    return normalize(quantity)


def unit_to_pint(unit: Any) -> Any:
    """Verify an OpenFF unit and rebuild in the shared Pint registry."""
    return quantity_to_pint(unit)


def quantity_to_openff_units(quantity: Any) -> Any:
    """Verify definitions and rebuild a Pint quantity in OpenFF's registry."""
    from .api_pint import normalize_registry as normalize

    return normalize(quantity, registry=require_openff())


def unit_to_openff_units(unit: Any) -> Any:
    """Verify and rebuild a Pint unit in OpenFF's registry."""
    return quantity_to_openff_units(unit)


def dimensionality(obj: Any) -> Dict[str, int]:
    """Describe dimensions using the shared Pint adapter."""
    from .api_pint import dimensionality as describe

    return describe(obj)


def compatibility(first: Any, second: Any) -> bool:
    """Compare dimensionally compatible quantities in one verified registry."""
    return normalize_registry(first).is_compatible_with(normalize_registry(second))


def make_quantity(value: Any, unit: Any) -> Any:
    """Construct in OpenFF, verifying incoming unit objects."""
    if not isinstance(unit, str):
        unit = normalize_registry(unit)
    return require_openff().Quantity(value, unit)


def get_value(quantity: Any) -> Any:
    """Extract the magnitude."""
    return quantity.magnitude


def get_unit(quantity: Any) -> Any:
    """Extract the unit."""
    return quantity.units


def change_value(quantity: Any, value: Any) -> Any:
    """Replace the value with the original verified unit."""
    return make_quantity(value, quantity.units)


def convert(obj: Any, unit: Any) -> Any:
    """Convert a verified quantity or unit within the OpenFF registry."""
    obj = normalize_registry(obj)
    if not isinstance(unit, str):
        unit = normalize_registry(unit)
    return obj.to(unit)


def string_to_quantity(text: str) -> Any:
    """Parse with OpenFF's actual registry."""
    if text.startswith("[") or text.startswith("("):
        from pyunitwizard.parse import _find_closing_bracket_position, _find_closing_parenthesis_position

        end = (
            _find_closing_bracket_position(text) if text.startswith("[") else _find_closing_parenthesis_position(text)
        )
        return require_openff().Quantity(np.asarray(ast.literal_eval(text[: end + 1])), text[end + 1 :].strip())
    return require_openff().Quantity(text)


def string_to_unit(text: str) -> Any:
    """Parse a unit with OpenFF's actual registry."""
    return require_openff().Unit(text)


def quantity_to_string(quantity: Any) -> str:
    """Return OpenFF's scalar spelling."""
    return str(quantity)


def unit_to_string(unit: Any) -> str:
    """Return long names independently of display settings."""
    return format(unit, "D")


def quantity_to_openmm_unit(quantity: Any) -> Any:
    """Use OpenFF's native translator after checking shared definitions."""
    quantity_to_pint(quantity)
    from openff.units.openmm import to_openmm

    return to_openmm(normalize_registry(quantity))


def unit_to_openmm_unit(unit: Any) -> Any:
    """Translate an OpenFF unit with its native OpenMM implementation."""
    return quantity_to_openmm_unit(make_quantity(1, unit)).unit


def from_dict(
    data: Mapping[str, Any], *, unit: Optional[str] = None, dimensionality: Optional[Dict[str, int]] = None
) -> Any:
    """Import an unsealed OpenFF val/unit node after reader checks.

    Parameters
    ----------
    data : mapping
        Exactly ``val`` (finite scalar/nested numeric array) and ``unit``.
    unit : str, optional
        Negotiated target unit. Stored units never default to session policy.
    dimensionality : dict, optional
        Required dimensions in PyUnitWizard notation.

    Returns
    -------
    quantity
        OpenFF quantity with verified definitions. The source node has no seal.
        Use QuantityRecord.from_quantity with an explicit field to enter the
        verified domain; consumers own field association at this raw boundary.

    Raises
    ------
    RecordError
        For invalid data, definitions or expectations.

    Examples
    --------
    >>> from_dict({'val': 3.0, 'unit': 'angstrom'}, unit='nanometer')
    """
    if not isinstance(data, Mapping) or set(data) != {"val", "unit"} or not isinstance(data["unit"], str):
        raise RecordError(reason="an unsealed OpenFF node requires exactly val and unit")
    from pyunitwizard.api.validation import check

    try:
        values = np.asarray(data["val"])
        if values.dtype.kind not in "fiu" or not np.isfinite(values).all():
            raise RecordError(reason="OpenFF JSON nodes require finite numeric values")
        result = make_quantity(values, data["unit"])
        quantity_to_pint(result)
        if dimensionality is not None and not check(result, dimensionality=dimensionality):
            raise RecordError(reason=f"expected dimensionality {dimensionality}")
        return result if unit is None else result.to(unit)
    except RecordError:
        raise
    except Exception as exc:
        raise RecordError(reason="OpenFF val/unit boundary failed definition or reader checks") from exc


def to_dict(quantity: Any) -> Dict[str, Any]:
    """Export an unsealed strict-JSON OpenFF val/unit node.

    Parameters
    ----------
    quantity : OpenFF quantity
        Input in the optional form.

    Returns
    -------
    dict
        Val and long unit name. This leaves the verified QuantityRecord domain:
        the node carries no seal, field or integrity guarantee.

    Raises
    ------
    RecordError
        For wrong form, inconsistent definitions or nonfinite values.

    Examples
    --------
    >>> to_dict(make_quantity(3.0, 'angstrom'))
    {'val': 3.0, 'unit': 'angstrom'}
    """
    if not is_quantity(quantity):
        raise RecordError(reason="OpenFF val/unit export requires an OpenFF quantity")
    quantity_to_pint(quantity)
    values = np.asarray(quantity.magnitude)
    if values.dtype.kind not in "fiu" or not np.isfinite(values).all():
        raise RecordError(reason="OpenFF JSON nodes require finite numeric values")
    return {"val": values.tolist(), "unit": unit_to_string(quantity.units)}
