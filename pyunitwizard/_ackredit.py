"""Lazy optional provider boundary for completed Pint/unyt dispatch operations."""

from contextvars import ContextVar
from functools import wraps
from weakref import WeakKeyDictionary

from depdigest import dep_digest, is_installed

_ENABLED = ContextVar("pyunitwizard_attribution_enabled", default=False)

_PILOT_BACKENDS = {"pint", "unyt"}
_PREPARED = WeakKeyDictionary()


@dep_digest("ackredit")
def _load_backend():
    import ackredit

    return ackredit


def backend():
    """Discover the provider only after a meaningful backend operation succeeds."""
    return _load_backend() if is_installed("ackredit") else None


def _failed(operation, error):
    from ._private.smonitor.emitter import warn
    from ._private.smonitor.warnings import AckreditTrackingWarning

    warn(AckreditTrackingWarning(extra={"operation": operation, "reason": f"{type(error).__name__}: {error}"}))


def _credit(libraries, operation):
    # This boundary catches attribution failures only. The scientific callable
    # has already returned, and its exceptions never enter this handler.
    try:
        provider = backend()
        if provider is None:
            return
        from ._private.backend_references import records

        with provider.scope(operation):
            for library in libraries:
                declarations = records(library)
                prepare = getattr(provider, "prepare_credit", None)
                if callable(prepare):
                    # Values, not mutable identities, select a privately detached
                    # fixed-use plan. Each credit still writes to the current
                    # session/captures and refuses replaced provider metadata.
                    cache = _PREPARED.setdefault(provider, {})
                    previous = cache.get((operation, library))
                    if previous is None or previous[0] != declarations:
                        credits = []
                        for declaration in declarations:
                            record = declaration["record"]
                            provider.register_item(**record)
                            credits.append(
                                prepare(
                                    record["id"],
                                    operation,
                                    roles=declaration["roles"],
                                    context=declaration["context"],
                                )
                            )
                        cache[(operation, library)] = declarations, credits
                    for credit in cache[(operation, library)][1]:
                        credit()
                    continue
                # Public Ackredit 0.9.0 retains its existing portable boundary.
                for declaration in declarations:
                    record = declaration["record"]
                    provider.register_item(**record)
                    provider.track_item(
                        record["id"], used_by=operation, roles=declaration["roles"], context=declaration["context"]
                    )
    except Exception as error:
        _failed(operation, error)


def wrap(function, *libraries, operation):
    """Bind actual dispatch endpoints; do not credit loading or failed calls.

    Bridges call wrapped child translators and are therefore not wrapped twice.
    Array operations produce one credit per completed dispatch, not per element.
    """
    reached = tuple(dict.fromkeys(lib for lib in libraries if lib in _PILOT_BACKENDS))
    if not reached or hasattr(function, "_puw_attribution") or function.__name__.endswith("_bridge"):
        return function

    @wraps(function)
    def observed(*args, **kwargs):
        result = function(*args, **kwargs)
        if _ENABLED.get():
            _credit(reached, operation)
        return result

    observed._puw_attribution = (reached, operation)
    return observed
