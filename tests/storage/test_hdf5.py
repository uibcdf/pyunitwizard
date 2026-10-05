"""Verified HDF5 snapshots refuse edits made outside the codec."""

import json

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import RecordError
from pyunitwizard.record import QuantityRecord
from pyunitwizard.storage import hdf5

h5py = pytest.importorskip("h5py")
pytest.importorskip("cf_units")


@pytest.mark.parametrize(
    "values,unit,spelling,metadata",
    [
        (np.arange(6, dtype=np.float32).reshape(1, 2, 3), "nanometer", "nm", None),
        (np.array([1, 2, 3], dtype=np.int32), "picosecond", "ps", None),
        (np.arange(6, dtype=np.float64).reshape(2, 3), "nanometer / picosecond", "nm ps-1", None),
        (np.array([1.0, 2.0]), "nanometer**2", "nm2", None),
        (3.0, "kilojoule / mole", "kJ mol-1", None),
        (25.0, "degree_Celsius", "degC", "temperature: on_scale"),
        (np.array([1.0, 2.0]), "delta_degree_Celsius", "degC", "temperature: difference"),
        (np.array([np.nan, np.inf, -np.inf]), "meter", "m", None),
        (np.array([], dtype=np.float32).reshape(0, 3), "nanometer", "nm", None),
    ],
)
def test_scalar_array_dtype_affine_and_nonfinite_round_trip(tmp_path, values, unit, spelling, metadata):
    source = QuantityRecord.from_quantity(puw.quantity(values, unit, form="pint"), field="sample")
    with h5py.File(tmp_path / "record.h5", "w") as file:
        group = hdf5.write(file, "sample", source, cf_unit=spelling, units_metadata=metadata)
        result = hdf5.read(group, field="sample", unit=unit, units_metadata=metadata)
        assert result.digest == source.digest
        assert result.values.dtype == source.values.dtype
        assert result.values.shape == source.values.shape
        assert np.array_equal(result.values, source.values, equal_nan=True)
        assert dict(group["values"].attrs) == {}
        assert group.attrs["units"] == spelling
        assert np.array_equal(group["values"][()], source.values, equal_nan=True)
    with h5py.File(tmp_path / "record.h5") as file:
        assert hdf5.read(file["sample"], field="sample", units_metadata=metadata).digest == source.digest


@pytest.mark.parametrize(
    "edit",
    [
        "value",
        "units",
        "manifest",
        "binding",
        "missing_manifest",
        "missing_units",
        "shape",
        "dtype",
        "raw_append",
        "missing_values",
        "extra_dataset",
        "duplicate_unit",
        "temperature",
    ],
)
def test_edits_missing_metadata_and_raw_appends_are_refused(tmp_path, edit):
    source = QuantityRecord.from_quantity(
        puw.quantity(np.array([1.0, 2.0]), "nanometer", form="pint"), field="coordinates"
    )
    with h5py.File(tmp_path / "edit.h5", "w") as file:
        group = hdf5.write(file, "coordinates", source, cf_unit="nm")
        if edit == "value":
            group["values"][0] = 10
        elif edit == "units":
            group.attrs["units"] = "m"
        elif edit == "manifest":
            node = json.loads(group.attrs["pyunitwizard"])
            node["record"]["manifest"]["field"] = "other"
            group.attrs["pyunitwizard"] = json.dumps(node)
        elif edit == "binding":
            node = json.loads(group.attrs["pyunitwizard"])
            node["units"] = "m"
            group.attrs["pyunitwizard"] = json.dumps(node)
        elif edit == "missing_manifest":
            del group.attrs["pyunitwizard"]
        elif edit == "missing_units":
            del group.attrs["units"]
        elif edit in ["shape", "dtype", "raw_append"]:
            data = group["values"][()]
            del group["values"]
            if edit == "shape":
                data = data.reshape(1, 2)
            if edit == "dtype":
                data = data.astype(np.float32)
            if edit == "raw_append":
                data = np.append(data, 3.0)
            group.create_dataset("values", data=data)
        elif edit == "missing_values":
            del group["values"]
        elif edit == "extra_dataset":
            group.create_dataset("extra", data=[1])
        elif edit == "duplicate_unit":
            group["values"].attrs["unit"] = "m"
        elif edit == "temperature":
            group.attrs["units_metadata"] = "temperature: difference"
        with pytest.raises(RecordError):
            hdf5.read(group)


