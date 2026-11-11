"""Recognize NumPy object containers whose elements are row sequences."""

import numpy as np


def is_object_row_array(value: object) -> bool:
    """Include empty outer containers while keeping numeric object scalars native."""
    if not isinstance(value, np.ndarray) or value.dtype.kind != "O":
        return False
    return value.size == 0 or any(
        isinstance(row, (list, tuple)) or (isinstance(row, np.ndarray) and row.ndim > 0) for row in value.flat
    )
