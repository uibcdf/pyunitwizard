# Testing and Coverage

PyUnitWizard is integration infrastructure. Tests should prioritize behavioral contracts.

## Minimum local test command

```bash
pytest -q
```

## Coverage command

```bash
pytest --cov=pyunitwizard --cov-report=term-missing
```

## Release-critical areas

- `api/*` public behavior and edge branches.
- parser/default configuration behavior.
- standardization and compatibility semantics.
- integration smoke with `argdigest`, `depdigest`, and `smonitor`.

## Quality target

Coverage trend should be stable or improving in public API modules.
