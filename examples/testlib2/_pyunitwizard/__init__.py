import pyunitwizard as puw

puw.configure.load_library(["pint", "openmm.unit"])
puw.configure.set_default_form("openmm.unit")
puw.configure.set_default_parser("pint")
