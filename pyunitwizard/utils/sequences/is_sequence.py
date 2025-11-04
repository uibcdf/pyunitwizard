"""Helpers to determine whether objects behave like sequences."""

from __future__ import annotations

from ... import is_quantity
import numpy as np

def is_sequence(item):
    """Check if a item is a sequence (list, tuple, set, or ndarray)."""
    return isinstance(item, (list, tuple, set, np.ndarray))

def is_sequence_of_sequences(item):
    """Check if a item is a sequence containing only sequences."""
    return is_sequence(item) and all(is_sequence(item) for item in item)

def is_sequence_of_sequences_of_sequences(item):
    """Check if an item is a sequence containing only sequences of sequences."""
    return is_sequence(item) and all(is_sequence_of_sequences(element) for element in item)

def is_sequence_of_quantities(item):
    """Check if an item is a sequence containing only quantities."""
    return is_sequence(item) and all(is_quantity(element) for element in item)

