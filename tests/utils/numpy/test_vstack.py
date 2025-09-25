import numpy as np
import pyunitwizard as puw
import pytest


def configure_libraries():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])


def test_vstack_numpy_array_shape():
    configure_libraries()

    sequence = [
        [puw.quantity([1, 2], "nanometer")],
        [puw.quantity([10, 20], "angstrom")],
    ]

    quantity = puw.utils.numpy.vstack(sequence, to_unit="nanometer", value_type="numpy.ndarray")
    value = puw.get_value(quantity)

    assert value.shape == (2, 2)
    np.testing.assert_allclose(value, [[1.0, 2.0], [1.0, 2.0]])


def test_vstack_tuple_value_type_matches_expected_values():
    configure_libraries()

    sequence = [
        [puw.quantity([1, 2], "meter")],
        [puw.quantity([3, 4], "meter")],
    ]

    quantity = puw.utils.numpy.vstack(sequence, value_type="tuple")
    value = puw.get_value(quantity)

    np.testing.assert_array_equal(value, [[1, 2], [3, 4]])


def test_vstack_invalid_value_type():
    configure_libraries()

    sequence = [[puw.quantity(1, "meter")]]

    with pytest.raises(ValueError):
        puw.utils.numpy.vstack(sequence, value_type="set")
