"""Stated measurements preserve association and units, without statistical inference."""

import copy
import json
import subprocess
import sys

import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import RecordError
from pyunitwizard.measurement import MeasurementRecord


def q(value, unit="nM"):
    return puw.quantity(value, unit, form="pint")


@pytest.mark.parametrize("kind", ["sd", "sem", "unspecified"])
def test_sabueso_statement_round_trip_under_another_policy(kind):
    record = MeasurementRecord.from_quantity(q(12.0), kind=kind, half_width=q(3.0), n=3, field="ic50")
    stored = json.loads(json.dumps(record.to_dict()))
    with puw.context(standard_units=["meter", "second"], default_form="unyt"):
        back = MeasurementRecord.from_dict(stored)
        result = back.to_quantities(field="ic50", kind=kind, unit="uM", form="pint")
    assert result["value"].magnitude == pytest.approx(0.012)
    assert result["half_width"].magnitude == pytest.approx(0.003)
    assert back.kind == kind and back.n == 3 and back.level is None
    assert back.to_dict() == stored


def test_sabueso_confidence_interval_and_estimator_outside_bounds():
    record = MeasurementRecord.from_quantity(q(10.0, "uM"), kind="ci", lower=q(8000.0), upper=q(12000.0), level=0.95)
    result = MeasurementRecord.from_dict(record.to_dict()).to_quantities(unit="nM", form="pint")
    assert [result[name].magnitude for name in ["value", "lower", "upper"]] == pytest.approx([10000, 8000, 12000])
    assert record.level == 0.95
    # An estimator need not lie in every stated CI; do not manufacture that rule.
    MeasurementRecord.from_quantity(q(20), kind="ci", lower=q(8), upper=q(12))


@pytest.mark.parametrize("unit", ["degC", "degF"])
def test_temperature_half_width_is_a_difference(unit):
    record = MeasurementRecord.from_quantity(q(20, "degC"), kind="sd", half_width=q(3, "delta_degC"))
    result = record.to_quantities(unit=unit, form="pint")
    expected = 3 if unit == "degC" else 5.4
    assert result["half_width"].magnitude == pytest.approx(expected)
    assert str(result["half_width"].units) == ("delta_degree_Celsius" if unit == "degC" else "delta_degree_Fahrenheit")
    kelvin = record.to_quantities(unit="kelvin", form="pint")
    assert kelvin["value"].magnitude == pytest.approx(293.15)
    assert kelvin["half_width"].magnitude == pytest.approx(3)


def test_temperature_interval_bounds_are_points():
    record = MeasurementRecord.from_quantity(q(20, "degC"), kind="ci", lower=q(17, "degC"), upper=q(23, "degC"))
    result = record.to_quantities(unit="kelvin", form="pint")
    assert result["lower"].magnitude == pytest.approx(290.15)
    assert result["upper"].magnitude == pytest.approx(296.15)


def test_absolute_temperature_is_refused_as_a_half_width():
    with pytest.raises(RecordError, match="difference unit"):
        MeasurementRecord.from_quantity(q(20, "degC"), kind="sd", half_width=q(3, "degC"))


def test_delta_temperature_is_refused_as_an_absolute_interval_bound():
    with pytest.raises(RecordError, match="point quantities"):
        MeasurementRecord.from_quantity(q(20, "degC"), kind="ci", lower=q(17, "delta_degC"), upper=q(23, "degC"))


def test_scalar_dtype_and_source_unit_are_retained():
    record = MeasurementRecord.from_quantity(q(np.float32(12)), kind="sd", half_width=q(np.float32(3)))
    output = MeasurementRecord.from_dict(record.to_dict()).to_quantities(form="pint")
    assert np.asarray(output["value"].magnitude).dtype == np.dtype("float32")
    assert np.asarray(output["half_width"].magnitude).dtype == np.dtype("float32")
    assert str(output["value"].units) == "nanomolar"


