from ._private.exceptions import *
from ._private.forms import digest_to_form
from ._private.parsers import digest_parser
from .forms import dict_translate_quantity
import ast
from typing import Optional

def _find_closing_bracket_position(string):
    stack = 0
    for i, char in enumerate(string):
        if char == '[':
            stack += 1
        elif char == ']':
            stack -= 1
            if stack == 0:
                return i
    raise ValueError  # If there is no closing bracket

def _find_closing_parenthesis_position(string):
    stack = 0
    for i, char in enumerate(string):
        if char == '(':
            stack += 1
        elif char == ')':
            stack -= 1
            if stack == 0:
                return i
    raise ValueError  # If there is no closing parenthesis

def _parse_with_pint(string: str):
    """ Parses a string and returns a pint quantity.

        Parameters
        ----------
        string : str
            A string quantity.
        
        Returns
        -------
        pint.quantity
            A pint quantity.
    """
    # Check if it's a non scalar quantity
    if string.startswith('['):

        end_list = _find_closing_bracket_position(string)
        value_string = string[:(end_list+1)]
        unit_string = string[(end_list+1):]

        return ast.literal_eval(value_string)*dict_translate_quantity['string']['pint'](unit_string)

    elif string.startswith('('):

        end_list = _find_closing_parenthesis_position(string)
        value_string = string[:(end_list+1)]
        unit_string = string[(end_list+1):]

        return ast.literal_eval(value_string)*dict_translate_quantity['string']['pint'](unit_string)

    else:
       return dict_translate_quantity['string']['pint'](string)

def parse(string: str, parser: Optional[str]=None, to_form: Optional[str]=None):
    """ Parses a string and returns a quantity.

        Parameters
        ----------
        string : str
            A string quantity.
        
        parser : str
            The parser that will be used.

        to_form; str, optional
            The form of the quantity. Can be "pint", "openmm.unit",
            "unyt", "astropy.units" or "string".

        Returns
        -------
        QuantityLike
            A quantity.
    """
    if not isinstance(string, str):
        raise BadCallError('string')

    parser = digest_parser(parser)
    to_form = digest_to_form(to_form)

    if parser == 'pint':
        if to_form == 'pint':
            return _parse_with_pint(string)

        elif to_form == 'openmm.unit':
            pint_quantity = _parse_with_pint(string)
            return dict_translate_quantity['pint']['openmm.unit'](pint_quantity)

        elif to_form == 'string':
            pint_quantity = _parse_with_pint(string)
            return dict_translate_quantity['pint']['string'](pint_quantity)

        elif to_form == 'unyt':
            pint_quantity = _parse_with_pint(string)
            return dict_translate_quantity['pint']['unyt'](pint_quantity)

        elif to_form == 'astropy.units':
            pint_quantity = _parse_with_pint(string)
            return dict_translate_quantity['pint']['astropy.units'](pint_quantity)

        else:
            raise NotImplementedParserError(parser, to_form)

    elif parser == 'openmm.unit':
        raise LibraryWithoutParserError('openmm.unit')
    elif parser == 'unyt':
        raise LibraryWithoutParserError("unyt")
    elif parser == 'astropy.units':
        astropy_quantity = dict_translate_quantity['string']['astropy.units'](string)

        if to_form == 'astropy.units':
            return astropy_quantity
        elif to_form == 'pint':
            return dict_translate_quantity['astropy.units']['pint'](astropy_quantity)
        elif to_form == 'string':
            return dict_translate_quantity['astropy.units']['string'](astropy_quantity)
        elif to_form == 'openmm.unit':
            return dict_translate_quantity['astropy.units']['openmm.unit'](astropy_quantity)
        elif to_form == 'unyt':
            return dict_translate_quantity['astropy.units']['unyt'](astropy_quantity)
        else:
            raise NotImplementedParserError(parser, to_form)
    else:
        raise NotImplementedParserError(parser, to_form)
