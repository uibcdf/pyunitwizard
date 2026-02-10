def initialize() -> None:

    global loaded_libraries
    global loaded_parsers
    global default_form
    global default_parser
    global standards
    global dimensional_fundamental_standards
    global dimensional_combinations_standards
    global adimensional_standards
    global tentative_base_standards

    loaded_libraries = []
    loaded_parsers = []
    default_form = None
    default_parser = None
    standards = {}
    dimensional_fundamental_standards = {}
    dimensional_combinations_standards = {}
    adimensional_standards = {}
    tentative_base_standards = {}


order_fundamental_units = ['[L]', '[M]', '[T]', '[K]', '[mol]', '[A]', '[Cd]']

