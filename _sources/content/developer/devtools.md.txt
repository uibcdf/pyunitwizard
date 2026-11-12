# Devtools

This appendix summarizes the development helpers under `devtools/`.

## Conda environments

Environment definitions are stored in `devtools/conda-envs/`.

Common choices:
- `development_env.yaml` for day-to-day development,
- `test_env.yaml` for test-focused execution,
- `docs_env.yaml` for documentation builds,
- `release_gates_env.yaml` for release-gate parity checks.

Standalone environment creation from the repository root (Python 3.14):

```bash
conda env create --name pyunitwizard-dev --file devtools/conda-envs/development_env.yaml
conda activate pyunitwizard-dev
python -m pip install --no-deps --editable .
```

## Recommended local baseline

```bash
python -m pytest --receptor=llm tests
make -C docs html
```

Use this baseline before opening PRs or preparing release tags.

Routine Linux development uses the shared Python 3.14 workspace described in
[Development Environment](development-environment.md). Authorized internal
direct pushes use the common scoped-checkpoint policy; PR and publication
gates retain their full requirements.

## Maintenance tools

- `python devtools/devguide_index.py` regenerates issue-backed report indexes;
  `--check` verifies them without changing files.
- `python devtools/check_dependency_routes.py` checks the declared dependency
  routes using the pinned suite SDK. It does not replace a clean installed
  artifact qualification or a global environment dependency check.
- `python devtools/benchmark_backend_attribution.py` measures warmed optional
  attribution paths; retain its raw samples and provider capabilities.
