from ._pyunitwizard import puw


def sum_quantities(a, b, form=None):
    aa = puw.quantity(a, form=form)
    bb = puw.quantity(b, form=form)
    return aa + bb


def get_form(quantity):

    return puw.get_form(quantity)


def libraries_loaded():
    return puw.configure.get_libraries_loaded()
