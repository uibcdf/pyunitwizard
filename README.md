# PyUnitWizard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/) 
[![Documentation](https://github.com/uibcdf/PyUnitWizard/actions/workflows/sphinx_docs_to_gh_pages.yaml/badge.svg)](https://github.com/uibcdf/PyUnitWizard/actions/workflows/sphinx_docs_to_gh_pages.yaml)
[![CI](https://github.com/uibcdf/PyUnitWizard/actions/workflows/CI.yaml/badge.svg)](https://github.com/uibcdf/PyUnitWizard/actions/workflows/CI.yaml)
[![codecov](https://codecov.io/github/uibcdf/PyUnitWizard/graph/badge.svg?token=9ZMA4YZLOR)](https://codecov.io/github/uibcdf/PyUnitWizard)
[![Install with conda](https://img.shields.io/badge/Install%20with-conda-brightgreen.svg)](https://conda.anaconda.org/uibcdf/pyunitwizard)
[![Installation on ubuntu-latest](https://github.com/uibcdf/PyUnitWizard/actions/workflows/install_ubuntu_latest.yaml/badge.svg)](https://github.com/uibcdf/PyUnitWizard/actions/workflows/install_ubuntu_latest.yaml)
[![Installation on macos-latest](https://github.com/uibcdf/PyUnitWizard/actions/workflows/install_macos_latest.yaml/badge.svg)](https://github.com/uibcdf/PyUnitWizard/actions/workflows/install_macos_latest.yaml)


There are several Python libraries to work with physical quantities in the
market, such as pint, unyt or openmm.unit. Imagine that your project or
workflow requires the interaction with more than one of these tools, or that
you are not sure if you will work with a different quantities library in the
future. Wouldn't having a unique API to work with different forms of physical
quantities be a relief? PyUnitWizard just does that. It is the wizard you need
in your code to change the form of your quantities with no effort.

## Example

```ipython
In [1]: import pyunitwizard as puw

In [2]: puw.configure.load_libraries(['pint', 'openmm.unit'])
   ...: puw.configure.set_default_form('pint')
   ...: puw.configure.set_standard_units(['nm', 'ps', 'kcal', 'mole'])
   ...: 

In [3]: q = puw.quantity(2.5, 'nanometers/picoseconds')

In [4]: puw.get_form(q)
Out[4]: 'pint'

In [5]: puw.get_value(q)
Out[5]: 2.5

In [6]: puw.get_unit(q)
Out[6]: <Unit('nanometer / picosecond')>

In [7]: puw.dimensionality(q)
Out[7]: {'[L]': 1, '[M]': 0, '[T]': -1, '[K]': 0, '[mol]': 0, '[A]': 0, '[Cd]': 0}

In [8]: q2 = puw.convert(q, to_unit='angstroms/femtoseconds', to_form='openmm.unit')

In [9]: print(q2)
0.025000000000000005 A/fs

In [10]: puw.get_form(q2)
Out[10]: 'openmm.unit'

In [11]: puw.compatibility(q, q2)
Out[11]: True

In [12]: q3 = puw.standardize(q2)

In [13]: print('q3 is now a {} quantity expressed in {}.'.format(puw.get_form(q3), puw.get_unit(q3)))
q3 is now a pint quantity expressed in nanometer / picosecond.
```

## Units Python libraries
- [openmm.unit](https://github.com/openmm/openmm/tree/master/wrappers/python/simtk/unit)
- [Pint](https://pint.readthedocs.io/en/stable/)
- [unyt](https://unyt.readthedocs.io/en/stable/)
- [astropy.units](https://docs.astropy.org/en/stable/units/)

## License

This project is under an MIT License. [A copy of the license text is included in this repository](LICENSE).

## smonitor

PyUnitWizard loads smonitor configuration from `_smonitor.py` in the package root
(`pyunitwizard/_smonitor.py`) to provide structured diagnostics. The catalog and
metadata live in `pyunitwizard/_private/smonitor/catalog.py` and
`pyunitwizard/_private/smonitor/meta.py` (docs/issues/API URLs used in hints).

### Copyright

Copyright (c) 2021-2022 [The Mexico Children's Hospital Federico Gómez](http://himfg.com.mx/), [its Unit of Research on Computational
Biology and Drug Design](http://uibcdf.org), and [authors](https://github.com/uibcdf/pyunitwizard/graphs/contributors).

## Acknowledgements

Project based on the [Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.5.

## Contributors

A complete list of contributors can be found checking [the insights section of this
repository](https://github.com/uibcdf/pyunitwizard/graphs/contributors).

The main project authors and contributors are:

- Daniel Ibarrola Sánchez
- Liliana M. Moreno Vargas
- Diego Prada Gracia
