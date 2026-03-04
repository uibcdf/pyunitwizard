import importlib

import numpy as np
import pyunitwizard as puw
import pytest

from pyunitwizard._private.exceptions import LibraryWithoutParserError
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


def _make_quantity(values, unit_name, form):
    q = puw.quantity(values, unit_name, form="pint", parser="pint")
    if form == "pint":
        return q
    return puw.convert(q, to_form=form)


@pytest.mark.parametrize("form", _available_forms())
def test_minimum_protocol_mandatory_capabilities_across_forms(form):
    libraries = sorted({"pint", form})
    with loaded_libraries(libraries):
        quantity = _make_quantity([1.0, 2.0], "meter", form)
        centimeter = puw.unit("centimeter", form="pint", parser="pint")
        converted = puw.convert(quantity, to_form="pint", to_unit=centimeter)

        assert puw.get_form(quantity) == form
        assert puw.is_quantity(quantity)
        assert puw.is_quantity(converted)
        assert puw.get_unit(quantity, to_form="string")
        meter = puw.unit("meter", form="pint", parser="pint")
        np.testing.assert_allclose(puw.get_value(converted, to_unit=meter), np.array([1.0, 2.0]))
        assert puw.are_compatible(quantity, converted)
        assert puw.check(quantity, dimensionality={"[L]": 1})


def test_minimum_protocol_is_deterministic_under_fixed_configuration():
    with loaded_libraries(["pint"]):
        puw.configure.set_default_form("pint")
        puw.configure.set_default_parser("pint")
        puw.configure.set_standard_units(["nm", "ps", "kcal", "mole"])

        def run_once():
            q = puw.quantity("10 angstrom")
            q2 = puw.convert(q, to_unit="nanometer")
            return puw.get_form(q2), puw.get_unit(q2, to_form="string"), puw.get_value(q2)

        assert run_once() == run_once()


def test_minimum_protocol_incompatible_conversion_fails_explicitly():
    with loaded_libraries(["pint"]):
        q = puw.quantity(1.0, "meter")
        with pytest.raises(Exception):
            puw.convert(q, to_unit="second")


@pytest.mark.parametrize("parser_name", ["openmm.unit", "unyt", "physipy", "quantities"])
def test_minimum_protocol_unsupported_parser_fails_explicitly(parser_name):
    if parser_name not in _available_forms():
        pytest.skip(f"{parser_name} is not available in this environment")

    with loaded_libraries(sorted({"pint", parser_name})):
        with pytest.raises(LibraryWithoutParserError):
            puw.quantity("3 meter", parser=parser_name)
