# Matplotlib Interoperability

Visualization is one of the most common places where units break.

Typical issues:

- quantities cannot be plotted
- units are stripped silently
- axis labels lose unit information

PyUnitWizard should allow plotting of any supported quantity type.

Example:

import pyunitwizard as puw

x = puw.quantity([0,1,2], 'nm')
y = puw.quantity([1,4,9], 'kcal/mol')

puw.plot(x, y)

Expected behavior:

• numerical values extracted automatically
• axes labeled with units
• dimensional mismatches detected
