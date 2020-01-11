import re

import jdog as jd
from jdog.placeholder.name import NamePlaceholder
from jdog.placeholder.placeholder import FuncStrPlaceholder, FuncPlaceholder


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


def test_add_new():
    scheme = """{"f":"{{test}}"}"""

    jdog = jd.Jdog()
    jdog.add_matcher('test', r'^{{test}}$', lambda tok, arg: FuncStrPlaceholder(tok, arg, lambda _: 'foo'))

    jdog.parse_scheme(scheme)
    res = jdog.generate()

    assert res == """{"f":"foo"}"""


def test_redefine():
    scheme = """{"f":"{{age}}"}"""
    jdog = jd.Jdog()
    jdog.add_matcher('age', r'^{{age}}$', lambda tok, arg: FuncPlaceholder(tok, arg, lambda _: 666))

    jdog.parse_scheme(scheme)
    res = jdog.generate()

    assert res == """{"f":666}"""

