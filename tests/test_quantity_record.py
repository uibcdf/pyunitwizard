"""QuantityRecord: the inert interchange form (uibcdf/pyunitwizard#82, design in #83).

These tests encode the contract: exact round trips, a seal that refuses every change made
outside the codec, a reader handshake, no default unit, and a record that stays inert.
"""

import copy
import json

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import RecordError
from pyunitwizard.record import QuantityRecord, QuantityRecordBundle

CONCENTRATION = {"[L]": -3, "[mol]": 1}


def _through_json(data):
    return json.loads(json.dumps(data))


def _record(values=(3.0, 12.5, 0.4), unit="nM", field="bioactivity.ic50", **kwargs):
    return QuantityRecord.from_quantity(puw.quantity(np.array(values), unit, form="pint"), field=field, **kwargs)


# --- round trips ---------------------------------------------------------------------------


@pytest.mark.parametrize("encoding", ["json", "base64"])
@pytest.mark.parametrize(
    "values, unit",
    [
        (3.0, "nM"),
        (np.array([3.0, 12.5, 0.4, np.nan, -0.0]), "nM"),
        (np.random.default_rng(0).random((4, 5, 3)).astype(np.float32), "nm"),
        (np.arange(10, dtype=np.int32), "dalton"),
        (np.array([1.5, 2.25]), "angstrom**2"),
        (np.array([0.1, 0.2]), "N*s/m**2"),
        (np.array([20.0, 37.0]), "degC"),
        (np.array([0.5, 1.0]), "radian"),
        (np.array([0.25]), "dimensionless"),
    ],
)
def test_round_trip_is_exact(values, unit, encoding):
    if encoding == "json" and not np.all(np.isfinite(values)):
        pytest.skip("strict JSON has no NaN; covered by test_json_refuses_non_finite_values")
    q = puw.quantity(values, unit, form="pint")
    record = QuantityRecord.from_dict(
        _through_json(QuantityRecord.from_quantity(q, field="f").to_dict(encoding=encoding))
    )
    back = record.to_quantity(field="f", form="pint")

    a, b = np.asarray(puw.get_value(q)), np.asarray(puw.get_value(back))
    assert a.dtype == b.dtype and a.shape == b.shape
    assert np.array_equal(a, b, equal_nan=True)
    assert np.array_equal(np.signbit(a), np.signbit(b))
    assert str(puw.get_unit(back)) == str(puw.get_unit(q))


def test_json_refuses_non_finite_values():
    # Python writes NaN, which is not JSON: a JavaScript or Go reader would reject the file.
    record = _record(values=(1.0, np.nan))
    with pytest.raises(RecordError, match="base64"):
        record.to_dict(encoding="json")
    assert np.isnan(QuantityRecord.from_dict(_through_json(record.to_dict(encoding="base64"))).values[1])


def test_the_descriptor_describes_the_unit_in_si():
    record = _record(unit="nM")
    assert record.unit == "nanomolar"
    assert record.si == {"factor": 1e-06, "offset": 0.0, "exponents": {"m": -3, "mol": 1}}
    celsius = _record(values=(20.0,), unit="degC", field="t")
    assert celsius.si["offset"] == pytest.approx(273.15)
    assert _record(values=(1.0,), unit="radian", field="a").si["exponents"] == {}


def test_reading_in_another_unit_converts_and_the_same_unit_does_not_round():
    record = _record(values=(5.0,), unit="pM")
    assert puw.get_value(record.to_quantity(unit="pM", form="pint"))[0] == 5.0
    assert puw.get_value(record.to_quantity(unit="picomolar", form="pint"))[0] == 5.0
    assert puw.get_value(record.to_quantity(unit="uM", form="pint"))[0] == pytest.approx(5e-6)


@pytest.mark.parametrize("form", ["pint", "openmm.unit", "astropy.units"])
def test_a_record_reaches_other_backends(form):
    pytest.importorskip({"pint": "pint", "openmm.unit": "openmm", "astropy.units": "astropy"}[form])
    record = _record(values=(1.5, 2.5), unit="nm", field="x")
    q = record.to_quantity(form=form, unit="angstrom")
    assert puw.get_form(q) == form
    assert np.allclose(puw.get_value(q, to_unit="angstrom"), [15.0, 25.0])


# --- integrity: every change made outside the codec is refused ---------------------------------


def _slip(mutate, field="bioactivity.ic50"):
    data = _through_json(_record().to_dict())
    mutate(data)
    return data


SLIPS = {
    "raw append": lambda d: (
        d["values"].append(7.0),
        d["manifest"]["shape"].__setitem__(0, 4),
        d["manifest"]["blocks"].__setitem__(0, 4),
    ),
    "hand edit of a value": lambda d: d["values"].__setitem__(1, 12.6),
    "unit renamed": lambda d: d["manifest"].__setitem__("unit", "picomolar"),
    "unit respelled": lambda d: d["manifest"].__setitem__("unit", "nM"),
    "SI factor edited": lambda d: d["manifest"]["si"].__setitem__("factor", 1e-9),
    "manifest deleted": lambda d: d.pop("manifest"),
    "values reordered": lambda d: d["values"].reverse(),
    "truncated": lambda d: (
        d["values"].pop(),
        d["manifest"]["shape"].__setitem__(0, 2),
        d["manifest"]["blocks"].__setitem__(0, 2),
    ),
    "pasted values": lambda d: d.__setitem__("values", [2.1, 1.8, 2.5]),
    "digest removed": lambda d: d.pop("digest"),
    "format changed": lambda d: d["manifest"].__setitem__("format", "qrec/9"),
}


