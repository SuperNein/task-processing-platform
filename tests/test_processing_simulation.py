from unittest.mock import patch

import pytest

from src.core.enums import TaskStatus
from src.sources.generator_source import GeneratorTaskSource
from src.processing_simulation import process_tasks

def test_integration_with_real_components():
    tasks_count = 5
    source = GeneratorTaskSource(tasks_count)

    with patch('time.sleep') as mock_sleep:
        tasks = process_tasks(source)

    for task in tasks:
        assert task.status == TaskStatus.done
