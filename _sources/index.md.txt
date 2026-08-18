```{eval-rst}
:html_theme.sidebar_secondary.remove:
```

:::{figure} _static/logo.svg
:width: 50%
:align: center

A Python Units Wizard that streamlines work with physical quantities.

```{image} https://img.shields.io/github/v/release/uibcdf/pyunitwizard?color=white&label=release
:target: https://github.com/uibcdf/pyunitwizard/releases
```
```{image} https://img.shields.io/badge/license-MIT-white.svg
:target: https://github.com/uibcdf/pyunitwizard/blob/main/LICENSE
```
```{image} https://img.shields.io/badge/install%20with-conda-white.svg
:target: https://anaconda.org/uibcdf/pyunitwizard
```
```{image} https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-white.svg
:target: https://www.python.org/downloads/
```
:::

## Install it

```bash
conda install -c uibcdf pyunitwizard
```

## Use it

PyUnitWizard provides a unified API to work with physical quantities across
different unit libraries (for example Pint, unyt, OpenMM units, Astropy units,
physipy, and quantities).

```python
import pyunitwizard as puw

puw.configure.load_library(["pint"])
distance = puw.quantity(1.0, "nanometer")
distance_in_angstrom = puw.convert(distance, to_unit="angstrom")
print(puw.to_string(distance_in_angstrom))
```

What happens here:
- quantities are constructed with one public API;
- conversion is delegated to the configured backend;
- output can be normalized for downstream interoperability.

## Why adopt now

- Reduce integration friction when users pass quantities from different unit backends.
- Make boundary-level unit checks explicit and reproducible in scientific workflows.
- Keep downstream interoperability stable through consistent conversion and standardization.

## Ecosystem proof

PyUnitWizard is part of the current UIBCDF interoperability stack:
- [ArgDigest](https://github.com/uibcdf/argdigest)
- [DepDigest](https://github.com/uibcdf/depdigest)
- [SMonitor](https://github.com/uibcdf/smonitor)

Start with the [User Guide](content/user/index.md) and then continue with
the [Developer Guide](content/developer/index.md) if you are contributing to
PyUnitWizard itself.

```{eval-rst}

.. toctree::
   :maxdepth: 2
   :hidden:

   content/about/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   content/showcase/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   content/user/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   content/developer/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   api/index.md

```
