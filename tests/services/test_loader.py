from typing import Iterable

import pytest

from src.services.loader import TaskSourceLoader


def test_load_invalid_source(invalid_source):
    with pytest.raises(TypeError):
        TaskSourceLoader(invalid_source)

def test_load_source(valid_source):
    loader = TaskSourceLoader(valid_source)
    tasks = loader.load()
    assert isinstance(tasks, Iterable)
