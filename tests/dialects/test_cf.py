"""Actual UDUNITS checks protect the negotiated H5MSM unit boundary."""

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import RecordError
from pyunitwizard.dialects import cf

pytest.importorskip("cf_units")


@pytest.mark.parametrize(
    "unit,spelling",
    [
        ("nanometer", "nm"),
        ("picosecond", "ps"),
        ("nanometer / picosecond", "nm ps-1"),
        ("nanometer**2", "nm2"),
        ("kilojoule / mole", "kJ mol-1"),
        ("dimensionless", "1"),
    ],
)
def test_published_h5msm_units_match_actual_udunits(unit, spelling):
    assert cf.validate_unit(unit, spelling) == spelling
    source = np.arange(6, dtype=np.float32).reshape(2, 3)
    result = cf.parse_quantity(source, spelling, unit=unit, form="pint")
    assert np.allclose(result.magnitude, source)
    assert result.magnitude.shape == source.shape
    assert np.array_equal(source, np.arange(6, dtype=np.float32).reshape(2, 3))


def test_cf_spelling_controls_import_instead_of_session_policy():
    with puw.context(standard_units=["meter", "second"]):
        result = cf.parse_quantity([10.0, 20.0], "nm", unit="angstrom", form="unyt")
        assert np.allclose(puw.get_value(result), [100, 200])
    assert cf.parse_quantity(1, "m s-1", unit="nanometer / picosecond", form="pint").magnitude == pytest.approx(0.001)


@pytest.mark.parametrize("unit,spelling", [("nanometer", "m"), ("second", "nm"), ("dalton", "u")])
def test_export_refuses_changed_scale_dimensions_and_real_definition_drift(unit, spelling):
    with pytest.raises(RecordError):
        cf.validate_unit(unit, spelling)


@pytest.mark.parametrize(
    "spelling", ["unknown", "no unit", "", "days since 2000-01-01", "1000 m", "m @ 3", "lg(re 1 m)"]
)
def test_unsupported_cf_meanings_are_refused(spelling):
    with pytest.raises(RecordError):
        cf.parse_quantity(1, spelling, unit="meter")


@pytest.mark.parametrize(
    "unit,spelling,metadata",
    [
        ("degree_Celsius", "degC", "temperature: on_scale"),
        ("delta_degree_Celsius", "degC", "temperature: difference"),
        ("kelvin", "K", "temperature: on_scale"),
        ("kelvin", "K", "temperature: difference"),
    ],
)
def test_temperature_semantics_are_explicit_and_affine_values_are_correct(unit, spelling, metadata):
    assert cf.validate_unit(unit, spelling, units_metadata=metadata) == spelling
    result = cf.parse_quantity([0.0, 25.0], spelling, unit="kelvin", units_metadata=metadata, form="pint")
    expected = [273.15, 298.15] if metadata == "temperature: on_scale" and spelling == "degC" else [0.0, 25.0]
    assert np.allclose(result.magnitude, expected)


@pytest.mark.parametrize("metadata", [None, "temperature: unknown", "temperature: arbitrary"])
def test_unknown_temperature_semantics_are_refused(metadata):
    with pytest.raises(RecordError):
        cf.validate_unit("kelvin", "K", units_metadata=metadata)


def test_difference_cannot_be_labeled_as_an_absolute_celsius_point():
    with pytest.raises(RecordError):
        cf.validate_unit("degree_Celsius", "degC", units_metadata="temperature: difference")
    with pytest.raises(RecordError):
        cf.validate_unit("meter", "m", units_metadata="temperature: on_scale")


def test_compound_temperature_requires_difference_semantics():
    assert cf.validate_unit("watt / meter**2 / kelvin", "W m-2 K-1", units_metadata="temperature: difference")
    with pytest.raises(RecordError):
        cf.validate_unit("watt / meter**2 / kelvin", "W m-2 K-1", units_metadata="temperature: on_scale")


def test_dimension_mismatch_on_import_is_refused():
    with pytest.raises(RecordError):
        cf.parse_quantity(1.0, "second", unit="meter")


@pytest.mark.parametrize("spelling", ["m^2", "m**2", "m2"])
def test_integer_power_spellings_use_actual_udunits(spelling):
    assert cf.validate_unit("meter**2", spelling) == spelling


def test_parse_quantity_uses_the_requested_and_default_form_without_unit_defaults():
    with puw.context(default_form="unyt", standard_units=["meter", "second"]):
        result = cf.parse_quantity(10, "nm", unit="angstrom")
        assert puw.get_form(result) == "unyt"
        assert puw.get_value(result) == pytest.approx(100.0)


def test_foreign_registry_unit_definition_cannot_change_the_label_check():
    import pint

    foreign = pint.UnitRegistry(on_redefinition="ignore")
    foreign.define("nanometer = 2e-9 * meter = nm")
    with pytest.raises(RecordError):
        cf.validate_unit(foreign.Unit("nanometer"), "nm")


def test_on_scale_temperature_cannot_target_a_named_difference_unit():
    with pytest.raises(RecordError):
        cf.parse_quantity(25.0, "degC", unit="delta_degree_Celsius", units_metadata="temperature: on_scale")
