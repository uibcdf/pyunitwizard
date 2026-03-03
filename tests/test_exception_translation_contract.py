import pytest

import pyunitwizard as puw
from pyunitwizard.parse import parse as parse_quantity
from pyunitwizard._private.exceptions import (
    LibraryWithoutParserError,
    NoStandardsError,
    NotImplementedMethodError,
)

from .helpers import loaded_libraries


def test_backend_failure_is_translated_to_catalog_exception():
    with loaded_libraries(["pint"]):
        with pytest.raises(NotImplementedMethodError) as excinfo:
            puw.quantity({"x": 1}, "meter", form="pint")

    assert "Docs: https://uibcdf.org/pyunitwizard" in str(excinfo.value)


def test_parser_unavailable_path_uses_catalog_exception():
    with pytest.raises(LibraryWithoutParserError) as excinfo:
        parse_quantity("1 nanometer", parser="openmm.unit")

    assert "Docs: https://uibcdf.org/pyunitwizard" in str(excinfo.value)


def test_standardization_without_standards_uses_catalog_exception():
    with loaded_libraries(["pint"]):
        puw.configure.set_standard_units(["radian"])
        with pytest.raises(NoStandardsError) as excinfo:
            puw.get_standard_units(dimensionality={"[L]": 1, "[T]": 1}, form="string")

    assert "Docs: https://uibcdf.org/pyunitwizard" in str(excinfo.value)
