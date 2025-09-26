import pyunitwizard as puw
import unyt

from .helpers import loaded_libraries


def test_quantity_openmm_unit():

    with loaded_libraries(['pint', 'openmm.unit']):
        openmm_unit = puw.forms.api_openmm_unit.openmm_unit
        quantity = puw.quantity('10 kilojoule/mole', form='openmm.unit')
        q_true = 10 * openmm_unit.kilojoule/openmm_unit.mole
        assert puw.are_close(quantity, q_true)

def test_quantity_pint():

    ureg = puw.forms.api_pint.ureg
    assert puw.quantity(2.5, 
        'nanometers/picoseconds') == ureg.Quantity(2.5, 'nanometers/picoseconds')

def test_quantity_unyt():

    with loaded_libraries(['pint', 'unyt']):
        assert puw.quantity(1.0,
            unyt.J/unyt.s, form="unyt") == 1.0 * unyt.J/unyt.s
