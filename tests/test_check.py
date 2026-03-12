import numpy as np
import pytest
import pyunitwizard as puw
from pyunitwizard.api.introspection import _DIMENSIONALITY_CACHE, is_dimensionless

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
    assert not puw.check(quantity, value_type=list)
    
def test_check_unit():

    puw.configure.reset()
    puw.configure.load_library(['pint'])
    
    quantity = puw.quantity(0.4,'cm')
    assert puw.check(quantity, unit='cm')

    quantity = puw.quantity(np.array([1.5, 2.0]), 's')
    assert puw.check(quantity, unit='s')
    assert not puw.check(quantity, unit='m')

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
    assert not puw.check(quantity, shape=(2,))

def test_check_unit_constraints():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    unit = puw.unit('nm')
    assert puw.check(unit, unit='nm')
    assert puw.check(unit, dimensionality={'[L]': 1})
    assert not puw.check(unit, dimensionality={'[T]': 1})
    assert not puw.check(unit, unit='ps')

def test_check_dtype_name_on_scalar_quantity_returns_false():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    quantity = puw.quantity(3.0, 'nm')
    assert not puw.check(quantity, dtype_name='float64')

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
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    assert puw.is_unit('meter')

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
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    assert puw.is_quantity('1 meter')

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


def test_get_dimensionality_from_unit_string_path():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    dim = puw.get_dimensionality('meter')
    assert isinstance(dim, dict)
    assert dim.get('[L]') == 1


def test_get_dimensionality_populates_cache_for_quantity_and_returns_copy():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    quantity = puw.quantity(2.0, 'meter')
    dim = puw.get_dimensionality(quantity)

    assert ('pint', 'meter') in _DIMENSIONALITY_CACHE
    dim['[L]'] = 99
    assert puw.get_dimensionality(quantity)['[L]'] == 1


def test_reset_clears_dimensionality_cache():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    puw.get_dimensionality(puw.unit('meter'))
    assert len(_DIMENSIONALITY_CACHE) > 0

    puw.configure.reset()

    assert _DIMENSIONALITY_CACHE == {}
