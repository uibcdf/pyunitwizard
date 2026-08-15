import pytest

import pyunitwizard as puw
import pyunitwizard._depdigest as puw_depdigest


def test_depdigest_runtime_policy_has_expected_hard_and_soft_dependencies():
    hard = {
        name for name, metadata in puw_depdigest.LIBRARIES.items() if metadata.get("type") == "hard"
    }
    soft = {
        name for name, metadata in puw_depdigest.LIBRARIES.items() if metadata.get("type") == "soft"
    }

    assert hard == {"numpy", "pint"}
    assert soft == {"unyt", "openmm.unit", "astropy.units", "physipy", "quantities"}


def test_depdigest_mapping_is_consistent_with_supported_forms():
    mapping = puw_depdigest.MAPPING
    supported = set(puw.configure.get_libraries_supported())

    assert set(mapping.keys()) == {
        "pint",
        "unyt",
        "openmm.unit",
        "astropy.units",
        "physipy",
        "quantities",
    }
    assert set(mapping.values()).issubset(set(puw_depdigest.LIBRARIES))
    assert set(mapping.keys()).issubset(supported)


def test_missing_backend_is_still_guarded_without_a_decorator_on_convert():
    """`convert()` declares no backend dependency, and must still be guarded.

    The five `@dep_digest` decorators it used to carry cost about 6.2 us per
    call and duplicated a check that already happens earlier: any route needing
    a backend passes through `digest_form()` -> `load_library()`. This pins that
    ordering, since it is what makes the declaration unnecessary there.
    """
    import depdigest

    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    quantity = puw.quantity(1.0, "nanometer", form="pint")

    real_is_installed = depdigest.is_installed

    def unyt_is_missing(library, *args, **kwargs):
        if library == "unyt":
            return False
        return real_is_installed(library, *args, **kwargs)

    depdigest.is_installed = unyt_is_missing
    try:
        with pytest.raises(ModuleNotFoundError) as excinfo:
            puw.convert(quantity, to_form="unyt")
    finally:
        depdigest.is_installed = real_is_installed

    assert "unyt" in str(excinfo.value)


def test_convert_carries_no_per_call_dependency_wrappers():
    """The declaration belongs to `_depdigest.py`, not to the hot dispatcher."""
    from pyunitwizard.api import conversion

    layers = 0
    function = conversion.convert
    while hasattr(function, "__wrapped__"):
        layers += 1
        function = function.__wrapped__

    # Only the @signal instrumentation remains.
    assert layers == 1
