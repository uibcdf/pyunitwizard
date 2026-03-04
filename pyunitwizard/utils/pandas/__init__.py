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
