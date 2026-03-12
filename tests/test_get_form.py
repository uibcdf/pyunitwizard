import pyunitwizard as puw
import openmm.unit as openmm_unit
import unyt
import pytest
from pyunitwizard.api.introspection import _TYPE_TO_FORM_CACHE

def test_string():
    assert puw.get_form('1 meter')=='string'

def test_pint_quantity():
    
    ureg = puw.forms.api_pint.ureg
    quantity = ureg.Quantity(1.0,'meter')
    assert puw.get_form(quantity)=='pint'

def test_pint_unit():
   
    ureg = puw.forms.api_pint.ureg
    unit = ureg.Unit('meter')
    assert puw.get_form(unit)=='pint'

def test_openmm_unit():
    
    assert puw.get_form(openmm_unit.meter/openmm_unit.second) == "openmm.unit"
    assert puw.get_form(openmm_unit.ampere) == "openmm.unit"

def test_openmm_quantity():

    quantity = 1 * openmm_unit.meter
    assert puw.get_form(quantity) == "openmm.unit"

    quantity = 4.0 * openmm_unit.ampere
    assert puw.get_form(quantity) == "openmm.unit"

    quantity = [2.0, 3.0] * openmm_unit.second
    assert puw.get_form(quantity) == "openmm.unit"

def test_unyt_unit():
    assert puw.get_form(unyt.m/unyt.s) == "unyt"
    assert puw.get_form(unyt.A) == "unyt"

def test_unyt_quantity():

    quantity = 1 * unyt.m
    assert puw.get_form(quantity) == "unyt"

    quantity = 4.0 * unyt.A
    assert puw.get_form(quantity) == "unyt"

    quantity = [2.0, 3.0] * unyt.s
    assert puw.get_form(quantity) == "unyt"


def test_astropy_quantity_and_unit_if_available():
    astropy_units = pytest.importorskip("astropy.units")

    puw.configure.reset()
    puw.configure.load_library(['pint', 'astropy.units'])

    assert puw.get_form(2.0 * astropy_units.m) == "astropy.units"
    assert puw.get_form(astropy_units.m) == "astropy.units"


def test_physipy_quantity_if_available():
    pytest.importorskip("physipy")

    puw.configure.reset()
    puw.configure.load_library(['pint', 'physipy'])

    quantity = puw.quantity(1.0, 'meter', form='physipy')
    assert puw.get_form(quantity) == "physipy"


def test_quantities_quantity_if_available():
    pytest.importorskip("quantities")

    puw.configure.reset()
    puw.configure.load_library(['pint', 'quantities'])

    quantity = puw.quantity(1.0, 'meter', form='quantities')
    assert puw.get_form(quantity) == "quantities"


def test_reset_clears_get_form_type_cache():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    quantity = puw.quantity(1.0, 'meter', form='pint')
    assert puw.get_form(quantity) == 'pint'
    assert len(_TYPE_TO_FORM_CACHE) > 0

    puw.configure.reset()

    assert _TYPE_TO_FORM_CACHE == {}
