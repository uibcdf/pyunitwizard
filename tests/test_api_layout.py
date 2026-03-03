import importlib
import sys
import warnings

import pyunitwizard as puw

API_SYMBOLS = [
    "are_close",
    "are_compatible",
    "are_equal",
    "change_value",
    "check",
    "compatibility",
    "context",
    "convert",
    "get_dimensionality",
    "get_form",
    "get_standard_units",
    "get_unit",
    "get_value",
    "get_value_and_unit",
    "is_dimensionless",
    "is_quantity",
    "is_unit",
    "quantity",
    "similarity",
    "standardize",
    "to_string",
    "unit",
]


def test_main_reexports_api():
    api = importlib.import_module("pyunitwizard.api")
    main = importlib.import_module("pyunitwizard.main")

    for name in API_SYMBOLS:
        assert getattr(main, name) is getattr(api, name)


def test_package_reexports_api():
    api = importlib.import_module("pyunitwizard.api")

    for name in API_SYMBOLS:
        assert getattr(puw, name) is getattr(api, name)


def test_main_deprecation_warning_emitted_once_for_attribute_access():
    sys.modules["pyunitwizard.main"] = puw._create_main_compat_module()
    main = importlib.import_module("pyunitwizard.main")

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        _ = main.convert
        _ = main.convert

    dep_warnings = [w for w in captured if issubclass(w.category, DeprecationWarning)]
    assert len(dep_warnings) == 1


def test_main_unknown_attribute_raises_attribute_error():
    main = importlib.import_module("pyunitwizard.main")

    try:
        _ = main.__definitely_unknown_attr__
    except AttributeError:
        pass
    else:
        raise AssertionError("Expected AttributeError for unknown pyunitwizard.main attribute")
