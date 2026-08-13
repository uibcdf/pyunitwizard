from testlib2 import _puw


def sum_quantities(a="3m", b="7m", form=None):
    aa = _puw.quantity(a, form=form)
    bb = _puw.quantity(b, form=form)
    return aa + bb


def get_form(quantity):

    return _puw.get_form(quantity)


def libraries_loaded():
    return _puw.configure.get_libraries_loaded()
