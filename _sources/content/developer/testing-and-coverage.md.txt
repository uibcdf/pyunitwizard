# Testing and Coverage

PyUnitWizard is integration infrastructure. Tests should prioritize behavioral contracts.

## Minimum local test command

```bash
conda run -n molsyssuite@uibcdf_3.14 python -m pytest --receptor=llm tests
```

## Coverage command

```bash
python -m pytest --receptor=llm tests --cov=pyunitwizard --cov-report=term-missing
```

## Performance baseline command

```bash
python benchmarks/conversion_baseline.py
```

Store RC snapshots under `devguide/` and compare candidate tags for regressions.
Follow `benchmarks/README.md` for telemetry modes and provenance. A source
benchmark does not qualify the installed public artifact.

## Validation scope

Keep `tests/test_import.py` in the full suite. The supported matrix covers
Python 3.11–3.14 on Linux and macOS arm64; optional provider profiles may be
narrower (see [Compatibility Matrix](compatibility-matrix.md)).

External PRs and releases require their mandatory full gates. For authorized
internal direct pushes, select checks appropriate to changed code, inputs,
environment and scope under the
[common checkpoint policy](https://github.com/uibcdf/pyunitwizard/blob/main/MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints).
Record missing evidence and its owning issue; documentation or administrative
checks do not clear scientific full-suite backlog.

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
