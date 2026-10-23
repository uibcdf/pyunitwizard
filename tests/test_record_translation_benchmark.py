"""The hub evaluation must compare complete, correct routes and retain evidence."""

import json
from pathlib import Path

import numpy as np
import pint
import pytest
import smonitor

import pyunitwizard as puw
from devtools.benchmark_record_translation import compare_translation
from pyunitwizard.record import QuantityRecord


@pytest.mark.parametrize(
    "source_form,target_form", [("pint", "openmm.unit"), ("openmm.unit", "unyt"), ("unyt", "astropy.units")]
)
def test_real_coordinates_compare_complete_routes(source_form, target_form):
    for name in ("openmm.unit", "unyt", "astropy.units"):
        pytest.importorskip(name)
    fixture = json.loads((Path(__file__).parent / "data/topomt_quantity_records.json").read_text())
    stored = QuantityRecord.from_dict(fixture["records"]["coordinates"])
    source = stored.to_quantity(form=source_form)
    report = compare_translation(source, target_form, "nanometer", field="coordinates", iterations=1, repeats=2)
    assert report["input"]["shape"] == [72, 3]
    for mode in ("telemetry_enabled", "telemetry_disabled"):
        paths = report["results"][mode]
        assert set(paths) == {"direct", "via_record", "read_existing", "read_wire"}
        for result in paths.values():
            assert len(result["samples_seconds"]) == 2
            assert result["parity"]["shape"] == [72, 3]
            assert result["parity"]["max_abs_error"] < 1e-12


def test_affine_route_and_float32_values_are_checked():
    pytest.importorskip("unyt")
    source = puw.quantity(np.array([-10.0, 0.0, 25.0], dtype=np.float32), "degree_Celsius", form="pint")
    report = compare_translation(source, "unyt", "kelvin", field="temperature", iterations=1, repeats=1)
    for paths in report["results"].values():
        for result in paths.values():
            assert result["parity"]["dtype"] == "float32"
            np.testing.assert_allclose(result["parity"]["preview"], [263.15, 273.15, 298.15], rtol=1e-6)


def test_conflicting_foreign_definition_is_refused_before_timing():
    foreign = pint.UnitRegistry(on_redefinition="ignore")
    foreign.define("nanometer = 2e-9 * meter = nm")
    with pytest.raises(ValueError, match="different definition"):
        compare_translation(foreign.Quantity(3.0, "nanometer"), "pint", "meter", iterations=1, repeats=1)


def test_wrong_translation_cannot_produce_a_successful_measurement(monkeypatch):
    pytest.importorskip("unyt")
    original = puw.convert

    def wrong(quantity, *args, **kwargs):
        if kwargs.get("to_form") == "unyt":
            return puw.quantity([999.0], "nanometer", form="unyt")
        return original(quantity, *args, **kwargs)

    monkeypatch.setattr(puw, "convert", wrong)
    source = puw.quantity([1.0], "angstrom", form="pint")
    with pytest.raises(AssertionError):
        compare_translation(source, "unyt", "nanometer", iterations=1, repeats=1)


def test_failed_measurement_restores_policy_and_telemetry(monkeypatch):
    from devtools import benchmark_record_translation as benchmark

    previous = smonitor.get_manager().enabled

    def fail():
        raise RuntimeError("clock failed")

    monkeypatch.setattr(benchmark, "perf_counter", fail)
    source = puw.quantity([1.0], "meter", form="pint")
    with puw.context(default_form="pint", default_parser="pint"):
        smonitor.configure(enabled=False)
        try:
            with pytest.raises(RuntimeError, match="clock failed"):
                compare_translation(source, "pint", "centimeter", iterations=1, repeats=1)
            assert smonitor.get_manager().enabled is False
            assert puw.configure.get_default_form() == "pint"
        finally:
            smonitor.configure(enabled=previous)


@pytest.mark.parametrize("iterations,repeats", [(0, 1), (1, 0), (-1, 1)])
def test_empty_measurement_is_refused(iterations, repeats):
    with pytest.raises(ValueError, match="positive"):
        compare_translation(None, "pint", "meter", iterations=iterations, repeats=repeats)
