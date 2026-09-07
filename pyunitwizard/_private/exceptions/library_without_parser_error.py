from .base import PyUnitWizardCatalogException


class LibraryWithoutParserError(PyUnitWizardCatalogException):
    catalog_key = "LibraryWithoutParserError"

    def __init__(self, message=None, *, library=None, caller=None):
        extra = {"library": library}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)
