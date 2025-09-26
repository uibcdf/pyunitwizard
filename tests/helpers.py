from contextlib import contextmanager

import pyunitwizard as puw


@contextmanager
def loaded_libraries(libraries):
    """Temporarily load the requested libraries for a test case."""
    previous_libraries = list(puw.configure.get_libraries_loaded())
    previous_default_form = puw.configure.get_default_form()
    previous_default_parser = puw.configure.get_default_parser()

    puw.configure.reset()
    puw.configure.load_library(libraries)
    try:
        yield
    finally:
        puw.configure.reset()
        if previous_libraries:
            puw.configure.load_library(previous_libraries)
        else:
            for library in ['pint', 'openmm.unit', 'unyt']:
                try:
                    puw.configure.load_library(library)
                except Exception:
                    continue
        if previous_default_form is not None:
            puw.configure.set_default_form(previous_default_form)
        if previous_default_parser is not None:
            puw.configure.set_default_parser(previous_default_parser)
