import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard import kernel


def test_context_restores_configuration_after_exit():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    puw.configure.set_standard_units(["nm", "ps", "kJ/mol"])

    baseline_form = puw.configure.get_default_form()
    baseline_parser = puw.configure.get_default_parser()
    baseline_standard_units = set(puw.configure.get_standard_units().keys())

    with puw.context(
        default_form="openmm.unit",
        default_parser="PINT",
        standard_units=["m", "s", "N"],
    ):
        assert puw.configure.get_default_form() == "openmm.unit"
        assert puw.configure.get_default_parser() == "pint"
        assert set(puw.configure.get_standard_units().keys()) == {"m", "s", "N"}

    assert puw.configure.get_default_form() == baseline_form
    assert puw.configure.get_default_parser() == baseline_parser
    assert set(puw.configure.get_standard_units().keys()) == baseline_standard_units


def test_context_without_overrides_keeps_configuration():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    puw.configure.set_standard_units(["nm"])

    baseline_form = puw.configure.get_default_form()
    baseline_parser = puw.configure.get_default_parser()
    baseline_standard_units = set(puw.configure.get_standard_units().keys())

    with puw.context():
        assert puw.configure.get_default_form() == baseline_form
        assert puw.configure.get_default_parser() == baseline_parser
        assert set(puw.configure.get_standard_units().keys()) == baseline_standard_units


def test_context_restores_configuration_after_exception():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    puw.configure.set_standard_units(["nm", "ps", "kJ/mol"])

    baseline_form = puw.configure.get_default_form()
    baseline_parser = puw.configure.get_default_parser()
    baseline_standard_units = set(puw.configure.get_standard_units().keys())

    with pytest.raises(RuntimeError):
        with puw.context(
            default_form="openmm.unit",
            default_parser="PINT",
            standard_units=["m", "s", "N"],
        ):
            assert puw.configure.get_default_form() == "openmm.unit"
            assert puw.configure.get_default_parser() == "pint"
            assert set(puw.configure.get_standard_units().keys()) == {"m", "s", "N"}
            raise RuntimeError("force context failure")

    assert puw.configure.get_default_form() == baseline_form
    assert puw.configure.get_default_parser() == baseline_parser
    assert set(puw.configure.get_standard_units().keys()) == baseline_standard_units


def test_context_restores_derived_standard_state_and_caches():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_standard_units(["nm", "ps", "kJ/mol"])

    baseline_fundamental_matrix = kernel.dimensional_fundamental_standards_matrix.copy()
    baseline_tentative_matrix = kernel.tentative_base_standards_matrix.copy()
    baseline_fundamental_units = list(kernel.dimensional_fundamental_standards_units)
    baseline_tentative_units = list(kernel.tentative_base_standards_units)

    length = puw.quantity(1.0, "angstrom")
    puw.get_standard_units(length)
    baseline_cache = dict(kernel.standard_units_by_dimensionality_cache)

    with puw.context(standard_units=["m", "s", "N"]):
        assert set(puw.configure.get_standard_units()) == {"m", "s", "N"}

    np.testing.assert_allclose(
        kernel.dimensional_fundamental_standards_matrix,
        baseline_fundamental_matrix,
    )
    np.testing.assert_allclose(
        kernel.tentative_base_standards_matrix,
        baseline_tentative_matrix,
    )
    assert kernel.dimensional_fundamental_standards_units == baseline_fundamental_units
    assert kernel.tentative_base_standards_units == baseline_tentative_units
    assert kernel.standard_units_by_dimensionality_cache == baseline_cache


def test_context_restores_canonical_standards():
    """Derived state must be in the snapshot, not just in the kernel.

    `canonical_standards` is rebuilt by `set_standard_units()`, so a context
    that changes the standards changes it too. Leaving it out of the snapshot
    would let a context leak the candidate list that `standardize()` walks on
    its canonical fast path.
    """
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_standard_units(["nm", "ps"])

    baseline = list(kernel.canonical_standards)
    assert [unit for unit, _ in baseline] == ["nm", "ps"]

    with puw.context(standard_units=["angstrom", "fs"]):
        assert [unit for unit, _ in kernel.canonical_standards] == ["angstrom", "fs"]

    assert kernel.canonical_standards == baseline


def test_context_restores_fast_track_registrations():
    """Fast tracks live outside the kernel and used to outlive the context."""
    from pyunitwizard.api.specialized import fast_track

    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_standard_units(["nm"])

    before = set(vars(fast_track))

    with puw.context():
        puw.register_fast_track("leaked_unit_for_context_test", puw.unit("nm"))
        assert hasattr(fast_track, "to_leaked_unit_for_context_test")

    assert set(vars(fast_track)) == before


def test_context_snapshot_is_deep_enough_to_undo_nested_mutation():
    """`copy.copy` shared the nested dictionaries with the live state."""
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_standard_units(["nm"])

    original = dict(kernel.standards["nm"])

    with puw.context():
        kernel.standards["nm"]["[L]"] = 999

    assert kernel.standards["nm"] == original


def test_context_leaves_backend_loading_alone():
    """Loading a backend is a capability, not a policy.

    Reverting `loaded_libraries` while the `forms/` registries stayed populated
    left the kernel claiming a backend was unloaded when it was not. A backend
    loaded inside a context now simply stays loaded, and the two agree.
    """
    from pyunitwizard import forms

    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")

    with puw.context():
        puw.configure.load_library(["unyt"])

    assert ("unyt" in kernel.loaded_libraries) == ("unyt" in forms.dict_is_form)
    assert kernel.loaded_libraries.count("unyt") == 1