@pytest.mark.parametrize("name", SLIPS)
def test_every_change_outside_the_codec_is_refused(name):
    with pytest.raises(RecordError):
        QuantityRecord.from_dict(_slip(SLIPS[name]))


def test_a_resealed_lie_is_caught_by_the_redundant_si_description():
    # Someone renames the unit AND recomputes the digest with the library's own helper.
    from pyunitwizard.record import _seal

    data = _slip(lambda d: d["manifest"].__setitem__("unit", "picomolar"))
    data["block_digests"], data["digest"] = _seal(data["manifest"], np.asarray(data["values"]))
    with pytest.raises(RecordError, match="SI factor"):
        QuantityRecord.from_dict(data)


def test_unit_definitions_may_differ_by_codata_revision_but_not_more():
    from pyunitwizard.record import _seal

    def with_factor(relative_change):
        data = _through_json(_record(values=(180.16,), unit="dalton", field="mw").to_dict())
        data["manifest"]["si"]["factor"] *= 1 + relative_change
        data["block_digests"], data["digest"] = _seal(data["manifest"], np.asarray(data["values"]))
        return data

    QuantityRecord.from_dict(with_factor(1.4e-9))  # CODATA 2018 vs 2022 dalton
    with pytest.raises(RecordError):
        QuantityRecord.from_dict(with_factor(1e-3))


def test_a_record_never_shares_state_with_the_unit_cache():
    from pyunitwizard.record import _descriptor

    data = _record().to_dict()
    data["manifest"]["si"]["factor"] = 123.0
    assert _descriptor("nanomolar")["si"]["factor"] == 1e-06


def test_values_held_in_memory_cannot_be_changed_behind_the_seal():
    record = _record()
    with pytest.raises(ValueError):
        record.values[0] = 99.0


# --- the handshake ----------------------------------------------------------------------------


def test_the_reader_must_name_the_field_it_expects():
    record = QuantityRecord.from_dict(_through_json(_record().to_dict()))
    with pytest.raises(RecordError, match="belongs to"):
        record.to_quantity(field="bioactivity.ki")
    unbound = QuantityRecord.from_quantity(puw.quantity(3.0, "nM", form="pint"))
    with pytest.raises(RecordError, match="belongs to"):
        unbound.to_quantity(field="bioactivity.ic50")


def test_the_reader_refuses_another_dimension():
    with pytest.raises(RecordError, match="dimensionality"):
        _record().to_quantity(dimensionality={"[L]": 1})
    with pytest.raises(Exception):
        _record().to_quantity(unit="nm")
    _record().to_quantity(dimensionality=CONCENTRATION)


def test_the_kind_distinguishes_units_that_share_dimensions():
    record = QuantityRecord.from_quantity(puw.quantity(1.0, "1/s", form="pint"), field="rate", kind="qudt:Frequency")
    record.to_quantity(kind="qudt:Frequency")
    with pytest.raises(RecordError, match="kind"):
        record.to_quantity(kind="qudt:Activity")


def test_there_is_no_default_unit():
    with pytest.raises(RecordError):
        QuantityRecord.from_dict({"values": [3.0], "digest": "x"})


def test_the_writer_refuses_bare_numbers():
    with pytest.raises(RecordError, match="quantity"):
        QuantityRecord.from_quantity(np.array([3.0]), field="f")


def test_a_consistent_writer_bug_is_not_detectable_by_any_format():
    # Meant nM, built pM, wrote pM: coherent with itself. Canaries and tests catch this.
    record = _record(values=(3.0,), unit="pM")
    assert record.unit == "picomolar"


# --- inert on purpose ---------------------------------------------------------------------------


def test_a_record_does_not_compute():
    record = _record()
    with pytest.raises(TypeError):
        _ = record + record
    with pytest.raises(TypeError):
        _ = record * 2


# --- a form of PyUnitWizard ------------------------------------------------------------------------


def test_record_is_a_form():
    q = puw.quantity(np.array([3.0, 12.5]), "nM", form="pint")
    record = puw.convert(q, to_form="record")
    assert isinstance(record, QuantityRecord)
    assert puw.get_form(record) == "record"
    assert puw.is_quantity(record) and not puw.is_unit(record)
    assert np.array_equal(puw.get_value(record), [3.0, 12.5])
    assert puw.get_unit(record) == "nanomolar"
    assert puw.get_dimensionality(record) == puw.get_dimensionality(q)
    back = puw.convert(record, to_form="pint", to_unit="uM")
    assert np.allclose(puw.get_value(back), [0.003, 0.0125])


