import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError
from tests.helpers import loaded_libraries

physipy = pytest.importorskip("physipy")
from physipy import units as physipy_units


def test_convert_from_physipy_to_pint_and_back():
    with loaded_libraries(["pint", "physipy"]):
        q_physipy = 2.5 * physipy_units["nm"] / physipy_units["ps"]
        q_pint = puw.convert(q_physipy, to_form="pint")

        assert puw.get_form(q_pint) == "pint"
        assert puw.get_value(puw.convert(q_pint, to_form="pint", to_unit="meter/second")) == pytest.approx(2500.0)

        q_back = puw.convert(q_pint, to_form="physipy")
        assert puw.get_form(q_back) == "physipy"
        assert puw.are_compatible(q_physipy, q_back)
        assert puw.get_value(puw.convert(q_back, to_form="pint", to_unit="meter/second")) == pytest.approx(2500.0)


def test_convert_from_string_to_physipy_with_pint_parser():
    with loaded_libraries(["pint", "physipy"]):
        out = puw.convert("3 meter", parser="pint", to_form="physipy")
        assert puw.get_form(out) == "physipy"
        assert puw.get_value(puw.convert(out, to_form="pint", to_unit="meter")) == pytest.approx(3.0)


def test_physipy_parser_is_explicitly_unsupported():
    with loaded_libraries(["pint", "physipy"]):
        with pytest.raises(LibraryWithoutParserError):
            puw.convert("3 meter", parser="physipy", to_form="pint")
