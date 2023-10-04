import os
from pathlib import Path
from typing import List, Set, Union
from unittest.mock import Mock

import pytest
from baby_steps import given, then, when
from pytest import raises
from vedro.core import VirtualScenario

from vedro_dependency_finder import get_indexes_of_scenarios


@pytest.fixture
def root():
    return Path(os.getcwd())


def create_scenario(filename) -> VirtualScenario:
    return Mock(VirtualScenario, __file__=filename)


def test_indexes_of_all_scenarios(root: Path):
    with given:
        scenarios = list()
        scenarios_paths = set()
        iterator = range(0, 3)

        for i in iterator:
            scenarios.append(create_scenario(root / f"scenario_{i}.py"))
            scenarios_paths.add(scenarios[i].path)

    with when:
        all_indexes, diff_indexes = get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert all_indexes == list(iterator)
        assert diff_indexes == list(iterator)


def test_diff_indexes_at_the_beginning_of_all_indexes(root: Path):
    with given:
        iterator = range(0, 5)
        diff_list = list(range(0, 3))

        scenarios = [create_scenario(root / f"scenario_{i}.py") for i in iterator]
        scenarios_paths = {scenarios[i].path for i in diff_list}

    with when:
        all_indexes, diff_indexes = get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert all_indexes == [3, 4, 0, 1, 2]
        assert diff_indexes == diff_list


def test_diff_indexes_in_the_middle_of_all_indexes(root: Path):
    with given:
        iterator = range(0, 5)
        diff_list = list(range(2, 4))

        scenarios = [create_scenario(root / f"scenario_{i}.py") for i in iterator]
        scenarios_paths = {scenarios[i].path for i in diff_list}

    with when:
        all_indexes, diff_indexes = get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert all_indexes == [0, 1, 4, 2, 3]
        assert diff_indexes == diff_list


def test_diff_indexes_at_the_end_of_all_indexes(root: Path):
    with given:
        iterator = range(0, 5)
        diff_list = list(range(3, 5))

        scenarios = [create_scenario(root / f"scenario_{i}.py") for i in iterator]
        scenarios_paths = {scenarios[i].path for i in diff_list}

    with when:
        all_indexes, diff_indexes = get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert all_indexes == list(iterator)
        assert diff_indexes == diff_list


def test_one_diff_index_contained_in_one_all_indexes(root: Path):
    with given:
        path = root / "scenario_0.py"
        scenarios = [create_scenario(path)]
        scenarios_paths = {scenarios[0].path}

    with when:
        all_indexes, diff_indexes = get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert all_indexes == [0]
        assert diff_indexes == [0]


def test_diff_indexes_not_contained_in_all_indexes(root: Path):
    with given:
        scenarios = [create_scenario(root / "scenario_0.py")]
        scenarios_paths = {root / "scenario_1.py"}

    with when, raises(BaseException) as exc_info:
        get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert exc_info.type is AssertionError
        assert str(exc_info.value) == "The selected scenarios are not contained " \
                                      "in the selected folder!"


@pytest.mark.parametrize("scenarios", [None, list()])
def test_empty_all_indexes(scenarios: Union[List, None]):
    with given:
        scenarios_paths = set("scenario_0.py")

    with when, raises(BaseException) as exc_info:
        get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert exc_info.type is AssertionError
        assert str(exc_info.value) == "Scenarios not found!"


@pytest.mark.parametrize("scenarios_paths", [None, set()])
def test_empty_diff_indexes(scenarios_paths: Union[Set, None]):
    with given:
        scenarios = ["banana"]

    with when, raises(BaseException) as exc_info:
        get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert exc_info.type is AssertionError
        assert str(exc_info.value) == "Paths of scenarios not found!"
