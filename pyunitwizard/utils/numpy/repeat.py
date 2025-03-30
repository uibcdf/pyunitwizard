import numpy as np
from pyunitwizard import quantity, get_unit, get_value

def repeat(sequence, repeats, axis=None, to_unit=None, to_form=None, value_type=None, standardized=False):

    if to_unit is None:
        output_unit = get_unit(sequence)
    else:
        output_unit = to_unit

    output_value = get_value(sequence)

    output_value = np.repeat(output_value, repeats, axis=axis)

    if value_type=='list':
        return quantity(output_value.tolist(), output_unit, form=to_form, standardized=standardized)
    elif value_type=='tuple':
        return quantity(tuple(output_value.tolist()), output_unit, form=to_form, standardized=standardized)
    elif value_type=='numpy.ndarray':
        return quantity(output_value, output_unit, form=to_form, standardized=standardized)
    elif value_type is None:
        return quantity(output_value, output_unit, form=to_form, standardized=standardized)
    else:
        raise ValueError

