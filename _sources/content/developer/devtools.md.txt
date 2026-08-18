# Devtools

This appendix summarizes the development helpers under `devtools/`.

## Conda environments

Environment definitions are stored in `devtools/conda-envs/`.

Common choices:
- `development_env.yaml` for day-to-day development,
- `tests_env.yaml` for test-focused execution,
- `docs_env.yaml` for documentation builds,
- `release_gates_env.yaml` for release-gate parity checks.

Example environment creation (Python 3.13):

```bash
cd devtools/conda-envs
python create_conda_env.py -n pyunitwizard-dev -p 3.13 development_env.yaml
conda activate pyunitwizard-dev
```

## Recommended local baseline

```bash
pytest -q
make -C docs html
```

Use this baseline before opening PRs or preparing release tags.
