"""The measurement tool actually compares matching scientific payloads."""

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord


def test_measurement_comparison_preserves_input_and_records_raw_samples():
    pytest.importorskip("zarr")
    pytest.importorskip("pyarrow")
    from devtools.benchmark_record_extensions import compare_storage

    record = QuantityRecord.from_quantity(
        puw.quantity(np.arange(24, dtype=np.float32).reshape(4, 2, 3), "nm", form="pint")
    )
    digest = record.digest
    report = compare_storage(record, repeats=2, chunk_rows=2)
    assert report["shape"] == [4, 2, 3]
    assert len(report["seconds"]["append"]) == 2
    assert record.digest == digest
