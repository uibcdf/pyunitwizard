from .base import PyUnitWizardCatalogException


class RecordError(PyUnitWizardCatalogException):
    """A quantity record that must not be read or written.

    Raised when a record fails its integrity seal, its self-description, or the reader's
    handshake. It is never a warning and there is never a fallback unit
    (uibcdf/pyunitwizard#82).
    """

    catalog_key = "RecordError"

    def __init__(self, message=None, *, reason=None, field=None, caller=None):
        extra = {"reason": reason, "field": field}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)
