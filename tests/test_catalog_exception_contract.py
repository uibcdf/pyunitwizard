import inspect
from pathlib import Path

import pytest

from pyunitwizard._private.exceptions import (
    ArgumentError,
    ConstantNotFoundError,
    FastTrackConflictError,
    LibraryNotFoundError,
    LibraryWithoutParserError,
    NoParserError,
    NoStandardsError,
    NotImplementedFormError,
    NotImplementedMethodError,
    NotImplementedParserError,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

EXCEPTION_CASES = [
    (ArgumentError, {"argument": "value", "value": -1}),
    (ConstantNotFoundError, {"constant": "speed_of_magic"}),
    (
        FastTrackConflictError,
        {
            "name": "nanometers",
            "existing_target": "nanometer",
            "requested_target": "angstrom",
        },
    ),
    (LibraryNotFoundError, {"library": "missing-library"}),
    (LibraryWithoutParserError, {"library": "parserless-library"}),
    (NoParserError, {}),
    (NoStandardsError, {}),
    (NotImplementedFormError, {"form": "future-form"}),
    (NotImplementedMethodError, {}),
    (NotImplementedParserError, {"parser": "future-parser"}),
]


@pytest.mark.parametrize(("exception_class", "domain_fields"), EXCEPTION_CASES)
def test_catalog_exception_constructor_is_safe_to_rebuild(
    exception_class, domain_fields
):
    parameters = list(inspect.signature(exception_class).parameters.values())

    assert parameters[0].name == "message"
    assert parameters[0].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY for parameter in parameters[1:]
    )

    original = exception_class(**domain_fields, caller="tests.catalog_contract")
    rebuilt = exception_class(*original.args)

    assert rebuilt.args == original.args
    assert str(rebuilt) == str(original)
    assert rebuilt.code == original.code


def test_conda_recipe_requires_the_supported_smonitor_version():
    recipe = (REPOSITORY_ROOT / "devtools" / "conda-build" / "meta.yaml").read_text()

    assert "- smonitor >=0.13.0" in recipe
