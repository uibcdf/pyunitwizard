"""One inert class with explicit heterogeneous unit descriptors and codes."""

import copy

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard.record import TAGGED_FORMAT, QuantityRecord, RecordError


def test_tagged_roundtrip_requires_explicit_unit_and_preserves_source_values():
    with puw.context(default_form="openmm.unit", default_parser="pint"):
        source = QuantityRecord.from_tagged(
            [puw.quantity(np.float32(1), "nm", form="pint"), puw.quantity(np.float32(20), "angstrom", form="pint")],
            field="distances",
            kinds=["length", "length"],
        )
        assert isinstance(source, QuantityRecord)
        assert source.layout == "tagged" and source.to_dict()["manifest"]["format"] == TAGGED_FORMAT
        assert source.values.dtype == np.dtype("float32")
        np.testing.assert_array_equal(source.values, [1, 20])
        with pytest.raises(RecordError, match="explicit"):
            source.to_quantity()
        result = source.to_quantity(unit="nm", field="distances", kind="length", form="pint")
        np.testing.assert_allclose(result.magnitude, [1, 2])
        for encoding in ("json", "base64"):
            restored = QuantityRecord.from_dict(source.to_dict(encoding=encoding))
            assert restored.digest == source.digest
            np.testing.assert_array_equal(restored.codes, source.codes)
        with pytest.raises(ValueError):
            source.codes.setflags(write=True)
        desc = source.descriptors
        desc[0]["unit"] = "meter"
        assert source.descriptors[0]["unit"] == "nanometer"


def test_incompatible_dimensions_and_kinds_require_splitting():
    source = QuantityRecord.from_tagged(
        [puw.quantity(15000, "nM", form="pint"), puw.quantity(50, "percent", form="pint")],
        field="activities",
        kinds=["Ki", "Inhibition"],
    )
    with pytest.raises(RecordError):
        source.to_quantity(unit="nM", form="pint")
    groups = source.split()
    assert groups[0].unit == "nanomolar" and groups[1].unit == "percent"
    assert groups[0].kind == "Ki" and groups[1].kind == "Inhibition"
    frequency = QuantityRecord.from_tagged(
        [puw.quantity(1, "Hz", form="pint"), puw.quantity(2, "Bq", form="pint")], kinds=["frequency", "activity"]
    )
    with pytest.raises(RecordError, match="kind"):
        frequency.to_quantity(unit="hertz", form="pint")


@pytest.mark.parametrize("edit", ["value", "code", "descriptor", "dtype", "shape", "kind"])
def test_tagged_seal_binds_every_part(edit):
    record = QuantityRecord.from_tagged([puw.quantity(1, "nm", form="pint"), puw.quantity(2, "angstrom", form="pint")])
    data = copy.deepcopy(record.to_dict())
    if edit == "value":
        data["values"][0] += 1
    elif edit == "code":
        data["codes"][0] = 1
    elif edit == "descriptor":
        data["manifest"]["descriptors"][0]["unit"] = "meter"
    elif edit == "dtype":
        data["manifest"]["dtype"] = "float32"
    elif edit == "shape":
        data["manifest"]["shape"] = [1, 2]
    else:
        data["manifest"]["descriptors"][0]["kind"] = "other"
    with pytest.raises(RecordError):
        QuantityRecord.from_dict(data)


def test_tagged_arrays_broadcast_codes_and_select_without_changing_old_format():
    record = QuantityRecord.from_tagged(
        [
            puw.quantity(np.array([1.0, 2.0]), "nm", form="pint"),
            puw.quantity(np.array([30.0, 40.0]), "angstrom", form="pint"),
        ]
    )
    np.testing.assert_array_equal(record.codes, [[0, 0], [1, 1]])
    selected = record.select(slice(1, 2))
    np.testing.assert_allclose(selected.to_quantity(unit="nm", form="pint").magnitude, [[3.0, 4.0]])
    old = QuantityRecord.from_quantity(puw.quantity(1, "nm", form="pint"))
    assert old.layout == "homogeneous" and old.to_dict()["manifest"]["format"] == "qrec/0.3"
    with pytest.raises(RecordError):
        QuantityRecord.from_tagged([1, 2])


def test_mixed_dtypes_must_not_round_large_integers():
    with pytest.raises(RecordError, match="precision"):
        QuantityRecord.from_tagged(
            [puw.quantity(np.int64(2**53 + 1), "nm", form="pint"), puw.quantity(1.5, "nm", form="pint")]
        )


def test_empty_multidimensional_tagged_payload_keeps_code_shape():
    source = QuantityRecord.from_tagged([puw.quantity(np.empty((0, 3), dtype=np.float32), "nm", form="pint")])
    restored = QuantityRecord.from_dict(source.to_dict())
    assert restored.codes.shape == (1, 0, 3)
    assert restored.values.dtype == np.dtype("float32")
