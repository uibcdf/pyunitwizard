from .base import PyUnitWizardCatalogException


class NoParserError(PyUnitWizardCatalogException):
    catalog_key = "NoParserError"

    def __init__(self, message=None, *, caller=None):
        extra = {}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)
