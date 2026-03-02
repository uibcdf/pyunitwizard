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
