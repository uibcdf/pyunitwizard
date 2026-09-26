"""The text form must preserve array values when read back by PyUnitWizard."""

import numpy as np
import pytest

import pyunitwizard as puw


@pytest.mark.parametrize(
    "values",
    [
        1.2345678901234567,
        np.array([1.5, np.nextafter(1.0, 2.0)], dtype=np.float64),
        np.array([[1.25, 2.5], [3.75, 4.125]], dtype=np.float32),
        np.array([[1, 2], [3, 4]], dtype=np.int64),
    ],
)
def test_pint_string_roundtrip_preserves_numeric_values_and_shape(values):
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    original = puw.quantity(values, "meter / second", form="pint")

    with np.printoptions(precision=1):
        text = puw.convert(original, to_form="string")
    restored = puw.quantity(text, form="pint", parser="pint")

    assert np.shape(puw.get_value(restored)) == np.shape(puw.get_value(original))
    assert np.array_equal(puw.get_value(restored), puw.get_value(original))
    assert puw.get_unit(restored) == puw.get_unit(original)


@pytest.mark.parametrize("form", ["unyt", "astropy.units", "openmm.unit"])
def test_other_backend_arrays_emit_parseable_string_values(form):
    pytest.importorskip(form)
    puw.configure.load_library(["pint", form])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    values = np.array([[1.25, 2.5], [3.75, 4.125]])
    original = puw.quantity(values, "meter / second", form=form)

    text = puw.convert(original, to_form="string")
    restored = puw.quantity(text, form="pint", parser="pint")

    assert np.array_equal(puw.get_value(restored), values)
    assert np.shape(puw.get_value(restored)) == values.shape
