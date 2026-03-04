# NumPy Interoperability

Scientific computing relies heavily on NumPy.

Common problems include:

- unit loss in numerical operations
- dimensional errors not detected

PyUnitWizard currently provides:

- explicit wrappers in `pyunitwizard.utils.numpy`:
  - `mean`, `sum`, `linalg_norm`, `trapz`
- transparent mode:
  - `pyunitwizard.utils.numpy.setup_numpy(enable=True)`
  - `pyunitwizard.utils.numpy.numpy_context()`

In transparent mode, standard NumPy calls (`np.mean`, `np.sum`,
`np.linalg.norm`, `np.trapezoid`) dispatch to PyUnitWizard when quantity inputs
are detected, while plain numeric inputs keep normal NumPy behavior.
