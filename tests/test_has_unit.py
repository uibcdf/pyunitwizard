import importlib

import pint
import pytest

import pyunitwizard as puw
from tests.helpers import loaded_libraries

_BACKEND_CANDIDATES = [
    ("pint", "pint"),
    ("openmm.unit", "openmm.unit"),
    ("unyt", "unyt"),
    ("astropy.units", "astropy.units"),
    ("physipy", "physipy"),
    ("quantities", "quantities"),
]


def _available_forms():
    forms = []
    for form, module_name in _BACKEND_CANDIDATES:
        try:
            importlib.import_module(module_name)
        except Exception:
            continue
        forms.append(form)
    return forms


@pytest.mark.parametrize("form", _available_forms())
def test_has_unit_distinguishes_exact_units_across_backends(form):
    with loaded_libraries(sorted({"pint", form})):
        quantity = puw.quantity(2.0, "nanometer", form=form, parser="pint")
        current_unit = puw.get_unit(quantity)
        different_unit = puw.unit("second", form=form, parser="pint")

        assert puw.has_unit(quantity, current_unit, parser="pint") is True
        assert puw.has_unit(quantity, different_unit, parser="pint") is False


def test_has_unit_normalizes_string_aliases_without_converting_values():
    with loaded_libraries(["pint"]):
        quantity = puw.quantity(2.0, "nanometer")

        assert puw.has_unit(quantity, "nm") is True
        assert puw.has_unit(quantity, "angstrom") is False


def test_has_unit_uses_the_registry_of_an_external_pint_quantity():
    registry = pint.UnitRegistry()
    quantity = registry.Quantity(2.0, "nanometer")

    assert puw.has_unit(quantity, "nm") is True
    assert puw.has_unit(quantity, "angstrom") is False


def test_has_unit_does_not_extract_the_quantity_magnitude(monkeypatch):
    with loaded_libraries(["pint"]):
        quantity = puw.quantity([1.0, 2.0], "nanometer")

        def fail_if_called(_quantity):
            raise AssertionError("magnitude extraction is forbidden")

        monkeypatch.setitem(puw.forms.dict_get_value, "pint", fail_if_called)

        assert puw.has_unit(quantity, "nanometer") is True


def test_has_unit_accepts_a_unit_object_and_text_is_undecidable():
    with loaded_libraries(["pint"]):
        quantity = puw.quantity(1.0, "nanometer")
        target = puw.unit("nm")

        assert puw.has_unit(quantity, target) is True
        assert puw.has_unit("1 nanometer", "nanometer") is None


def test_check_uses_has_unit_without_extracting_values(monkeypatch):
    with loaded_libraries(["pint"]):
        quantity = puw.quantity([1.0, 2.0], "nanometer")

        def fail_if_called(_quantity):
            raise AssertionError("magnitude extraction is forbidden")

        monkeypatch.setitem(puw.forms.dict_get_value, "pint", fail_if_called)

        assert puw.check(quantity, unit="nm") is True
        assert puw.check(quantity, unit="angstrom") is False
