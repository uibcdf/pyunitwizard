from .is_sequence import is_sequence
from .is_sequence import is_sequence_of_quantities
from .is_quantity_value_sequence import is_quantity_value_sequence
from .concatenate import concatenate
from numpy import ndarray
import numpy as np

def slice(item, indices=None, start=None, stop=None, step=None, to_unit=None, to_form=None, value_type=None,
          standardized=False):

    from pyunitwizard import get_value, change_value, convert, standardize

    if is_quantity_value_sequence(item):

        value = get_value(item)

        if indices is not None:
            if isinstance(value, ndarray):
                value = value[indices]
            elif isinstance(value, list):
                value = [value[ii] for ii in indices]
            elif isinstance(value, tuple):
                value = tuple(value[ii] for ii in indices)
            else:
                raise ValueError('Invalid value type')

        if start is not None or stop is not None or step is not None:
            if isinstance(value, ndarray):
                value = value[start:stop:step]
            elif isinstance(value, list):
                value = value[start:stop:step]
            elif isinstance(value, tuple):
                value = value[start:stop:step]
            else:
                raise ValueError('Invalid value type')

        if value_type is not None:
            if value_type == 'list':
                value = list(value)
            elif value_type == 'tuple':
                value = tuple(value)
            elif value_type == 'ndarray':
                value = np.asarray(value)
            else:
                raise ValueError('Invalid value_type')

        item = change_value(item, value)

    elif is_sequence_of_quantities(item):

        item = concatenate(item)

        return slice(item, indices=indices, start=start, stop=stop, step=step, to_unit=to_unit, to_form=to_form,
                     standardized=False)

    else:

        raise ValueError('Invalid item type')

    if (to_unit is not None) and (to_form is not None):

        item = convert(item, to_unit=to_unit, to_form=to_form)

    elif standardized:
        item = standardize(item)

    return item
