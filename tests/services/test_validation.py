import pytest


def test_source_is_valid(source_validator, valid_source):
    assert source_validator.is_valid(valid_source)

def test_source_is_invalid(source_validator, invalid_source):
    assert not source_validator.is_valid(invalid_source)

def test_source_validating(source_validator, invalid_source):
    with pytest.raises(TypeError):
        source_validator.validate(invalid_source)
