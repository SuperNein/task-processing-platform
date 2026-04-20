import json
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest


@pytest.fixture
def mock_file_exists():
    def _set_exists(return_value: bool):
        return patch.object(Path, 'exists', return_value=return_value)
    return _set_exists

@pytest.fixture
def mock_json_file():
    def _mock(data):
        return patch('builtins.open', mock_open(read_data=json.dumps(data)))
    return _mock

@pytest.fixture
def mock_json_load():
    def _set_return_value(data):
        return patch('json.load', return_value=data)
    return _set_return_value

@pytest.fixture
def sample_data():
    return [
        {"description": "task_1"},
        {"description": "", "priority": "high"},
        {},
    ]

@pytest.fixture
def file_task_source(
        mock_file_exists,
        mock_json_file,
        mock_json_load,
        sample_data,
):
    def _create_source(data=None, file_exists=True):
        if data is None:
            data = sample_data

        patches = [
            mock_file_exists(file_exists),
            mock_json_file(data),
            mock_json_load(data),
        ]

        for patch in patches:
            patch.start()

        from src.sources.file_source import JSONTaskSource
        source = JSONTaskSource("")

        return source

    yield _create_source
