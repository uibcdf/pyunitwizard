# Production Checklist

Use this list before releasing a library integrated with PyUnitWizard.

## Configuration

- [ ] `puw.configure` initialization is centralized.
- [ ] Supported backends are loaded explicitly.
- [ ] Default parser and form are deterministic.
- [ ] Standard units are defined for normalization paths.

## API contracts

- [ ] Public entry points normalize incoming quantities.
- [ ] Dimensional checks are explicit where needed.
- [ ] Output standardization is applied before external handoff.
- [ ] Display/logging formatting (`to_string`) is separated from core logic.

## Testing

- [ ] Conversion success and failure paths are tested.
- [ ] Compatibility and dimensional edge cases are tested.
- [ ] Regression tests exist for known unit bugs.
- [ ] Test fixtures reset and reconfigure runtime state.

## Documentation

- [ ] User docs match actual runtime behavior.
- [ ] Examples are runnable with supported Python versions.
- [ ] Troubleshooting entries reflect real failures from CI/support.

If all items are checked, integration is typically ready for release.
