import pyunitwizard as puw
import openmm.unit as openmm_unit

def test_compatibility_pint():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    q1 = puw.quantity(2.5, 'nanometers/picoseconds', form="pint")
    q2 = puw.convert(q1, to_unit='angstroms/picoseconds', to_form="pint")
    assert puw.compatibility(q1, q2)


def test_compatibility_openmm():
    puw.configure.reset()
    puw.configure.load_library(['openmm.unit'])

    q1 = puw.quantity(2.5, openmm_unit.nanometer/openmm_unit.picosecond, form="openmm.unit")
    q2 = puw.quantity(3.0, openmm_unit.angstrom/openmm_unit.second,  form="openmm.unit")
    assert puw.compatibility(q1, q2)