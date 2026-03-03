import pyunitwizard as puw
import pytest


def test_context_restores_configuration_after_exit():
    puw.configure.reset()
    puw.configure.load_library(["pint", "openmm.unit"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    puw.configure.set_standard_units(["nm", "ps", "kJ/mol"])

    baseline_form = puw.configure.get_default_form()
    baseline_parser = puw.configure.get_default_parser()
    baseline_standard_units = set(puw.configure.get_standard_units().keys())

    with puw.context(default_form="openmm.unit", default_parser="PINT", standard_units=["m", "s", "N"]):
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
        with puw.context(default_form="openmm.unit", default_parser="PINT", standard_units=["m", "s", "N"]):
            assert puw.configure.get_default_form() == "openmm.unit"
            assert puw.configure.get_default_parser() == "pint"
            assert set(puw.configure.get_standard_units().keys()) == {"m", "s", "N"}
            raise RuntimeError("force context failure")

    assert puw.configure.get_default_form() == baseline_form
    assert puw.configure.get_default_parser() == baseline_parser
    assert set(puw.configure.get_standard_units().keys()) == baseline_standard_units
