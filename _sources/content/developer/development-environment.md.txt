# Development Environment

For routine Linux work, use the qualified `molsyssuite@uibcdf_3.14` Conda
environment and install participating local clones with
`python -m pip install --no-deps --editable PATH`. Follow the suite's
[development workspace contract](https://github.com/uibcdf/molsyssuite/blob/main/devguide/development_workspace.md)
for the canonical recipe, bootstrap and current eligibility. Check Python,
editable import origins and `python -m pip check`; report existing environment
conflicts separately from test results. The shared environment's outstanding
dependency conflicts are tracked in
[MolSysSuite #82](https://github.com/uibcdf/molsyssuite/issues/82).

For a standalone environment, use the repository's Conda profiles below.

## Recommended environments

- `development_env.yaml`: core development tasks.
- `test_env.yaml`: test execution.
- `docs_env.yaml`: Sphinx and notebook documentation.
- `release_gates_env.yaml`: release-gate parity checks.

## Typical setup

```bash
# From the repository root; this profile selects Python 3.14.
conda env create --name pyunitwizard-dev --file devtools/conda-envs/development_env.yaml
conda activate pyunitwizard-dev
python -m pip install --no-deps --editable .
python --version
python -m pip check
```

## Local validation baseline

```bash
python -m pytest --receptor=llm tests
make -C docs html
```

The full supported matrix remains Python 3.11–3.14; a local Python 3.14 run
does not qualify another interpreter, platform or installed release artifact.

The development, test and release-gate profiles pin public Ackredit 0.9.0
`py_0` to exercise the optional Pint/unyt attribution pilot. Ackredit remains
optional for normal package use. Fresh-process absence tests run with the
provider blocked, and provisional function-observer tests skip when that
capability is unavailable in the public release.

Run `python devtools/benchmark_backend_attribution.py` with PyUnitWizard
installed in the environment to measure the warmed attribution cost. The
tool retains all seven samples per case and reports whether function
observation is available. Public 0.9.0 measures the portable backend paths;
development providers exposing the observer also measure function attribution.
Timing does not include imports, activation or first registration.

The prepared-provider path reuses immutable backend declaration plans only
while software versions and bibliographic values still match. Nested metadata
edits invalidate the plan; every completed credit continues to call the
provider, including its registry conflict checks and independent captures.
Public 0.9.0 retains the portable registration/tracking path. Compare paired
normally installed producer wheels with identical scientific/provider inputs
and retain raw samples; a source profile locates allocations but does not
establish timing improvement. This optimization does not change the optional
provider minimum or promote the provisional APIs.
