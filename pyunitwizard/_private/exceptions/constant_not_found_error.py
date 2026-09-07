from .base import PyUnitWizardCatalogException


class ConstantNotFoundError(PyUnitWizardCatalogException, ValueError):
    """Raised when a requested physical constant is not registered."""

    catalog_key = "ConstantNotFoundError"

    def __init__(self, message=None, *, constant=None, caller=None):
        extra = {"constant": constant}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)
