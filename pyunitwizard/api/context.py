"""Context manager for temporary PyUnitWizard configuration."""

from __future__ import annotations
from contextlib import contextmanager
from typing import Optional, List, Any
from .. import kernel
from ..configure import configure

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
    # 1. Save current state
    old_state = {
        'default_form': kernel.default_form,
        'default_parser': kernel.default_parser,
        'standards': kernel.standards.copy(),
        'dimensional_fundamental_standards': kernel.dimensional_fundamental_standards.copy(),
        'dimensional_combinations_standards': kernel.dimensional_combinations_standards.copy(),
        'adimensional_standards': kernel.adimensional_standards.copy(),
        'tentative_base_standards': kernel.tentative_base_standards.copy(),
    }

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
        # 3. Restore state
        kernel.default_form = old_state['default_form']
        kernel.default_parser = old_state['default_parser']
        kernel.standards = old_state['standards']
        kernel.dimensional_fundamental_standards = old_state['dimensional_fundamental_standards']
        kernel.dimensional_combinations_standards = old_state['dimensional_combinations_standards']
        kernel.adimensional_standards = old_state['adimensional_standards']
        kernel.tentative_base_standards = old_state['tentative_base_standards']
