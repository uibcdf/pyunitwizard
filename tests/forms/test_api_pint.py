import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard.forms import api_pint


def test_api_pint_compatibility_accepts_units():
    ureg = puw.forms.api_pint.ureg
    assert puw.forms.api_pint.compatibility(ureg.meter, ureg.centimeter)


def test_api_pint_string_to_unit_and_translation_helpers():
    api = puw.forms.api_pint
    ureg = api.ureg

    unit = api.string_to_unit("meter")
    assert str(unit) == "meter"

    unyt_unit = api.unit_to_unyt(ureg.nanometer)
    assert str(unyt_unit) == "nm"

    astropy_unit = api.unit_to_astropy_units(ureg.nanometer)
    assert "nm" in str(astropy_unit).lower() or "nanometer" in str(astropy_unit).lower()


@pytest.mark.parametrize("spelling", ["dalton", "Da", "amu", "unified_atomic_mass_unit", "kilodalton", "millidalton"])
@pytest.mark.parametrize("suffix", ["", "/nanometer**3", "**2", "**-1", "**0.5"])
def test_pint_atomic_mass_quantities_and_units_reach_unyt(spelling, suffix):
    unyt = pytest.importorskip("unyt")
    source_name = spelling + suffix
    with puw.context(default_form="openmm.unit", default_parser="pint"):
        puw.configure.load_library(["pint", "unyt"])
        source = api_pint.ureg.Quantity(2.5, source_name)
        target = api_pint.ureg.Unit("amu" + suffix)
        expected = source.to(target).magnitude
        for result in (
            api_pint.quantity_to_unyt(source),
            puw.convert(source, to_form="unyt"),
            puw.quantity(2.5, source_name, form="unyt"),
        ):
            assert isinstance(result, unyt.unyt_quantity)
            assert result.to_value("amu" + suffix) == pytest.approx(expected)
            restored = puw.convert(result, to_form="pint", to_unit=source_name)
            assert restored.magnitude == pytest.approx(2.5)
            # Providers use slightly different CODATA constants; preserve their
            # existing atomic-mass convention within 1 ppm, without a molar factor.
            assert result.in_mks().value == pytest.approx(source.to_base_units().magnitude, rel=1e-6)
        for result in (
            api_pint.unit_to_unyt(source.units),
            puw.convert(source.units, to_form="unyt", to_type="unit"),
            puw.unit(source_name, form="unyt"),
        ):
            assert isinstance(result, unyt.Unit)
            assert result.get_conversion_factor(unyt.Unit("amu" + suffix))[0] == pytest.approx(expected / 2.5)
            restored = puw.convert(result, to_form="pint", to_type="unit")
            assert api_pint.ureg.Quantity(1, restored).to(source.units).magnitude == pytest.approx(1)


@pytest.mark.parametrize("dtype", [np.float32, np.float64])
@pytest.mark.parametrize("source_name", ["dalton", "kilodalton", "dalton/nanometer**3"])
def test_pint_atomic_mass_arrays_preserve_values_shape_and_dtype(dtype, source_name):
    pytest.importorskip("unyt")
    with puw.context(default_form="pint", default_parser="pint"):
        values = np.array([[1.0, -2.0], [0.0, 12.0]], dtype=dtype)
        source = api_pint.ureg.Quantity(values, source_name)
        result = puw.convert(source, to_form="unyt")
        np.testing.assert_array_equal(result.value, values)
        assert result.shape == values.shape and result.dtype == values.dtype
        restored = puw.convert(result, to_form="pint", to_unit=source_name)
        np.testing.assert_allclose(restored.magnitude, values, rtol=1e-6)
        assert restored.magnitude.dtype == values.dtype
        np.testing.assert_array_equal(source.magnitude, values)


def test_openmm_atomic_mass_reaches_unyt_through_pint():
    pytest.importorskip("unyt")
    openmm = pytest.importorskip("openmm.unit")
    with puw.context(default_form="pint", default_parser="pint"):
        source = openmm.Quantity(np.array([12.0, 16.0]), openmm.dalton)
        result = puw.convert(source, to_form="unyt")
        np.testing.assert_allclose(result.to_value("amu"), [12.0, 16.0])
        assert puw.get_dimensionality(result)["[M]"] == 1
        assert puw.get_dimensionality(result)["[mol]"] == 0
        restored = puw.convert(result, to_form="openmm.unit", to_unit="dalton")
        np.testing.assert_allclose(restored.value_in_unit(openmm.dalton), [12.0, 16.0])


def test_atomic_mass_translation_keeps_registries_local(monkeypatch):
    import pint

    unyt = pytest.importorskip("unyt")
    from unyt.unit_registry import default_unit_registry

    before = default_unit_registry.lut.copy()
    source = api_pint.ureg.Quantity(1, "dalton")

    def forbid_pint_registry(*args, **kwargs):
        raise AssertionError("translation constructed a Pint registry")

    monkeypatch.setattr(pint, "UnitRegistry", forbid_pint_registry)
    first = api_pint.quantity_to_unyt(source)
    second = api_pint.quantity_to_unyt(source)
    assert first.units.registry is not default_unit_registry
    assert first.units.registry is not second.units.registry
    assert default_unit_registry.lut == before
    assert first.to_value(unyt.amu) == pytest.approx(1)


def test_atomic_mass_conversion_rejects_a_changed_foreign_definition():
    import pint

    pytest.importorskip("unyt")
    foreign = pint.UnitRegistry()
    foreign.define("dalton = 2 * kilogram = Da")
    with puw.context(default_form="pint", default_parser="pint"):
        with pytest.raises(ValueError, match="different definition"):
            puw.convert(foreign.Quantity(1, "dalton"), to_form="unyt")


def test_atomic_mass_translation_retains_other_unyt_definitions(monkeypatch):
    import pint

    unyt = pytest.importorskip("unyt")
    from unyt.unit_registry import default_unit_registry

    foreign = pint.UnitRegistry()
    foreign.define("atomic_mass_test_length = 2 * meter")
    monkeypatch.setitem(
        default_unit_registry.lut,
        "atomic_mass_test_length",
        (2.0, unyt.dimensions.length, 0.0, "test length", False),
    )
    source = foreign.Quantity(3.0, "dalton * atomic_mass_test_length")
    result = api_pint.quantity_to_unyt(source)
    assert result.to_value("amu * m") == pytest.approx(6)
