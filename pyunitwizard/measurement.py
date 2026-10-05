"""Inert scalar measurements with stated uncertainty (provisional, #90).

This separate envelope binds meaning to an existing quantity bundle. It does not
estimate uncertainty, propagate errors, or change the qrec/0.3 wire format.
"""

from __future__ import annotations

import copy
import math
from typing import Any, Dict, Literal, Mapping, Optional

import numpy as np

from ._private.exceptions import RecordError
from .record import QuantityRecordBundle, _descriptor, _digest, _registry, _to_pint

__all__ = ["MEASUREMENT_FORMAT", "MeasurementRecord"]
MEASUREMENT_FORMAT = "qrec-measurement/0.1"
UncertaintyKind = Literal["sd", "sem", "unspecified", "ci"]


def _validate(metadata: Mapping[str, Any], quantities: Mapping[str, Any]) -> None:
    """Validate the stated association, never infer a statistical relationship."""
    if set(metadata) != {"field", "kind", "level", "n"}:
        raise RecordError(reason="measurement metadata must contain field, kind, level and n")
    if metadata["field"] is not None and not isinstance(metadata["field"], str):
        raise RecordError(reason="measurement field must be a string or None")
    kind, level, n = metadata["kind"], metadata["level"], metadata["n"]
    if kind not in ("sd", "sem", "unspecified", "ci"):
        raise RecordError(reason="stated uncertainty kind must be sd, sem, unspecified or ci")
    expected = {"value", "lower", "upper"} if kind == "ci" else {"value", "half_width"}
    if set(quantities) != expected:
        raise RecordError(reason=f"{kind!r} requires exactly {sorted(expected)}")
    if n is not None and (type(n) is not int or not 0 < n < 2**63):
        raise RecordError(reason="n must be a positive signed 64-bit integer, not a boolean")
    if level is not None and (
        kind != "ci" or type(level) not in (int, float) or not 0 < level < 1 or not math.isfinite(level)
    ):
        raise RecordError(reason="level is a fraction strictly between zero and one, for ci only")
    value = quantities["value"]
    for name, quantity in quantities.items():
        magnitude = np.asarray(quantity.magnitude)
        if magnitude.ndim != 0 or magnitude.dtype.kind not in "fiu" or not np.isfinite(magnitude).all():
            raise RecordError(reason="stated measurements require finite scalar quantities", field=name)
        if quantity.dimensionality != value.dimensionality:
            raise RecordError(reason="uncertainty must have the value's dimensionality", field=name)
    if kind == "ci":
        try:
            lower = quantities["lower"].to(value.units).magnitude
            upper = quantities["upper"].to(value.units).magnitude
        except Exception as exc:
            raise RecordError(reason="interval bounds must be compatible point quantities") from exc
        if lower > upper:
            raise RecordError(reason="confidence interval lower bound exceeds upper bound")
    else:
        spread = quantities["half_width"]
        if _descriptor(str(spread.units))["si"]["offset"] != 0:
            raise RecordError(reason="a half-width requires a difference unit, such as delta_degC or kelvin")
        if spread.magnitude < 0:
            raise RecordError(reason="a half-width cannot be negative")


