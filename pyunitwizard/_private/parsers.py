parsers = ['openmm.unit', 'pint', 'unyt', 'astropy.units']

def digest_parser(parser: str) -> str:
    """ Check if parser is correct."""
    if parser is not None:
        if parser.lower() in parsers:
            return parser.lower()
        else:
            raise ValueError
    else:
        from pyunitwizard.kernel import default_parser
        return default_parser

