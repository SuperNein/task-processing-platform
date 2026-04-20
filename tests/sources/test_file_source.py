from typing import Iterable

import pytest

from src.sources.file_source import JSONTaskSource


def test_file_not_found(mock_file_exists):
    with mock_file_exists(False):
        source = JSONTaskSource("")
        with pytest.raises(FileNotFoundError):
            source.get_tasks()

def test_file_source(file_task_source):
    source = file_task_source()
    tasks = source.get_tasks()
    assert isinstance(tasks, Iterable)
