from pyunitwizard import kernel

forms = ['openmm.unit', 'pint', 'unyt', 'astropy.units', 'string']

def digest_form(form: str) -> str:
    """ Check if the form is correct. 

        Parameters
        ----------
        form: str
            The form of the unit
        
        Returns
        -------
        str
            The form of the unit.
    """
    if form is None:
        return kernel.default_form
    elif form.lower() in forms:
        return form.lower()
    else:
        raise ValueError

def digest_to_form(to_form: str, from_form: str=None) -> str:
    """ Check if the form is correct. 

        Parameters
        ----------
        to_form: str
            The form the unit will be converted.

        from_form : str, optional
            The original form of the unit.
        
        Returns
        -------
        str
            The form of the unit.
    """
    if to_form is not None:
        return digest_form(to_form)
    else:
        if from_form == 'string':
            from_form = None
        return digest_form(from_form)

