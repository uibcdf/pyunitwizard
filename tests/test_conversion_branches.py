import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import ArgumentError


def _configure_pint():
    puw.configure.reset()
    puw.configure.load_library(["pint"])


def test_convert_raises_argument_error_for_invalid_to_type():
    _configure_pint()

    with pytest.raises(ArgumentError):
        puw.convert("1 meter", to_type="invalid")


def test_convert_string_unit_to_string_unit_keeps_unit_path():
    _configure_pint()

    output = puw.convert("meter", to_form="string", to_type="unit", parser="pint")
    assert output == "meter"


def test_convert_string_unit_to_pint_unit_keeps_unit_path():
    _configure_pint()

    output = puw.convert("meter", to_form="pint", to_type="unit", parser="pint")
    assert str(output) == "meter"


def test_convert_quantity_to_string_value_returns_stringified_value():
    _configure_pint()

    quantity = puw.quantity(3, "meter", form="pint")
    output = puw.convert(quantity, to_form="string", to_type="value")
    assert output == "3"


def test_convert_string_quantity_to_string_value_uses_string_path():
    _configure_pint()

    output = puw.convert("3 meter", to_form="string", to_type="value", parser="pint")
    assert output == "3"


def test_convert_pint_unit_to_string_unit_keeps_unit_path():
    _configure_pint()

    unit = puw.unit("meter", form="pint")
    output = puw.convert(unit, to_form="string", to_type="unit")
    assert output == "meter"
