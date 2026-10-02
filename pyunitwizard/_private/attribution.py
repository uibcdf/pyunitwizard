"""Explicit optional attribution of completed third-party backend operations."""

from contextlib import contextmanager
from typing import Iterator

from .._ackredit import _ENABLED


@contextmanager
def attribution() -> Iterator[None]:
    """Enable the bounded Pint/unyt attribution pilot in this context.

    Returns
    -------
    context manager
        Enables optional credit for completed dispatch operations in this context
        and restores the enclosing choice on exit. Nested contexts are supported.
        Application-owned Ackredit sessions/captures retain workflow and result
        bibliography. This context does not replace a session or alter quantities.

    Raises
    ------
    Exception
        Scientific exceptions propagate. Provider failures emit a catalog warning
        while preserving completed results; applications may promote warnings.

    Examples
    --------
    >>> import pyunitwizard as puw
    >>> with puw.attribution():
    ...     quantity = puw.quantity(2.0, "meter", form="pint")
    ...     result = puw.convert(quantity, to_unit="centimeter")

    Notes
    -----
    Provisional source integration under uibcdf/pyunitwizard#92. Entering this
    context imports no optional provider/backend. Without Ackredit, calculations
    keep working. Ordinary operations outside the context do not load Ackredit.
    Cached parse returns, direct adapter calls and other backends are outside
    the initial coverage. No hooks, enrichment, journals or reminders are enabled.
    """
    token = _ENABLED.set(True)
    try:
        yield
    finally:
        _ENABLED.reset(token)
