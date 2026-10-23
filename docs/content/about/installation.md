# Installation

Published PyUnitWizard packages are available from the `uibcdf` Conda
channel. The current published release, 0.28.1, supports Python 3.11–3.14 on Linux and macOS
Apple Silicon (arm64). Intel macOS is outside the supported matrix; see
[the suite support decision](https://github.com/uibcdf/molsyssuite/issues/59)
for reconsideration based on concrete user demand.
Use the supported Conda route below to provision the required dependencies.

## Basic installation

```bash
conda install -c uibcdf -c conda-forge 'pyunitwizard>=0.28.1'
```

For a source installation, first create a Conda environment with the required
public dependencies:

```bash
conda create -n pyunitwizard-source -c uibcdf -c conda-forge python=3.14 \
  'smonitor>=0.16.0' 'depdigest>=0.11.0' 'argdigest>=0.14.0' numpy pint pip
conda activate pyunitwizard-source
```

Then install the released source tag without asking pip to resolve those
Conda-provided dependencies from PyPI:

```bash
python -m pip install --no-deps 'git+https://github.com/uibcdf/pyunitwizard.git@0.28.1'
```

## Install from source

For development, activate the dependency environment above before installing an
editable checkout. This follows the current branch rather than the released tag:

```bash
git clone https://github.com/uibcdf/pyunitwizard.git
cd pyunitwizard
python -m pip install --no-deps -e .
```

Check `python -m pip check` and the imported module's location after installation.
Optional backends are not required for basic Pint use; consult the
[compatibility matrix](../developer/compatibility-matrix.md) for qualified
OpenFF, CF/HDF5 and attribution profiles. Installing from source does not
requalify the published Conda file.
