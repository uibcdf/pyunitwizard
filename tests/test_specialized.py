import numpy as np
import pytest

import pyunitwizard as puw
from pyunitwizard._private.exceptions import FastTrackConflictError


def test_dynamic_fast_track_registration():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    # 1. Register fast track dynamically
    nm_unit = puw.unit("nm")
    puw.register_fast_track("nanometers", nm_unit)

    # 2. Test conversion using the dynamic fallback attribute
    quantity = puw.quantity(1.0, "meter", form="pint")
    output = puw.to_nanometers(quantity)

    assert puw.get_unit(output) == "nanometer"
    assert puw.get_value(output) == pytest.approx(np.float64(1e9))


def test_specialized_passthrough_for_plain_ndarray():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    puw.register_fast_track("nanometers", puw.unit("nm"))
    array = np.array([1.0, 2.0, 3.0], dtype=np.float64)

    assert puw.to_nanometers(array) is array


def test_specialized_passthrough_does_not_use_general_unit_extraction(monkeypatch):
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    target_unit = puw.unit("nm")
    quantity = puw.quantity([1.0, 2.0], "nm")

    def fail_if_called(_quantity):
        raise AssertionError("general unit extraction is forbidden on the fast path")

    monkeypatch.setattr("pyunitwizard.api.extraction.get_unit", fail_if_called)
    puw.register_fast_track("nanometers", target_unit)

    assert puw.fast_track.to_nanometers(quantity) is quantity


def test_equivalent_fast_track_registration_is_idempotent():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    puw.register_fast_track("idempotent_nanometers", puw.unit("nm"))
    registered = puw.fast_track.to_idempotent_nanometers

    puw.register_fast_track("idempotent_nanometers", puw.unit("nanometer"))

    assert puw.fast_track.to_idempotent_nanometers is registered


def test_conflicting_fast_track_registration_is_rejected():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    puw.register_fast_track("conflicting_length", puw.unit("nm"))
    registered = puw.fast_track.to_conflicting_length

    with pytest.raises(FastTrackConflictError) as excinfo:
        puw.register_fast_track("conflicting_length", puw.unit("angstrom"))

    assert excinfo.value.code == "PUW-ERR-FAST-001"
    assert excinfo.value.extra["name"] == "conflicting_length"
    assert puw.fast_track.to_conflicting_length is registered
