from pyunitwizard.api import get_value, is_quantity
from .is_sequence import is_sequence

def is_quantity_value_sequence(item):
    """Check if an item is a quantity whose value is a sequence."""
    return is_quantity(item) and is_sequence(get_value(item))

