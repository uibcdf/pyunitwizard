import numpy as np
import pytest

import pyunitwizard as puw
from tests.helpers import loaded_libraries

matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def test_setup_matplotlib_allows_plotting_with_pint_quantities():
    pytest.importorskip("pint")

    with loaded_libraries(["pint"]):
        puw.configure.set_default_form("pint")
        puw.configure.set_default_parser("pint")

        x = puw.quantity(np.linspace(0.0, 1.0, 6), "second", form="pint")
        y = puw.quantity(np.linspace(0.0, 2.0, 6), "meter", form="pint")

        puw.utils.matplotlib.setup_matplotlib(enable=True)
        fig, ax = plt.subplots()
        ax.plot(x, y)

        assert ax.xaxis.get_units() is not None
        assert ax.yaxis.get_units() is not None
        assert "second" in ax.xaxis.get_label_text()
        assert "meter" in ax.yaxis.get_label_text()
        plt.close(fig)

        puw.utils.matplotlib.setup_matplotlib(enable=False)


def test_plotting_context_supports_mixed_backends_on_same_axis():
    pytest.importorskip("pint")
    pytest.importorskip("astropy.units")

    with loaded_libraries(["pint", "astropy.units"]):
        x_pint = puw.quantity(np.linspace(0.0, 1.0, 4), "second", form="pint")
        y_pint = puw.quantity(np.linspace(0.0, 2.0, 4), "meter", form="pint")
        y_astropy = puw.quantity(np.linspace(0.0, 200.0, 4), "centimeter", form="astropy.units")

        with puw.utils.matplotlib.plotting_context():
            fig, ax = plt.subplots()
            ax.plot(x_pint, y_pint)
            ax.plot(x_pint, y_astropy)
            plt.close(fig)


def test_plotting_context_raises_on_incompatible_axis_units():
    pytest.importorskip("pint")

    with loaded_libraries(["pint"]):
        x_seconds = puw.quantity(np.linspace(0.0, 1.0, 4), "second", form="pint")
        y_meters = puw.quantity(np.linspace(0.0, 2.0, 4), "meter", form="pint")
        x_meters = puw.quantity(np.linspace(0.0, 1.0, 4), "meter", form="pint")

        with puw.utils.matplotlib.plotting_context():
            fig, ax = plt.subplots()
            ax.plot(x_seconds, y_meters)
            with pytest.raises(ValueError):
                ax.plot(x_meters, y_meters)
            plt.close(fig)
