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
