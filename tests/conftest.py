import pytest

from src.core.models import Task


@pytest.fixture
def task() -> Task:
    return Task("test_description")
