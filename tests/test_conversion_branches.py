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


def test_convert_string_quantity_without_explicit_target_still_parses():
    _configure_pint()

    output = puw.convert("1 meter")
    assert puw.get_form(output) == "pint"
    assert puw.get_value(output) == pytest.approx(1.0)


def test_convert_string_quantity_with_parser_without_explicit_target_still_parses():
    _configure_pint()

    output = puw.convert("1 meter", parser="pint")
    assert puw.get_form(output) == "pint"
    assert puw.get_value(output) == pytest.approx(1.0)


def test_convert_pint_unit_to_string_unit_keeps_unit_path():
    _configure_pint()

    unit = puw.unit("meter", form="pint")
    output = puw.convert(unit, to_form="string", to_type="unit")
    assert output == "meter"


def test_convert_to_unit_string_without_numeric_prefix_works_with_astropy_default_parser():
    pytest.importorskip("astropy.units")

    puw.configure.reset()
    puw.configure.load_library(["astropy.units", "pint"])

    quantity = puw.quantity([1.0, 2.0], "meter", form="pint", parser="pint")
    converted = puw.convert(quantity, to_form="pint", to_unit="centimeter")

    assert puw.get_unit(converted, to_form="string") == "centimeter"
    assert puw.get_value(converted).tolist() == [100.0, 200.0]


def test_get_value_to_unit_string_without_numeric_prefix_works_with_astropy_default_parser():
    pytest.importorskip("astropy.units")

    puw.configure.reset()
    puw.configure.load_library(["astropy.units", "pint"])

    quantity = puw.quantity([100.0, 200.0], "centimeter", form="pint", parser="pint")
    values_in_meter = puw.get_value(quantity, to_unit="meter")

    assert values_in_meter.tolist() == [1.0, 2.0]
