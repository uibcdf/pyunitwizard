import numpy as np
import pyunitwizard as puw
import pytest

from tests.helpers import loaded_libraries


def _config_snapshot():
    return (
        tuple(puw.configure.get_libraries_loaded()),
        puw.configure.get_default_form(),
        puw.configure.get_default_parser(),
    )


def test_numpy_transparent_mode_does_not_mutate_runtime_configuration():
    with loaded_libraries(["pint"]):
        puw.configure.set_default_form("pint")
        puw.configure.set_default_parser("pint")
        before = _config_snapshot()

        puw.utils.numpy.setup_numpy(enable=True)
        try:
            _ = np.mean(np.array([1.0, 2.0, 3.0]))
        finally:
            puw.utils.numpy.setup_numpy(enable=False)

        after = _config_snapshot()
        assert after == before


def test_numpy_transparent_mode_keeps_plain_numeric_behavior():
    with loaded_libraries(["pint"]):
        puw.utils.numpy.setup_numpy(enable=True)
        try:
            arr = np.array([1.0, 2.0, 3.0, 4.0])
            assert np.mean(arr) == 2.5
            assert np.sum(arr) == 10.0
            assert np.dot(arr[:2], arr[2:]) == 11.0
        finally:
            puw.utils.numpy.setup_numpy(enable=False)


def test_numpy_context_restores_original_symbol_binding():
    original_mean = np.mean
    with puw.utils.numpy.numpy_context():
        pass
    assert np.mean is original_mean


def test_pandas_transparent_mode_does_not_mutate_runtime_configuration():
    pd = pytest.importorskip("pandas")
    with loaded_libraries(["pint"]):
        puw.configure.set_default_form("pint")
        puw.configure.set_default_parser("pint")
        before = _config_snapshot()

        puw.utils.pandas.setup_pandas(enable=True)
        dataframe = pd.DataFrame({"a": [1.0, 2.0]})
        _ = dataframe.puw.get_units_map()
        puw.utils.pandas.setup_pandas(enable=False)

        after = _config_snapshot()
        assert after == before


def test_pandas_context_restores_accessor_state():
    pd = pytest.importorskip("pandas")
    puw.utils.pandas.setup_pandas(enable=False)
    assert not hasattr(pd.DataFrame, "puw")

    with puw.utils.pandas.pandas_context():
        assert hasattr(pd.DataFrame, "puw")

    assert not hasattr(pd.DataFrame, "puw")


def test_matplotlib_transparent_mode_does_not_mutate_runtime_configuration():
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")
    plt = pytest.importorskip("matplotlib.pyplot")

    with loaded_libraries(["pint"]):
        puw.configure.set_default_form("pint")
        puw.configure.set_default_parser("pint")
        before = _config_snapshot()

        puw.utils.matplotlib.setup_matplotlib(enable=True)
        fig, ax = plt.subplots()
        ax.plot([0.0, 1.0], [0.0, 1.0])
        plt.close(fig)
        puw.utils.matplotlib.setup_matplotlib(enable=False)

        after = _config_snapshot()
        assert after == before
