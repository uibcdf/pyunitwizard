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
