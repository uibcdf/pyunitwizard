import importlib

import pyunitwizard as puw

API_SYMBOLS = [
    "are_close",
    "are_compatible",
    "are_equal",
    "change_value",
    "check",
    "compatibility",
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
