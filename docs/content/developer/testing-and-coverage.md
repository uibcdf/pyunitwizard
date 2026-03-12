# Testing and Coverage

PyUnitWizard is integration infrastructure. Tests should prioritize behavioral contracts.

## Minimum local test command

```bash
conda run -n molsyssuite@uibcdf_3.13 pytest -q tests --ignore=tests/test_import.py
```

## Coverage command

```bash
pytest --cov=pyunitwizard --cov-report=term-missing
```

## Performance baseline command

```bash
python benchmarks/conversion_baseline.py
```

Store RC snapshots under `devguide/` and compare candidate tags for regressions.

## Release-critical areas

- `api/*` public behavior and edge branches.
- parser/default configuration behavior.
- standardization and compatibility semantics.
- integration smoke with `argdigest`, `depdigest`, and `smonitor`.
- frontend interoperability bridges:
  - `tests/utils/numpy/test_transparent_bridge.py`
  - `tests/utils/pandas/test_workflows.py`
  - `tests/utils/matplotlib/test_complex_layouts.py`
  - `tests/integration/test_frontend_cross_backend_matrix.py`

## Quality target

Coverage trend should be stable or improving in public API modules.
