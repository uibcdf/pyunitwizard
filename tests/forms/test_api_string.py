import pytest
from contextlib import contextmanager

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError


@contextmanager
def loaded_libraries(libraries):
    previous_libraries = list(puw.configure.get_libraries_loaded())
    previous_default_form = puw.configure.get_default_form()
    previous_default_parser = puw.configure.get_default_parser()

    puw.configure.reset()
    puw.configure.load_library(libraries)
    try:
        yield
    finally:
        puw.configure.reset()
        if previous_libraries:
            puw.configure.load_library(previous_libraries)
        else:
            for library in ['pint', 'openmm.unit', 'unyt']:
                try:
                    puw.configure.load_library(library)
                except (ImportError, ModuleNotFoundError):
                    continue
        if previous_default_form is not None:
            puw.configure.set_default_form(previous_default_form)
        if previous_default_parser is not None:
            puw.configure.set_default_parser(previous_default_parser)


def test_api_string_basic_ops_with_pint_defaults():
    with loaded_libraries(["pint"]):
        puw.configure.set_default_form("pint")
        puw.configure.set_default_parser("pint")

        api = puw.forms.api_string

        assert api.is_form("1 meter")
        assert api.is_quantity("1 meter")
        assert api.is_unit("meter")
        assert api.compatibility("1 meter", "2 centimeter")

        dim = api.dimensionality("1 meter")
        assert dim["[L]"] == 1

        q = api.make_quantity(3.0, "meter")
        assert isinstance(q, str)
        assert "3.0" in q

        assert api.get_value("3 meter") == "3"
        assert api.get_unit("3 meter") == "meter"
        assert api.change_value("3 meter", 4.0) == "4.0 meter"
        assert api.convert("1 meter", "centimeter") == "100.0 centimeter"


def test_api_string_openmm_conversion_paths_raise_expected_error():
    with loaded_libraries(["openmm.unit"]):
        with pytest.raises(LibraryWithoutParserError):
            puw.forms.api_string.quantity_to_openmm_unit("1 meter")
        with pytest.raises(LibraryWithoutParserError):
            puw.forms.api_string.unit_to_openmm_unit("meter")


def test_api_string_openmm_bridge_return_paths_with_monkeypatch(monkeypatch):
    with loaded_libraries(["openmm.unit"]):
        openmm_unit = pytest.importorskip("openmm.unit")

        def _fake_string_to_quantity(_):
            return 1.0 * openmm_unit.meter

        monkeypatch.setattr(
            puw.forms.api_openmm_unit,
            "string_to_quantity",
            _fake_string_to_quantity,
        )

        quantity = puw.forms.api_string.quantity_to_openmm_unit("meter")
        unit = puw.forms.api_string.unit_to_openmm_unit("meter")

        assert str(quantity.unit) == "meter"
        assert str(unit) == "meter"


def test_api_string_unyt_stubs_raise_not_implemented():
    with pytest.raises(NotImplementedError):
        puw.forms.api_string.quantity_to_unyt("1 meter")
    with pytest.raises(NotImplementedError):
        puw.forms.api_string.unit_to_unyt("meter")


def test_api_string_pint_bridge_functions():
    with loaded_libraries(["pint"]):
        quantity = puw.forms.api_string.quantity_to_pint("2 meter")
        unit = puw.forms.api_string.unit_to_pint("meter")

        assert puw.forms.api_pint.get_value(quantity) == 2
        assert str(unit) == "meter"


def test_api_string_astropy_bridge_functions():
    pytest.importorskip("astropy.units")

    with loaded_libraries(["pint", "astropy.units"]):
        quantity = puw.forms.api_string.quantity_to_astropy_units("2 meter")
        unit = puw.forms.api_string.unit_to_astropy_units("1 meter")

        assert puw.forms.api_astropy_unit.get_value(quantity) == 2
        assert puw.forms.api_astropy_unit.unit_to_string(unit) == "m"
