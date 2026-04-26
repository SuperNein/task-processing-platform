import pytest

from src.core.task_model import Task


@pytest.fixture
def task() -> Task:
    return Task(description="test_description", priority=1)

@pytest.fixture
def tasks():
    return [
        Task(description=f"task_{i}", priority=1)
        for i in range(3)
    ]
