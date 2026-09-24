# Data and Package Resources

Use this appendix when you need to ship or access non-code package resources in
PyUnitWizard.

## Primary guidance

Prefer modern Python packaging mechanisms (`importlib.resources`) for new code.
Avoid introducing legacy resource APIs unless there is a strong compatibility
reason.

## Reference links

- [Setuptools data files guide](https://setuptools.readthedocs.io/en/latest/userguide/datafiles.html)
- [Setuptools pkg_resources reference](https://setuptools.readthedocs.io/en/latest/pkg_resources.html#resourcemanager-api)

## Project rule of thumb

If a feature requires resource files, document:
- where resources are located in the repository,
- how they are loaded at runtime,
- which tests validate that packaged data is available after installation.
