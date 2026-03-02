from pyunitwizard._private.exceptions import LibraryWithoutParserError
import pyunitwizard as puw
import pytest
import openmm.unit as openmm_unit
import unyt
import numpy as np

def test_column_stack_1():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])

    aa = puw.quantity([0,1,2,3,4,5,6,7,8,9], 'nm')
    bb = puw.quantity([0,1,2,3,4,5,6,7,8,9], 'nm')
    quantity = puw.utils.numpy.column_stack([aa,bb], value_type='numpy.ndarray')
    value = puw.get_value(quantity)
    assert value.shape==(10, 2)


def test_column_stack_with_explicit_unit_and_tuple_output():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    aa = puw.quantity([0, 1, 2], 'nm')
    bb = puw.quantity([3, 4, 5], 'nm')
    quantity = puw.utils.numpy.column_stack([aa, bb], to_unit='angstrom', value_type='tuple')
    value = puw.get_value(quantity)
    assert puw.get_unit(quantity) == puw.unit('angstrom')
    np.testing.assert_allclose(value, [[0.0, 30.0], [10.0, 40.0], [20.0, 50.0]])


def test_column_stack_list_output_and_invalid_value_type():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    aa = puw.quantity([0, 1, 2], 'nm')
    bb = puw.quantity([3, 4, 5], 'nm')
    quantity = puw.utils.numpy.column_stack([aa, bb], value_type='list')
    np.testing.assert_array_equal(puw.get_value(quantity), [[0, 3], [1, 4], [2, 5]])

    with pytest.raises(ValueError):
        puw.utils.numpy.column_stack([aa, bb], value_type='invalid')
