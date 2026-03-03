from pyunitwizard.parse import (
    _find_closing_bracket_position,
    _find_closing_parenthesis_position,
    _parse_with_pint,
    parse,
)
import numpy as np
import pyunitwizard as puw
import pytest
from pyunitwizard._private.exceptions import (
    ArgumentError,
    LibraryWithoutParserError,
)

from .helpers import loaded_libraries


def test_parse_with_pint_scalar():

    quantity = _parse_with_pint("5 meters")
    assert quantity.magnitude == 5
    assert str(quantity.units) == "meter"

def test_parse_with_pint_array():

    quantity = _parse_with_pint("[2] mole")
    assert np.allclose(quantity.magnitude, np.array([2]))
    assert str(quantity.units) == "mole"

    quantity = _parse_with_pint("[2, 5, 7] joules")
    assert np.allclose(quantity.magnitude, np.array([2, 5, 7]))
    assert str(quantity.units) == "joule"

    quantity = _parse_with_pint("(3, 2, 1) meters")
    assert np.allclose(quantity.magnitude, np.array([3, 2, 1]))
    assert str(quantity.units) == "meter"

    quantity = _parse_with_pint("[[2, 5, 7], [7, 8, 9]] kilojoules/(mol*nanometer)")
    assert np.allclose(quantity.magnitude, np.array([[2, 5, 7], [7, 8, 9]]))
    assert str(quantity.units) == "kilojoule / mole / nanometer"

def test_parse_to_pint():
    
    quantity = parse("[2, 5, 7] joules", to_form="pint")
    assert np.allclose(quantity.magnitude, np.array([2, 5, 7]))
    assert str(quantity.units) == "joule"

def test_parse_to_string():

    quantity = _parse_with_pint("5 meters")
    assert quantity.magnitude == 5
    assert str(quantity.units) == "meter"

    quantity = parse("5 meter", to_form="string")
    assert isinstance(quantity, str)
    assert quantity == "5 meter"

    quantity = parse("[2, 5, 7] joules", to_form="string")
    assert isinstance(quantity, str)
    assert quantity == "[2 5 7] joule"

def test_parse_to_openmm_scalar():

    with loaded_libraries(['pint', 'openmm.unit']):
        quantity = parse("5 meters", to_form="openmm.unit")
        assert quantity._value == 5
        assert str(quantity.unit) == "meter"

def test_parse_to_openmm_array():

    with loaded_libraries(['pint', 'openmm.unit']):
        quantity = parse("[2, 5, 7] joules", to_form="openmm.unit")
        assert np.allclose(quantity._value, np.array([2, 5, 7]))
        assert str(quantity.unit) == "joule"

        quantity = parse("(3, 2, 1) meters", to_form="openmm.unit")
        assert np.allclose(quantity._value, np.array([3, 2, 1]))
        assert str(quantity.unit) == "meter"

        quantity = parse("[[2, 5, 7], [7, 8, 9]] joules", to_form="openmm.unit")
        assert np.allclose(quantity._value, np.array([[2, 5, 7], [7, 8, 9]]))
        assert str(quantity.unit) == "joule"


def test_parse_to_unyt():

    with loaded_libraries(['pint', 'unyt']):
        quantity = parse("5 meters", to_form="unyt")
        assert quantity.value == 5
        assert str(quantity.units) == "m"

        quantity = parse("[2, 5, 7] joules", to_form="unyt")
        assert np.allclose(quantity.value, np.array([2, 5, 7]))
        assert str(quantity.units) == "J"

        quantity = parse("(3, 2, 1) meters", to_form="unyt")
        assert np.allclose(quantity.value, np.array([3, 2, 1]))
        assert str(quantity.units) == "m"

        quantity = parse("[[2, 5, 7], [7, 8, 9]] joules", to_form="unyt")
        assert np.allclose(quantity.value, np.array([[2, 5, 7], [7, 8, 9]]))
        assert str(quantity.units) == "J"


def test_parse_library_without_parser_has_readable_message():
    with pytest.raises(LibraryWithoutParserError) as excinfo:
        parse("1 nm", parser="openmm.unit")

    message = str(excinfo.value)
    assert isinstance(message, str)
    assert message.strip() != ""
    assert "parser" in message.lower()

def test_parse_rejects_non_string_input():
    with pytest.raises(ArgumentError):
        parse(3.0)  # type: ignore[arg-type]

def test_parse_rejects_invalid_parser_name():
    with pytest.raises(ValueError):
        parse("1 nm", parser="unknown")

def test_parse_bracket_helpers_raise_on_unbalanced_input():
    with pytest.raises(ValueError):
        _find_closing_bracket_position("[1, 2")
    with pytest.raises(ValueError):
        _find_closing_parenthesis_position("(1, 2")

def test_parse_parenthesis_helper_handles_nested_parentheses():
    text = "((1, 2), (3, 4)) meters"
    idx = _find_closing_parenthesis_position(text)
    assert idx == text.index(") meters")

def test_parse_with_astropy_parser_if_available():
    pytest.importorskip("astropy.units")
    with loaded_libraries(['pint', 'astropy.units']):
        quantity = parse("2 meter", parser="astropy.units", to_form="string")
        assert isinstance(quantity, str)
        assert "2" in quantity
        assert "m" in quantity.lower()


def test_parse_with_unyt_parser_raises_library_without_parser():
    with pytest.raises(LibraryWithoutParserError):
        parse("1 nm", parser="unyt")


def test_parse_with_astropy_parser_to_multiple_forms_if_available():
    pytest.importorskip("astropy.units")
    with loaded_libraries(['pint', 'openmm.unit', 'unyt', 'astropy.units']):
        q_pint = parse("2 meter", parser="astropy.units", to_form="pint")
        assert puw.get_form(q_pint) == "pint"

        q_openmm = parse("2 meter", parser="astropy.units", to_form="openmm.unit")
        assert puw.get_form(q_openmm) == "openmm.unit"

        q_unyt = parse("2 meter", parser="astropy.units", to_form="unyt")
        assert puw.get_form(q_unyt) == "unyt"


def test_parse_rejects_unknown_to_form_for_pint_parser():
    with pytest.raises(ValueError):
        parse("1 meter", parser="pint", to_form="unknown")

def test_parse_rejects_unknown_to_form_for_astropy_parser():
    pytest.importorskip("astropy.units")
    with pytest.raises(ValueError):
        parse("1 meter", parser="astropy.units", to_form="unknown")

def test_parse_rejects_unknown_parser_before_dispatch():
    with pytest.raises(ValueError):
        parse("1 meter", parser="unknown-parser", to_form="pint")
