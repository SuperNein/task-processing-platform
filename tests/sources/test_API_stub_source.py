from typing import Iterable

import pytest

from src.sources.API_stub_source import APIStubTasksSource


def test_api_stub_source():
    source = APIStubTasksSource("url")
    tasks = source.get_tasks()

    assert isinstance(tasks, Iterable)