def test_quantity_can_be_built_directly_in_the_record_form():
    record = puw.quantity(np.array([1.0, 2.0]), "nm", form="record")
    assert isinstance(record, QuantityRecord) and record.unit == "nanometer"


def test_converting_a_record_to_another_unit_keeps_it_a_record():
    record = puw.convert(_record(), to_unit="uM")
    assert isinstance(record, QuantityRecord)
    assert record.unit == "micromolar" and record.field == "bioactivity.ic50"
    assert np.allclose(record.values, [0.003, 0.0125, 0.0004])


def test_records_are_independent_of_the_session_policy():
    # A record states its own unit; standard units belong to the user, never to the data.
    q = puw.quantity(np.array([1.5]), "nm", form="pint")
    with puw.context(standard_units=["angstrom", "ps", "K", "mole", "dalton"]):
        record = QuantityRecord.from_quantity(q, field="x")
        assert record.unit == "nanometer"
        assert puw.get_value(record.to_quantity(field="x", form="pint"))[0] == 1.5


def test_canonical_spelling_does_not_follow_pint_display_settings():
    from pyunitwizard.forms.api_pint import ureg

    previous = ureg.formatter.default_format
    try:
        ureg.formatter.default_format = "~P"
        assert _record().unit == "nanomolar"
    finally:
        ureg.formatter.default_format = previous


# --- bundles --------------------------------------------------------------------------------------

CARD = {
    "properties.physchem.molecular_weight": puw.quantity(180.16, "dalton", form="pint"),
    "properties.physchem.tpsa": puw.quantity(63.6, "angstrom**2", form="pint"),
    "structures.resolution": puw.quantity(2.1, "angstrom", form="pint"),
}
EXPECTED = {
    "properties.physchem.molecular_weight": {"[M]": 1},
    "properties.physchem.tpsa": {"[L]": 2},
    "structures.resolution": {"[L]": 1},
}


def test_bundle_round_trip():
    bundle = QuantityRecordBundle.from_dict(_through_json(QuantityRecordBundle.from_quantities(CARD).to_dict()))
    out = bundle.to_quantities(expected=EXPECTED, form="pint")
    assert float(puw.get_value(out["properties.physchem.tpsa"])) == 63.6
    assert str(puw.get_unit(out["structures.resolution"])) == "angstrom"


BUNDLE_SLIPS = {
    "a scalar edited": lambda b: b["entries"]["structures.resolution"].__setitem__("values", 2.2),
    "a unit renamed": lambda b: b["entries"]["structures.resolution"].__setitem__("unit", "nanometer"),
    "an entry removed": lambda b: b["entries"].pop("properties.physchem.tpsa"),
    "two entries swapped": lambda b: b["entries"].update(
        {
            "properties.physchem.tpsa": b["entries"]["structures.resolution"],
            "structures.resolution": b["entries"]["properties.physchem.tpsa"],
        }
    ),
}


@pytest.mark.parametrize("name", BUNDLE_SLIPS)
def test_bundle_slips_are_refused(name):
    data = _through_json(QuantityRecordBundle.from_quantities(CARD).to_dict())
    BUNDLE_SLIPS[name](data)
    with pytest.raises(RecordError):
        QuantityRecordBundle.from_dict(data).to_quantities(expected=EXPECTED)


def test_bundle_reader_declares_every_field_it_expects():
    bundle = QuantityRecordBundle.from_quantities(CARD)
    with pytest.raises(RecordError, match="expected"):
        bundle.to_quantities(expected={"structures.resolution": {"[L]": 1}})
    with pytest.raises(RecordError, match="dimensionality"):
        bundle.to_quantities(expected={**EXPECTED, "structures.resolution": {"[M]": 1}})


# --- published test vectors: the format stays stable, and third parties can check readers ---------


def test_published_vectors_verify_and_are_reproduced_exactly():
    from pathlib import Path

    folder = Path(__file__).parent / "quantity_record_vectors"
    for path in sorted(folder.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        record = QuantityRecord.from_dict(case["record"])
        q = record.to_quantity(field=case["record"]["manifest"]["field"], form="pint")
        rebuilt = QuantityRecord.from_quantity(q, field=record.field, kind=record.kind)
        assert rebuilt.to_dict() == case["record"], path.name
        si = np.asarray(record.values, dtype=float).reshape(-1) * record.si["factor"] + record.si["offset"]
        assert np.allclose(si, case["si_values"]), path.name


def test_the_standard_library_reference_reader_agrees():
    from pathlib import Path

    from pyunitwizard._private.record_reference_reader import read_si

    folder = Path(__file__).parent / "quantity_record_vectors"
    cases = sorted(folder.glob("*.json"))
    assert len(cases) >= 4
    for path in cases:
        case = json.loads(path.read_text(encoding="utf-8"))
        manifest = case["record"]["manifest"]
        values = read_si(case["record"], manifest["field"], manifest["si"]["exponents"])
        assert np.allclose(values, case["si_values"]), path.name
        tampered = copy.deepcopy(case["record"])
        tampered["manifest"]["unit"] = "tampered"
        with pytest.raises(ValueError):
            read_si(tampered, manifest["field"], manifest["si"]["exponents"])
