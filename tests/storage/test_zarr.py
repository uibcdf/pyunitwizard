"""Verified Zarr snapshots, including bounded partial reads."""

import json

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord, RecordError, metadata_digest
from pyunitwizard.storage import zarr as binding

zarr = pytest.importorskip("zarr")


@pytest.mark.parametrize("shape", [(7, 2, 3), (), (0, 3), (2, 0, 3)])
def test_roundtrip_and_partial_read(tmp_path, shape):
    values = np.arange(np.prod(shape, dtype=int), dtype=np.float32).reshape(shape)
    with puw.context(default_form="openmm.unit", default_parser="pint"):
        source = QuantityRecord.from_quantity(puw.quantity(values, "nm", form="pint"), field="coordinates")
        root = zarr.open_group(str(tmp_path / "records"), mode="w")
        group = binding.write(root, "coordinates", source, chunk_rows=2)
        result = binding.read(group, field="coordinates", unit="angstrom")
        assert result.digest == source.digest
        np.testing.assert_array_equal(result.values, values)
        if values.ndim:
            subset = binding.read(group, selection=slice(1, 4), unit="nm")
            np.testing.assert_array_equal(subset.values, values[1:4])
    reopened = zarr.open_group(str(tmp_path / "records"), mode="r")
    assert binding.read(reopened["coordinates"], unit="nm").digest == source.digest


def test_partial_reads_only_selected_chunks(tmp_path, monkeypatch):
    source = QuantityRecord.from_quantity(puw.quantity(np.arange(30).reshape(10, 3), "nm", form="pint"))
    group = binding.write(zarr.open_group(str(tmp_path / "data"), mode="w"), "x", source, chunk_rows=2)
    original = zarr.Array.__getitem__
    reads = []

    def observe(array, key):
        reads.append(key)
        return original(array, key)

    monkeypatch.setattr(zarr.Array, "__getitem__", observe)
    result = binding.read(group, selection=slice(3, 5), unit="nm")
    np.testing.assert_array_equal(result.values, source.values[3:5])
    assert reads == [slice(2, 4), slice(4, 6)]
    group["values"][8, 0] = 999
    binding.read(group, selection=slice(0, 2), unit="nm")
    with pytest.raises(RecordError):
        binding.read(group, unit="nm")


@pytest.mark.parametrize("edit", ["values", "unit", "missing", "shape", "chunks", "extra", "duplicate", "headers"])
def test_tampering_is_refused(tmp_path, edit):
    source = QuantityRecord.from_quantity(puw.quantity(np.arange(12).reshape(4, 3), "nm", form="pint"))
    group = binding.write(zarr.open_group(str(tmp_path / "data"), mode="w"), "x", source, chunk_rows=2)
    if edit == "values":
        group["values"][0, 0] = 999
    elif edit == "unit":
        group.attrs["units"] = "meter"
    elif edit == "missing":
        del group.attrs["pyunitwizard"]
    elif edit == "shape":
        group["values"].resize((5, 3))
    elif edit == "chunks":
        data = group["values"][:]
        del group["values"]
        group.create_array("values", data=data, chunks=(1, 3))
    elif edit == "extra":
        group.create_group("extra")
    elif edit == "duplicate":
        group["values"].attrs["units"] = "nm"
    else:
        node = json.loads(group.attrs["pyunitwizard"])
        node["chunks"].reverse()
        group.attrs["pyunitwizard"] = json.dumps(node)
    with pytest.raises(RecordError):
        binding.read(group, unit="nm")


def test_expectations_and_failure_leave_existing_data_untouched(tmp_path, monkeypatch):
    root = zarr.open_group(str(tmp_path / "data"), mode="w")
    source = QuantityRecord.from_quantity(puw.quantity([1.0, 2.0], "nm", form="pint"), field="x")
    group = binding.write(root, "x", source, chunk_rows=1)
    for kwargs in ({"field": "other"}, {"unit": "second"}, {"kind": "other"}):
        with pytest.raises(RecordError):
            binding.read(group, **kwargs)
    with pytest.raises(RecordError):
        binding.read(group)
    with pytest.raises(RecordError):
        binding.write(root, "x", source)
    original = zarr.Group.create_array

    def fail(*args, **kwargs):
        raise OSError("injected write failure")

    monkeypatch.setattr(zarr.Group, "create_array", fail)
    with pytest.raises(RecordError):
        binding.write(root, "failed", source)
    monkeypatch.setattr(zarr.Group, "create_array", original)
    assert set(root.keys()) == {"x"}
    assert binding.read(group, unit="nm").digest == source.digest


def test_missing_zero_chunk_is_not_replaced_by_implicit_fill(tmp_path):
    source = QuantityRecord.from_quantity(puw.quantity(np.zeros((4, 3)), "nm", form="pint"))
    group = binding.write(zarr.open_group(str(tmp_path / "data"), mode="w"), "x", source, chunk_rows=2)
    chunk_files = [p for p in (tmp_path / "data" / "x" / "values" / "c").rglob("*") if p.is_file()]
    assert chunk_files
    chunk_files[0].unlink()
    with pytest.raises(RecordError):
        binding.read(group, unit="nm")


def test_empty_selection_still_checks_the_descriptor(tmp_path):
    source = QuantityRecord.from_quantity(puw.quantity(np.ones((4, 3)), "nm", form="pint"))
    group = binding.write(zarr.open_group(str(tmp_path / "data"), mode="w"), "x", source, chunk_rows=2)
    node = json.loads(group.attrs["pyunitwizard"])
    node["record"]["manifest"]["si"]["factor"] = 1
    node.pop("digest")
    node["digest"] = metadata_digest(node)
    group.attrs["pyunitwizard"] = json.dumps(node)
    with pytest.raises(RecordError):
        binding.read(group, selection=slice(0, 0), unit="nm")
