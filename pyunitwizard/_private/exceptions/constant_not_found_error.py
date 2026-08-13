from .base import PyUnitWizardCatalogException


class ConstantNotFoundError(PyUnitWizardCatalogException, ValueError):
    """Raised when a requested physical constant is not registered."""

    catalog_key = "ConstantNotFoundError"

    def __init__(self, constant, caller=None, message=None):
        extra = {"constant": constant}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)
