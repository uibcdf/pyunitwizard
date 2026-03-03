import pyunitwizard as puw
import unyt
import pytest
from pyunitwizard._private.exceptions import ArgumentError
from pyunitwizard._private.exceptions import NotImplementedMethodError

from .helpers import loaded_libraries


def test_quantity_openmm_unit():

    with loaded_libraries(['pint', 'openmm.unit']):
        openmm_unit = puw.forms.api_openmm_unit.openmm_unit
        quantity = puw.quantity('10 kilojoule/mole', form='openmm.unit')
        q_true = 10 * openmm_unit.kilojoule/openmm_unit.mole
        assert puw.are_close(quantity, q_true)

def test_quantity_pint():

    ureg = puw.forms.api_pint.ureg
    assert puw.quantity(2.5, 
        'nanometers/picoseconds') == ureg.Quantity(2.5, 'nanometers/picoseconds')

def test_quantity_unyt():

    with loaded_libraries(['pint', 'unyt']):
        assert puw.quantity(1.0,
            unyt.J/unyt.s, form="unyt") == 1.0 * unyt.J/unyt.s

def test_quantity_string_value_with_explicit_unit_string():

    with loaded_libraries(['pint']):
        q = puw.quantity("2.5", unit="meter", form="pint", parser="pint")
        assert puw.get_value(q) == 2.5
        assert puw.get_unit(q) == "meter"

def test_quantity_string_value_with_unit_object():

    with loaded_libraries(['pint']):
        unit = puw.unit("meter", form="pint")
        q = puw.quantity("2.5", unit=unit, form="pint", parser="pint")
        assert puw.get_value(q) == 2.5
        assert puw.get_unit(q) == "meter"

def test_quantity_string_value_without_unit_is_promoted_to_quantity():

    with loaded_libraries(['pint']):
        q = puw.quantity("meter", form="pint", parser="pint")
        assert puw.get_value(q) == 1
        assert puw.get_unit(q) == "meter"

def test_quantity_numeric_without_unit_raises():

    with loaded_libraries(['pint']):
        with pytest.raises(ArgumentError):
            puw.quantity(2.5, form="pint")

def test_quantity_standardized_flag_applies_standardize():

    with loaded_libraries(['pint']):
        puw.configure.set_standard_units(["nm", "ps", "kcal", "mole"])
        q = puw.quantity(1.0, "meter", form="pint", standardized=True)
        assert puw.get_unit(q) == "nanometer"


def test_quantity_string_without_unit_raises_when_parser_returns_non_quantity(monkeypatch):
    with loaded_libraries(['pint']):
        monkeypatch.setattr("pyunitwizard.api.conversion.convert", lambda *args, **kwargs: "not-a-quantity")
        with pytest.raises(ArgumentError):
            puw.quantity("meter", form="pint", parser="pint")


def test_quantity_string_with_unit_object_uses_unit_object_branch():
    with loaded_libraries(['pint']):
        unit = puw.unit("meter", form="pint")
        q = puw.quantity("2.5", unit=unit, form="pint", parser="pint")
        assert puw.get_value(q) == 2.5
        assert puw.get_unit(q) == "meter"


def test_quantity_numeric_raises_not_implemented_method_when_backend_fails(monkeypatch):
    with loaded_libraries(['pint']):
        monkeypatch.setitem(puw.forms.dict_make_quantity, "pint", lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("boom")))
        with pytest.raises(NotImplementedMethodError):
            puw.quantity(2.5, "meter", form="pint")


def test_quantity_string_with_non_unit_object_returns_none_current_behavior():
    with loaded_libraries(['pint']):
        output = puw.quantity("2.5", unit=object(), form="pint", parser="pint")
        assert output is None
