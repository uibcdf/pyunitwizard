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
