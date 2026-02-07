# DepDigest configuration for PyUnitWizard

LIBRARIES = {
    'numpy': {'type': 'hard', 'pypi': 'numpy'},
    'pint': {'type': 'hard', 'pypi': 'Pint'},
    'unyt': {'type': 'soft', 'pypi': 'unyt'},
    'openmm.unit': {'type': 'soft', 'pypi': 'openmm', 'conda': 'openmm'},
    'astropy.units': {'type': 'soft', 'pypi': 'astropy'},
}

# Mapping of form names to their required library
MAPPING = {
    'unyt': 'unyt',
    'pint': 'pint',
    'openmm.unit': 'openmm.unit',
    'astropy.units': 'astropy.units',
}

SHOW_ALL_CAPABILITIES = True
