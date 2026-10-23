"""Authoritative bounded annotations distinguish equal SI dimensions."""

import copy
import json
from pathlib import Path

import numpy as np
import pytest

from pyunitwizard.dialects import vocabulary
from pyunitwizard.forms.api_pint import ureg
from pyunitwizard.record import QuantityRecord, RecordError, metadata_digest

QK = "http://qudt.org/vocab/quantitykind/"
QU = "http://qudt.org/vocab/unit/"
UO = "http://purl.obolibrary.org/obo/"


@pytest.mark.parametrize(
    "unit,kind,qudt,obo",
    [
        ("hertz", "Frequency", "HZ", "UO_0000106"),
        ("becquerel", "Activity", "BQ", "UO_0000132"),
        ("radian / second", "AngularVelocity", "RAD-PER-SEC", "UO_0000079"),
    ],
)
def test_named_physical_meaning_is_validated_for_both_explicit_vocabularies(unit, kind, qudt, obo):
    record = QuantityRecord.from_quantity(ureg.Quantity([1, 2], unit), kind=QK + kind)
    for unit_iri in [QU + qudt, UO + obo]:
        annotation = vocabulary.annotate(record, unit_iri=unit_iri, kind_iri=QK + kind)
        assert annotation["format"] == vocabulary.FORMAT
        assert annotation["record_digest"] == record.digest
        assert vocabulary.validate_annotation(record, annotation, unit_iri=unit_iri, kind_iri=QK + kind) is None
    assert record.kind == QK + kind


def test_gaia_proper_motion_has_explicit_angular_meaning_without_astropy_dependency():
    fixture = json.loads((Path(__file__).parents[1] / "data" / "gaia_proper_motion.json").read_text())
    # Gaia's angular-unit conversion is explicit consumer policy, not inferred
    # from inverse-time dimensions by an ontology or computing registry.
    rate = np.deg2rad(np.array(fixture["values"]) / 3_600_000) / (365.25 * 86400)
    record = QuantityRecord.from_quantity(
        ureg.Quantity(rate, "radian/second"), field="proper_motion", kind=QK + "AngularVelocity"
    )
    annotation = vocabulary.annotate(record, unit_iri=QU + "RAD-PER-SEC", kind_iri=QK + "AngularVelocity")
    vocabulary.validate_annotation(record, annotation, unit_iri=QU + "RAD-PER-SEC", kind_iri=QK + "AngularVelocity")
    for unit_iri, kind_iri in [(QU + "HZ", QK + "Frequency"), (QU + "BQ", QK + "Activity")]:
        with pytest.raises(RecordError):
            vocabulary.annotate(record, unit_iri=unit_iri, kind_iri=kind_iri)


@pytest.mark.parametrize(
    "record_unit,record_kind,unit_iri,kind_iri",
    [
        ("hertz", "Frequency", QU + "BQ", QK + "Activity"),
        ("becquerel", "Frequency", QU + "HZ", QK + "Frequency"),
        ("hertz", "Activity", QU + "HZ", QK + "Activity"),
        ("radian/second", "Frequency", QU + "HZ", QK + "Frequency"),
        ("1/second", "Frequency", QU + "HZ", QK + "Frequency"),
        ("kilohertz", "Frequency", QU + "HZ", QK + "Frequency"),
        ("hertz", "Frequency", UO + "UO_0000106", UO + "UO_0000106"),
    ],
)
def test_dimensions_and_numeric_convertibility_never_choose_semantics(record_unit, record_kind, unit_iri, kind_iri):
    record = QuantityRecord.from_quantity(ureg.Quantity(1, record_unit), kind=QK + record_kind)
    assert record.si["exponents"] == {"s": -1}
    with pytest.raises(RecordError):
        vocabulary.annotate(record, unit_iri=unit_iri, kind_iri=kind_iri)


def test_absent_or_unregistered_kinds_and_units_are_refused():
    for kind in [None, "Frequency", QK + "Unknown"]:
        record = QuantityRecord.from_quantity(ureg.Quantity(1, "hertz"), kind=kind)
        with pytest.raises(RecordError):
            vocabulary.annotate(record, unit_iri=QU + "HZ", kind_iri=QK + "Frequency")
    record = QuantityRecord.from_quantity(ureg.Quantity(1, "hertz"), kind=QK + "Frequency")
    with pytest.raises(RecordError):
        vocabulary.annotate(record, unit_iri="https://example.org/unit/hertz", kind_iri=QK + "Frequency")


def test_annotation_binds_record_identity_catalogue_and_reader_intent():
    record = QuantityRecord.from_quantity(ureg.Quantity([1, 2], "hertz"), kind=QK + "Frequency")
    annotation = vocabulary.annotate(record, unit_iri=QU + "HZ", kind_iri=QK + "Frequency")
    for key, value in [
        ("record_digest", "changed"),
        ("catalog_digest", "changed"),
        ("unit_iri", QU + "BQ"),
        ("format", "future"),
    ]:
        changed = copy.deepcopy(annotation)
        changed[key] = value
        changed.pop("digest")
        changed["digest"] = metadata_digest(changed)
        with pytest.raises(RecordError):
            vocabulary.validate_annotation(record, changed, unit_iri=QU + "HZ", kind_iri=QK + "Frequency")
    other = QuantityRecord.from_quantity(ureg.Quantity([1, 3], "hertz"), kind=QK + "Frequency")
    with pytest.raises(RecordError):
        vocabulary.validate_annotation(other, annotation, unit_iri=QU + "HZ", kind_iri=QK + "Frequency")


def test_catalogue_is_detached_attributed_and_has_reviewed_alignment_provenance():
    catalog = vocabulary.catalog()
    assert catalog["sources"]["qudt"]["release"] == "3.5.3"
    assert catalog["sources"]["uo"]["release"] == "2026-10-12"
    assert all(source["license"] == "CC-BY-4.0" for source in catalog["sources"].values())
    assert "PyUnitWizard" in catalog["alignment"]
    assert "not an upstream exactMatch" in catalog["alignment"]
    assert len(catalog["units"]) == 6
    catalog["units"].clear()
    assert len(vocabulary.catalog()["units"]) == 6


def test_tagged_source_cannot_receive_one_silent_global_annotation():
    tagged = QuantityRecord.from_tagged([ureg.Quantity(1, "hertz"), ureg.Quantity(1, "becquerel")])
    with pytest.raises(RecordError):
        vocabulary.annotate(tagged, unit_iri=QU + "HZ", kind_iri=QK + "Frequency")
