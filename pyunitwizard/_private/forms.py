from pyunitwizard import kernel

forms = ['openmm.unit', 'pint', 'unyt', 'astropy.units', 'physipy', 'quantities', 'string']

_LOADING = False


def digest_form(form: str) -> str:
    """Check if the form is correct and dynamically load the backend on-demand."""
    global _LOADING
    if form is None:
        form_name = kernel.default_form
        if form_name is None:
            # Probe for the first available installed form to set as default on-the-fly
            from depdigest import is_installed
            for candidate in ['pint', 'openmm.unit', 'unyt', 'astropy.units', 'physipy', 'quantities']:
                if is_installed(candidate):
                    form_name = candidate
                    break
    elif form.lower() in forms:
        form_name = form.lower()
    else:
        raise ValueError

    # Dynamic on-demand lazy library loading with re-entrancy guard
    if form_name is not None and form_name != 'string':
        if form_name not in kernel.loaded_libraries and not _LOADING:
            _LOADING = True
            try:
                from pyunitwizard.configure import load_library
                load_library(form_name)
            finally:
                _LOADING = False

    return form_name


def digest_to_form(to_form: str, from_form: str = None) -> str:
    """Check if the target form is correct.

    Parameters
    ----------
    to_form : str
        The form the unit will be converted.
    from_form : str, optional
        The original form of the unit.

    Returns
    -------
    str
        The target form of the unit.
    """
    if to_form is not None:
        return digest_form(to_form)
    else:
        if from_form == 'string':
            from_form = None
        return digest_form(from_form)
