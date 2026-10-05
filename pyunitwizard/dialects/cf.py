"""Bounded optional CF physical-unit tools backed by actual UDUNITS.

Named units, products and integer powers are supported. Calendar/reference-time,
logarithmic and arbitrary numeric scale/offset expressions are refused. These
operations do not establish CF dataset conformance or infer quantity kinds.
"""

from __future__ import annotations

import re
from typing import Any, Optional

import numpy as np

from pyunitwizard._private.exceptions import RecordError

__all__ = ["validate_unit", "parse_quantity"]
_METADATA = {"temperature: on_scale", "temperature: difference"}
_TOKEN = re.compile(r"[A-Za-z_]+(?:[+-]?\d+)?|\*\*|[*/.^()]|[+-]?\d+|\S")


def _provider():
    from depdigest import is_installed

    if not is_installed("cf_units"):
        raise ModuleNotFoundError("Install optional CF tools with conda install -c conda-forge cf-units=3.3.1")
    import cf_units

    return cf_units


def _parse(spelling, provider):
    if not isinstance(spelling, str) or not spelling.strip():
        raise RecordError(reason="CF units require an explicit nonempty spelling")
    tokens = _TOKEN.findall(spelling)
    if spelling.strip() != "1":
        for index, token in enumerate(tokens):
            if re.fullmatch(r"[+-]?\d+", token):
                if index == 0 or tokens[index - 1] not in {"^", "**"}:
                    raise RecordError(reason="arbitrary numeric scale factors are outside the CF unit dialect")
            elif not re.fullmatch(r"[A-Za-z_]+(?:[+-]?\d+)?|\*\*|[*/.^()]", token):
                raise RecordError(reason="unsupported CF physical-unit syntax")
    try:
        parsed = provider.Unit(spelling)
    except ValueError as exc:
        raise RecordError(reason=f"invalid CF physical unit {spelling!r}") from exc
    if parsed.is_unknown() or parsed.is_no_unit() or parsed.is_time_reference():
        raise RecordError(reason="unknown, no-unit and calendar/reference-time units are outside this dialect")
    return parsed


def _reference(unit, metadata):
    from pyunitwizard.forms.api_pint import normalize_registry, ureg
    from pyunitwizard.record import QuantityRecord

    try:
        if not isinstance(unit, str):
            unit = normalize_registry(unit)
        quantity = ureg.Quantity(np.array([0.0, 1.0, 2.0]), unit)
        record = QuantityRecord.from_quantity(quantity)
        exponents = record.si["exponents"]
        # The SI descriptor is owned by the existing codec, not a dialect alias table.
        base = " ".join(f"{name}^{exponent}" for name, exponent in exponents.items()) or "1"
        if any(not float(exponent).is_integer() for exponent in exponents.values()):
            raise RecordError(reason="fractional powers are outside the bounded CF unit dialect")
        temperature = "K" in exponents
        if temperature:
            if metadata not in _METADATA:
                raise RecordError(reason="temperature requires explicit on_scale or difference units_metadata")
            if metadata == "temperature: on_scale" and exponents != {"K": 1}:
                raise RecordError(reason="compound on-scale temperatures cannot be converted from units alone")
            if metadata == "temperature: on_scale" and str(quantity.units).startswith("delta_"):
                raise RecordError(reason="an on-scale temperature cannot use a computing difference unit")
        elif metadata is not None:
            raise RecordError(reason="units_metadata is only valid for temperature units")
        points = np.asarray(quantity.to_base_units().magnitude, dtype=float)
        if not np.allclose(np.diff(points), record.si["factor"], rtol=1e-12, atol=0):
            raise RecordError(reason="nonlinear computing units are outside the CF physical-unit dialect")
        if metadata == "temperature: difference" and points[0] != 0:
            raise RecordError(reason="a temperature difference requires a computing difference unit")
        return quantity, base, points
    except RecordError:
        raise
    except Exception as exc:
        raise RecordError(reason="invalid computing unit for the CF dialect") from exc


