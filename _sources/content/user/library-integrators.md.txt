# Library Integrators

You are in the right place if you maintain a scientific library and need a
single, explicit units contract at your public API boundaries.

PyUnitWizard is most useful when your users pass quantities in mixed forms
(strings, Pint, unyt, OpenMM, Astropy, physipy, quantities) and you want your library internals to
remain unit-agnostic.

A practical way to adopt it is incremental:
- start with one backend and one API entry point,
- make dimensional checks explicit,
- standardize outputs in release-critical paths,
- expand only after tests are stable.

## Recommended reading order

1. [What PyUnitWizard Solves](what-pyunitwizard-solves.md)
2. [Adoption Story: From Drift to Determinism](adoption-story.md)
3. [Quick Start](quickstart.md)
4. [Mini Library Walkthrough](mini-library-walkthrough.md)
5. [Configuration](configuration.md)
6. [Backend Coverage and Expectations](backend-coverage.md)
7. [NumPy, Pandas, and Matplotlib Interoperability](numpy-pandas-matplotlib.md)
8. [Integrating Your Library](integrating-your-library.md)
9. [Troubleshooting](troubleshooting.md)
10. [Production Checklist](production-checklist.md)
11. [FAQ](faq.md)

Notebook companion for this route:
- [In_Your_Library.ipynb](In_Your_Library.ipynb)
- [Dimensionality.ipynb](Dimensionality.ipynb)
- [Standardize.ipynb](Standardize.ipynb)

If you need full signatures and module-level detail while implementing, keep
[Users API Reference](../../api/users/api_user.rst) open in parallel.
