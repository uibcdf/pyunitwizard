"""Optional OpenFF bridge exercises actual registries and official OpenMM parity."""

import json

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import RecordError
from pyunitwizard.forms import api_openff_units, api_pint
from pyunitwizard.record import QuantityRecord

openff = pytest.importorskip("openff.units")


@pytest.mark.parametrize(
    "value,unit",
    [
        (3.0, "nanometer"),
        (np.arange(24, dtype=np.float32).reshape(2, 3, 4), "angstrom"),
        (np.arange(3, dtype=np.int32), "second"),
        (np.array([1.5, 2.0]), "kilocalorie / mole / nanometer**2"),
        (25.0, "degree_Celsius"),
    ],
)
def test_round_trip_retains_registry_values_shape_dtype_and_arithmetic(value, unit):
    source = openff.Quantity(value, unit)
    assert puw.get_form(source) == "openff.units"
    assert puw.is_quantity(source) and puw.is_unit(source.units)
    result = puw.convert(source, to_form="pint")
    assert result._REGISTRY is api_pint.ureg
    back = puw.convert(result, to_form="openff.units")
    assert back._REGISTRY is openff.unit
    assert np.array_equal(np.asarray(back.magnitude), np.asarray(source.magnitude))
    assert np.asarray(back.magnitude).dtype == np.asarray(source.magnitude).dtype
    if unit != "degree_Celsius":
        assert np.array_equal((back + source).magnitude, 2 * np.asarray(source.magnitude))


def test_units_construction_strings_and_reader_policy():
    with puw.context(standard_units=["meter", "second"]):
        created = puw.quantity(3, "nanometer", form="openff.units")
        unit = puw.unit("angstrom", form="openff.units")
        translated = puw.convert(created, to_unit=unit, to_form="openff.units")
        assert translated.magnitude == pytest.approx(30)
        assert puw.get_form(puw.get_unit(created)) == "openff.units"
        scalar = puw.convert(str(created), parser="openff.units", to_form="openff.units")
        assert scalar == created
        assert puw.get_dimensionality(created)["[L]"] == 1
        assert puw.are_compatible(created, unit)


@pytest.mark.parametrize("target", ["pint", "openff.units", "record"])
def test_altered_foreign_openff_definitions_are_refused(target):
    from openff.units.units import UnitRegistry, get_defaults_path

    foreign = UnitRegistry(get_defaults_path(), on_redefinition="ignore")
    foreign.define("nanometer = 2e-9 * meter = nm")
    with pytest.raises(ValueError, match="different definition"):
        puw.convert(foreign.Quantity(3, "nanometer"), to_form=target)


def test_altered_pint_definition_is_refused_on_entering_openff():
    import pint

    foreign = pint.UnitRegistry(on_redefinition="ignore")
    foreign.define("nanometer = 2e-9 * meter = nm")
    with pytest.raises(ValueError, match="different definition"):
        puw.convert(foreign.Quantity(3, "nanometer"), to_form="openff.units")


@pytest.mark.parametrize("unit", ["angstrom", "kilocalorie / mole / nanometer**2"])
def test_native_openmm_round_trip_matches_openff(unit):
    pytest.importorskip("openmm")
    from openff.units.openmm import from_openmm, to_openmm

    source = openff.Quantity(np.array([1.5, 2.0]), unit)
    official = to_openmm(source)
    actual = puw.convert(source, to_form="openmm.unit")
    assert np.array_equal(actual.value_in_unit(official.unit), official._value)
    back = puw.convert(actual, to_form="openff.units")
    assert np.array_equal(back.magnitude, from_openmm(official).magnitude)


def test_openmm_vec3_matches_official_array_shape_and_values():
    openmm = pytest.importorskip("openmm")
    from openff.units.openmm import from_openmm

    source = openmm.unit.Quantity([openmm.Vec3(1, 2, 3), openmm.Vec3(4, 5, 6)], openmm.unit.nanometer)
    result = puw.convert(source, to_form="openff.units")
    expected = from_openmm(source)
    assert isinstance(result.magnitude, np.ndarray)
    assert result.magnitude.shape == (2, 3)
    assert np.array_equal(result.magnitude, expected.magnitude)


def test_unsealed_val_unit_boundary_and_verified_record_round_trip():
    node = {"val": [[1.0, 2.0], [3.0, 4.0]], "unit": "angstrom"}
    quantity = api_openff_units.from_dict(node, unit="nanometer", dimensionality={"[L]": 1})
    assert quantity._REGISTRY is openff.unit
    assert np.allclose(quantity.magnitude, np.asarray(node["val"]) * 0.1)
    sealed = QuantityRecord.from_quantity(quantity, field="coordinates")
    result = sealed.to_quantity(field="coordinates", unit="angstrom", form="openff.units")
    exported = api_openff_units.to_dict(result)
    assert set(exported) == {"val", "unit"}  # Leaving the verified domain is explicit.
    assert np.allclose(exported["val"], node["val"])
    assert json.loads(json.dumps(exported)) == exported
    with pytest.raises(RecordError):
        api_openff_units.from_dict(node, dimensionality={"[T]": 1})
    with pytest.raises(RecordError):
        sealed.to_quantity(field="another_field", form="openff.units")


@pytest.mark.parametrize(
    "data",
    [
        {"val": 1},
        {"unit": "nm"},
        {"val": 1, "unit": "nm", "digest": "pretend"},
        {"val": float("inf"), "unit": "nm"},
        {"val": [1, "bad"], "unit": "nm"},
    ],
)
def test_invalid_openff_nodes_are_refused(data):
    with pytest.raises(RecordError):
        api_openff_units.from_dict(data)


def test_array_string_and_backends_are_reachable_via_the_existing_hub():
    source = openff.Quantity(np.arange(6, dtype=np.float64).reshape(2, 3), "nanometer")
    text = puw.convert(source, to_form="string")
    back = puw.convert(text, parser="pint", to_form="openff.units")
    assert np.array_equal(source.magnitude, back.magnitude)
    assert np.array_equal(puw.convert(text, parser="openff.units", to_form="openff.units").magnitude, source.magnitude)
    for form in ["unyt", "astropy.units"]:
        pytest.importorskip({"unyt": "unyt", "astropy.units": "astropy"}[form])
        result = puw.convert(source, to_form=form)
        restored = puw.convert(result, to_form="openff.units")
        assert np.array_equal(source.magnitude, restored.magnitude)
