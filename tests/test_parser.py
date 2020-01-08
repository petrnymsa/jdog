from jdog.parser import SchemeParser
import random


def test_bool(monkeypatch):
    parser = SchemeParser()
    scheme = '{"value":"{{bool}}"}'

    def rnd_number():
        return 0.6

    monkeypatch.setattr(random, 'random', rnd_number)
    res = parser.parse(scheme)
    assert res.exec() == '{"value":"true"}'


def test_option():
    parser = SchemeParser()
    scheme = '{"value":"{{option(foo,bar)}}"}'

    parsed = parser.parse(scheme)
    res = parsed.exec()

    assert res == '{"value":"foo"}' or res == '{"value":"bar"}'


def test_option_nested(monkeypatch):
    parser = SchemeParser()
    scheme = '{"value":"{{option(foo,{{age}})}}"}'

    monkeypatch.setattr(random, 'randint', lambda a, b: 1)

    parsed = parser.parse(scheme)
    res = parsed.exec()

    assert res == '{"value":"foo"}' or res == '{"value":1}'

# todo test other default placeholders
