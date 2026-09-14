import unyt as unyt

form_name = "unyt"
parser = False

is_form = {}


def is_quantity(quantity_or_unit):

    raise NotImplementedError


def is_unit(quantity_or_unit):

    raise NotImplementedError


def dimensionality(quantity_or_unit):

    raise NotImplementedError


def compatibility(quantity_or_unit_1, quantity_or_unit_2):

    raise NotImplementedError


def make_quantity(value, unit_name):

    raise NotImplementedError


def string_to_quantity(string):

    raise NotImplementedError


def to_string(unit):

    raise NotImplementedError


def convert(quantity, unit_name):

    raise NotImplementedError


def get_value(quantity):

    raise NotImplementedError


def get_unit(quantity):

    raise NotImplementedError
