import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError
from tests.helpers import loaded_libraries

physipy = pytest.importorskip("physipy")
from physipy import units as physipy_units

pq = pytest.importorskip("quantities")


def test_api_physipy_core_and_bridges():
    with loaded_libraries(["pint", "physipy", "openmm.unit", "unyt", "astropy.units", "quantities"]):
        api = puw.forms.api_physipy

        q = api.make_quantity(2.0, "meter")
        u = api.get_unit(q)
        assert api.compatibility(q, api.make_quantity(1.0, "centimeter"))
        assert api.is_quantity(q)
        assert api.is_unit(u)
        assert api.unit_to_string(u)

        converted_q = api.convert(q, "centimeter")
        assert api.is_quantity(converted_q)

        converted_u = api.convert(u, "centimeter")
        assert api.is_unit(converted_u)
        assert api.unit_to_string(converted_u)

        with pytest.raises(LibraryWithoutParserError):
            api.string_to_quantity("1 meter")
        with pytest.raises(LibraryWithoutParserError):
            api.string_to_unit("meter")

        assert api.unit_to_openmm_unit(u) is not None
        assert api.unit_to_unyt(u) is not None
        assert api.unit_to_astropy_units(u) is not None
        assert api.unit_to_quantities(u) is not None

        q_undefined = physipy.Quantity(3.0, physipy_units["m"].dimension)
        assert api.unit_to_string(q_undefined)


def test_api_quantities_core_and_bridges():
    with loaded_libraries(["pint", "quantities", "openmm.unit", "unyt", "astropy.units", "physipy"]):
        api = puw.forms.api_quantities

        q = api.make_quantity(2.0, "meter")
        u = api.get_unit(q)
        assert api.compatibility(q, api.make_quantity(1.0, "centimeter"))
        assert api.is_quantity(q)
        assert api.is_unit(u)

        converted_q = api.convert(q, "centimeter")
        assert api.is_quantity(converted_q)
        converted_u = api.convert(u, "centimeter")
        assert api.is_unit(converted_u)
        assert api.compatibility(converted_u, pq.cm)

        with pytest.raises(LibraryWithoutParserError):
            api.string_to_quantity("1 meter")
        with pytest.raises(LibraryWithoutParserError):
            api.string_to_unit("meter")

        assert api.unit_to_openmm_unit(u) is not None
        assert api.unit_to_unyt(u) is not None
        assert api.unit_to_astropy_units(u) is not None
        assert api.unit_to_physipy(u) is not None

        assert api.unit_to_string(pq.m) == "m"
