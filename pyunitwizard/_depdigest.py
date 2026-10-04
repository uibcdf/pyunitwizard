# DepDigest configuration for PyUnitWizard

LIBRARIES = {
    "argdigest": {"type": "hard", "pypi": "argdigest", "conda": "argdigest"},
    "ackredit": {"type": "soft", "pypi": None, "conda": None},
    "numpy": {"type": "hard", "pypi": "numpy"},
    "pint": {"type": "hard", "pypi": "Pint"},
    "unyt": {"type": "soft", "pypi": "unyt"},
    "openmm.unit": {"type": "soft", "pypi": "openmm", "conda": "openmm"},
    "astropy.units": {"type": "soft", "pypi": "astropy"},
    "physipy": {"type": "soft", "pypi": "physipy"},
    "quantities": {"type": "soft", "pypi": "quantities"},
}

# Mapping of form names to their required library
MAPPING = {
    "unyt": "unyt",
    "pint": "pint",
    "openmm.unit": "openmm.unit",
    "astropy.units": "astropy.units",
    "physipy": "physipy",
    "quantities": "quantities",
}

SHOW_ALL_CAPABILITIES = True
