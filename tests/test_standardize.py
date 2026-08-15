# This file contains test for get_standard_units and standardize
import pyunitwizard as puw
from pyunitwizard._private.exceptions import NoStandardsError
import openmm.unit as openmm_unit
import pytest
import numpy as np
import unyt
from pyunitwizard.api.standardization import _standard_units_lstsq

puw.configure.reset()
puw.configure.load_library(['pint', 'openmm.unit', 'unyt'])

### Tests for get standard units ####

def test_raises_no_standard_error():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    with pytest.raises(NoStandardsError):
        quantity = puw.quantity(value=3.0, unit='radian', form='pint')
        puw.get_standard_units(quantity)
    
    with pytest.raises(NoStandardsError):
        quantity = puw.quantity(value=3.0, unit='meter', form='pint')
        puw.get_standard_units(quantity)

def test_get_standard_units_pint_quantity():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])

    quantity = puw.quantity(value=[3.0, 5.0, 5.0], unit='joules', form='pint')
    standard_unit = puw.get_standard_units(quantity)
    assert standard_unit == "kcal"

def test_get_standard_units_openmm_quantity():
    puw.configure.reset()
    puw.configure.load_library(['pint','openmm.unit'])
    puw.configure.set_standard_units([openmm_unit.meter, openmm_unit.second, openmm_unit.joule])

    quantity = puw.quantity(value=5.0, unit=openmm_unit.centimeter/openmm_unit.picosecond, form='openmm.unit')
    standard_unit = puw.get_standard_units(quantity)
    assert standard_unit == "meter/second"

def test_get_standard_units_unyt_quantity():
    puw.configure.reset()
    puw.configure.load_library(['pint','unyt'])
    puw.configure.set_standard_units([unyt.m, unyt.s, unyt.J])

    quantity = puw.quantity(value=5.0, unit=unyt.cm/unyt.ps, form='unyt')
    standard_unit = puw.get_standard_units(quantity, form='string')
    assert standard_unit == "meter / second"

def test_get_standard_units_dimensionality():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])

    standard_unit = puw.get_standard_units(dimensionality={'[L]':1}, form='string')
    assert standard_unit == "nanometer"

    standard_unit = puw.get_standard_units(dimensionality={'[L]':1})
    unit = puw.unit("nanometer", form="pint")
    assert standard_unit == unit

def test_get_standard_units_adimensional_from_dimensionality_only():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['radian'])

    standard_unit = puw.get_standard_units(dimensionality={}, form='string')
    assert standard_unit == "radian"


def test_get_standard_units_populates_dimensionality_cache():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps'])

    assert puw.kernel.standard_units_by_dimensionality_cache == {}

    standard_unit = puw.get_standard_units(dimensionality={'[L]': 1}, form='string')

    assert standard_unit == 'nanometer'
    assert puw.kernel.standard_units_by_dimensionality_cache[
        (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    ] == 'nm'


def test_set_standard_units_invalidates_dimensionality_cache():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm'])

    assert puw.get_standard_units(dimensionality={'[L]': 1}, form='string') == 'nanometer'
    assert puw.kernel.standard_units_by_dimensionality_cache

    puw.configure.set_standard_units(['angstrom'])

    assert puw.kernel.standard_units_by_dimensionality_cache == {}
    assert puw.get_standard_units(dimensionality={'[L]': 1}, form='string') == 'angstrom'


### Tests for standardize ###

def test_standardize_pint_quantity():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])

    quantity = puw.quantity(1.0, "meter", form="pint")
    quantity = puw.standardize(quantity)
    assert np.allclose(puw.get_value(quantity), 1e9)
    assert quantity.units == "nanometer"

    quantity = puw.quantity([1e-12, 2e-12], "second", form="pint")
    quantity = puw.standardize(quantity)
    assert np.allclose(puw.get_value(quantity), [1.0, 2.0])
    assert quantity.units == "picosecond"


def test_standardize_already_canonical_quantity_returns_same_object():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_standard_units(["nm"])

    quantity = puw.quantity([1.0, 2.0], "nm", form="pint")

    assert puw.standardize(quantity) is quantity


def test_standardize_canonical_fast_path_does_not_recompute_dimensionality(
    monkeypatch,
):
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_standard_units(["nm"])
    quantity = puw.quantity([1.0, 2.0], "nm", form="pint")

    def fail_if_called(_quantity):
        raise AssertionError("dimensionality lookup is forbidden on the fast path")

    monkeypatch.setattr(
        "pyunitwizard.api.standardization.get_dimensionality", fail_if_called
    )

    assert puw.standardize(quantity) is quantity


