import numpy as np
from pyunitwizard import quantity, get_unit, get_value

def column_stack(sequence, to_unit=None, to_form=None, value_type='tuple', standardized=False):

    if to_unit is None:
        output_unit = get_unit(sequence[0][0])
    else:
        output_unit = to_unit

    output_value = []

    for aux_seq in sequence:
        aux_list = []
        for aux_quantity in aux_seq:
            aux_list.append(get_value(aux_quantity, to_unit=output_unit))
        output_value.append(aux_list)

    output_value = np.column_stack(output_value)

    if value_type=='list':
        return quantity(output_value.tolist(), output_unit, form=to_form, standardized=standardized)
    elif value_type=='tuple':
        return quantity(tuple(output_value.tolist()), output_unit, form=to_form, standardized=standardized)
    elif value_type=='numpy.ndarray':
        return quantity(output_value, output_unit, form=to_form, standardized=standardized)
    else:
        raise ValueError

