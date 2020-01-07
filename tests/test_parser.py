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


