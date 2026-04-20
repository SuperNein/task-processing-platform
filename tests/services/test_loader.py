from typing import Iterable

import pytest

from src.services.loader import TasksLoader


def test_load_invalid_source(invalid_source):
    with pytest.raises(TypeError):
        TasksLoader(invalid_source)

def test_load_source(valid_source):
    loader = TasksLoader(valid_source)
    tasks = loader.load()
    assert isinstance(tasks, Iterable)
