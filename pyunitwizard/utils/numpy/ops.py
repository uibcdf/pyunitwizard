import numpy as np

from pyunitwizard import (
    convert,
    get_form,
    get_unit,
    get_value,
    is_quantity,
    quantity,
)


def _format_output_value(value, value_type):
    if value_type == "list":
        return np.asarray(value).tolist()
    if value_type == "tuple":
        return tuple(np.asarray(value).tolist())
    if value_type == "numpy.ndarray":
        return np.asarray(value)
    if value_type is None:
        return value
    raise ValueError


def _trapezoid(y, x=None, dx=1.0, axis=-1):
    if hasattr(np, "trapezoid"):
        return np.trapezoid(y, x=x, dx=dx, axis=axis)
    return np.trapz(y, x=x, dx=dx, axis=axis)


def mean(
    quantity_like,
    axis=None,
    to_unit=None,
    to_form=None,
    value_type=None,
    standardized=False,
    **kwargs,
):
    output_unit = get_unit(quantity_like) if to_unit is None else to_unit
    output_value = np.mean(get_value(quantity_like, to_unit=output_unit), axis=axis, **kwargs)
    output_value = _format_output_value(output_value, value_type)
    return quantity(output_value, output_unit, form=to_form, standardized=standardized)


def sum(
    quantity_like,
    axis=None,
    to_unit=None,
    to_form=None,
    value_type=None,
    standardized=False,
    **kwargs,
):
    output_unit = get_unit(quantity_like) if to_unit is None else to_unit
    output_value = np.sum(get_value(quantity_like, to_unit=output_unit), axis=axis, **kwargs)
    output_value = _format_output_value(output_value, value_type)
    return quantity(output_value, output_unit, form=to_form, standardized=standardized)


def linalg_norm(
    quantity_like,
    ord=None,
    axis=None,
    keepdims=False,
    to_unit=None,
    to_form=None,
    value_type=None,
    standardized=False,
):
    output_unit = get_unit(quantity_like) if to_unit is None else to_unit
    output_value = np.linalg.norm(
        get_value(quantity_like, to_unit=output_unit),
        ord=ord,
        axis=axis,
        keepdims=keepdims,
    )
    output_value = _format_output_value(output_value, value_type)
    return quantity(output_value, output_unit, form=to_form, standardized=standardized)


def trapz(
    y,
    x=None,
    dx=1.0,
    axis=-1,
    to_unit=None,
    to_form=None,
    value_type=None,
    standardized=False,
):
    y_form = get_form(y)
    y_unit = get_unit(y) if to_unit is None else to_unit
    y_value = get_value(y, to_unit=y_unit)

    if x is not None:
        if get_form(x) != y_form:
            x = convert(x, to_form=y_form)
        x_unit = get_unit(x)
        x_value = get_value(x, to_unit=x_unit)
        output_value = _trapezoid(y_value, x=x_value, axis=axis)
        output_unit = get_unit(
            quantity(1.0, y_unit, form=y_form) * quantity(1.0, x_unit, form=y_form)
        )
    else:
        if is_quantity(dx):
            if get_form(dx) != y_form:
                dx = convert(dx, to_form=y_form)
            dx_unit = get_unit(dx)
            dx_value = get_value(dx, to_unit=dx_unit)
            output_value = _trapezoid(y_value, dx=dx_value, axis=axis)
            output_unit = get_unit(
                quantity(1.0, y_unit, form=y_form) * quantity(1.0, dx_unit, form=y_form)
            )
        else:
            output_value = _trapezoid(y_value, dx=dx, axis=axis)
            output_unit = y_unit

    output_value = _format_output_value(output_value, value_type)
    return quantity(output_value, output_unit, form=to_form, standardized=standardized)
