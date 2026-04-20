from typing import Iterable

import pytest

from src.sources.generator_source import GeneratorTaskSource


@pytest.mark.parametrize(
    "count, description",
    [
        (3, None),
        (2, "42"),
        (5, "abc"),
        (1, "")
    ]
)
def test_generator_source(count, description):
    source = GeneratorTaskSource(count, description)
    tasks = source.get_tasks()

    assert isinstance(tasks, Iterable)
    assert len([task for task in tasks]) == count
