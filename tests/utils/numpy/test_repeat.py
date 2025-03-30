from pyunitwizard._private.exceptions import LibraryWithoutParserError
import pyunitwizard as puw
import pytest
import openmm.unit as openmm_unit
import unyt
import numpy as np

def test_stack_1():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])

    value = np.zeros((1,3,3))
    quantity = puw.quantity(value, 'nm')
    quantity = puw.utils.numpy.repeat(quantity, 4, axis=0, value_type='numpy.ndarray')
    value = puw.get_value(quantity)
    assert value.shape==(4, 3, 3)


