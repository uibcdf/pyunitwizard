# Devtools guide

This directory contains the Conda recipes and environment definitions used to
build, test, document, and develop PyUnitWizard.

## Files and scope

- `conda-build/meta.yaml`: Conda package recipe.
- `conda-envs/setup_env.yaml`: minimal setup/build helpers.
- `conda-envs/production_env.yaml`: runtime dependencies only.
- `conda-envs/test_env.yaml`: test dependencies.
- `conda-envs/docs_env.yaml`: documentation dependencies.
- `conda-envs/development_env.yaml`: full development environment.

The supported Python range is `>=3.11,<3.14` across all environments.

## Channels

Environment files use:

1. `uibcdf`
2. `conda-forge`

`uibcdf` is required because runtime dependencies such as `smonitor` and
`depdigest` are published there.

## Common commands

Create an environment from any profile:

```bash
micromamba create -n puw-dev -f devtools/conda-envs/development_env.yaml
```

Update an existing environment:

```bash
micromamba env update -n puw-dev -f devtools/conda-envs/development_env.yaml
```

Build the Conda package locally:

```bash
micromamba create -n puw-build -f devtools/conda-envs/build_env.yaml
micromamba run -n puw-build conda build devtools/conda-build
```

## Maintenance rules

- Keep `devtools/conda-build/meta.yaml` and `conda-envs/*.yaml` consistent.
- If runtime dependencies change in `pyproject.toml`, mirror them in:
  - `meta.yaml` `requirements.run`
  - `production_env.yaml`
  - any env profiles that run tests/docs requiring those packages.
- Prefer small, explicit edits to YAML files; avoid hidden generation steps.