class MeasurementRecord:
    """A finite scalar value bound to its stated uncertainty under one seal.

    The API and ``qrec-measurement/0.1`` envelope are provisional. Use the
    existing quantity forms for computation. Source precision remains with the
    consumer; neither ``n`` nor a confidence level implies a distribution.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> from pyunitwizard.measurement import MeasurementRecord
    >>> record = MeasurementRecord.from_quantity(
    ...     puw.quantity(12, 'nM'), kind='sd', half_width=puw.quantity(3, 'nM'), n=3)
    >>> result = record.to_quantities(unit='uM', form='pint')
    """

    __slots__ = ("_metadata", "_bundle", "_digest")

    def __init__(self) -> None:
        raise TypeError("build a MeasurementRecord with from_quantity() or from_dict()")

    @classmethod
    def _new(cls, metadata, bundle, digest) -> "MeasurementRecord":
        record = object.__new__(cls)
        record._metadata, record._bundle, record._digest = copy.deepcopy(metadata), bundle, digest
        return record

    @staticmethod
    def _seal(metadata, bundle) -> str:
        return _digest(
            {"format": MEASUREMENT_FORMAT, "metadata": metadata}, bundle.to_dict()["digest"].encode("ascii")
        )

    @classmethod
    def from_quantity(
        cls,
        quantity: Any,
        *,
        kind: UncertaintyKind,
        half_width: Optional[Any] = None,
        lower: Optional[Any] = None,
        upper: Optional[Any] = None,
        level: Optional[float] = None,
        n: Optional[int] = None,
        field: Optional[str] = None,
    ) -> "MeasurementRecord":
        """Seal a scalar statement without computing a spread or interval.

        Parameters
        ----------
        quantity : quantity
            Finite scalar measured value, in any supported form.
        kind : {'sd', 'sem', 'unspecified', 'ci'}
            Meaning stated by the source. Bare ± uses ``unspecified``.
        half_width : quantity, optional
            Nonnegative spread for SD, SEM or unspecified. Affine temperatures
            require difference units (for example ``delta_degC``).
        lower, upper : quantity, optional
            Ordered interval bounds, required together for CI.
        level : float, optional
            Stated confidence fraction, only for CI. Never inferred.
        n : int, optional
            Positive stated replicate count. Never used to transform the spread.
        field : str, optional
            Application field for the reader's expectation check.

        Returns
        -------
        MeasurementRecord
            An independent sealed scalar snapshot.

        Raises
        ------
        RecordError
            For an incomplete, invalid or dimensionally inconsistent statement.
        """
        metadata = {"field": field, "kind": kind, "level": level, "n": n}
        quantities = {"value": _to_pint(quantity)}
        for name, item in (("half_width", half_width), ("lower", lower), ("upper", upper)):
            if item is not None:
                quantities[name] = _to_pint(item)
        _validate(metadata, quantities)
        bundle = QuantityRecordBundle.from_quantities(quantities)
        return cls._new(metadata, bundle, cls._seal(metadata, bundle))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MeasurementRecord":
        """Verify the envelope, nested bundle and semantic association.

        Parameters
        ----------
        data : mapping
            Stored ``qrec-measurement/0.1`` document.

        Returns
        -------
        MeasurementRecord
            Verified independent snapshot.

        Raises
        ------
        RecordError
            For missing data, altered seals or invalid semantics. No defaults
            or statistical inference repair an incomplete stored document.
        """
        if not isinstance(data, Mapping) or data.get("format") != MEASUREMENT_FORMAT:
            raise RecordError(reason=f"not a {MEASUREMENT_FORMAT!r} measurement")
        if set(data) != {"format", "metadata", "bundle", "digest"} or not isinstance(data["metadata"], Mapping):
            raise RecordError(reason="incomplete measurement envelope")
        metadata = copy.deepcopy(dict(data["metadata"]))
        bundle = QuantityRecordBundle.from_dict(data["bundle"])
        digest = cls._seal(metadata, bundle)
        if data["digest"] != digest:
            raise RecordError(reason="measurement association was changed outside the codec")
        _validate(metadata, bundle.to_quantities(form="pint"))
        return cls._new(metadata, bundle, digest)

    def to_dict(self) -> Dict[str, Any]:
        """Return a detached strict-JSON representation.

        Returns
        -------
        dict
            Format, metadata, sealed quantity bundle and association digest.
        """
        return {
            "format": MEASUREMENT_FORMAT,
            "metadata": copy.deepcopy(self._metadata),
            "bundle": self._bundle.to_dict(),
            "digest": self._digest,
        }

    def to_quantities(
        self,
        *,
        field: Optional[str] = None,
        kind: Optional[UncertaintyKind] = None,
        unit: Optional[str] = None,
        dimensionality: Optional[Dict[str, int]] = None,
        form: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Read the original components after checking reader expectations.

        Parameters
        ----------
        field, kind : str, optional
            Required field and stated uncertainty meaning.
        unit : str, optional
            Negotiated point unit. Half-widths use its difference unit, so
            affine offsets apply to points/bounds only.
        dimensionality : dict, optional
            Expected value dimensions in PyUnitWizard notation.
        form : str, optional
            Output computing form; otherwise the session default or Pint.

        Returns
        -------
        dict
            ``value`` with ``half_width`` or ``lower`` and ``upper`` quantities.

        Raises
        ------
        RecordError
            For wrong expectations or unsupported unit/backend conversion.
        """
        from . import kernel
        from .api.conversion import convert
        from .api.validation import check

        for name, wanted in (("field", field), ("kind", kind)):
            if wanted is not None and self._metadata[name] != wanted:
                raise RecordError(reason=f"expected {name} {wanted!r}, stored {self._metadata[name]!r}")
        quantities = self._bundle.to_quantities(form="pint")
        if dimensionality is not None and not check(quantities["value"], dimensionality=dimensionality):
            raise RecordError(reason=f"expected dimensionality {dimensionality}")
        try:
            if unit is not None:
                # Subtraction derives the target difference unit without a temperature table.
                spread_unit = (_registry().Quantity(1, unit) - _registry().Quantity(0, unit)).units
                quantities = {
                    name: quantity.to(spread_unit if name == "half_width" else unit)
                    for name, quantity in quantities.items()
                }
            target = form or kernel.default_form or "pint"
            return {
                name: quantity if target == "pint" else convert(quantity, to_form=target)
                for name, quantity in quantities.items()
            }
        except Exception as exc:
            raise RecordError(reason=f"cannot read measurement with unit {unit!r} and form {form!r}") from exc

    @property
    def field(self) -> Optional[str]:
        """The application field, or None."""
        return self._metadata["field"]

    @property
    def kind(self) -> UncertaintyKind:
        """The stated uncertainty meaning."""
        return self._metadata["kind"]

    @property
    def level(self) -> Optional[float]:
        """The stated confidence fraction, or None."""
        return self._metadata["level"]

    @property
    def n(self) -> Optional[int]:
        """The stated replicate count, or None."""
        return self._metadata["n"]

    @property
    def digest(self) -> str:
        """The seal binding association metadata and quantity bundle."""
        return self._digest
