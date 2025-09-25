import numpy as np
import pyunitwizard as puw
import pytest


def configure_libraries():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])


def test_hstack_numpy_array_with_unit_conversion():
    configure_libraries()

    sequence = [
        [puw.quantity(1, "nanometer"), puw.quantity(2, "nanometer")],
        [puw.quantity(10, "angstrom"), puw.quantity(20, "angstrom")],
    ]

    quantity = puw.utils.numpy.hstack(sequence, to_unit="nanometer", value_type="numpy.ndarray")
    value = puw.get_value(quantity)

    np.testing.assert_allclose(value, [1.0, 2.0, 1.0, 2.0])
    assert str(puw.get_unit(quantity)) == "nanometer"


def test_hstack_list_value_type_matches_expected_values():
    configure_libraries()

    sequence = [
        [puw.quantity(1, "meter"), puw.quantity(2, "meter")],
        [puw.quantity(3, "meter"), puw.quantity(4, "meter")],
    ]

    quantity = puw.utils.numpy.hstack(sequence, value_type="list")
    value = puw.get_value(quantity)

    np.testing.assert_array_equal(value, [1, 2, 3, 4])


def test_hstack_invalid_value_type_raises_value_error():
    configure_libraries()

    sequence = [[puw.quantity(1, "meter")]]

    with pytest.raises(ValueError):
        puw.utils.numpy.hstack(sequence, value_type="dictionary")
