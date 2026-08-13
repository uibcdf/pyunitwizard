import importlib
import sys
from pathlib import Path

import pyunitwizard as puw

EXAMPLES_DIRECTORY = Path(__file__).resolve().parents[1] / "examples"


def _import_example(package_name):
    sys.path.insert(0, str(EXAMPLES_DIRECTORY))
    try:
        return importlib.import_module(package_name)
    finally:
        sys.path.remove(str(EXAMPLES_DIRECTORY))


def test_example_libraries_use_the_current_public_api():
    puw.configure.reset()

    testlib = _import_example("testlib")
    testlib2 = _import_example("testlib2")

    assert puw.are_equal(testlib.sum_quantities("2 cm", "3 cm"), "5 cm")
    assert puw.are_equal(testlib2.sum_quantities("3 m", "7 m"), "10 m")
    assert {"pint", "openmm.unit"}.issubset(testlib.libraries_loaded())
