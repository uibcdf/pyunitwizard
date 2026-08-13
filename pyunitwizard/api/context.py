"""Context manager for temporary PyUnitWizard configuration."""

from __future__ import annotations

import copy
from contextlib import contextmanager
from typing import List, Optional

import numpy as np
from smonitor import signal

from .. import kernel
from ..configure import configure


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
    state_names = (
        "loaded_libraries",
        "loaded_parsers",
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
    )
    old_state = {}
    for name in state_names:
        value = getattr(kernel, name)
        old_state[name] = (
            value.copy() if isinstance(value, np.ndarray) else copy.copy(value)
        )

    # 2. Apply new state
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
