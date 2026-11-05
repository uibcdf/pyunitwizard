from .base import PyUnitWizardCatalogException


class UnitDefinitionError(PyUnitWizardCatalogException, ValueError):
    """A named unit disagrees with the physical meaning required by a translator."""

    catalog_key = "UnitDefinitionError"

    def __init__(self, message=None, *, unit=None, form=None, caller=None):
        extra = {"unit": unit, "form": form}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)
