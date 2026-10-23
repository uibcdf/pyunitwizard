import numpy as np
import pint
import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError
from pyunitwizard.forms import api_unyt


def test_api_unyt_parser_stubs_raise():
    with pytest.raises(LibraryWithoutParserError):
        api_unyt.string_to_quantity("1 m")
    with pytest.raises(LibraryWithoutParserError):
        api_unyt.string_to_unit("m")


def test_api_unyt_unit_translation_helpers():
    unyt = api_unyt.unyt
    unit = unyt.nm

    pint_unit = api_unyt.unit_to_pint(unit)
    assert str(pint_unit) == "nanometer"

    openmm_unit = api_unyt.unit_to_openmm_unit(unit)
    assert "nm" in str(openmm_unit).lower() or "nanometer" in str(openmm_unit).lower()

    astropy_unit = api_unyt.unit_to_astropy_units(unit)
    assert "nm" in str(astropy_unit).lower() or "nanometer" in str(astropy_unit).lower()


@pytest.mark.parametrize(
    "unit,target,expected",
    [("angstrom", "nanometer", [0.1, 0.2, 0.3]), ("angstrom/picosecond", "meter/second", [100, 200, 300])],
)
def test_unyt_to_astropy_does_not_construct_a_registry_per_conversion(monkeypatch, unit, target, expected):
    pytest.importorskip("astropy.units")
    with puw.context(default_form="pint", default_parser="pint"):
        puw.configure.load_library(["pint", "unyt", "astropy.units"])
        source = puw.quantity(np.array([1.0, 2.0, 3.0], dtype=np.float32), unit, form="unyt")

        def forbid_new_registry(*args, **kwargs):
            raise AssertionError("conversion constructed a new Pint registry")

        monkeypatch.setattr(pint, "UnitRegistry", forbid_new_registry)
        for _ in range(2):
            result = puw.convert(source, to_form="astropy.units", to_unit=target)
            values = np.asarray(puw.get_value(result))
            np.testing.assert_allclose(values, expected, rtol=1e-6)
            assert values.dtype == np.dtype("float32")


@pytest.mark.parametrize("as_unit", [False, True])
@pytest.mark.parametrize(
    "unit,expected",
    [("angstrom", {"[L]": 1}), ("angstrom/picosecond", {"[L]": 1, "[T]": -1}), ("amu", {"[M]": 1})],
)
def test_unyt_dimensionality_reuses_the_shared_registry(monkeypatch, unit, expected, as_unit):
    with puw.context(default_form="pint", default_parser="pint"):
        puw.configure.load_library(["pint", "unyt"])
        quantity = api_unyt.unyt.unyt_array([1.0, 2.0], unit)
        source = puw.get_unit(quantity) if as_unit else quantity

        def forbid_new_registry(*args, **kwargs):
            raise AssertionError("dimensionality constructed a new Pint registry")

        monkeypatch.setattr(pint, "UnitRegistry", forbid_new_registry)
        # Calling the adapter also exercises misses independently of the public cache.
        for _ in range(2):
            for result in (api_unyt.dimensionality(source), puw.get_dimensionality(source)):
                assert {key: power for key, power in result.items() if power} == expected


@pytest.mark.parametrize("dtype", [np.float32, np.float64])
@pytest.mark.parametrize(
    "unit,target,factor,dimensions",
    [
        ("angstrom", "nanometer", 0.1, {"[L]": 1}),
        ("angstrom/picosecond", "meter/second", 100.0, {"[L]": 1, "[T]": -1}),
        ("amu", "dalton", 1.0, {"[M]": 1}),
    ],
)
def test_unyt_to_openmm_reuses_the_shared_registry(monkeypatch, unit, target, factor, dimensions, dtype):
    pytest.importorskip("openmm.unit")
    with puw.context(default_form="pint", default_parser="pint"):
        puw.configure.load_library(["pint", "unyt", "openmm.unit"])
        values = np.array([[1.0, -2.0, 3.0], [4.0, 5.0, -6.0]], dtype=dtype)
        source = api_unyt.unyt.unyt_array(values, unit)

        def forbid_new_registry(*args, **kwargs):
            raise AssertionError("OpenMM conversion constructed a new Pint registry")

        monkeypatch.setattr(pint, "UnitRegistry", forbid_new_registry)
        for _ in range(2):
            result = puw.convert(source, to_form="openmm.unit", to_unit=target)
            actual = np.asarray(puw.get_value(result))
            np.testing.assert_allclose(actual, values * factor, rtol=1e-6)
            assert actual.shape == values.shape and actual.dtype == values.dtype
            # OpenMM's molar-mass convention returns to pure mass through Pint.
            restored = puw.convert(result, to_form="pint", to_unit=unit)
            np.testing.assert_allclose(puw.get_value(restored), values, rtol=1e-6)
            assert {key: power for key, power in puw.get_dimensionality(restored).items() if power} == dimensions


@pytest.mark.parametrize(
    "unit,target,factor",
    [("angstrom", "nanometer", 0.1), ("angstrom/picosecond", "meter/second", 100.0), ("amu", "dalton", 1.0)],
)
def test_unyt_units_reach_openmm_without_a_new_registry(monkeypatch, unit, target, factor):
    pytest.importorskip("openmm.unit")
    with puw.context(default_form="pint", default_parser="pint"):
        puw.configure.load_library(["pint", "unyt", "openmm.unit"])
        source = api_unyt.unyt.Unit(unit)
        target_unit = puw.unit(target, form="openmm.unit")

        def forbid_new_registry(*args, **kwargs):
            raise AssertionError("unit conversion constructed a new Pint registry")

        monkeypatch.setattr(pint, "UnitRegistry", forbid_new_registry)
        for _ in range(2):
            for result in (
                api_unyt.unit_to_openmm_unit(source),
                puw.convert(source, to_form="openmm.unit", to_type="unit"),
            ):
                assert puw.is_unit(result)
                assert result.conversion_factor_to(target_unit) == pytest.approx(factor)
