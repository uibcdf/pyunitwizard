from .base import PyUnitWizardCatalogException


class NotImplementedFormError(PyUnitWizardCatalogException):
    catalog_key = "NotImplementedFormError"

    def __init__(self, message=None, *, form=None, caller=None):
        extra = {"form": form}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)
