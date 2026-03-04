import numpy as np
import pyunitwizard as puw
import pytest


def configure_libraries():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])


def test_mean_with_unit_conversion():
    configure_libraries()

    quantity = puw.quantity([1.0, 2.0, 3.0], "nanometer")
    out = puw.utils.numpy.mean(quantity, to_unit="angstrom")

    assert puw.get_unit(out, to_form="string") == "angstrom"
    assert np.isclose(puw.get_value(out), 20.0)


def test_sum_axis_and_numpy_array_value_type():
    configure_libraries()

    quantity = puw.quantity([[1.0, 2.0], [3.0, 4.0]], "meter")
    out = puw.utils.numpy.sum(quantity, axis=0, value_type="numpy.ndarray")

    np.testing.assert_allclose(puw.get_value(out), np.array([4.0, 6.0]))
    assert puw.get_unit(out, to_form="string") == "meter"


def test_linalg_norm_preserves_dimensions():
    configure_libraries()

    quantity = puw.quantity([3.0, 4.0], "meter")
    out = puw.utils.numpy.linalg_norm(quantity)

    assert np.isclose(puw.get_value(out), 5.0)
    assert puw.get_unit(out, to_form="string") == "meter"


def test_trapz_with_quantity_x_builds_product_unit():
    configure_libraries()

    y = puw.quantity([0.0, 1.0, 2.0], "meter")
    x = puw.quantity([0.0, 1.0, 2.0], "second")
    out = puw.utils.numpy.trapz(y, x=x)

    assert np.isclose(puw.get_value(out), 2.0)
    assert "meter * second" in puw.get_unit(out, to_form="string")


def test_trapz_with_quantity_dx_builds_product_unit():
    configure_libraries()

    y = puw.quantity([0.0, 1.0, 2.0], "meter")
    dx = puw.quantity(2.0, "second")
    out = puw.utils.numpy.trapz(y, dx=dx)

    assert np.isclose(puw.get_value(out), 4.0)
    assert "meter * second" in puw.get_unit(out, to_form="string")


def test_ops_invalid_value_type_raises_value_error():
    configure_libraries()

    quantity = puw.quantity([1.0, 2.0], "meter")

    with pytest.raises(ValueError):
        puw.utils.numpy.mean(quantity, value_type="invalid")
    with pytest.raises(ValueError):
        puw.utils.numpy.sum(quantity, value_type="invalid")
    with pytest.raises(ValueError):
        puw.utils.numpy.linalg_norm(quantity, value_type="invalid")
    with pytest.raises(ValueError):
        puw.utils.numpy.trapz(quantity, value_type="invalid")
