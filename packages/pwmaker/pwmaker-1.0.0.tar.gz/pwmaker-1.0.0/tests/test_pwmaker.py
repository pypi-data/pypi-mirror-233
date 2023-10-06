import string
import pytest

from context import PasswordBuilder


@pytest.fixture
def password_builder():
    return PasswordBuilder()


def test_default_password():
    """
    Default password should be 10 charachters long and all small letters
    """
    builder = PasswordBuilder()

    password = builder.build().password

    assert len(password) == 10
    assert all([True if x in string.ascii_lowercase else False for x in password])


def test_password_length(password_builder):
    password = password_builder.length(20).build()

    assert len(password) == 20


def test_password_numbers(password_builder):
    password = password_builder.numbers(3).build().password

    assert len(list(filter(lambda x: x in string.digits, password))) == 3


def test_password_special(password_builder):
    password = password_builder.special(3).build().password

    assert len(list(filter(lambda x: x in string.punctuation, password))) == 3


def test_more_numbers_symbols_than_length():
    builder = PasswordBuilder()

    with pytest.raises(ValueError):
        password = builder.length(10).numbers(7).special(4).build()
