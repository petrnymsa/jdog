from jdog.parser import SchemeParser
import pytest

from jdog.placeholder.name import NamePlaceholder, NamePlaceholderOption

FIRST_NAME_MALE = 'John'
FIRST_NAME_FEMALE = 'Julia'
FIRST_NAME = 'Chuck'
NAME_MALE = 'John Doe'
NAME_FEMALE = 'Julia Doe'
NAME = 'John Julia'
LAST_NAME_MALE = 'Doe'
LAST_NAME_FEMALE = 'Roberts'
LAST_NAME = 'Wick'


@pytest.fixture
def name_placeholder(monkeypatch):
    def get_name(pl):
        option = pl.option
        if NamePlaceholderOption.FIRST_NAME in option:
            return f'"{_first_name(option)}"'
        elif NamePlaceholderOption.LAST_NAME in option:
            return f'"{_last_name(option)}"'
        else:
            return f'"{_name(option)}"'

    def _name(option):
        if NamePlaceholderOption.GENDER_MALE in option:
            return NAME_MALE
        elif NamePlaceholderOption.GENDER_FEMALE in option:
            return NAME_FEMALE
        else:
            return NAME

    def _first_name(option):
        if NamePlaceholderOption.GENDER_MALE in option:
            return FIRST_NAME_MALE
        elif NamePlaceholderOption.GENDER_FEMALE in option:
            return FIRST_NAME_FEMALE
        else:
            return FIRST_NAME

    def _last_name(option):
        if NamePlaceholderOption.GENDER_MALE in option:
            return LAST_NAME_MALE
        elif NamePlaceholderOption.GENDER_FEMALE in option:
            return LAST_NAME_FEMALE
        else:
            return LAST_NAME

    monkeypatch.setattr(NamePlaceholder, 'exec', get_name)


def test_name(name_placeholder):
    parser = SchemeParser()
    scheme = '{"value":"{{name}}"}'
    res = parser.parse(scheme)
    assert res.exec() == f'{{"value":"{NAME}"}}'


def test_first_name(name_placeholder):
    parser = SchemeParser()
    scheme = '{"value":"{{first_name}}"}'

    res = parser.parse(scheme)
    assert res.exec() == f'{{"value":"{FIRST_NAME}"}}'


def test_last_name(name_placeholder):
    parser = SchemeParser()
    scheme = '{"value":"{{last_name}}"}'

    res = parser.parse(scheme)
    assert res.exec() == f'{{"value":"{LAST_NAME}"}}'
