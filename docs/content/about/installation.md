# Installation

Published PyUnitWizard packages are available from the `uibcdf` Conda
channel. Version 0.26.0 and later support Python 3.11–3.14 on Linux and macOS.
The public PyPI index does not currently distribute PyUnitWizard, SMonitor,
or DepDigest.

## Basic installation

```bash
conda install -c uibcdf 'pyunitwizard>=0.26.0'
```

For a source installation, first create a Conda environment with the required
public dependencies:

```bash
conda create -n pyunitwizard-source -c uibcdf -c conda-forge python=3.14 \
  'smonitor>=0.16.0' 'depdigest>=0.11.0' numpy pint pip
conda activate pyunitwizard-source
```

Then install the released source tag without asking pip to resolve those
Conda-provided dependencies from PyPI:

```bash
python -m pip install --no-deps 'git+https://github.com/uibcdf/pyunitwizard.git@0.26.0'
```

## Install from source

```bash
git clone https://github.com/uibcdf/pyunitwizard.git
cd pyunitwizard
python -m pip install --no-deps -e .
```
