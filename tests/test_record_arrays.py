"""Storage-neutral codec operations keep metadata and typed payloads bound."""

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord, RecordError, metadata_digest


def test_typed_array_restoration_and_selection():
    source = QuantityRecord.from_quantity(
        puw.quantity(np.arange(24, dtype=np.float32).reshape(4, 2, 3), "nm", form="pint"), field="coordinates"
    )
    metadata = source.to_metadata()
    assert "values" not in metadata
    restored = QuantityRecord.from_array(source.values, metadata=metadata)
    assert restored.digest == source.digest
    for selection in (slice(1, 3), slice(0, 0)):
        subset = source.select(selection)
        np.testing.assert_array_equal(subset.values, source.values[selection])
        assert subset.field == source.field and subset.unit == source.unit
        assert subset.values.dtype == source.values.dtype
    with pytest.raises(RecordError):
        QuantityRecord.from_array(source.values.astype(np.float64), metadata=metadata)
    values = source.values.copy()
    values[0, 0, 0] = 100
    with pytest.raises(RecordError):
        QuantityRecord.from_array(values, metadata=metadata)
    metadata["manifest"]["unit"] = "meter"
    assert source.unit == "nanometer"


def test_binding_digest_is_deterministic_and_sensitive():
    assert metadata_digest({"a": 1, "b": 2}) == metadata_digest({"b": 2, "a": 1})
    assert metadata_digest({"a": 1}) != metadata_digest({"a": 2})
