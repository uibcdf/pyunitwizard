"""Receiving-boundary regressions from retained MolSysMT/Sabueso fixtures."""

import json
from pathlib import Path

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord

DATA = Path(__file__).parent / "data"


def test_existing_molecular_coordinates_zarr_and_append(tmp_path):
    zarr = pytest.importorskip("zarr")
    from pyunitwizard.storage import zarr as binding

    fixture = json.loads((DATA / "h5msm_quantity_boundary.json").read_text())
    values = np.array(fixture["values"], dtype=fixture["dtype"])
    with puw.context(default_form="openmm.unit", default_parser="pint"):
        source = QuantityRecord.from_quantity(puw.quantity(values, fixture["unit"], form="pint"), field="coordinates")
        incoming = puw.quantity(values * np.float32(10), "angstrom", form="pint")
        combined = source.append(incoming)
        group = binding.write(
            zarr.open_group(str(tmp_path / "trajectory"), mode="w"), "coordinates", combined, chunk_rows=1
        )
        result = binding.read(group, selection=slice(1, 2), field="coordinates", dimensionality={"[L]": 1})
        np.testing.assert_allclose(result.to_quantity(unit="nanometer", form="pint").magnitude, values, rtol=1e-6)
        assert combined.values.dtype == values.dtype


def test_existing_heterogeneous_activity_results(tmp_path):
    pytest.importorskip("pyarrow")
    from pyunitwizard.storage import arrow

    fixture = json.loads((DATA / "sabueso_activity_quantities.json").read_text())
    observations = fixture["observations"]
    quantities = [puw.quantity(row["value"], row["unit"], form="pint") for row in observations]
    with puw.context(default_form="openmm.unit", default_parser="pint"):
        source = QuantityRecord.from_tagged(quantities, field="activities", kinds=[r["kind"] for r in observations])
        arrow.write(tmp_path / "activities.parquet", source)
        restored = arrow.read(
            tmp_path / "activities.parquet",
            field="activities",
            units=["nM", "nM", "percent", "nM", "nM"],
            kinds=["Ki", "IC50", "Inhibition", "Kd", "ED50"],
        )
        assert restored.digest == source.digest
        for index, group in restored.split().items():
            expected = [
                row["value"] for row in observations if row["unit"] == group.unit and row["kind"] == group.kind
            ]
            np.testing.assert_array_equal(group.values, expected)
            assert np.count_nonzero(restored.codes == index) == len(expected)
