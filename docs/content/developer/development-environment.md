# Development Environment

Use conda environments from `devtools/conda-envs`.

## Recommended environments

- `development_env.yaml`: core development tasks.
- `tests_env.yaml`: test execution.
- `docs_env.yaml`: Sphinx and notebook documentation.
- `release_gates_env.yaml`: release-gate parity checks.

## Typical setup

```bash
cd devtools/conda-envs
python create_conda_env.py -n pyunitwizard-dev -p 3.13 development_env.yaml
conda activate pyunitwizard-dev
```

## Local validation baseline

```bash
pytest -q
make -C docs html
```
