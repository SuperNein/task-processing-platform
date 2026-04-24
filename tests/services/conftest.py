import pytest

from src.services.validation import ProtocolValidator
from src.protocols.source import TaskSource


# Services
@pytest.fixture
def source_validator():
    return ProtocolValidator(protocol=TaskSource)


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
