import pytest

from src.core.task_model import Task


@pytest.fixture
def task() -> Task:
    return Task("test_description")
