import threading
from importlib import import_module as _import_module

#: Serializes construction of the dispatch dictionaries below. Reentrant because
#: `load_library` imports adapter modules that can re-enter it.
_REGISTRY_LOCK = threading.RLock()


def ensure_library(library: str) -> None:
    """Guarantees `library` is usable before a reader touches the registry.

    The registry has three states -- absent, half-built and ready -- and a reader cannot
    tell them apart. `dict_translate_quantity['string']` is created when this module is
    imported, but `['string']['pint']` only exists once `load_library('pint')` has run, so
    between those two moments the package is importable and unusable with nothing marking
    the difference.

    That gap is reachable from two threads. Two top-level packages that both configure
    PyUnitWizard have two different import locks, so nothing serializes them: the loser
    finds `pyunitwizard` already in `sys.modules`, put there by the winner, and proceeds as
    though the package were configured. It then reads `dict_translate_quantity['string']`
    without `'pint'` in it (uibcdf/PyUnitWizard#70).

    So whoever needs a form asks for it here. The first caller builds it; every other
    caller blocks on the lock until that build has finished, instead of reading a registry
    someone else is still filling.
    """
    from pyunitwizard.kernel import loaded_libraries

    if library in loaded_libraries:
        return
    with _REGISTRY_LOCK:
        if library in loaded_libraries:  # settled while we waited for the lock
            return
        load_library(library)

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
    'physipy': 'api_physipy',
    'quantities': 'api_quantities',
}

def load_library(library: str) -> None:
    """ Loads a library. This means that it updates all dictionaries defined above
        with their respective values for the library.

        Parameters
        ----------
        library : str
            Name of the library backend to load.

        Returns
        -------
        None
            Internal forms dispatch dictionaries are updated in place.
    """
    with _REGISTRY_LOCK:
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

        # Build missing direct translators through Pint as an interoperability hub.
        # This keeps cross-library conversions available when adapters only define
        # `to_pint` / `from_pint` pairs.
        for in_form in list(loaded_libraries):
            for out_form in list(loaded_libraries):
                if in_form == out_form:
                    continue

                if out_form not in dict_translate_quantity.get(in_form, {}):
                    if (
                        in_form != 'pint'
                        and 'pint' in dict_translate_quantity.get(in_form, {})
                        and out_form in dict_translate_quantity.get('pint', {})
                    ):
                        def _qty_bridge(x, _in=in_form, _out=out_form):
                            return dict_translate_quantity['pint'][_out](
                                dict_translate_quantity[_in]['pint'](x)
                            )

                        dict_translate_quantity[in_form][out_form] = _qty_bridge

                if out_form not in dict_translate_unit.get(in_form, {}):
                    if (
                        in_form != 'pint'
                        and 'pint' in dict_translate_unit.get(in_form, {})
                        and out_form in dict_translate_unit.get('pint', {})
                    ):
                        def _unit_bridge(x, _in=in_form, _out=out_form):
                            return dict_translate_unit['pint'][_out](
                                dict_translate_unit[_in]['pint'](x)
                            )

                        dict_translate_unit[in_form][out_form] = _unit_bridge

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
