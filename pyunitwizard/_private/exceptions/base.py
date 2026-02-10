from __future__ import annotations

from smonitor.integrations import CatalogException
from ..functions import caller_name
from ..smonitor.catalog import CATALOG, META


class PyUnitWizardCatalogException(CatalogException):
    def __init__(self, **kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        if "caller" not in kwargs["extra"]:
            kwargs["extra"]["caller"] = caller_name()
        
        super().__init__(catalog=CATALOG, meta=META, **kwargs)
