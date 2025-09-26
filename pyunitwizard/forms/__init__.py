from importlib import import_module as _import_module

dict_is_form={} 
# These dictionaries contain functions for each of the libraries loaded.
# For instance, if loaded libraries are pint an openmm.unit dict_is_unit
# will be {'pint' : puw.api_pint.is_unit, 'openmm.unit': puw.api_openmm.is_unit}
dict_is_unit={}
dict_is_quantity={}
dict_get_value={}
dict_get_unit={}
dict_change_value={}
dict_make_quantity={}
dict_translate_quantity={} # This contains a sub-dictionary for each loaded library. Contains functions such as to_pint
dict_translate_unit={} # This contains a sub-dictionary for each loaded library. Contains functions such as to_pint
dict_convert={}
dict_dimensionality={}
dict_compatibility={}

_base_package = __name__.replace('.base','')
_forms_apis_modules = {
    'openmm.unit': 'api_openmm_unit',
    'pint': 'api_pint',
    'unyt': 'api_unyt',
    'astropy.units': 'api_astropy_unit',
}

def load_library(library: str) -> None:
    """ Loads a library. This means that it updates all dictionaries defined above
        with their respective values for the library.

        Parameters
        ----------
        library : str
            Name of the libraries.
    """
    from pyunitwizard.kernel import loaded_libraries, loaded_parsers
    api = _import_module('.'+_forms_apis_modules[library], _base_package)

    dict_is_form[library] = api.is_form
    dict_is_unit[library] = api.is_unit
    dict_is_quantity[library] = api.is_quantity
    dict_get_value[library] = api.get_value
    dict_get_unit[library] = api.get_unit
    dict_change_value[library] = api.change_value
    dict_make_quantity[library] = api.make_quantity
    dict_convert[library] = api.convert
    dict_translate_quantity[library] = {}
    dict_translate_unit[library] = {}
    dict_dimensionality[library] = api.dimensionality
    dict_compatibility[library] = api.compatibility

    dict_translate_quantity[library]['string'] = api.quantity_to_string
    dict_translate_unit[library]['string'] = api.unit_to_string
    api_string = _import_module('.api_string', _base_package)
    dict_translate_quantity['string'][library]= getattr(api_string, 'quantity_to_'+library.replace('.','_'))
    dict_translate_unit['string'][library]= getattr(api_string, 'unit_to_'+library.replace('.','_'))
    del(api_string)

    for method in api.__dict__.keys():
        if method.startswith('quantity_to_'):
            out_form = method.replace('quantity_to_','').replace('_','.')
            if out_form in loaded_libraries:
                dict_translate_quantity[library][out_form] = getattr(api, method)
        if method.startswith('unit_to_'):
            out_form = method.replace('unit_to_','').replace('_','.')
            if out_form in loaded_libraries:
                dict_translate_unit[library][out_form] = getattr(api, method)

    if api.parser:
        loaded_parsers.append(library)

    for library_loaded in loaded_libraries:
        api = _import_module('.'+_forms_apis_modules[library_loaded], _base_package)
        for method in api.__dict__.keys():
            if method.startswith('quantity_to_'):
                out_form=method.replace('quantity_to_','').replace('_','.')
                if out_form == library:
                    dict_translate_quantity[library_loaded][library]= getattr(api, method)
                    break
        for method in api.__dict__.keys():
            if method.startswith('unit_to_'):
                out_form=method.replace('unit_to_','').replace('_','.')
                if out_form == library:
                    dict_translate_unit[library_loaded][library]= getattr(api, method)
                    break

    loaded_libraries.append(library)
    del(api)

    pass

# Load the string api.

api = _import_module('.api_string', _base_package)

dict_is_form['string'] = api.is_form
dict_is_unit['string'] = api.is_unit
dict_is_quantity['string'] = api.is_quantity
dict_get_value['string'] = api.get_value
dict_get_unit['string'] = api.get_unit
dict_change_value['string'] = api.change_value
dict_make_quantity['string'] = api.make_quantity
dict_convert['string'] = api.convert
dict_translate_quantity['string']={}
dict_translate_unit['string']={}
dict_dimensionality['string'] = api.dimensionality
dict_compatibility['string'] = api.compatibility

del(api)

