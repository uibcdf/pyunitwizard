"""Explicit, bounded physical UCUM exchange using ucumvert's case-sensitive parser.

This optional dialect does not infer quantity kinds, interpret annotations or
canonicalize computing-unit names into guessed UCUM codes.
"""

from __future__ import annotations

from functools import lru_cache
from importlib.resources import as_file, files
from typing import Any, Optional
from xml.etree import ElementTree

import numpy as np

from pyunitwizard._private.exceptions import RecordError

from ._physical import reference

__all__ = ["validate_unit", "parse_quantity"]
# Admission is deliberately narrower than the beta provider's complete grammar.
# These SI atoms, litre/percent/time atoms and simple temperatures have explicit
# independent conformance guards. Other provider mappings need qualification.
_ATOMS = frozenset(
    "m s g rad K C cd mol sr Hz Bq N Pa J W A V F Ohm S Wb Cel T H l L % min h d [degF] [degRe]".split()
)


@lru_cache(maxsize=1)
def _tools():
    import pint
    from ucumvert.parser import get_ucum_parser
    from ucumvert.ucum_pint import UcumToPintTransformer

    resources = files("ucumvert")
    registry = pint.UnitRegistry()
    # Supplying the registry explicitly avoids the transformer's default of
    # changing Pint's application registry. Provider definitions stay isolated.
    with as_file(resources.joinpath("pint_ucum_defs.txt")) as definitions:
        registry.load_definitions(definitions)
    with resources.joinpath("vendor", "ucum-essence.xml").open("rb") as source:
        essence = ElementTree.parse(source).getroot()
    restricted = {
        unit.attrib["Code"]
        for unit in essence
        if unit.attrib.get("isArbitrary") == "yes" or unit.attrib.get("isSpecial") == "yes"
    }
    return get_ucum_parser(), UcumToPintTransformer(ureg=registry), restricted


def _parse(code):
    from depdigest import is_installed

    if not is_installed("ucumvert"):
        raise ModuleNotFoundError("Install optional UCUM tools with pip install ucumvert==0.3.2")
    if not isinstance(code, str) or not code or code != code.strip():
        raise RecordError(reason="UCUM requires an explicit nonempty case-sensitive code without whitespace")
    parser, transformer, restricted = _tools()
    try:
        tree = parser.parse(code)
        for token in tree.scan_values(lambda value: hasattr(value, "type")):
            if token.type == "ANNOTATION" or (token.type == "FACTOR" and str(token) != "1"):
                raise RecordError(reason="UCUM annotations and arbitrary numeric scale expressions are unsupported")
            if token.type == "UNIT_NON_METRIC" and str(token) in {"10*", "10^"}:
                raise RecordError(reason="arbitrary UCUM powers-of-ten scale expressions are unsupported")
            if token.type in {"UNIT_METRIC", "UNIT_NON_METRIC"} and str(token) not in _ATOMS:
                raise RecordError(reason="UCUM atom is outside the independently qualified physical subset")
            if token.type in {"UNIT_METRIC", "UNIT_NON_METRIC"} and str(token) in restricted:
                if code not in {"Cel", "[degF]", "[degRe]"}:
                    raise RecordError(reason="arbitrary, nonlinear and compound special UCUM units are unsupported")
        return transformer.transform(tree)
    except RecordError:
        raise
    except Exception as exc:
        raise RecordError(reason=f"invalid or unsupported case-sensitive UCUM code {code!r}") from exc


def _converter(code, unit, metadata):
    source = _parse(code)
    target, base, expected = reference(unit, metadata)
    try:
        probes = source._REGISTRY.Quantity(np.array([0.0, 1.0, 2.0]) * source.magnitude, source.units)
        actual = np.asarray(probes.to(base).magnitude, dtype=float)
        if metadata == "temperature: difference":
            actual -= actual[0]
        if (
            actual[1] == actual[0]
            or not np.isfinite(actual).all()
            or not np.allclose(np.diff(actual), actual[1] - actual[0], rtol=1e-12, atol=0)
        ):
            raise RecordError(reason="nonlinear UCUM conversions are outside the physical dialect")
        return target, expected, actual
    except RecordError:
        raise
    except Exception as exc:
        raise RecordError(reason="UCUM and computing units have incompatible physical definitions") from exc


def validate_unit(unit: Any, code: str, *, units_metadata: Optional[str] = None) -> str:
    """Verify and emit an explicit UCUM code for unchanged computing values.

    Parameters
    ----------
    unit : str or pint.Unit
        Computing unit verified against PyUnitWizard's dedicated registry.
    code : str
        Caller-negotiated, case-sensitive UCUM code, retained verbatim.
    units_metadata : str, optional
        Required for temperatures: ``temperature: on_scale`` or
        ``temperature: difference``. Difference computing units must have zero offset.

    Returns
    -------
    str
        The checked code. This operation never guesses a canonical spelling.

    Raises
    ------
    RecordError
        For unsupported syntax/semantics or different dimensions, scale or offset
        (relative tolerance 1e-12). Quantity kinds are never inferred.
    ModuleNotFoundError
        If the optional ucumvert provider is unavailable.

    Examples
    --------
    >>> validate_unit('nanomolar', 'nmol/L')
    'nmol/L'
    """
    _, expected, actual = _converter(code, unit, units_metadata)
    if not np.allclose(actual, expected, rtol=1e-12, atol=0):
        raise RecordError(reason="UCUM code has a different scale or offset from the computing unit")
    return code


def parse_quantity(
    value: Any,
    code: str,
    *,
    unit: Any,
    units_metadata: Optional[str] = None,
    form: Optional[str] = None,
) -> Any:
    """Convert UCUM values into an explicitly required computing unit.

    Parameters
    ----------
    value : numeric scalar or array-like
        Values in the declared UCUM code. Inputs are not modified.
    code : str
        Case-sensitive UCUM code parsed by actual ucumvert.
    unit : str or pint.Unit
        Required computing destination; session units supply no defaults.
    units_metadata : str, optional
        Required temperature semantics, as in ``validate_unit``.
    form : str, optional
        Computing backend; defaults to the session form or Pint.

    Returns
    -------
    quantity
        Converted values, potentially promoted to floating point.

    Raises
    ------
    RecordError
        For unsupported codes, nonnumeric values or incompatible definitions.
    ModuleNotFoundError
        If the optional provider or requested backend is unavailable.

    Examples
    --------
    >>> round(float(parse_quantity(1000, 'nmol/L', unit='micromolar', form='pint').magnitude), 12)
    1.0
    """
    target, expected, actual = _converter(code, unit, units_metadata)
    values = np.asarray(value)
    if values.dtype.kind not in "fiu":
        raise RecordError(reason="UCUM quantity import requires real numeric values")
    converted = (values * (actual[1] - actual[0]) + actual[0] - expected[0]) / (expected[1] - expected[0])
    from pyunitwizard import kernel
    from pyunitwizard.api.conversion import convert
    from pyunitwizard.forms.api_pint import ureg

    return convert(ureg.Quantity(converted, target.units), to_form=form or kernel.default_form or "pint")
