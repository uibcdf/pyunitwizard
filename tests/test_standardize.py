# This file contains test for get_standard_units and standardize
import pyunitwizard as puw
from pyunitwizard._private.exceptions import NoStandardsError
import openmm.unit as openmm_unit
import pytest
import numpy as np
import unyt
from pyunitwizard.api.standardization import _standard_units_lstsq
import pyunitwizard.api.standardization as standardization_module

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


def test_get_standard_units_combination_uses_tentative_base_when_fundamental_lstsq_fails(monkeypatch):
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps'])

    original_lstsq = standardization_module._standard_units_lstsq
    calls = {"n": 0}

    def fake_lstsq(solution, standards):
        calls["n"] += 1
        if calls["n"] == 1:
            return None
        return original_lstsq(solution, standards)

    monkeypatch.setattr(standardization_module, "_standard_units_lstsq", fake_lstsq)

    standard_unit = puw.get_standard_units(dimensionality={'[L]': 1, '[T]': 1}, form='string')
    assert standard_unit == 'nanometer * picosecond'
    assert calls["n"] >= 2


def test_get_standard_units_raises_when_all_lstsq_strategies_fail(monkeypatch):
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps'])

    monkeypatch.setattr(standardization_module, "_standard_units_lstsq", lambda *_args, **_kwargs: None)

    with pytest.raises(NoStandardsError):
        puw.get_standard_units(dimensionality={'[L]': 1, '[T]': 1}, form='string')


def test_standardize_fallback_except_path_when_initial_convert_fails(monkeypatch):
    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])

    quantity = puw.quantity(1.0, "meter", form="pint")
    original_convert = standardization_module.convert
    calls = {"n": 0}

    def flaky_convert(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("force standardize fallback")
        return original_convert(*args, **kwargs)

    monkeypatch.setattr(standardization_module, "convert", flaky_convert)

    standardized = puw.standardize(quantity)
    assert puw.get_unit(standardized) == "nanometer"
    assert np.allclose(puw.get_value(standardized), 1e9)
