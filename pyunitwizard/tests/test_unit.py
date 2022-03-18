import pyunitwizard as puw

def test_unit_with_openmm_unit():
    puw.configure.reset()
    puw.configure.load_library(['openmm.unit'])

    openmm_unit = puw.forms.api_openmm_unit.openmm_unit
    unit = puw.unit(openmm_unit.kilojoule/openmm_unit.mole)
    assert unit == openmm_unit.kilojoule/openmm_unit.mole

def test_unit_with_pint():
    puw.configure.reset()
    puw.configure.load_library(['pint'])

    ureg = puw.forms.api_pint.ureg
    unit = puw.unit('kJ/mol')
    assert unit == ureg.Unit('kJ/mol')