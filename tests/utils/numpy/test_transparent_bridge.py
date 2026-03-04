import numpy as np
import pyunitwizard as puw

from tests.helpers import loaded_libraries


def test_setup_numpy_dispatches_mean_sum_and_norm_for_quantities():
    with loaded_libraries(["pint"]):
        q = puw.quantity([1.0, 2.0, 3.0], "meter")

        puw.utils.numpy.setup_numpy(enable=True)
        try:
            mean_q = np.mean(q)
            sum_q = np.sum(q)
            norm_q = np.linalg.norm(q)
        finally:
            puw.utils.numpy.setup_numpy(enable=False)

        assert puw.is_quantity(mean_q)
        assert puw.is_quantity(sum_q)
        assert puw.is_quantity(norm_q)
        assert puw.get_unit(mean_q, to_form="string") == "meter"
        assert puw.get_unit(sum_q, to_form="string") == "meter"
        assert puw.get_unit(norm_q, to_form="string") == "meter"
        assert np.isclose(puw.get_value(mean_q), 2.0)
        assert np.isclose(puw.get_value(sum_q), 6.0)


def test_numpy_context_dispatches_trapezoid_for_quantities():
    with loaded_libraries(["pint"]):
        y = puw.quantity([0.0, 1.0, 2.0], "meter")
        x = puw.quantity([0.0, 1.0, 2.0], "second")

        with puw.utils.numpy.numpy_context():
            result = np.trapezoid(y, x=x)

        assert puw.is_quantity(result)
        assert "meter * second" in puw.get_unit(result, to_form="string")
        assert np.isclose(puw.get_value(result), 2.0)


def test_setup_numpy_is_idempotent_and_restores_original_functions():
    original_mean = np.mean
    original_sum = np.sum
    original_norm = np.linalg.norm
    original_trapezoid = np.trapezoid

    puw.utils.numpy.setup_numpy(enable=True)
    puw.utils.numpy.setup_numpy(enable=True)
    puw.utils.numpy.setup_numpy(enable=False)

    assert np.mean is original_mean
    assert np.sum is original_sum
    assert np.linalg.norm is original_norm
    assert np.trapezoid is original_trapezoid
