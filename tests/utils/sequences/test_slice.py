# This file contains test for get_unit, get_value, and get_dimensionality
import pyunitwizard as puw
import pytest
import numpy as np

def test_get_value_pint():

    item = puw.quantity([0,1,2,3,4,5], 'm', 'pint')
    item2 = puw.utils.sequences.slice(item, [1,3,4,5])
    output = puw.quantity([1,3,4,5], 'm', 'pint')

    assert puw.are_equal(item2, output, same_form=True)

def test_slice_sequence_of_quantities():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    q1 = puw.quantity(1.0, 'm', 'pint')
    q2 = puw.quantity(2.0, 'm', 'pint')
    q3 = puw.quantity(3.0, 'm', 'pint')
    item = [q1, q2, q3]

    sliced = puw.utils.sequences.slice(item, indices=[0, 2])

    assert puw.get_value(sliced).tolist() == [1.0, 3.0]
    assert puw.get_unit(sliced) == "meter"

def test_slice_value_type_ndarray_from_list_values():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    item = puw.quantity([0, 1, 2], 'm', 'pint')
    sliced = puw.utils.sequences.slice(item, start=0, stop=2, value_type='ndarray')

    value = puw.get_value(sliced)
    assert isinstance(value, np.ndarray)
    assert np.all(value == np.array([0, 1]))

def test_slice_tuple_values_with_indices_and_value_type_tuple():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    item = puw.quantity((0, 1, 2, 3), 'm', 'pint')
    sliced = puw.utils.sequences.slice(item, indices=[1, 3], value_type='tuple')

    assert np.allclose(puw.get_value(sliced), np.array([1, 3]))

def test_slice_invalid_item_type_raises():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    with pytest.raises(ValueError):
        puw.utils.sequences.slice(3.14)

def test_slice_invalid_value_type_option_raises():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    item = puw.quantity([0, 1, 2], 'm', 'pint')
    with pytest.raises(ValueError):
        puw.utils.sequences.slice(item, value_type='invalid')

def test_slice_with_to_unit_and_to_form_applies_conversion():

    puw.configure.reset()
    puw.configure.load_library(['pint'])

    item = puw.quantity([0, 1], 'm', 'pint')
    sliced = puw.utils.sequences.slice(item, to_unit='cm', to_form='string')

    assert isinstance(sliced, str)
    assert 'centimeter' in sliced

def test_slice_with_standardized_flag_applies_standardize():

    puw.configure.reset()
    puw.configure.load_library(['pint'])
    puw.configure.set_standard_units(['nm', 'ps'])

    item = puw.quantity([1.0], 'meter', 'pint')
    sliced = puw.utils.sequences.slice(item, standardized=True)

    assert puw.get_unit(sliced) == 'nanometer'
