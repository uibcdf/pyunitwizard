"""Context manager for temporary PyUnitWizard configuration."""

from __future__ import annotations

import copy
from contextlib import contextmanager
from typing import List, Optional

import numpy as np
from smonitor import signal

from .. import kernel
from ..configure import configure


def _snapshot(value):
    """Copy a kernel value deeply enough that restoring it actually restores it.

    `copy.copy` is not sufficient for the standard maps: their values are
    dictionaries and lists shared with the live state, so mutating one in place
    inside a context survived the context. Only one level of nesting exists, so
    that is the level copied — `copy.deepcopy` would also try to duplicate unit
    objects and registries, which are immutable and must stay shared.
    """

    if isinstance(value, np.ndarray):
        return value.copy()

    if isinstance(value, dict):
        return {
            key: dict(item) if isinstance(item, dict) else copy.copy(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            (item[0], dict(item[1]))
            if isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], dict)
            else item
            for item in value
        ]

    return copy.copy(value)


@signal(tags=["context"])
@contextmanager
def context(
    default_form: Optional[str] = None,
    default_parser: Optional[str] = None,
    standard_units: Optional[List[str]] = None,
):
    """
    Context manager to temporarily change PyUnitWizard configuration.

    Parameters
    ----------
    default_form : str, optional
        Temporary default form.
    default_parser : str, optional
        Temporary default parser.
    standard_units : list of str, optional
        Temporary standard units.

    Examples
    --------
    >>> with puw.context(default_form='pint', standard_units=['nm', 'ps']):
    >>>     q = puw.standardize(input_q)
    """
    # Backend loading is deliberately absent. Loading a backend is a capability,
    # not a policy: Python cannot truly unload a module, and reverting
    # `loaded_libraries` while the `forms/` dispatch registries stay populated
    # left the kernel claiming a backend was unloaded when it was not. A backend
    # loaded inside a context stays loaded, which is both honest and harmless.
    #
    # The introspection caches are absent for the same kind of reason: a unit's
    # dimensionality and a type's form are facts, not configuration. `reset()`
    # clears them because it tears everything down for tests; a context has no
    # cause to discard them.
    state_names = (
        "default_form",
        "default_parser",
        "standards",
        "dimensional_fundamental_standards",
        "dimensional_combinations_standards",
        "adimensional_standards",
        "tentative_base_standards",
        "dimensional_fundamental_standards_matrix",
        "dimensional_fundamental_standards_units",
        "tentative_base_standards_matrix",
        "tentative_base_standards_units",
        "standard_units_by_dimensionality_cache",
        "conversion_factor_cache",
        "canonical_standards",
        "policy_provenance",
    )
    old_state = {name: _snapshot(getattr(kernel, name)) for name in state_names}

    # Fast tracks live on a module-level object rather than in the kernel, so
    # they need their own snapshot; without it a registration made inside a
    # context outlived it.
    from .specialized import fast_track

    old_fast_tracks = dict(vars(fast_track))

    try:
        if default_form is not None:
            configure.set_default_form(default_form)
        if default_parser is not None:
            configure.set_default_parser(default_parser)
        if standard_units is not None:
            configure.set_standard_units(standard_units)

        yield

    finally:
        for name, value in old_state.items():
            setattr(kernel, name, value)

        for name in set(vars(fast_track)) - set(old_fast_tracks):
            delattr(fast_track, name)
        for name, value in old_fast_tracks.items():
            setattr(fast_track, name, value)
