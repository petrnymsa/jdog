import mock
import random
import jdog.node as jn
import jdog.placeholder.placeholder as jph


def test_scalar():
    node = jn.ScalarNode('test')
    assert node.exec() == '"test"'


def test_scalar_number():
    assert jn.ScalarNode(1).exec() == 1


def test_scalar_str_number():
    assert jn.ScalarNode('1').exec() == '"1"'


def test_property():
    node = jn.PropertyNode(jn.ScalarNode('test'), jn.ScalarNode('value'))
    assert node.exec() == '"test":"value"'


def test_property_empty():
    node = jn.PropertyNode(jn.ScalarNode('test'), None)
    assert node.exec() == '"test":""'


def test_func():
    expected = '{"test":"value"}'
    node = jn.FuncNode(lambda: expected)
    assert node.exec() == expected


def test_object():
    expected = '{"test":"value","foo":"bar"}'
    node = jn.ObjectNode([
        jn.PropertyNode(jn.ScalarNode('test'), jn.ScalarNode('value')),
        jn.PropertyNode(jn.ScalarNode('foo'), jn.ScalarNode('bar'))
    ])
    assert node.exec() == expected


def test_array():
    expected = '[1,2,3]'
    node = jn.ArrayNode([
        jn.ScalarNode(1),
        jn.ScalarNode(2),
        jn.ScalarNode(3),
    ])
    assert node.exec() == expected


def test_placeholder():
    pl = jph.FuncStrPlaceholder('ff', [], lambda _: 'test_value')
    node = jn.PlaceholderNode(pl)
    assert node.exec() == '"test_value"'


def test_range():
    node = jn.RangeNode('values', 2, jn.ScalarNode('foo'))
    assert node.exec() == '"values": ["foo","foo"]'


def test_range_top():
    with mock.patch.object(random, 'randint') as m:
        m.return_value = 3

        node = jn.RangeNode('values', 2, jn.ScalarNode('foo'), 4)
        assert node.exec() == '"values": ["foo","foo","foo"]'


def test_complex():
    node = jn.ObjectNode([
        jn.PropertyNode(jn.ScalarNode('A'), jn.ScalarNode('a')),
        jn.PropertyNode(jn.ScalarNode('B'), jn.ScalarNode('b')),
        jn.PropertyNode(jn.ScalarNode('NestedObject'), jn.ObjectNode([
            jn.PropertyNode(jn.ScalarNode('age'), jn.ScalarNode(18)),
            jn.PropertyNode(jn.ScalarNode('name'), jn.ScalarNode('joker'))
        ])),
        jn.PropertyNode(jn.ScalarNode('SomeArray'), jn.ArrayNode([
            jn.ScalarNode(1),
            jn.ScalarNode(2)
        ])),
    ])

    expected = '{"A":"a","B":"b","NestedObject":{"age":18,"name":"joker"},"SomeArray":[1,2]}'
    assert node.exec() == expected
