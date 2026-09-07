from .base import PyUnitWizardCatalogException


class FastTrackConflictError(PyUnitWizardCatalogException):
    """Raised when a fast-track name is bound to a different target unit."""

    catalog_key = "FastTrackConflictError"

    def __init__(
        self,
        message=None,
        *,
        name=None,
        existing_target=None,
        requested_target=None,
        caller=None,
    ):
        extra = {
            "name": name,
            "existing_target": existing_target,
            "requested_target": requested_target,
        }
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)
