import importlib
from itertools import combinations

import numpy as np
import pytest

import pyunitwizard as puw
from tests.helpers import loaded_libraries


matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")
import matplotlib.pyplot as plt

pytest.importorskip("pandas")


_BACKEND_CANDIDATES = [
    ("pint", "pint"),
    ("openmm.unit", "openmm.unit"),
    ("unyt", "unyt"),
    ("astropy.units", "astropy.units"),
    ("physipy", "physipy"),
    ("quantities", "quantities"),
]


def _available_forms():
    forms = []
    for form, module_name in _BACKEND_CANDIDATES:
        try:
            importlib.import_module(module_name)
        except Exception:
            continue
        forms.append(form)
    return forms


AVAILABLE_FORMS = _available_forms()

BASE_FORM = "pint"


def _make_quantity(values, unit_name, form):
    q = puw.quantity(values, unit_name, form=BASE_FORM, parser=BASE_FORM)
    if form == BASE_FORM:
        return q
    return puw.convert(q, to_form=form)


@pytest.mark.parametrize("form", AVAILABLE_FORMS)
def test_each_backend_works_in_numpy_pandas_and_matplotlib_frontends(form):
    libraries = ["pint"] if form == "pint" else ["pint", form]

    with loaded_libraries(libraries):
        x = _make_quantity(np.linspace(0.0, 1.0, 5), "second", form=form)
        y = _make_quantity(np.linspace(1.0, 3.0, 5), "meter", form=form)

        with puw.utils.numpy.numpy_context():
            mean_q = np.mean(y)
        assert puw.is_quantity(mean_q)
        assert puw.get_unit(mean_q, to_form="string") == "meter"

        dataframe = puw.utils.pandas.dataframe_from_quantities({"y": y})
        y_roundtrip = puw.utils.pandas.get_quantity_column(dataframe, "y")
        assert puw.get_unit(y_roundtrip, to_form="string") == "meter"
        np.testing.assert_allclose(
            puw.get_value(y_roundtrip, to_unit="meter"),
            puw.get_value(y, to_unit="meter"),
        )

        with puw.utils.matplotlib.plotting_context():
            fig, ax = plt.subplots()
            ax.plot(x, y)
            assert ax.xaxis.get_units() is not None
            assert ax.yaxis.get_units() is not None
            assert puw.are_compatible(ax.yaxis.get_units(), puw.unit("meter", parser=BASE_FORM))
            plt.close(fig)


@pytest.mark.parametrize("form_a,form_b", list(combinations(AVAILABLE_FORMS, 2)))
def test_mixed_backend_pairs_work_in_numpy_and_matplotlib(form_a, form_b):
    libraries = sorted({"pint", form_a, form_b})

    with loaded_libraries(libraries):
        a = _make_quantity([1.0, 2.0], "meter", form=form_a)
        b = _make_quantity([3.0, 4.0], "second", form=form_b)

        with puw.utils.numpy.numpy_context():
            dot_q = np.dot(a, b)
        assert puw.is_quantity(dot_q)
        assert np.isclose(puw.get_value(dot_q), 11.0)
        expected = puw.quantity(1.0, "meter", form="pint", parser="pint") * puw.quantity(
            1.0, "second", form="pint", parser="pint"
        )
        assert puw.are_compatible(dot_q, expected)

        x = _make_quantity(np.linspace(0.0, 1.0, 4), "second", form=form_a)
        y0 = _make_quantity(np.linspace(0.0, 2.0, 4), "meter", form=form_a)
        y1 = _make_quantity(np.linspace(0.0, 200.0, 4), "centimeter", form=form_b)

        with puw.utils.matplotlib.plotting_context():
            fig, ax = plt.subplots()
            ax.plot(x, y0)
            ax.plot(x, y1)
            assert puw.are_compatible(ax.yaxis.get_units(), puw.unit("meter", parser=BASE_FORM))
            plt.close(fig)