def test_standardize_does_not_bypass_first_standard_for_same_dimensionality():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_standard_units(["nm", "angstrom"])
    quantity = puw.quantity(1.0, "angstrom", form="pint")

    output = puw.standardize(quantity)

    assert output is not quantity
    assert puw.has_unit(output, "nm") is True


def test_standardize_keeps_form_conversion_for_canonical_unit():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])
    puw.configure.set_default_form("pint")
    puw.configure.set_standard_units(["nm"])

    quantity = puw.quantity([1.0, 2.0], "nm", form="openmm.unit")
    output = puw.standardize(quantity)

    assert output is not quantity
    assert puw.get_form(output) == "pint"
    assert puw.has_unit(output, "nm") is True

def test_standardize_openmm_quantity():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])
    puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])

    quantity = puw.quantity(1.0, openmm_unit.meter, form="openmm.unit")
    quantity = puw.standardize(quantity)
    assert np.allclose(puw.get_value(quantity), 1e9)
    assert puw.get_unit(quantity) == "nanometer"

    quantity = puw.quantity([1e-12, 2e-12], openmm_unit.second, form="openmm.unit")
    quantity = puw.standardize(quantity)
    assert np.allclose(puw.get_value(quantity), [1.0, 2.0])
    assert puw.get_unit(quantity) == "picosecond"

def test_standardize_unyt_quantity():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'unyt'])
    puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])

    quantity = puw.quantity(1.0, unyt.m, form="unyt")
    quantity = puw.standardize(quantity)
    assert np.allclose(puw.get_value(quantity), 1e9)
    assert str(puw.get_unit(quantity)) == "nanometer"

    quantity = puw.quantity([1e-12, 2e-12], unyt.s, form="unyt")
    quantity = puw.standardize(quantity)
    assert np.allclose(puw.get_value(quantity), [1.0, 2.0])
    assert str(puw.get_unit(quantity)) == "picosecond"

def test_get_standard_units_uses_tentative_base_standards_for_combinations():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm*ps'])

    standard_unit = puw.get_standard_units(dimensionality={'[L]': 1, '[T]': 1}, form='string')
    assert standard_unit == 'nm*ps'

def test_standardize_unit_input_returns_standard_unit():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps'])

    standardized_unit = puw.standardize(puw.unit('meter', form='pint'))
    assert puw.get_unit(standardized_unit) == 'nanometer'

def test_get_standard_units_without_args_uses_adimensional_standard():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['radian'])

    standard_unit = puw.get_standard_units(form='string')
    assert standard_unit == 'radian'

def test_get_standard_units_combination_raises_without_fundamental_standards():
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['radian'])

    with pytest.raises(NoStandardsError):
        puw.get_standard_units(dimensionality={'[L]': 1, '[T]': 1}, form='string')

def test_standard_units_lstsq_returns_none_when_unsatisfied():
    solution = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    standards = {'second': np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0])}
    assert _standard_units_lstsq(solution, standards) is None


def test_standardize_resolves_the_input_form_once(monkeypatch):
    """standardize() must not re-resolve a form it has already resolved.

    It resolves the input form and then hands it to
    ``_matching_configured_standard``; that helper previously resolved the very
    same object again.
    """
    import importlib

    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps'])

    standardization = importlib.import_module("pyunitwizard.api.standardization")
    original_get_form = standardization.get_form
    inputs = []

    def counting_get_form(item, *args, **kwargs):
        inputs.append(item)
        return original_get_form(item, *args, **kwargs)

    monkeypatch.setattr(standardization, "get_form", counting_get_form)

    quantity = puw.quantity(1.0, 'meter', form='pint')
    puw.standardize(quantity)

    assert inputs == [quantity]


def test_get_dimensionality_extracts_the_unit_without_reconverting(monkeypatch):
    """get_dimensionality() must not re-enter convert() to read the unit.

    The unit is only used to build the cache key, so it is taken from the form
    dispatch already resolved. Routing it through the public ``get_unit()``
    re-entered ``convert()`` and resolved the same form twice more.
    """
    import importlib

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    # Built before instrumenting: quantity() legitimately goes through convert().
    quantity = puw.quantity(1.0, 'nanometer', form='pint')

    conversion = importlib.import_module("pyunitwizard.api.conversion")
    calls = []
    original_convert = conversion.convert

    def counting_convert(*args, **kwargs):
        calls.append(args[:1])
        return original_convert(*args, **kwargs)

    monkeypatch.setattr(conversion, "convert", counting_convert)

    assert puw.get_dimensionality(quantity)['[L]'] == 1

    assert calls == []
