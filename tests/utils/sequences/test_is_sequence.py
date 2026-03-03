import numpy as np
import pyunitwizard as puw


def test_is_sequence_predicates():
    assert puw.utils.sequences.is_sequence([1, 2])
    assert puw.utils.sequences.is_sequence((1, 2))
    assert puw.utils.sequences.is_sequence({1, 2})
    assert puw.utils.sequences.is_sequence(np.array([1, 2]))
    assert not puw.utils.sequences.is_sequence(3.14)


def test_is_sequence_of_sequences_predicates():
    assert puw.utils.sequences.is_sequence_of_sequences([[1], (2,)])
    assert not puw.utils.sequences.is_sequence_of_sequences([1, [2]])


def test_is_sequence_of_sequences_of_sequences_predicates():
    assert puw.utils.sequences.is_sequence_of_sequences_of_sequences([[[1]], [[2]]])
    assert not puw.utils.sequences.is_sequence_of_sequences_of_sequences([[1], [2]])


def test_is_sequence_of_quantities_predicates():
    puw.configure.reset()
    puw.configure.load_library(["pint"])

    sequence_ok = [puw.quantity(1, "meter"), puw.quantity(2, "meter")]
    sequence_bad = [puw.quantity(1, "meter"), 2]

    assert puw.utils.sequences.is_sequence_of_quantities(sequence_ok)
    assert not puw.utils.sequences.is_sequence_of_quantities(sequence_bad)
