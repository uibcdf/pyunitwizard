def initialize() -> None:
    """Initialize global runtime state containers.

    Returns
    -------
    None
        Global runtime variables are reset in place.

    Examples
    --------
    >>> import pyunitwizard.kernel as kernel
    >>> kernel.initialize()
    """

    global loaded_libraries
    global loaded_parsers
    global default_form
    global default_parser
    global standards
    global dimensional_fundamental_standards
    global dimensional_combinations_standards
    global adimensional_standards
    global tentative_base_standards
    global dimensional_fundamental_standards_matrix
    global dimensional_fundamental_standards_units
    global tentative_base_standards_matrix
    global tentative_base_standards_units
    global standard_units_by_dimensionality_cache

    loaded_libraries = []
    loaded_parsers = []
    default_form = None
    default_parser = None
    standards = {}
    dimensional_fundamental_standards = {}
    dimensional_combinations_standards = {}
    adimensional_standards = {}
    tentative_base_standards = {}
    dimensional_fundamental_standards_matrix = None
    dimensional_fundamental_standards_units = None
    tentative_base_standards_matrix = None
    tentative_base_standards_units = None
    standard_units_by_dimensionality_cache = {}


order_fundamental_units = ['[L]', '[M]', '[T]', '[K]', '[mol]', '[A]', '[Cd]']
