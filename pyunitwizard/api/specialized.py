"""Specialized conversion fast-tracks for ecosystem canonical units."""

from __future__ import annotations

from typing import Any, Optional

import numpy as np

from .conversion import convert
from .extraction import get_unit
from .introspection import get_form


class FastTrack:
    """Container for dynamically registered conversion fast-tracks."""
    pass

fast_track = FastTrack()

def register_fast_track(name: str, target_unit: Any):
    """Register a new fast-track conversion function.
    
    Parameters
    ----------
    name : str
        The name of the function (e.g., "nanometers" will create fast_track.to_nanometers).
    target_unit : Any
        The pre-parsed unit object from a supported backend.
    """
    from .conversion import convert
    from .extraction import get_unit
    from .introspection import get_form

    def to_standard(obj, parser=None):
        # 1. Bypass for naked arrays (trusted internal calls)
        if isinstance(obj, np.ndarray):
            return obj
        
        # 2. Bypass if already in the right unit
        if get_unit(obj) == target_unit:
            return obj
            
        # 3. Fallback to general conversion
        return convert(obj, to_unit=target_unit, parser=parser)

    # Inject into the fast_track instance
    setattr(fast_track, f"to_{name}", to_standard)

# Pre-register common ones if needed or leave empty for host libraries
# register_fast_track("nanometers", convert("nm", to_type="unit"))
