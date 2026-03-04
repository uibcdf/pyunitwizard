import numpy as np
import pytest

import pyunitwizard as puw
from tests.helpers import loaded_libraries


matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def test_subplots_with_shared_x_accept_compatible_units():
    pytest.importorskip("pint")

    with loaded_libraries(["pint"]):
        x_seconds = puw.quantity(np.linspace(0.0, 1.0, 5), "second", form="pint")
        x_milliseconds = puw.quantity(np.linspace(0.0, 1000.0, 5), "millisecond", form="pint")
        y_a = puw.quantity(np.linspace(0.0, 2.0, 5), "meter", form="pint")
        y_b = puw.quantity(np.linspace(0.0, 3.0, 5), "meter", form="pint")

        with puw.utils.matplotlib.plotting_context():
            fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True)
            ax0.plot(x_seconds, y_a)
            ax1.plot(x_milliseconds, y_b)
            plt.close(fig)


def test_twin_axes_keep_independent_unit_contexts():
    pytest.importorskip("pint")

    with loaded_libraries(["pint"]):
        x = puw.quantity(np.linspace(0.0, 1.0, 5), "second", form="pint")
        y_left = puw.quantity(np.linspace(0.0, 2.0, 5), "meter", form="pint")
        y_right = puw.quantity(np.linspace(0.0, 200.0, 5), "kilojoule", form="pint")

        with puw.utils.matplotlib.plotting_context():
            fig, ax_left = plt.subplots()
            ax_right = ax_left.twinx()
            ax_left.plot(x, y_left)
            ax_right.plot(x, y_right)

            assert "meter" in ax_left.yaxis.get_label_text()
            assert "kilojoule" in ax_right.yaxis.get_label_text()
            plt.close(fig)


def test_same_axis_handles_three_backends_when_compatible():
    pytest.importorskip("pint")
    pytest.importorskip("astropy.units")
    pytest.importorskip("unyt")

    with loaded_libraries(["pint", "astropy.units", "unyt"]):
        x_pint = puw.quantity(np.linspace(0.0, 1.0, 4), "second", form="pint")
        y_pint = puw.quantity(np.linspace(0.0, 2.0, 4), "meter", form="pint")
        y_astropy = puw.quantity(np.linspace(0.0, 200.0, 4), "centimeter", form="astropy.units")
        y_unyt = puw.quantity(np.linspace(0.0, 0.002, 4), "kilometer", form="unyt")

        with puw.utils.matplotlib.plotting_context():
            fig, ax = plt.subplots()
            ax.plot(x_pint, y_pint)
            ax.plot(x_pint, y_astropy)
            ax.plot(x_pint, y_unyt)
            assert "meter" in ax.yaxis.get_label_text()
            plt.close(fig)
