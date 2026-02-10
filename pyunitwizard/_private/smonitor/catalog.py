from __future__ import annotations

from pathlib import Path

from .meta import DOC_URL, ISSUES_URL, API_URL

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

META = {
    "doc_url": DOC_URL,
    "issues_url": ISSUES_URL,
    "api_url": API_URL,
}

CATALOG = {
    "exceptions": {
        "ArgumentError": {
            "code": "PUW-ERR-ARG-001",
            "source": "pyunitwizard.error.argument",
            "category": "argument",
            "level": "ERROR",
        },
        "LibraryNotFoundError": {
            "code": "PUW-ERR-DEP-001",
            "source": "pyunitwizard.error.library_not_found",
            "category": "dependency",
            "level": "ERROR",
        },
        "NoParserError": {
            "code": "PUW-ERR-PARSER-001",
            "source": "pyunitwizard.error.no_parser",
            "category": "parser",
            "level": "ERROR",
        },
        "LibraryWithoutParserError": {
            "code": "PUW-ERR-PARSER-002",
            "source": "pyunitwizard.error.library_without_parser",
            "category": "parser",
            "level": "ERROR",
        },
        "NotImplementedFormError": {
            "code": "PUW-ERR-FORM-001",
            "source": "pyunitwizard.error.not_implemented_form",
            "category": "not_implemented",
            "level": "ERROR",
        },
        "NotImplementedMethodError": {
            "code": "PUW-ERR-METHOD-001",
            "source": "pyunitwizard.error.not_implemented_method",
            "category": "not_implemented",
            "level": "ERROR",
        },
        "NotImplementedParserError": {
            "code": "PUW-ERR-PARSER-003",
            "source": "pyunitwizard.error.not_implemented_parser",
            "category": "parser",
            "level": "ERROR",
        },
        "NoStandardsError": {
            "code": "PUW-ERR-STD-001",
            "source": "pyunitwizard.error.no_standards",
            "category": "standards",
            "level": "ERROR",
        },
    }
}

CODES = {
    "PUW-ERR-ARG-001": {
        "title": "Argument error",
        "user_message": "Error in argument '{argument}' with value '{value}'.",
        "user_hint": "Check the API documentation for correct argument usage. Docs: {doc_url}",
        "dev_message": "Argument error in '{caller}' for '{argument}'.",
        "dev_hint": "Validate input arguments. Docs: {doc_url}",
    },
    "PUW-ERR-DEP-001": {
        "title": "Library not found",
        "user_message": "The required library '{library}' is not installed.",
        "user_hint": "Install the missing library to use this feature. Docs: {doc_url}",
        "dev_message": "Missing dependency '{library}' in '{caller}'.",
        "dev_hint": "Check installation environment. Docs: {doc_url}",
    },
    "PUW-ERR-PARSER-001": {
        "title": "No parser found",
        "user_message": "No suitable parser was found for the input.",
        "user_hint": "Ensure the input format is supported. Docs: {doc_url}",
        "dev_message": "No parser found in '{caller}'.",
        "dev_hint": "Register a suitable parser or check input. Docs: {doc_url}",
    },
    "PUW-ERR-PARSER-002": {
        "title": "Library without parser",
        "user_message": "Library '{library}' does not have an associated parser.",
        "user_hint": "This library is supported but lacks a parser implementation. Docs: {doc_url}",
        "dev_message": "Library '{library}' has no parser in '{caller}'.",
        "dev_hint": "Implement parser for '{library}'. Docs: {doc_url}",
    },
    "PUW-ERR-FORM-001": {
        "title": "Form not implemented",
        "user_message": "The form '{form}' is not implemented.",
        "user_hint": "Check supported forms in documentation. Docs: {doc_url}",
        "dev_message": "Form '{form}' not implemented in '{caller}'.",
        "dev_hint": "Implement form handling logic. Docs: {doc_url}",
    },
    "PUW-ERR-METHOD-001": {
        "title": "Method not implemented",
        "user_message": "This method is not implemented yet.",
        "user_hint": "Check alternative methods or wait for updates. Docs: {doc_url}",
        "dev_message": "Method not implemented in '{caller}'.",
        "dev_hint": "Implement method logic. Docs: {doc_url}",
    },
    "PUW-ERR-PARSER-003": {
        "title": "Parser not implemented",
        "user_message": "Parser for '{parser}' is not implemented.",
        "user_hint": "Check supported parsers. Docs: {doc_url}",
        "dev_message": "Parser '{parser}' not implemented in '{caller}'.",
        "dev_hint": "Implement parser logic. Docs: {doc_url}",
    },
    "PUW-ERR-STD-001": {
        "title": "No standards defined",
        "user_message": "No standard units have been defined.",
        "user_hint": "Define standard units before performing this operation. Docs: {doc_url}",
        "dev_message": "No standards defined in '{caller}'.",
        "dev_hint": "Call configure.set_standard_units(). Docs: {doc_url}",
    },
}

SIGNALS = {
    "pyunitwizard.error.argument": {"extra_required": ["argument", "value", "caller"]},
    "pyunitwizard.error.library_not_found": {"extra_required": ["library", "caller"]},
    "pyunitwizard.error.no_parser": {"extra_required": ["caller"]},
    "pyunitwizard.error.library_without_parser": {"extra_required": ["library", "caller"]},
    "pyunitwizard.error.not_implemented_form": {"extra_required": ["form", "caller"]},
    "pyunitwizard.error.not_implemented_method": {"extra_required": ["caller"]},
    "pyunitwizard.error.not_implemented_parser": {"extra_required": ["parser", "caller"]},
    "pyunitwizard.error.no_standards": {"extra_required": ["caller"]},
}