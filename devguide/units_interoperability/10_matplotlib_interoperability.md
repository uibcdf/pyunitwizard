# Matplotlib Interoperability

Visualization is one of the most common places where units break.

Typical issues:

- quantities cannot be plotted
- units are stripped silently
- axis labels lose unit information

PyUnitWizard provides a transparent matplotlib bridge through:

- `pyunitwizard.utils.matplotlib.setup_matplotlib(enable=True)`
- `pyunitwizard.utils.matplotlib.plotting_context()`

Example:

import pyunitwizard as puw

x = puw.quantity([0,1,2], 'nm')
y = puw.quantity([1,4,9], 'kcal/mol')

puw.utils.matplotlib.setup_matplotlib(enable=True)

Expected behavior:

- numerical values extracted automatically
- axes labeled with units
- dimensional mismatches detected

Contract tests:
- baseline bridge behavior: `tests/utils/matplotlib/test_units_bridge.py`
- advanced layouts: `tests/utils/matplotlib/test_complex_layouts.py`
