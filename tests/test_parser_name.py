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


@pytest.mark.parametrize("scheme,expected",
                         [("name", NAME), ("name(m)", NAME_MALE), ("name(f)", NAME_FEMALE),
                          ("first_name", FIRST_NAME), ("first_name(m)", FIRST_NAME_MALE),
                          ("first_name(f)", FIRST_NAME_FEMALE),
                          ("last_name", LAST_NAME), ("last_name(m)", LAST_NAME_MALE),
                          ("last_name(f)", LAST_NAME_FEMALE)])
def test_name(name_placeholder, scheme, expected):
    parser = SchemeParser()
    scheme = f'{{"value":"{{{{{scheme}}}}}"}}'
    res = parser.parse(scheme)
    assert res.exec() == f'{{"value":"{expected}"}}'

#todo negative tests
