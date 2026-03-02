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


def test_stack_with_explicit_unit_and_tuple_output():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    list_list_quantities = [[puw.quantity(ii, 'nm') for ii in range(3)] for jj in range(2)]
    quantity = puw.utils.numpy.stack(list_list_quantities, to_unit='angstrom', value_type='tuple')
    value = puw.get_value(quantity)
    assert puw.get_unit(quantity) == puw.unit('angstrom')
    np.testing.assert_allclose(value, [[0.0, 10.0, 20.0], [0.0, 10.0, 20.0]])


def test_stack_list_output_and_invalid_value_type():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    list_list_quantities = [[puw.quantity(ii, 'nm') for ii in range(3)] for jj in range(2)]
    quantity = puw.utils.numpy.stack(list_list_quantities, value_type='list')
    np.testing.assert_array_equal(puw.get_value(quantity), [[0, 1, 2], [0, 1, 2]])

    with pytest.raises(ValueError):
        puw.utils.numpy.stack(list_list_quantities, value_type='invalid')
