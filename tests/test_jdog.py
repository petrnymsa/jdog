import jdog as jd
from jdog.placeholder.name import NamePlaceholder


def test_parse_basic():
    scheme = """{"data": [1,2,3]}"""
    jdog = jd.Jdog()
    jdog.parse_scheme(scheme)


def test_basic():
    scheme = """{"data":[1,2,3]}"""
    jdog = jd.Jdog()
    jdog.parse_scheme(scheme)
    assert jdog.generate() == scheme.strip()


def test_simple_placeholder(monkeypatch):
    def name_placeholder(_):
        return '"John Doe"'

    scheme = """{"name":"{{name}}"}"""
    jdog = jd.Jdog()
    jdog.parse_scheme(scheme)
    monkeypatch.setattr(NamePlaceholder, 'exec', name_placeholder)

    assert jdog.generate() == '{"name":"John Doe"}'