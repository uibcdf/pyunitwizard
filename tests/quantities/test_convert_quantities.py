import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import LibraryWithoutParserError
from tests.helpers import loaded_libraries

pq = pytest.importorskip("quantities")


def test_convert_from_quantities_to_pint_and_back():
    with loaded_libraries(["pint", "quantities"]):
        q_quantities = 2.5 * pq.nm / pq.ps
        q_pint = puw.convert(q_quantities, to_form="pint")

        assert puw.get_form(q_pint) == "pint"
        assert puw.get_value(puw.convert(q_pint, to_form="pint", to_unit="meter/second")) == pytest.approx(2500.0)

        q_back = puw.convert(q_pint, to_form="quantities")
        assert puw.get_form(q_back) == "quantities"
        assert puw.are_compatible(q_quantities, q_back)
        assert puw.get_value(puw.convert(q_back, to_form="pint", to_unit="meter/second")) == pytest.approx(2500.0)


def test_convert_from_string_to_quantities_with_pint_parser():
    with loaded_libraries(["pint", "quantities"]):
        out = puw.convert("3 meter", parser="pint", to_form="quantities")
        assert puw.get_form(out) == "quantities"
        assert puw.get_value(puw.convert(out, to_form="pint", to_unit="meter")) == pytest.approx(3.0)


def test_quantities_parser_is_explicitly_unsupported():
    with loaded_libraries(["pint", "quantities"]):
        with pytest.raises(LibraryWithoutParserError):
            puw.convert("3 meter", parser="quantities", to_form="pint")
