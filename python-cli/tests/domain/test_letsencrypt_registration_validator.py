from mock import patch, MagicMock
import pytest
from thegate.domain.validation import LetsencryptRegistrationValidator

@pytest.fixture
def validator():
    return LetsencryptRegistrationValidator()

@pytest.fixture
def validator_with_agreed_tos(validator):
    class ValidatorWithAgreedTos():
        def __init__(self, validator):
            self.validator = validator
        def is_valid(self, email):
            return self.validator.is_valid(email, agree_tos=True)
    return ValidatorWithAgreedTos(validator)

def test_refuse_tos__always_invalid(validator):
    assert False == validator.is_valid("hello@gmail.com", agree_tos=False)
    assert False == validator.is_valid("hello", agree_tos=False)
    assert False == validator.is_valid("", agree_tos=False)

def test_accept_tos__valid_email(validator_with_agreed_tos):
    assert True == validator_with_agreed_tos.is_valid('hello@gmail.com')

def test_accept_tos__invalid_email__wrong_format(validator_with_agreed_tos):
    assert False == validator_with_agreed_tos.is_valid('hello@gmail')
    assert False == validator_with_agreed_tos.is_valid('@gmail.com')
    assert False == validator_with_agreed_tos.is_valid('hellogmail.com')
    assert False == validator_with_agreed_tos.is_valid('hello@')
    assert False == validator_with_agreed_tos.is_valid('hello')

def test_accept_tos__invalid_email__none(validator):
    with pytest.raises(RuntimeError):
        validator.is_valid(None, agree_tos=True)

    with pytest.raises(RuntimeError):
        validator.is_valid(None, agree_tos=False)