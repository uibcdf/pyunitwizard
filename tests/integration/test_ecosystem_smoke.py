import subprocess
import sys

import pytest

import pyunitwizard as puw


def test_smonitor_registers_pyunitwizard_catalog_entries():
    smonitor = pytest.importorskip("smonitor")
    manager = smonitor.get_manager()
    codes = manager.get_codes()

    assert "PUW-ERR-PARSER-001" in codes
    assert "PUW-ERR-FORM-001" in codes


def test_depdigest_can_introspect_pyunitwizard_contract():
    depdigest = pytest.importorskip("depdigest")

    payload = depdigest.get_info("pyunitwizard", format="dict")

    assert payload["schema"] == {"name": "depdigest.get_info", "version": "1.0"}
    assert payload["module_path"] == "pyunitwizard"
    assert "dependencies" in payload


def test_depdigest_reports_expected_runtime_dependencies():
    depdigest = pytest.importorskip("depdigest")

    payload = depdigest.get_info("pyunitwizard", format="dict")
    dependencies = payload["dependencies"]

    libraries = {item["library"] for item in dependencies}
    assert {
        "numpy",
        "pint",
        "unyt",
        "openmm.unit",
        "astropy.units",
        "physipy",
        "quantities",
    }.issubset(libraries)

    type_by_library = {item["library"]: item["type"] for item in dependencies}
    assert type_by_library["numpy"] == "hard"
    assert type_by_library["pint"] == "hard"
    assert type_by_library["argdigest"] == "hard"


def test_argdigest_pyunitwizard_rule_pipeline_smoke():
    argdigest = pytest.importorskip("argdigest")
    puw_support = pytest.importorskip("argdigest.contrib.pyunitwizard_support")

    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")

    @argdigest.arg_digest.map(
        distance={
            "kind": "quantity",
            "rules": [
                puw_support.check(dimensionality={"[L]": 1}),
            ],
        }
    )
    def _accept_distance(distance):
        return distance

    distance_ok = puw.quantity(1.5, "nm")
    accepted = _accept_distance(distance_ok)
    assert puw.are_equal(accepted, distance_ok)

    distance_bad = puw.quantity(1.0, "ps")
    with pytest.raises(argdigest.DigestValueError):
        _accept_distance(distance_bad)


def test_argdigest_pyunitwizard_standardize_and_convert_pipeline():
    argdigest = pytest.importorskip("argdigest")
    puw_support = pytest.importorskip("argdigest.contrib.pyunitwizard_support")

    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    puw.configure.set_standard_units(["nanometer", "picosecond", "kilocalorie", "mole"])

    @argdigest.arg_digest.map(
        distance={
            "kind": "quantity",
            "rules": [
                puw_support.is_quantity(),
                puw_support.standardize(),
                puw_support.convert("angstrom", to_form="pint"),
            ],
        }
    )
    def _normalize_distance(distance):
        return distance

    out = _normalize_distance(puw.quantity(1.0, "nanometer", form="pint"))
    assert puw.get_form(out) == "pint"
    assert puw.get_unit(out) == "angstrom"
    assert puw.get_value(out) == 10.0


@pytest.mark.parametrize("skip", [False, 1, "yes", "False"])
def test_argdigest_only_literal_true_bypasses_consumer_normalization(skip):
    import argdigest

    @argdigest.arg_digest.map(puw_review_value={"rules": [lambda value, ctx: int(value)]})
    def consume(puw_review_value, skip_digestion=False):
        return puw_review_value

    assert consume("5", skip_digestion=skip) == 5
    assert consume("5", skip) == 5
    assert consume("5", skip_digestion=True) == "5"


def test_argdigest_classmethod_preserves_caller_and_supplies_optional_qualname():
    import argdigest

    observed = []

    @argdigest.argument_digest("puw_review_label")
    def digest_label(value, caller=None, qualname=None):
        observed.append((caller, qualname))
        return int(value)

    class Consumer:
        @classmethod
        @argdigest.arg_digest(digestion_style="decorator", strictness="error")
        def normalize(cls, puw_review_label):
            return cls, puw_review_label

    assert Consumer.normalize("5") == (Consumer, 5)
    assert observed == [(f"{__name__}.normalize", f"{__name__}.Consumer.normalize")]


def test_argdigest_adapter_creation_defers_missing_pyunitwizard_failure():
    script = """
import importlib.util
import sys

find_spec = importlib.util.find_spec
def without_puw(name, *args, **kwargs):
    if name == 'pyunitwizard':
        return None
    return find_spec(name, *args, **kwargs)
importlib.util.find_spec = without_puw

import argdigest
from argdigest.contrib import pyunitwizard_support as support
rule = support.is_quantity()
assert 'pyunitwizard' not in sys.modules
try:
    rule(1, None)
except argdigest.DigestTypeError as error:
    assert error.code == 'ARG-ERR-OPTDEP-001'
else:
    raise AssertionError('Missing optional PyUnitWizard was accepted')
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
