"""Empty record shapes survive codec export with unchanged seals."""

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord


@pytest.mark.parametrize("shape", [(0,), (0, 3), (1, 0, 3)])
@pytest.mark.parametrize("dtype", ["float32", "int32"])
def test_empty_multidimensional_record_base64_round_trip(shape, dtype):
    record = QuantityRecord.from_quantity(puw.quantity(np.empty(shape, dtype=dtype), "nanometer", form="pint"))
    node = record.to_dict(encoding="base64")
    assert node["values"] == {"base64": ""}
    restored = QuantityRecord.from_dict(node)
    assert restored.digest == record.digest
    assert restored.values.shape == shape
    assert restored.values.dtype == np.dtype(dtype)
