"""Catalog-backed warnings for optional scientific attribution."""

from smonitor.integrations import CatalogWarning

from .catalog import CATALOG, META


class AckreditTrackingWarning(CatalogWarning):
    catalog_key = "AckreditTrackingWarning"

    def __init__(self, message=None, **kwargs):
        if message is None or kwargs:
            kwargs.setdefault("catalog", CATALOG)
            kwargs.setdefault("meta", META)
        super().__init__(message, **kwargs)
