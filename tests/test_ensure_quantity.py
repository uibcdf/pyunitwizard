"""Tests for pyunitwizard.ensure_quantity."""

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import ArgumentError


@pytest.fixture(autouse=True)
def _configured():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_standard_units(["nm", "ps", "kcal", "mole", "K"])


def test_ensure_quantity_parses_string_and_standardizes():
    result = puw.ensure_quantity("3.5 angstroms", dimensionality={"[L]": 1})
    assert puw.is_quantity(result)
    assert puw.get_value(result, to_unit="angstroms") == pytest.approx(3.5)
    # Standardized to the configured length unit (nm).
    assert puw.get_unit(result, to_form="string") == "nanometer"


def test_ensure_quantity_accepts_existing_quantity():
    q = puw.quantity(0.35, "nm")
    result = puw.ensure_quantity(q, dimensionality={"[L]": 1})
    assert puw.get_value(result, to_unit="angstroms") == pytest.approx(3.5)


def test_ensure_quantity_to_unit_without_standardization():
    result = puw.ensure_quantity("0.35 nm", dimensionality={"[L]": 1},
                                 to_unit="angstroms", standardized=False)
    assert puw.get_value(result) == pytest.approx(3.5)


def test_ensure_quantity_batch_positions():
    result = puw.ensure_quantity(puw.quantity(np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]), "angstrom"),
                                 dimensionality={"[L]": 1})
    assert np.asarray(puw.get_value(result, to_unit="angstroms")).shape == (2, 3)


@pytest.mark.parametrize("bare", [3.5, [1, 2, 3], (1.0, 2.0, 3.0), np.array([1.0, 2.0]), None])
def test_ensure_quantity_rejects_bare_numbers(bare):
    with pytest.raises(ArgumentError):
        puw.ensure_quantity(bare, dimensionality={"[L]": 1})


def test_ensure_quantity_rejects_wrong_dimensionality():
    with pytest.raises(ArgumentError):
        puw.ensure_quantity("3.5 seconds", dimensionality={"[L]": 1})


def test_ensure_quantity_without_dimensionality_accepts_any_quantity():
    # No dimensionality constraint: any quantity is fine, bare still rejected.
    assert puw.is_quantity(puw.ensure_quantity("3.5 seconds"))
    with pytest.raises(ArgumentError):
        puw.ensure_quantity(3.5)
