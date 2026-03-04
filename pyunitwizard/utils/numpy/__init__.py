from __future__ import annotations

from contextlib import contextmanager

import numpy as _np

import pyunitwizard as _puw

from .stack import stack
from .hstack import hstack
from .vstack import vstack
from .column_stack import column_stack
from .repeat import repeat
from .ops import mean, std, sum, var, linalg_norm, dot, trapz

_NUMPY_PATCH_STATE = {
    "enabled": False,
    "mean": None,
    "sum": None,
    "std": None,
    "var": None,
    "dot": None,
    "trapezoid": None,
    "trapz": None,
    "linalg_norm": None,
}


def _is_quantity_payload(obj):
    if _puw.is_quantity(obj):
        return True
    if isinstance(obj, (list, tuple)):
        return any(_is_quantity_payload(item) for item in obj)
    return False


def _patched_mean(a, *args, **kwargs):
    if _is_quantity_payload(a):
        return mean(a, *args, **kwargs)
    return _NUMPY_PATCH_STATE["mean"](a, *args, **kwargs)


def _patched_sum(a, *args, **kwargs):
    if _is_quantity_payload(a):
        return sum(a, *args, **kwargs)
    return _NUMPY_PATCH_STATE["sum"](a, *args, **kwargs)


def _patched_std(a, *args, **kwargs):
    if _is_quantity_payload(a):
        return std(a, *args, **kwargs)
    return _NUMPY_PATCH_STATE["std"](a, *args, **kwargs)


def _patched_var(a, *args, **kwargs):
    if _is_quantity_payload(a):
        return var(a, *args, **kwargs)
    return _NUMPY_PATCH_STATE["var"](a, *args, **kwargs)


def _patched_dot(a, b, *args, **kwargs):
    if _is_quantity_payload(a) or _is_quantity_payload(b):
        return dot(a, b, *args, **kwargs)
    return _NUMPY_PATCH_STATE["dot"](a, b, *args, **kwargs)


def _patched_trapezoid(y, x=None, dx=1.0, axis=-1):
    if _is_quantity_payload(y) or _is_quantity_payload(x) or _puw.is_quantity(dx):
        return trapz(y, x=x, dx=dx, axis=axis)
    return _NUMPY_PATCH_STATE["trapezoid"](y, x=x, dx=dx, axis=axis)


def _patched_linalg_norm(x, ord=None, axis=None, keepdims=False):
    if _is_quantity_payload(x):
        return linalg_norm(x, ord=ord, axis=axis, keepdims=keepdims)
    return _NUMPY_PATCH_STATE["linalg_norm"](x, ord=ord, axis=axis, keepdims=keepdims)


def setup_numpy(enable: bool = True) -> None:
    """Enable or disable transparent NumPy quantity dispatch for common ops."""
    if enable:
        if _NUMPY_PATCH_STATE["enabled"]:
            return

        _NUMPY_PATCH_STATE["mean"] = _np.mean
        _NUMPY_PATCH_STATE["sum"] = _np.sum
        _NUMPY_PATCH_STATE["std"] = _np.std
        _NUMPY_PATCH_STATE["var"] = _np.var
        _NUMPY_PATCH_STATE["dot"] = _np.dot
        _NUMPY_PATCH_STATE["trapezoid"] = getattr(_np, "trapezoid", None)
        _NUMPY_PATCH_STATE["trapz"] = getattr(_np, "trapz", None)
        _NUMPY_PATCH_STATE["linalg_norm"] = _np.linalg.norm

        _np.mean = _patched_mean
        _np.sum = _patched_sum
        _np.std = _patched_std
        _np.var = _patched_var
        _np.dot = _patched_dot
        _np.linalg.norm = _patched_linalg_norm
        if hasattr(_np, "trapezoid"):
            _np.trapezoid = _patched_trapezoid
        if hasattr(_np, "trapz"):
            _np.trapz = _patched_trapezoid

        _NUMPY_PATCH_STATE["enabled"] = True
    else:
        if not _NUMPY_PATCH_STATE["enabled"]:
            return

        _np.mean = _NUMPY_PATCH_STATE["mean"]
        _np.sum = _NUMPY_PATCH_STATE["sum"]
        _np.std = _NUMPY_PATCH_STATE["std"]
        _np.var = _NUMPY_PATCH_STATE["var"]
        _np.dot = _NUMPY_PATCH_STATE["dot"]
        _np.linalg.norm = _NUMPY_PATCH_STATE["linalg_norm"]
        if _NUMPY_PATCH_STATE["trapezoid"] is not None:
            _np.trapezoid = _NUMPY_PATCH_STATE["trapezoid"]
        if _NUMPY_PATCH_STATE["trapz"] is not None:
            _np.trapz = _NUMPY_PATCH_STATE["trapz"]

        _NUMPY_PATCH_STATE["enabled"] = False
        _NUMPY_PATCH_STATE["mean"] = None
        _NUMPY_PATCH_STATE["sum"] = None
        _NUMPY_PATCH_STATE["std"] = None
        _NUMPY_PATCH_STATE["var"] = None
        _NUMPY_PATCH_STATE["dot"] = None
        _NUMPY_PATCH_STATE["trapezoid"] = None
        _NUMPY_PATCH_STATE["trapz"] = None
        _NUMPY_PATCH_STATE["linalg_norm"] = None


@contextmanager
def numpy_context():
    """Temporarily enable transparent NumPy quantity dispatch."""
    already_enabled = _NUMPY_PATCH_STATE["enabled"]
    setup_numpy(enable=True)
    try:
        yield
    finally:
        if not already_enabled:
            setup_numpy(enable=False)


__all__ = [
    "stack",
    "hstack",
    "vstack",
    "column_stack",
    "repeat",
    "mean",
    "std",
    "sum",
    "var",
    "linalg_norm",
    "dot",
    "trapz",
    "setup_numpy",
    "numpy_context",
]
