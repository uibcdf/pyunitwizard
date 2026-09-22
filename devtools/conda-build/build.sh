echo "Building"
$PYTHON devtools/conda-build/freeze_project_version.py "$PKG_VERSION"
$PYTHON -m pip install --no-deps --no-build-isolation --ignore-installed .
echo "Done"
