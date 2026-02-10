from .base import PyUnitWizardCatalogException

class ArgumentError(PyUnitWizardCatalogException):
    catalog_key = "ArgumentError"

    def __init__(self, argument=None, value=None, caller=None, message=None):
        extra = {"argument": argument, "value": value}
        if caller:
            extra["caller"] = caller
        
        super().__init__(message=message, extra=extra)