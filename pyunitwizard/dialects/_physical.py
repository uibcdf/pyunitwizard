"""Shared computing-side affine SI verification for optional physical dialects."""

import numpy as np

from pyunitwizard._private.exceptions import RecordError

TEMPERATURE_METADATA = {"temperature: on_scale", "temperature: difference"}


def reference(unit, metadata):
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
            raise RecordError(reason="fractional powers are outside the bounded physical-unit dialect")
        temperature = "K" in exponents
        if temperature:
            if metadata not in TEMPERATURE_METADATA:
                raise RecordError(reason="temperature requires explicit on_scale or difference units_metadata")
            if metadata == "temperature: on_scale" and exponents != {"K": 1}:
                raise RecordError(reason="compound on-scale temperatures cannot be converted from units alone")
            if metadata == "temperature: on_scale" and str(quantity.units).startswith("delta_"):
                raise RecordError(reason="an on-scale temperature cannot use a computing difference unit")
        elif metadata is not None:
            raise RecordError(reason="units_metadata is only valid for temperature units")
        points = np.asarray(quantity.to_base_units().magnitude, dtype=float)
        if not np.allclose(np.diff(points), record.si["factor"], rtol=1e-12, atol=0):
            raise RecordError(reason="nonlinear computing units are outside the physical-unit dialect")
        if metadata == "temperature: difference" and points[0] != 0:
            raise RecordError(reason="a temperature difference requires a computing difference unit")
        return quantity, base, points
    except RecordError:
        raise
    except Exception as exc:
        raise RecordError(reason="invalid computing unit for a physical-unit dialect") from exc
