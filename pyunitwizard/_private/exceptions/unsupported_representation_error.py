from typing import Optional

from .base import PyUnitWizardCatalogException


class UnsupportedRepresentationError(PyUnitWizardCatalogException, TypeError):
    """An operation cannot represent a NumPy object array of row sequences.

    Parameters
    ----------
    message : str, optional
        Explicit message used when reconstructing an existing exception.
    form : str, optional
        Backend refusing the representation.
    operation : str, optional
        Refused operation, such as construct or convert.
    caller : str, optional
        Diagnostic caller context.
    """

    catalog_key = "UnsupportedRepresentationError"

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        form: Optional[str] = None,
        operation: Optional[str] = None,
        caller: Optional[str] = None,
    ) -> None:
        extra = {"form": form, "operation": operation}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)
