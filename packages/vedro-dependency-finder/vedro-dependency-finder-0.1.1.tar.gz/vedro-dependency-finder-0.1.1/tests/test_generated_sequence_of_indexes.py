from copy import deepcopy

from baby_steps import given, then, when

from vedro_dependency_finder import generate_sequence_of_indexes


def test_sequence_with_one_diff_index():
    with given:
        all_indexes = list(range(0, 3))
        diff_indexes = [2]

    with when:
        sequence = generate_sequence_of_indexes(all_indexes, diff_indexes)

    with then:
        assert sequence == [2, 0, 2, 1, 2]


def test_sequence_with_two_diff_indexes():
    with given:
        all_indexes = list(range(0, 6))
        diff_indexes = list(range(4, 6))

    with when:
        sequence = generate_sequence_of_indexes(all_indexes, diff_indexes)

    with then:
        assert sequence == [5, 0, 5, 1, 5, 2, 5, 3, 5, 4, 0, 4, 1, 4, 2, 4, 3, 4, 5]


def test_sequence_with_identical_indexes():
    with given:
        all_indexes = list(range(0, 3))
        diff_indexes = deepcopy(all_indexes)

    with when:
        sequence = generate_sequence_of_indexes(all_indexes, diff_indexes)

    with then:
        assert sequence == [2, 0, 2, 1, 0, 1, 2]


def test_sequence_without_all_indexes():
    with given:
        all_indexes = list()
        diff_indexes = list(range(0, 3))

    with when:
        sequence = generate_sequence_of_indexes(all_indexes, diff_indexes)

    with then:
        assert sequence == [2, 0, 2, 1, 0, 1, 2]


def test_sequence_without_diff_indexes():
    with given:
        all_indexes = list(range(0, 3))
        diff_indexes = list()

    with when:
        sequence = generate_sequence_of_indexes(all_indexes, diff_indexes)

    with then:
        assert sequence == all_indexes
