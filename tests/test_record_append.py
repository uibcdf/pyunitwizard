"""Verified append produces an independent immutable homogeneous snapshot."""

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord, RecordError


def test_append_converts_units_and_retains_previous_blocks():
    original = QuantityRecord.from_quantity(
        puw.quantity(np.arange(6, dtype=np.float32).reshape(1, 2, 3), "nm", form="pint"), field="coordinates"
    )
    old = original.to_dict()
    with puw.context(default_form="openmm.unit", default_parser="pint"):
        updated = original.append(puw.quantity(np.full((2, 2, 3), 20, dtype=np.float32), "angstrom", form="pint"))
    np.testing.assert_array_equal(updated.values, np.concatenate([original.values, np.full((2, 2, 3), 2)]))
    assert updated.values.dtype == np.dtype("float32")
    assert updated.to_metadata()["manifest"]["blocks"] == [6, 12]
    assert updated.to_metadata()["block_digests"][0] == original.to_metadata()["block_digests"][0]
    assert original.to_dict() == old
    assert QuantityRecord.from_dict(updated.to_dict()).digest == updated.digest
    empty = QuantityRecord.from_quantity(puw.quantity(np.empty((0, 2, 3), dtype=np.float32), "nm", form="pint"))
    assert empty.append(puw.quantity(np.ones((1, 2, 3), dtype=np.float32), "nm", form="pint")).values.shape == (
        1,
        2,
        3,
    )


@pytest.mark.parametrize("failure", ["unit", "shape", "dtype", "bare", "kind", "field", "lossy"])
def test_append_failure_preserves_source(failure):
    record = QuantityRecord.from_quantity(
        puw.quantity(np.ones((1, 3), dtype=np.int32), "nm", form="pint"), field="x", kind="length"
    )
    before = record.to_dict()
    source = puw.quantity(np.ones((1, 3), dtype=np.int32), "nm", form="pint")
    if failure == "unit":
        source = puw.quantity(np.ones((1, 3), dtype=np.int32), "s", form="pint")
    elif failure == "shape":
        source = puw.quantity(np.ones((1, 2), dtype=np.int32), "nm", form="pint")
    elif failure == "dtype":
        source = puw.quantity(np.ones((1, 3), dtype=np.float64), "nm", form="pint")
    elif failure == "bare":
        source = np.ones((1, 3))
    elif failure == "kind":
        source = QuantityRecord.from_quantity(source, field="x", kind="other")
    elif failure == "field":
        source = QuantityRecord.from_quantity(source, field="other", kind="length")
    elif failure == "lossy":
        source = puw.quantity(np.ones((1, 3), dtype=np.int32), "angstrom", form="pint")
    with pytest.raises(RecordError):
        record.append(source)
    assert record.to_dict() == before


def test_affine_append_and_raw_append_rejection():
    record = QuantityRecord.from_quantity(puw.quantity(np.array([0.0], dtype=np.float64), "degC", form="pint"))
    result = record.append(puw.quantity(np.array([298.15]), "K", form="pint"))
    np.testing.assert_allclose(result.values, [0, 25])
    data = result.to_dict()
    data["values"].append(30)
    data["manifest"]["shape"] = [3]
    data["manifest"]["blocks"][-1] += 1
    with pytest.raises(RecordError):
        QuantityRecord.from_dict(data)


def test_conversion_overflow_is_refused():
    record = QuantityRecord.from_quantity(puw.quantity(np.array([1], dtype=np.float32), "nm", form="pint"))
    with pytest.raises(RecordError, match="overflow"):
        record.append(puw.quantity(np.array([np.finfo(np.float32).max], dtype=np.float32), "m", form="pint"))
