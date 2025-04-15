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


