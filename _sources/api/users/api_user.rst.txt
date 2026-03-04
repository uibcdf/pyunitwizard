Users API
=========

This reference covers the public runtime API used by scientific users and
library integrators.

Core Construction
-----------------

.. autosummary::
   :toctree: autosummary

   pyunitwizard.quantity
   pyunitwizard.unit

Core Conversion and Display
---------------------------

.. autosummary::
   :toctree: autosummary

   pyunitwizard.convert
   pyunitwizard.to_string

Core Validation and Comparison
------------------------------

.. autosummary::
   :toctree: autosummary

   pyunitwizard.check
   pyunitwizard.compatibility
   pyunitwizard.are_compatible
   pyunitwizard.similarity
   pyunitwizard.are_close
   pyunitwizard.are_equal

Core Introspection and Extraction
---------------------------------

.. autosummary::
   :toctree: autosummary

   pyunitwizard.get_form
   pyunitwizard.is_quantity
   pyunitwizard.is_unit
   pyunitwizard.get_dimensionality
   pyunitwizard.is_dimensionless
   pyunitwizard.get_value
   pyunitwizard.get_unit
   pyunitwizard.get_value_and_unit
   pyunitwizard.change_value

Standardization and Context
---------------------------

.. autosummary::
   :toctree: autosummary

   pyunitwizard.get_standard_units
   pyunitwizard.standardize
   pyunitwizard.context

Runtime Configuration
---------------------

.. autosummary::
   :toctree: autosummary

   pyunitwizard.configure.reset
   pyunitwizard.configure.load_library
   pyunitwizard.configure.get_libraries_loaded
   pyunitwizard.configure.get_libraries_supported
   pyunitwizard.configure.get_parsers_loaded
   pyunitwizard.configure.get_parsers_supported
   pyunitwizard.configure.get_default_form
   pyunitwizard.configure.set_default_form
   pyunitwizard.configure.get_default_parser
   pyunitwizard.configure.set_default_parser
   pyunitwizard.configure.get_standard_units
   pyunitwizard.configure.set_standard_units
