import pytest

from pyunitwizard._private.exceptions import (
    LibraryNotFoundError,
    NoParserError,
    NotImplementedParserError,
)
from pyunitwizard._private.lists_and_tuples import (
    is_list_or_tuple,
    list_to_csv_string,
    list_to_ssv_string,
)


def test_is_list_or_tuple_contract():
    assert is_list_or_tuple([1, 2, 3]) is True
    assert is_list_or_tuple((1, 2, 3)) is True
    assert is_list_or_tuple("abc") is False
    assert is_list_or_tuple({"a": 1}) is False


def test_list_string_helpers_contract():
    assert list_to_csv_string([1, "nm", 3.0]) == "1,nm,3.0"
    assert list_to_ssv_string([1, "nm", 3.0]) == "1 nm 3.0"


def test_library_not_found_error_includes_library_and_docs():
    exc = LibraryNotFoundError("not-a-real-lib")
    text = str(exc)
    assert "not-a-real-lib" in text
    assert "Docs: https://uibcdf.org/pyunitwizard" in text


def test_no_parser_error_supports_optional_caller():
    no_caller = NoParserError()
    with_caller = NoParserError(caller="tests.fake")

    assert "No suitable parser was found for the input." in str(no_caller)
    assert "No suitable parser was found for the input." in str(with_caller)


def test_not_implemented_parser_error_mentions_parser():
    exc = NotImplementedParserError("fancy-parser")
    text = str(exc)
    assert "fancy-parser" in text
    assert "Parser for" in text
