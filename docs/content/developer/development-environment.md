# Development Environment

Use conda environments from `devtools/conda-envs`.

## Recommended environments

- `development_env.yaml`: core development tasks.
- `test_env.yaml`: test execution.
- `docs_env.yaml`: Sphinx and notebook documentation.
- `release_gates_env.yaml`: release-gate parity checks.

## Typical setup

```bash
cd devtools/conda-envs
python create_conda_env.py -n pyunitwizard-dev -p 3.14 development_env.yaml
conda activate pyunitwizard-dev
```

## Local validation baseline

```bash
python -m pytest --receptor=llm tests
make -C docs html
```

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
