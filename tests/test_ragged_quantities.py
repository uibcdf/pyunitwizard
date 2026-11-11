"""Qualify the object-row representation used by molecular neighbor outputs."""

import gc
import weakref

import numpy as np
import pytest

import pyunitwizard as puw

FORMS = ["pint", "openmm.unit", "unyt"]
CASES = ["unequal", "equal", "empty_rows", "empty_outer"]


@pytest.fixture(autouse=True)
def isolated_unit_policy():
    with puw.context(default_form="pint", default_parser="pint"):
        yield


def _object_rows(case):
    backing = np.array([0.2, 0.4, 0.6], dtype=np.float64)
    if case == "empty_outer":
        return backing, np.empty((1, 0), dtype=object)
    rows = np.empty((1, 2), dtype=object)
    if case == "unequal":
        rows[0, 0], rows[0, 1] = backing[:1], backing[1:]
    elif case == "equal":
        rows[0, 0], rows[0, 1] = backing[:1], backing[1:2]
    else:
        rows[0, 0], rows[0, 1] = backing[:0], backing[:0]
    return backing, rows


@pytest.mark.parametrize("form", FORMS)
@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("standard", ["nm", "angstrom"])
def test_object_row_construction_retains_rows_and_policy(form, case, standard):
    backing, rows = _object_rows(case)
    retained = weakref.ref(backing)
    expected = [row.copy() for row in rows.flat]
    with puw.context(default_form=form, default_parser="pint", standard_units=[standard, "ps"]):
        policy = puw.configure.report()
        quantity = puw.quantity(rows, puw.unit("nm", form=form), form=form)
        result = puw.get_value(quantity)
        assert result.shape == rows.shape and result.dtype == object
        assert all(observed is source for source, observed in zip(rows.flat, result.flat))
        del result, rows, backing
        gc.collect()
        if case != "empty_outer":
            assert retained() is not None
        for observed, reference in zip(puw.get_value(quantity).flat, expected):
            np.testing.assert_array_equal(observed, reference)
        assert puw.configure.report() == policy


@pytest.mark.parametrize("form", ["pint", "openmm.unit"])
@pytest.mark.parametrize("case", CASES)
def test_object_row_conversion_preserves_shape_input_and_policy(form, case):
    _, rows = _object_rows(case)
    before = [row.copy() for row in rows.flat]
    with puw.context(default_form=form, default_parser="pint", standard_units=["pm", "fs"]):
        policy = puw.configure.report()
        quantity = puw.quantity(rows, "nm", form=form, parser="pint")
        converted = puw.convert(quantity, to_unit="angstrom", parser="pint")
        extracted = puw.get_value(quantity, to_unit="angstrom", parser="pint")
        assert puw.get_unit(converted) == puw.unit("angstrom", form=form)
        for result in (puw.get_value(converted), extracted):
            assert result.shape == rows.shape
            for observed, original in zip(result.flat, before):
                np.testing.assert_allclose(observed, original * 10, rtol=1e-15, atol=0)
        for observed, original in zip(rows.flat, before):
            np.testing.assert_array_equal(observed, original)
        assert puw.configure.report() == policy


@pytest.mark.parametrize("case", CASES)
def test_astropy_rejects_object_rows_with_actionable_diagnostic(case):
    _, rows = _object_rows(case)
    with pytest.raises(TypeError) as captured:
        puw.quantity(rows, "nm", form="astropy.units", parser="pint")
    error = captured.value
    assert isinstance(error, puw.UnsupportedRepresentationError)
    assert error.code == "PUW-ERR-REP-001"
    assert "astropy.units" in str(error) and "construct" in str(error)
    assert "CSR" in str(error)


@pytest.mark.parametrize("form", FORMS)
@pytest.mark.parametrize("case", CASES)
def test_translation_to_astropy_has_the_same_representation_diagnostic(form, case):
    _, rows = _object_rows(case)
    quantity = puw.quantity(rows, "nm", form=form, parser="pint")
    with pytest.raises(TypeError) as captured:
        puw.convert(quantity, to_form="astropy.units", parser="pint")
    assert isinstance(captured.value, puw.UnsupportedRepresentationError)
    assert captured.value.code == "PUW-ERR-REP-001"


@pytest.mark.parametrize("case", CASES[:-1])
def test_unyt_row_conversion_has_actionable_diagnostic(case):
    _, rows = _object_rows(case)
    quantity = puw.quantity(rows, "nm", form="unyt", parser="pint")
    with pytest.raises(TypeError) as captured:
        puw.get_value(quantity, to_unit="angstrom", parser="pint")
    assert isinstance(captured.value, puw.UnsupportedRepresentationError)
    assert captured.value.code == "PUW-ERR-REP-001"
    assert "unyt" in str(captured.value) and "convert" in str(captured.value)
    assert "CSR" in str(captured.value)


def test_unyt_representation_diagnostic_preserves_unit_errors():
    unyt = pytest.importorskip("unyt")
    _, rows = _object_rows("unequal")
    quantity = puw.quantity(rows, "nm", form="unyt", parser="pint")
    with pytest.raises(unyt.exceptions.UnitConversionError):
        puw.convert(quantity, to_unit="second", parser="pint")


@pytest.mark.parametrize("form", ["unyt", "astropy.units"])
def test_numeric_object_scalars_keep_native_construction(form):
    values = np.array([[0.2, 0.4]], dtype=object)
    quantity = puw.quantity(values, "nm", form=form, parser="pint")
    np.testing.assert_array_equal(puw.get_value(quantity), values)


def test_unyt_empty_outer_conversion_keeps_native_behavior():
    _, rows = _object_rows("empty_outer")
    quantity = puw.quantity(rows, "nm", form="unyt", parser="pint")
    assert puw.get_value(quantity, to_unit="angstrom", parser="pint").shape == rows.shape


def test_openff_object_rows_construct_and_convert():
    pytest.importorskip("openff.units")
    _, rows = _object_rows("unequal")
    quantity = puw.quantity(rows, "nm", form="openff.units", parser="pint")
    assert puw.get_value(quantity)[0, 1] is rows[0, 1]
    result = puw.get_value(quantity, to_unit="angstrom", parser="pint")
    for observed, original in zip(result.flat, rows.flat):
        np.testing.assert_allclose(observed, original * 10, rtol=1e-15, atol=0)


@pytest.mark.parametrize("source_form", FORMS)
@pytest.mark.parametrize("target_form", FORMS)
def test_object_rows_translate_between_compatible_containers(source_form, target_form):
    _, rows = _object_rows("unequal")
    quantity = puw.quantity(rows, "nm", form=source_form, parser="pint")
    translated = puw.convert(quantity, to_form=target_form, parser="pint")
    result = puw.get_value(translated)
    assert result.shape == rows.shape
    for observed, original in zip(result.flat, rows.flat):
        np.testing.assert_array_equal(observed, original)
