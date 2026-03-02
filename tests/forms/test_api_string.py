import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError
from tests.helpers import loaded_libraries


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


def test_api_string_unyt_stubs_raise_not_implemented():
    with pytest.raises(NotImplementedError):
        puw.forms.api_string.quantity_to_unyt("1 meter")
    with pytest.raises(NotImplementedError):
        puw.forms.api_string.unit_to_unyt("meter")
