# What is PyUnitWizard?

PyUnitWizard is a Python library that provides one API for working with
physical quantities across multiple unit backends.

Instead of coupling your project to a single units implementation, PyUnitWizard
lets you:

- build quantities and units with a stable public interface;
- convert values and units between supported forms;
- validate compatibility and dimensionality in a consistent way;
- standardize outputs to project-level unit conventions.

This model is especially useful in scientific software stacks where different
subsystems may use different unit libraries.

## Design goals

1. Interoperability across unit ecosystems.
2. Explicit unit handling at API boundaries.
3. Reproducible conversions and checks in production workflows.
4. Integration-friendly behavior for host libraries.

## Typical use cases

- Convert and compare quantities coming from different dependencies.
- Normalize values before writing trajectories, reports, or serialized outputs.
- Enforce unit contracts in high-level public APIs.

## Project scope

PyUnitWizard focuses on unit representation and interoperability. It does not
replace domain models or simulation engines.

## License

PyUnitWizard's implementation uses the
[MIT License](https://github.com/uibcdf/pyunitwizard/blob/main/LICENSE).
Its bundled derived QUDT/UO unit catalogue retains CC-BY-4.0 and the
[original attribution notice](https://github.com/uibcdf/pyunitwizard/blob/main/pyunitwizard/vocabularies/NOTICE.md).
Distribution metadata records these existing licenses as `MIT AND CC-BY-4.0`.