def test_reader_expectations_refuse_wrong_field_dimensions_and_kind(tmp_path):
    record = QuantityRecord.from_quantity(
        puw.quantity([1.0, 2.0], "nanometer", form="pint"), field="coordinates", kind="position"
    )
    with h5py.File(tmp_path / "handshake.h5", "w") as file:
        group = hdf5.write(file, "q", record, cf_unit="nm")
        for kwargs in [{"field": "other"}, {"unit": "second"}, {"kind": "velocity"}, {"dimensionality": {"[T]": 1}}]:
            with pytest.raises(RecordError):
                hdf5.read(group, **kwargs)
        with puw.context(standard_units=["meter", "second"]):
            assert hdf5.read(group, field="coordinates", kind="position").unit == "nanometer"


def test_invalid_write_leaves_parent_unchanged_and_never_overwrites(tmp_path):
    record = QuantityRecord.from_quantity(puw.quantity(1.0, "nanometer", form="pint"), field="coordinates")
    with h5py.File(tmp_path / "atomic.h5", "w") as file:
        with pytest.raises(RecordError):
            hdf5.write(file, "bad", record, cf_unit="m")
        assert list(file) == []
        hdf5.write(file, "q", record, cf_unit="nm")
        with pytest.raises(RecordError):
            hdf5.write(file, "q", record, cf_unit="nm")
        assert hdf5.read(file["q"]).digest == record.digest
        for name in ["a/b", "", "..", "."]:
            with pytest.raises(RecordError):
                hdf5.write(file, name, record, cf_unit="nm")
        assert list(file) == ["q"]


def test_partial_write_failure_removes_staging_group(tmp_path, monkeypatch):
    record = QuantityRecord.from_quantity(puw.quantity(1.0, "nanometer", form="pint"))
    original = h5py.Group.create_dataset

    def fail(group, *args, **kwargs):
        original(group, *args, **kwargs)
        raise OSError("simulated interrupted writer")

    with h5py.File(tmp_path / "failure.h5", "w") as file:
        monkeypatch.setattr(h5py.Group, "create_dataset", fail)
        with pytest.raises(RecordError):
            hdf5.write(file, "q", record, cf_unit="nm")
        assert list(file) == []


def test_published_h5msm_coordinates_keep_dtype_values_and_unit_under_another_policy(tmp_path):
    from pathlib import Path

    fixture = json.loads((Path(__file__).resolve().parents[1] / "data" / "h5msm_quantity_boundary.json").read_text())
    values = np.asarray(fixture["values"], dtype=fixture["dtype"])
    assert list(values.shape) == fixture["shape"]
    source = QuantityRecord.from_quantity(puw.quantity(values, fixture["unit"], form="pint"), field="coordinates")
    with h5py.File(tmp_path / "consumer.h5", "w") as file:
        group = hdf5.write(file, "coordinates", source, cf_unit="nm")
        with puw.context(standard_units=["angstrom", "second"]):
            result = hdf5.read(group, field="coordinates", unit="nanometer", dimensionality={"[L]": 1})
            assert result.digest == source.digest
            assert result.values.dtype == np.float32
            assert np.array_equal(result.values, values)
            assert np.allclose(result.to_quantity(unit="angstrom", form="pint").magnitude, values * 10)


def test_temperature_reader_must_declare_the_expected_semantics(tmp_path):
    record = QuantityRecord.from_quantity(puw.quantity(25.0, "kelvin", form="pint"), field="temperature")
    with h5py.File(tmp_path / "temperature.h5", "w") as file:
        group = hdf5.write(file, "temperature", record, cf_unit="K", units_metadata="temperature: difference")
        with pytest.raises(RecordError):
            hdf5.read(group)
        with pytest.raises(RecordError):
            hdf5.read(group, units_metadata="temperature: on_scale")
        with pytest.raises(RecordError):
            hdf5.read(group, units_metadata="temperature: difference", unit="degree_Celsius")
        assert (
            hdf5.read(group, units_metadata="temperature: difference", unit="delta_degree_Celsius").digest
            == record.digest
        )
