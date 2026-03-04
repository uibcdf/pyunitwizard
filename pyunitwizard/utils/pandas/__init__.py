from contextlib import contextmanager

from pyunitwizard import convert, get_unit, get_value, quantity


UNITS_ATTR_KEY = "pyunitwizard_units"


def _import_pandas():
    import pandas as pd

    return pd


def _normalize_unit(unit_like):
    return convert(unit_like, to_form="string", to_type="unit")


def get_units_map(dataframe):
    units = dataframe.attrs.get(UNITS_ATTR_KEY, {})
    return dict(units)


def set_units_map(dataframe, units_map, inplace=False, strict=True):
    if inplace:
        target = dataframe
    else:
        target = dataframe.copy()

    normalized = {}
    columns = set(target.columns)
    for name, unit_like in units_map.items():
        if strict and name not in columns:
            raise ValueError(f"Column '{name}' is not present in dataframe.")
        if name in columns:
            normalized[name] = _normalize_unit(unit_like)

    target.attrs[UNITS_ATTR_KEY] = normalized
    return target


def sync_units_map(dataframe, inplace=False):
    units = get_units_map(dataframe)
    return set_units_map(dataframe, units, inplace=inplace, strict=False)


def _merge_units_maps(*maps):
    merged = {}
    for units_map in maps:
        for name, unit_name in units_map.items():
            normalized = _normalize_unit(unit_name)
            if name in merged and merged[name] != normalized:
                raise ValueError(
                    f"Incompatible units metadata for column '{name}': "
                    f"'{merged[name]}' vs '{normalized}'."
                )
            merged[name] = normalized
    return merged


def concat(dataframes, axis=0, **kwargs):
    pd = _import_pandas()
    dataframes = list(dataframes)
    output = pd.concat(dataframes, axis=axis, **kwargs)
    merged_units = _merge_units_maps(*(get_units_map(df) for df in dataframes))
    return set_units_map(output, merged_units, inplace=True, strict=False)


def merge(left, right, **kwargs):
    pd = _import_pandas()
    output = pd.merge(left, right, **kwargs)
    merged_units = _merge_units_maps(get_units_map(left), get_units_map(right))
    return set_units_map(output, merged_units, inplace=True, strict=False)


def dataframe_from_quantities(columns, index=None, to_units=None, copy=True):
    pd = _import_pandas()
    to_units = to_units or {}

    values = {}
    units = {}
    for name, quantity_like in columns.items():
        output_unit = to_units.get(name, get_unit(quantity_like))
        values[name] = get_value(quantity_like, to_unit=output_unit)
        units[name] = _normalize_unit(output_unit)

    dataframe = pd.DataFrame(values, index=index, copy=copy)
    dataframe.attrs[UNITS_ATTR_KEY] = units
    return dataframe


def add_quantity_column(dataframe, name, quantity_like, to_unit=None, inplace=False):
    output_unit = get_unit(quantity_like) if to_unit is None else to_unit
    output_values = get_value(quantity_like, to_unit=output_unit)

    if inplace:
        target = dataframe
    else:
        target = dataframe.copy()

    target[name] = output_values
    units = get_units_map(target)
    units[name] = _normalize_unit(output_unit)
    target.attrs[UNITS_ATTR_KEY] = units

    return target


def get_quantity_column(
    dataframe,
    name,
    unit_name=None,
    to_form=None,
    standardized=False,
    value_type=None,
):
    if unit_name is None:
        units = get_units_map(dataframe)
        if name not in units:
            raise ValueError(
                f"Column '{name}' has no associated unit metadata. "
                "Provide unit_name explicitly or attach units first."
            )
        output_unit = units[name]
    else:
        output_unit = unit_name

    series = dataframe[name]
    values = series.to_numpy()

    if value_type == "list":
        values = values.tolist()
    elif value_type == "tuple":
        values = tuple(values.tolist())
    elif value_type == "numpy.ndarray" or value_type is None:
        pass
    else:
        raise ValueError(f"Unsupported value_type='{value_type}'.")

    return quantity(values, output_unit, form=to_form, standardized=standardized)


class _PyUnitWizardDataFrameAccessor:
    def __init__(self, dataframe):
        self._dataframe = dataframe

    def get_units_map(self):
        return get_units_map(self._dataframe)

    def set_units_map(self, units_map, inplace=True, strict=True):
        output = set_units_map(
            self._dataframe,
            units_map,
            inplace=inplace,
            strict=strict,
        )
        if inplace:
            return self._dataframe
        return output

    def sync_units_map(self, inplace=True):
        output = sync_units_map(self._dataframe, inplace=inplace)
        if inplace:
            return self._dataframe
        return output

    def get_quantity(
        self,
        name,
        unit_name=None,
        to_form=None,
        standardized=False,
        value_type=None,
    ):
        return get_quantity_column(
            self._dataframe,
            name,
            unit_name=unit_name,
            to_form=to_form,
            standardized=standardized,
            value_type=value_type,
        )

    def set_quantity(self, name, quantity_like, to_unit=None, inplace=True):
        output = add_quantity_column(
            self._dataframe,
            name,
            quantity_like,
            to_unit=to_unit,
            inplace=inplace,
        )
        if inplace:
            return self._dataframe
        return output


def _build_accessor_property():
    def _get_accessor(dataframe):
        return _PyUnitWizardDataFrameAccessor(dataframe)

    return property(_get_accessor)


def setup_pandas(enable=True):
    pd = _import_pandas()

    if enable:
        if not hasattr(pd.DataFrame, "puw"):
            pd.DataFrame.puw = _build_accessor_property()
    else:
        if hasattr(pd.DataFrame, "puw"):
            delattr(pd.DataFrame, "puw")


@contextmanager
def pandas_context():
    pd = _import_pandas()
    had_accessor = hasattr(pd.DataFrame, "puw")
    setup_pandas(enable=True)
    try:
        yield
    finally:
        if not had_accessor:
            setup_pandas(enable=False)


__all__ = [
    "UNITS_ATTR_KEY",
    "dataframe_from_quantities",
    "add_quantity_column",
    "get_quantity_column",
    "get_units_map",
    "set_units_map",
    "sync_units_map",
    "concat",
    "merge",
    "setup_pandas",
    "pandas_context",
]
