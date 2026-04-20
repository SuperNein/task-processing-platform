import pytest

from src.services.validation import SourceValidator


# Services
@pytest.fixture
def validator():
    return SourceValidator()


# Sources
@pytest.fixture
def valid_source():
    class ValidSource:
        def get_tasks(self):
            return ()
    return ValidSource()

@pytest.fixture
def invalid_source():
    class InvalidSource:
        pass
    return InvalidSource()
