from .base import PyUnitWizardCatalogException


class NotImplementedMethodError(PyUnitWizardCatalogException):
    catalog_key = "NotImplementedMethodError"

    def __init__(self, message=None, *, caller=None):
        extra = {}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)
