from pyunitwizard._private.exceptions import LibraryWithoutParserError
import pyunitwizard as puw
import pytest
import openmm.unit as openmm_unit
import unyt
import numpy as np

def test_stack_1():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])

    list_list_quantities = [ [puw.quantity(ii, 'nm') for ii in range(3)] for jj in range(4)]
    quantity = puw.utils.numpy.stack(list_list_quantities, value_type='numpy.ndarray')
    value = puw.get_value(quantity)
    assert value.shape==(4, 3)

def test_stack_2():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])

    aa = puw.quantity([0,1,2,3,4,5,6,7,8,9], 'nm')
    bb = puw.quantity([0,1,2,3,4,5,6,7,8,9], 'nm')
    quantity = puw.utils.numpy.stack([aa,bb], axis=1, value_type='numpy.ndarray')
    value = puw.get_value(quantity)
    assert value.shape==(10, 2)


