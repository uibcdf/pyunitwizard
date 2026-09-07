"""Specialized conversion fast-tracks for ecosystem canonical units."""

from __future__ import annotations

from threading import RLock
from typing import Any

import numpy as np

from .._private.exceptions import FastTrackConflictError


class FastTrack:
    """Container for dynamically registered conversion fast-tracks."""


fast_track = FastTrack()
_REGISTRATION_LOCK = RLock()


def register_fast_track(name: str, target_unit: Any) -> None:
    """Register a new fast-track conversion function.

    Parameters
    ----------
    name : str
        The name of the function (e.g., "nanometers" will create fast_track.to_nanometers).
    target_unit : Any
        The pre-parsed unit object from a supported backend.

    Raises
    ------
    FastTrackConflictError
        If ``name`` is already registered for a different target unit.
    """
    from .introspection import has_unit

    attribute_name = f"to_{name}"

    with _REGISTRATION_LOCK:
        existing = getattr(fast_track, attribute_name, None)
        if existing is not None:
            existing_target = getattr(existing, "_pyunitwizard_target_unit", None)
            if existing_target is not None and has_unit(existing_target, target_unit):
                return
            raise FastTrackConflictError(
                name=name,
                existing_target=str(existing_target),
                requested_target=str(target_unit),
            )

        _register_fast_track(attribute_name, target_unit)


def _register_fast_track(attribute_name: str, target_unit: Any) -> None:
    from .conversion import convert
    from .introspection import has_unit

    def to_standard(obj, parser=None):
        # 1. Bypass for naked arrays (trusted internal calls)
        if isinstance(obj, np.ndarray):
            return obj

        # 2. Bypass if already in the right unit
        if has_unit(obj, target_unit, parser=parser) is True:
            return obj

        # 3. Fallback to general conversion
        return convert(obj, to_unit=target_unit, parser=parser)

    to_standard._pyunitwizard_target_unit = target_unit
    setattr(fast_track, attribute_name, to_standard)


__all__ = [
    "fast_track",
    "register_fast_track",
]
