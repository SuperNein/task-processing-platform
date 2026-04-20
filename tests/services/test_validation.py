import pytest


def test_source_is_valid(validator, valid_source):
    assert validator.is_valid(valid_source)

def test_source_is_invalid(validator, invalid_source):
    assert not validator.is_valid(invalid_source)

def test_source_validating(validator, invalid_source):
    with pytest.raises(TypeError):
        validator.validate(invalid_source)