def _converter(spelling, unit, metadata):
    provider = _provider()
    source = _parse(spelling, provider)
    reference, base, expected = _reference(unit, metadata)
    try:
        target = provider.Unit(base)
        if not source.is_convertible(target):
            raise RecordError(reason="CF and computing units have incompatible dimensions")
        probes = np.asarray(source.convert(np.array([0.0, 1.0, 2.0]), target), dtype=float)
        if metadata == "temperature: difference":
            probes -= probes[0]
        if not np.isfinite(probes).all() or not np.allclose(
            np.diff(probes), probes[1] - probes[0], rtol=1e-12, atol=0
        ):
            raise RecordError(reason="nonlinear CF unit conversions are outside this dialect")
        return reference, expected, probes
    except RecordError:
        raise
    except (ValueError, TypeError) as exc:
        raise RecordError(reason="CF provider cannot verify the negotiated unit") from exc


def validate_unit(unit: Any, spelling: str, *, units_metadata: Optional[str] = None) -> str:
    """Verify that a CF label describes unchanged numbers in a computing unit.

    Parameters
    ----------
    unit : unit or str
        Computing unit understood by PyUnitWizard's verified Pint registry.
    spelling : str
        Explicitly negotiated CF physical-unit spelling. It is retained verbatim;
        UDUNITS formatting may introduce numeric factors forbidden by CF.
    units_metadata : str, optional
        Required for temperature: ``temperature: on_scale`` or
        ``temperature: difference``. Differences need a computing difference
        unit such as delta_degree_Celsius or Kelvin.

    Returns
    -------
    str
        The checked spelling, without changing values or session settings.

    Raises
    ------
    RecordError
        If dimensions, scale, offset or temperature semantics disagree, or
        syntax is outside the bounded dialect. Relative tolerance is 1e-12.
    ModuleNotFoundError
        If the optional cf-units provider is unavailable.

    Examples
    --------
    >>> validate_unit('nanometer', 'nm')
    'nm'
    """
    _, expected, actual = _converter(spelling, unit, units_metadata)
    if not np.allclose(actual, expected, rtol=1e-12, atol=0):
        raise RecordError(reason="CF spelling has a different scale or offset from the computing unit")
    return spelling


def parse_quantity(
    value: Any,
    spelling: str,
    *,
    unit: Any,
    units_metadata: Optional[str] = None,
    form: Optional[str] = None,
) -> Any:
    """Import CF values into an explicitly negotiated computing unit.

    Parameters
    ----------
    value : numeric scalar or array-like
        Values in the declared CF unit. Inputs are never modified.
    spelling : str
        Explicit CF physical-unit spelling interpreted by UDUNITS.
    unit : unit or str
        Required target computing unit. No session unit default is assumed.
    units_metadata : str, optional
        Explicit temperature semantics, as in validate_unit.
    form : str, optional
        Output computing backend; defaults to the session form or Pint.

    Returns
    -------
    quantity
        Values converted using the CF provider's scale/offset and the verified
        computing unit. Numeric conversion may promote integer dtypes.

    Raises
    ------
    RecordError
        For unsupported syntax, mismatched dimensions/semantics or nonnumeric
        values. A missing value is never interpreted as dimensionless.
    ModuleNotFoundError
        If cf-units or the requested computing backend is unavailable.

    Examples
    --------
    >>> parse_quantity(10, 'nm', unit='angstrom', form='pint').magnitude
    100.0
    """
    reference, expected, actual = _converter(spelling, unit, units_metadata)
    values = np.asarray(value)
    if values.dtype.kind not in "fiu":
        raise RecordError(reason="CF quantity import requires real numeric values")
    source_factor = actual[1] - actual[0]
    target_factor = expected[1] - expected[0]
    converted = (values * source_factor + actual[0] - expected[0]) / target_factor
    from pyunitwizard import kernel
    from pyunitwizard.api.conversion import convert
    from pyunitwizard.forms.api_pint import ureg

    quantity = ureg.Quantity(converted, reference.units)
    return convert(quantity, to_form=form or kernel.default_form or "pint")
