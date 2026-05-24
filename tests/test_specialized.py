import numpy as np
import pytest

import pyunitwizard as puw


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
