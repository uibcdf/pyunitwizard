import pytest

import pyunitwizard as puw
from pyunitwizard.api.comparison import _compatible_dimensionalities


def _configure_pint():
    puw.configure.reset()
    puw.configure.load_library(["pint"])


def test_similarity_alias_matches_are_close():
    _configure_pint()

    q1 = puw.quantity(1.0, "meter", form="pint")
    q2 = puw.quantity(100.0, "centimeter", form="pint")
    assert puw.similarity(q1, q2)


def test_compatibility_alias_matches_are_compatible():
    _configure_pint()

    assert puw.compatibility("1 meter", "100 centimeter")


def test_are_close_returns_false_for_incompatible_quantities():
    _configure_pint()

    q1 = puw.quantity(1.0, "meter", form="pint")
    q2 = puw.quantity(1.0, "second", form="pint")
    assert not puw.are_close(q1, q2)


def test_are_equal_same_form_guard_returns_false_for_mismatch():
    puw.configure.reset()
    puw.configure.load_library(["pint", "unyt"])

    q_pint = puw.quantity(1.0, "meter", form="pint")
    q_unyt = puw.quantity(1.0, "meter", form="unyt")
    assert not puw.are_equal(q_pint, q_unyt, same_form=True)


def test_are_equal_unit_vs_quantity_falls_back_to_false():
    _configure_pint()

    unit = puw.unit("meter", form="pint")
    quantity = puw.quantity(1.0, "meter", form="pint")
    assert not puw.are_equal(unit, quantity)


def test_are_compatible_dimensionless_cross_form_try_branch():
    _configure_pint()
    assert puw.are_compatible("0.0 radians", puw.quantity(1.0, "radian", form="pint"))


def test_are_compatible_dimensionless_cross_form_except_branch(monkeypatch):
    _configure_pint()
    q_pint = puw.quantity(1.0, "radian", form="pint")

    import pyunitwizard.api.conversion as conversion_module

    original_convert = conversion_module.convert
    call_count = {"n": 0}

    def flaky_convert(*args, **kwargs):
        call_count["n"] += 1
        if call_count["n"] == 1:
            raise RuntimeError("force fallback")
        return original_convert(*args, **kwargs)

    monkeypatch.setattr(conversion_module, "convert", flaky_convert)

    assert puw.are_compatible("0.0 radians", q_pint)
    assert call_count["n"] >= 2


def test_are_compatible_dimensionless_forced_except_fallback_branch(monkeypatch):
    import pyunitwizard.api.comparison as comparison_module
    import pyunitwizard.api.conversion as conversion_module

    monkeypatch.setattr(comparison_module, "is_dimensionless", lambda _: True)
    monkeypatch.setattr(comparison_module, "get_form", lambda x: "f1" if x == "a" else "f2")
    monkeypatch.setattr(
        comparison_module,
        "dict_compatibility",
        {
            "f1": lambda x, y: x == "converted-b" and y == "a",
            "f2": lambda x, y: x == "converted-a" and y == "b",
        },
    )

    calls = {"n": 0}

    def flaky_convert(value, to_form=None):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("force first conversion error")
        if value == "b" and to_form == "f1":
            return "converted-b"
        if value == "a" and to_form == "f2":
            return "converted-a"
        return value

    monkeypatch.setattr(conversion_module, "convert", flaky_convert)

    assert comparison_module.are_compatible("a", "b")
    assert calls["n"] >= 2


def test_compatible_dimensionalities_fills_missing_keys_in_dim1():
    dim1 = {"[L]": 1}
    dim2 = {"[L]": 1, "[M]": 0, "[T]": 0, "[K]": 0, "[mol]": 0, "[A]": 0, "[Cd]": 0}

    assert _compatible_dimensionalities(dim1, dim2)
    assert dim1["[M]"] == 0
