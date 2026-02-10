from .base import PyUnitWizardCatalogException

class NoStandardsError(PyUnitWizardCatalogException):
    catalog_key = "NoStandardsError"

    def __init__(self, caller=None, message=None):
        extra = {}
        if caller:
            extra["caller"] = caller
        
        super().__init__(message=message, extra=extra)