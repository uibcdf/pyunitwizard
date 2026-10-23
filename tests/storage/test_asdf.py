"""Actual native Astropy quantities and sealed snapshots in real ASDF files."""

import json
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("asdf")
pytest.importorskip("asdf_astropy")
from astropy import units as u

from pyunitwizard.forms.api_pint import ureg
from pyunitwizard.record import QuantityRecord, RecordError, metadata_digest
from pyunitwizard.storage import asdf


@pytest.mark.parametrize("dtype", ["float32", "float64", "int16", "int32", "int64", "uint8", "uint16"])
@pytest.mark.parametrize("shape", [(), (0, 3), (2, 3)])
def test_native_asdf_round_trip_retains_exact_record_and_array(tmp_path, dtype, shape):
    import asdf as provider

    values = np.zeros(shape, dtype=dtype) if 0 in shape else np.arange(np.prod(shape) or 1, dtype=dtype).reshape(shape)
    record = QuantityRecord.from_quantity(ureg.Quantity(values, "nanometer"), field="position", kind="length")
    path = tmp_path / "quantity.asdf"
    asdf.write(path, record)
    with provider.open(path, lazy_load=False) as archive:
        native = archive["quantity"]
        assert isinstance(native, u.Quantity)
        assert native.unit == u.nm
        assert native.dtype == values.dtype
        np.testing.assert_array_equal(native.value, values)
    restored = asdf.read(path, field="position", unit="nanometer", kind="length")
    assert restored == record
    assert restored.digest == record.digest
    assert restored.values.dtype == values.dtype


def test_actual_gaia_proper_motion_archive_and_kind(tmp_path):
    data = json.loads((Path(__file__).parents[1] / "data" / "gaia_proper_motion.json").read_text())
    assert len(data["source_ids"]) == 6
    # This explicit astronomical conversion belongs to the consumer. A unit
    # bridge must not guess sky geometry, reference epochs or physical kinds.
    native = u.Quantity(data["values"], data["unit"]).to(u.radian / u.second)
    kind = "http://qudt.org/vocab/quantitykind/AngularVelocity"
    record = QuantityRecord.from_quantity(native, field="proper_motion", kind=kind)
    asdf.write(tmp_path / "gaia.asdf", record)
    restored = asdf.read(tmp_path / "gaia.asdf", unit="radian / second", kind=kind, field="proper_motion")
    assert restored == record
    np.testing.assert_allclose(restored.to_quantity(form="astropy.units").to_value(u.mas / u.yr), data["values"])
    with pytest.raises(RecordError):
        asdf.read(tmp_path / "gaia.asdf", unit="hertz", kind="http://qudt.org/vocab/quantitykind/Frequency")


def test_detached_tree_and_explicit_expectations():
    record = QuantityRecord.from_quantity(ureg.Quantity([1.0, 2.0], "meter"))
    tree = asdf.to_tree(record)
    assert asdf.from_tree(tree, dimensionality={"[L]": 1}) == record
    with pytest.raises(RecordError):
        asdf.from_tree(tree)
    with pytest.raises(RecordError):
        asdf.from_tree(tree, unit="second")
    tree["quantity"][0] = 5 * u.m
    np.testing.assert_array_equal(record.values, [1, 2])
    with pytest.raises(RecordError):
        asdf.from_tree(tree, unit="meter")


@pytest.mark.parametrize("change", ["unit", "native_label", "metadata", "dtype", "shape", "extra", "missing"])
def test_corrupt_or_relabelled_native_tree_is_refused(change):
    tree = asdf.to_tree(QuantityRecord.from_quantity(ureg.Quantity(np.array([1, 2], dtype="int16"), "nanometer")))
    if change == "unit":
        tree["quantity"] = u.Quantity([1, 2], u.m, dtype="int16")
    elif change == "native_label":
        tree["quantity"] = u.Quantity([1, 2], u.AA, dtype="int16")
        header = tree["pyunitwizard"]
        header["native_unit"] = tree["quantity"].unit.to_string()
        header.pop("digest")
        header["digest"] = metadata_digest(header)
    elif change == "metadata":
        tree["pyunitwizard"]["record"]["manifest"]["field"] = "different"
    elif change == "dtype":
        tree["quantity"] = u.Quantity([1, 2], u.nm, dtype="float64")
    elif change == "shape":
        tree["quantity"] = tree["quantity"].reshape(1, 2)
    elif change == "extra":
        tree["pyunitwizard"]["fallback_unit"] = "meter"
    else:
        del tree["pyunitwizard"]
    with pytest.raises(RecordError):
        asdf.from_tree(tree, unit="nanometer")


def test_snapshot_publication_never_overwrites_and_cleans_owned_files(tmp_path, monkeypatch):
    import asdf as provider

    record = QuantityRecord.from_quantity(ureg.Quantity([1.0], "meter"))
    path = tmp_path / "archive.asdf"
    path.write_bytes(b"existing")
    with pytest.raises(RecordError):
        asdf.write(path, record)
    assert path.read_bytes() == b"existing"
    assert sorted(p.name for p in tmp_path.iterdir()) == ["archive.asdf"]

    def fail(*args, **kwargs):
        raise OSError("injected disk failure")

    monkeypatch.setattr(provider.AsdfFile, "write_to", fail)
    with pytest.raises(RecordError, match="injected disk failure"):
        asdf.write(tmp_path / "failed.asdf", record)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["archive.asdf"]


def test_unsealed_native_archive_is_never_silently_promoted(tmp_path):
    import asdf as provider

    path = tmp_path / "native.asdf"
    with provider.AsdfFile({"quantity": [1, 2] * u.nm}) as archive:
        archive.write_to(path)
    with pytest.raises(RecordError):
        asdf.read(path, unit="nanometer")


def test_unsupported_layout_and_affine_unit_are_explicit():
    tagged = QuantityRecord.from_tagged([ureg.Quantity(1, "meter"), ureg.Quantity(1, "second")])
    with pytest.raises(RecordError):
        asdf.to_tree(tagged)
    affine = QuantityRecord.from_quantity(ureg.Quantity([20.0], "degree_Celsius"))
    with pytest.raises(RecordError):
        asdf.to_tree(affine)


def test_resealed_native_frequency_cannot_be_relabelled_as_activity():
    record = QuantityRecord.from_quantity(ureg.Quantity([1.0], "hertz"), kind="frequency")
    tree = asdf.to_tree(record)
    tree["quantity"] = u.Quantity([1.0], u.Bq)
    header = tree["pyunitwizard"]
    header["native_unit"] = tree["quantity"].unit.to_string()
    header.pop("digest")
    header["digest"] = metadata_digest(header)
    with pytest.raises(RecordError):
        asdf.from_tree(tree, unit="hertz", kind="frequency")
