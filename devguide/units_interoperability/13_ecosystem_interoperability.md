# Scientific Ecosystem Interoperability

PyUnitWizard aims to integrate smoothly with major Scientific Python
libraries.

Targets include:

- NumPy
- SciPy
- pandas
- Matplotlib
- scikit-learn

Ensuring safe handling of quantities across these tools will greatly
improve reliability of scientific workflows.

Current evidence includes a cross-backend frontend matrix:
- `tests/integration/test_frontend_cross_backend_matrix.py`
- verifies available backend forms and mixed-form pairs across NumPy, pandas,
  and Matplotlib integration surfaces.
