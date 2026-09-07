from .base import PyUnitWizardCatalogException


class NotImplementedParserError(PyUnitWizardCatalogException):
    catalog_key = "NotImplementedParserError"

    def __init__(self, message=None, *, parser=None, caller=None):
        extra = {"parser": parser}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)
