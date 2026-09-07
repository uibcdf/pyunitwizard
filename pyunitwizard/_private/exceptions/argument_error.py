from .base import PyUnitWizardCatalogException


class ArgumentError(PyUnitWizardCatalogException):
    catalog_key = "ArgumentError"

    def __init__(self, message=None, *, argument=None, value=None, caller=None):
        extra = {"argument": argument, "value": value}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)
