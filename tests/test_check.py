import numpy as np
import pytest
import pyunitwizard as puw
from pyunitwizard.api.introspection import is_dimensionless

#### Tests for puw.check() function ####

def test_check_no_parameters():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    quantity = puw.quantity(0.4,'cm')
    assert puw.check(quantity)

def test_check_not_quantity():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    assert not puw.check(2)

def test_check_value_type():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    quantity = puw.quantity(0.4,'cm')
    assert puw.check(quantity, value_type=float)

    quantity = puw.quantity(4, 'cm')
    assert puw.check(quantity, value_type=int)

    quantity = puw.quantity(np.array([1.5, 2.0]), 's')
    assert puw.check(quantity, value_type=np.ndarray)
    
def test_check_unit():

    puw.configure.reset()
    puw.configure.load_library(['pint'])
    
    quantity = puw.quantity(0.4,'cm')
    assert puw.check(quantity, unit='cm')

    quantity = puw.quantity(np.array([1.5, 2.0]), 's')
    assert puw.check(quantity, unit='s')

def test_check_dimensionality():
    
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    quantity = puw.quantity(0.4,'cm')
    assert puw.check(quantity, dimensionality={'[L]':1})

    quantity = puw.quantity(np.array([1.5, 2.0]), 'm/s')
    assert puw.check(quantity, dimensionality={'[L]': 1, '[T]': -1})

    quantity = puw.quantity(4, 'kcal')
    assert puw.check(quantity, dimensionality={'[L]': 2, '[T]': -2, '[M]': 1})
    
def test_check_multiple():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    quantity = puw.quantity(np.zeros([3,3]),'nm/ps')
    assert puw.check(quantity, dimensionality={'[L]':1, '[T]':-1}, value_type=np.ndarray, dtype_name='float64')
    assert not puw.check(quantity, dimensionality={'[L]':1, '[T]':-1}, value_type=np.ndarray, dtype_name='int')

    quantity = puw.quantity(np.zeros([3,3], dtype=np.int64),'nm/ps')
    assert puw.check(quantity, dimensionality={'[L]':1, '[T]':-1}, value_type=np.ndarray, dtype_name='int64')

    quantity = puw.quantity([0,0,0], 'nm/ps')
    assert puw.check(quantity, dimensionality={'[L]':1, '[T]':-1}, value_type=np.ndarray, shape=(3,))

@pytest.fixture
def pint_quantity():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    """ Returns a pint quantity. """
    ureg = puw.forms.api_pint.ureg
    return ureg.Quantity(2.5, 'nanometers/picoseconds')

@pytest.fixture
def openmm_quantity():

    puw.configure.reset()
    puw.configure.load_library(['pint','openmm.unit'])

    """ Returns an openmm quantity"""
    openmm_unit = puw.forms.api_openmm_unit.openmm_unit
    return  5 * openmm_unit.kilojoule/openmm_unit.mole

@pytest.fixture
def unyt_quantity():

    puw.configure.reset()
    puw.configure.load_library(['pint', 'unyt'])

    unyt = puw.forms.api_unyt.unyt
    return 5 * unyt.nm/unyt.ps

@pytest.fixture
def pint_unit():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    """ Returns a pint unit"""
    ureg = puw.forms.api_pint.ureg
    return ureg.meter

@pytest.fixture
def openmm_unit():
    
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])

    """ Returns an openmm unit"""
    openmm_unit = puw.forms.api_openmm_unit.openmm_unit
    return openmm_unit.meter

@pytest.fixture
def unyt_unit():

    puw.configure.reset()
    puw.configure.load_library(['pint', 'unyt'])

    """Returns a unyt unit"""
    unyt = puw.forms.api_unyt.unyt
    return unyt.m

#### Tests for puw.is_unit ####
def test_is_unit_str():
    pass

def test_is_unit_quantity(pint_quantity, 
        openmm_quantity,unyt_quantity):

    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit', 'unyt'])
    
    assert not puw.is_unit(pint_quantity)
    assert not puw.is_unit(openmm_quantity)
    assert not puw.is_unit(unyt_quantity)

def test_is_unit_pint_unit(pint_unit):

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    assert puw.is_unit(pint_unit)

def test_is_unit_openmm_unit(openmm_unit):

    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])

    assert puw.is_unit(openmm_unit)

def test_is_unit_unyt(unyt_unit):

    puw.configure.reset()
    puw.configure.load_library(['pint', 'unyt'])

    assert puw.is_unit(unyt_unit)

#### Tests for puw.is_quantity ####

def test_is_quantity_str():
    pass

def test_is_quantity_pint_quantity(pint_quantity):

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    assert puw.is_quantity(pint_quantity)

def test_is_quantity_openmm_quantity(openmm_quantity):

    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])

    assert puw.is_quantity(openmm_quantity)

def test_is_quantity_unyt_quantity(unyt_quantity):

    puw.configure.reset()
    puw.configure.load_library(['pint', 'unyt'])

    assert puw.is_quantity(unyt_quantity)

def test_is_quantity_unit(pint_unit, openmm_unit, unyt_unit):

    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit', 'unyt'])

    assert not puw.is_quantity(pint_unit)
    assert not puw.is_quantity(openmm_unit)
    assert not puw.is_quantity(unyt_unit)

#### Tests for is dimensionless ####

def test_is_dimensionless(pint_quantity):

    puw.configure.reset()
    puw.configure.load_library(['pint'])
    
    quantity = puw.quantity(2, "radian")
    assert is_dimensionless(quantity)

    assert not is_dimensionless(pint_quantity)
