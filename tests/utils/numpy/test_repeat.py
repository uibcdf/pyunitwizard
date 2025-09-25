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


@pytest.mark.parametrize('value_type', [None, 'list', 'tuple', 'numpy.ndarray'])
def test_repeat_respects_requested_unit(value_type):
    puw.configure.reset()
    puw.configure.load_library('pint')

    quantity = puw.quantity([1, 2], 'meter')
    repeated = puw.utils.numpy.repeat(quantity, 2, to_unit='centimeter', value_type=value_type)

    value = puw.get_value(repeated)
    assert np.array_equal(value, np.array([1, 1, 2, 2]))
    assert np.allclose(puw.get_value(repeated, to_unit='meter'), np.array([0.01, 0.01, 0.02, 0.02]))
    assert puw.get_unit(repeated, to_form='string') == 'centimeter'


def test_repeat_raises_for_unknown_value_type():
    puw.configure.reset()
    puw.configure.load_library('pint')

    quantity = puw.quantity([1, 2], 'meter')

    with pytest.raises(ValueError):
        puw.utils.numpy.repeat(quantity, 1, value_type='invalid')

