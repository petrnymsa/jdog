import json
import random
from faker import Faker

from jdog.placeholder.name import NamePlaceholder, NamePlaceholderOption
from jdog.node.base import ObjectNode, ArrayNode, Node, RangeNode, FuncNode
from jdog.node.property import PropertyNode
from jdog.node.placeholder import PlaceholderNode
from jdog.node.scalar import ScalarNode
from jdog.parser import SchemeParser


# todo sphinx  https://readthedocs.org/


def validate(text):
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    faker = Faker('cs-CZ')

    # root = ObjectNode([
    #     PropertyNode(ScalarNode('A'), ScalarNode('a')),
    #     PropertyNode(ScalarNode('B'), ScalarNode('b')),
    #     PropertyNode(ScalarNode('NestedObject'), ObjectNode([
    #         PropertyNode(ScalarNode('age'), ScalarNode(18)),
    #         PropertyNode(ScalarNode('name'), PlaceholderNode(NamePlaceholder('sad', [], faker)))
    #     ])),
    #     PropertyNode(ScalarNode('SomeArray'), ArrayNode([
    #         ScalarNode(1),
    #         ScalarNode(2),
    #         ObjectNode([
    #             PropertyNode(ScalarNode('foo'), ScalarNode('baz'))
    #         ])
    #     ])),
    # ])
    # root = ObjectNode([
    #     RangeNode('people', 1, ObjectNode([
    #         # PropertyNode(ScalarNode('name'), PlaceholderNode(NamePlaceholder('name', [], faker))),
    #         PropertyNode(ScalarNode('age'), FuncNode(lambda: random.randint(18, 100)))
    #     ]), 4)
    # ])

    parser = SchemeParser()
    raw = """{"SomeName": "{{first_name}}"}"""
    root = parser.parse(raw)
    res = root.exec()

    if validate(res):
        print('valid json')
    else:
        print('not valid json')
    # print(json.dumps(json.loads(res), indent=4, sort_keys=True, ensure_ascii=False).encode('utf8').decode())
    print()
    print(res)
