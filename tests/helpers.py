from contextlib import contextmanager

import pyunitwizard as puw


@contextmanager
def loaded_libraries(libraries):
    """
    Context manager to temporarily load the requested libraries for a test case.

    Parameters
    ----------
    libraries : list of str
        List of library names to load temporarily for the duration of the context.

    Behavior
    --------
    - Saves the current loaded libraries, default form, and default parser.
    - Resets the configuration and loads the specified libraries.
    - After the context, restores the previous configuration.
    - If no previous libraries were loaded, attempts to load a default set
      ('pint', 'openmm.unit', 'unyt'), ignoring failures.

    Exceptions
    ----------
    - Any exception raised by `puw.configure.load_library` when loading the requested libraries
      will propagate unless caught internally.
    - Exceptions when loading default libraries after the context are caught and ignored.
    """
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
                except (ImportError, ModuleNotFoundError):
                    continue
        if previous_default_form is not None:
            puw.configure.set_default_form(previous_default_form)
        if previous_default_parser is not None:
            puw.configure.set_default_parser(previous_default_parser)
