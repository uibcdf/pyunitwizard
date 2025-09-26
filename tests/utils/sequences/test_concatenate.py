from pyunitwizard._private.exceptions import LibraryWithoutParserError
import pyunitwizard as puw
import pytest
import openmm.unit as openmm_unit
import unyt
import numpy as np

def test_concatenate_1():
    puw.configure.reset()
    puw.configure.load_library(['pint', 'openmm.unit'])

    list_quantities = [ puw.quantity(np.zeros([6,3]), 'nm') for ii in range(10)]
    quantity = puw.utils.sequences.concatenate(list_quantities, value_type='numpy.ndarray')
    value = puw.get_value(quantity)
    assert value.shape==(10, 6, 3)


@pytest.mark.parametrize('value_type', ['list', 'tuple', 'numpy.ndarray'])
def test_concatenate_flat_sequence_value_types(value_type):
    puw.configure.reset()
    puw.configure.load_library('pint')

    sequence = [puw.quantity(index + 1, 'meter') for index in range(3)]
    concatenated = puw.utils.sequences.concatenate(sequence, to_unit='centimeter', value_type=value_type)

    value = puw.get_value(concatenated)
    assert np.array_equal(value, np.array([100, 200, 300]))
    assert puw.get_unit(concatenated, to_form='string') == 'centimeter'


def test_concatenate_nested_sequences_and_error_branch():
    puw.configure.reset()
    puw.configure.load_library('pint')

    nested = [
        [puw.quantity(1, 'meter'), puw.quantity(2, 'meter')],
        [puw.quantity(3, 'meter')],
    ]

    concatenated = puw.utils.sequences.concatenate(nested, to_unit='centimeter', value_type='numpy.ndarray')
    value = puw.get_value(concatenated)
    assert np.array_equal(value, np.array([100, 200, 300]))

    with pytest.raises(ValueError):
        puw.utils.sequences.concatenate(nested, value_type='invalid')


