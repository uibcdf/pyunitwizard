import numpy as np

from pyunitwizard import get_unit, get_value, quantity


def concatenate(sequence, to_unit=None, to_form=None, value_type="tuple", standardized=False):

    sequence_of_sequences = False

    if isinstance(sequence, (list, tuple, np.ndarray)):
        if isinstance(sequence[0], (list, tuple, np.ndarray)):
            sequence_of_sequences = True

    if not sequence_of_sequences:
        if to_unit is None:
            output_unit = get_unit(sequence[0])
        else:
            output_unit = to_unit

        output_value = []

        for aux_quantity in sequence:
            output_value.append(get_value(aux_quantity, to_unit=output_unit))

        if value_type == "list":
            return quantity(output_value, output_unit, form=to_form, standardized=standardized)
        elif value_type == "tuple":
            return quantity(tuple(output_value), output_unit, form=to_form, standardized=standardized)
        elif value_type == "numpy.ndarray":
            return quantity(np.array(output_value), output_unit, form=to_form, standardized=standardized)
        else:
            raise ValueError

    else:
        if to_unit is None:
            output_unit = get_unit(sequence[0][0])
        else:
            output_unit = to_unit

        output_value = []

        for aux_seq in sequence:
            for aux_quantity in aux_seq:
                output_value.append(get_value(aux_quantity, to_unit=output_unit))

        if value_type == "list":
            return quantity(output_value, output_unit, form=to_form, standardized=standardized)
        elif value_type == "tuple":
            return quantity(tuple(output_value), output_unit, form=to_form, standardized=standardized)
        elif value_type == "numpy.ndarray":
            return quantity(np.array(output_value), output_unit, form=to_form, standardized=standardized)
        else:
            raise ValueError
