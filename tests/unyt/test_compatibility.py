import pyunitwizard as puw


def test_unyt_compatibility_accepts_units():
    puw.configure.reset()
    puw.configure.load_library(["unyt"])

    unyt = puw.forms.api_unyt.unyt
    assert puw.forms.api_unyt.compatibility(unyt.m, unyt.cm)