def test_a_resealed_invalid_association_is_still_refused():
    from pyunitwizard.record import _digest

    data = MeasurementRecord.from_quantity(q(12), kind="ci", lower=q(8), upper=q(16), level=0.95).to_dict()
    data["metadata"]["level"] = 0
    data["digest"] = _digest(
        {"format": data["format"], "metadata": data["metadata"]}, data["bundle"]["digest"].encode("ascii")
    )
    with pytest.raises(RecordError, match="level"):
        MeasurementRecord.from_dict(data)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda data: data["metadata"].update(kind="sem"),
        lambda data: data["metadata"].update(n=300),
        lambda data: data["metadata"].update(field="ki"),
        lambda data: data["bundle"]["entries"]["value"].update(values=120),
        lambda data: data["bundle"]["entries"]["half_width"].update(unit="picomolar"),
        lambda data: data.pop("digest"),
        lambda data: data.update(format="qrec/0.3"),
    ],
)
def test_changes_to_association_metadata_and_values_are_refused(mutation):
    data = MeasurementRecord.from_quantity(q(12), kind="sd", half_width=q(3), n=3, field="ic50").to_dict()
    mutation(data)
    with pytest.raises(RecordError):
        MeasurementRecord.from_dict(data)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"kind": "variance", "half_width": q(3)},
        {"kind": "sd"},
        {"kind": "sd", "half_width": q(-3)},
        {"kind": "sd", "half_width": q(3), "lower": q(8), "upper": q(12)},
        {"kind": "ci", "lower": q(8)},
        {"kind": "ci", "lower": q(12), "upper": q(8)},
        {"kind": "sd", "half_width": q(3), "level": 0.95},
        {"kind": "ci", "lower": q(8), "upper": q(12), "level": 1.0},
        {"kind": "ci", "lower": q(8), "upper": q(12), "level": True},
        {"kind": "sd", "half_width": q(3), "n": True},
        {"kind": "sd", "half_width": q(3), "n": 0},
        {"kind": "sd", "half_width": q(3), "n": 3.0},
        {"kind": "sd", "half_width": q(3, "second")},
        {"kind": "sd", "half_width": q(np.nan)},
        {"kind": "sd", "half_width": q([3])},
        {"kind": "sd", "half_width": 3},
        {"kind": "sd", "half_width": q(3, "degC")},
    ],
)
def test_invalid_statements_are_refused(kwargs):
    with pytest.raises(RecordError):
        MeasurementRecord.from_quantity(q(12), **kwargs)


@pytest.mark.parametrize("value", [q([12]), q(np.inf), 12])
def test_value_must_be_a_finite_scalar_quantity(value):
    with pytest.raises(RecordError):
        MeasurementRecord.from_quantity(value, kind="sd", half_width=q(3))


@pytest.mark.parametrize(
    "expectation", [{"field": "ki"}, {"kind": "sem"}, {"unit": "second"}, {"dimensionality": {"[L]": 1}}]
)
def test_reader_expectations_are_checked(expectation):
    record = MeasurementRecord.from_quantity(q(12), kind="sd", half_width=q(3), field="ic50")
    with pytest.raises(RecordError):
        record.to_quantities(**expectation)


@pytest.mark.parametrize("form", ["unyt", "openmm.unit", "astropy.units"])
def test_existing_backends_receive_the_original_quantities(form):
    pytest.importorskip({"unyt": "unyt", "openmm.unit": "openmm", "astropy.units": "astropy"}[form])
    record = MeasurementRecord.from_quantity(q(12), kind="sd", half_width=q(3))
    result = record.to_quantities(unit="mole/liter", form=form)
    assert puw.get_form(result["value"]) == form
    assert puw.get_value(result["half_width"]) == pytest.approx(3e-9)


def test_returned_data_and_quantities_cannot_change_the_snapshot():
    value = q(np.array(12.0))
    record = MeasurementRecord.from_quantity(value, kind="sd", half_width=q(3))
    original = copy.deepcopy(record.to_dict())
    value.magnitude[...] = 120
    output = record.to_quantities(form="pint")
    output["value"].magnitude[...] = 1200
    record.to_dict()["metadata"]["kind"] = "sem"
    assert record.to_dict() == original


def test_import_does_not_load_a_unit_backend():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import pyunitwizard.measurement; assert 'pint' not in sys.modules; assert 'openmm' not in sys.modules",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
