# PyUnitWizard 0.29.3

The virtual `pyunitwizard.main` compatibility module identifies the package
initializer that creates it through `__file__`, its module spec and its
package parent. Installed-origin validation and Python source introspection
can resolve the creator. Legacy imports retain lazy forwarding, function
identity and their one-time deprecation warning.
[#146](https://github.com/uibcdf/pyunitwizard/issues/146) ·
[PR #147](https://github.com/uibcdf/pyunitwizard/pull/147)

The regression verifies the actual registered module in fresh interpreters,
under both cold start and an active application unit policy. It checks the
creator metadata, policy, loaded adapters and warning state.

The maintenance release uses the existing Python 3.11–3.14 Linux/macOS arm64
baseline and the Python 3.12–3.14 OpenFF profile.
[Release qualification](https://github.com/uibcdf/pyunitwizard/issues/149)
