import json
from faker import Faker

from jdog.placeholder.name import NamePlaceholder, NamePlaceholderOption
from jdog.node.base import ObjectNode, ArrayNode
from jdog.node.property import PropertyNode
from jdog.node.placeholder import PlaceholderNode
from jdog.node.scalar import ScalarNode

# todo sphinx  https://readthedocs.org/

if __name__ == '__main__':

    faker = Faker('cs-CZ')

    root = ObjectNode([
        PropertyNode('A', ScalarNode('a')),
        PropertyNode('B', ScalarNode('b')),
        PropertyNode('NestedObject', ObjectNode([
            PropertyNode('age', ScalarNode(18)),
            PropertyNode('name', PlaceholderNode(NamePlaceholder('sad', [], faker)))
        ])),
        PropertyNode('SomeArray', ArrayNode([
            ScalarNode(1),
            ScalarNode(2),
            ObjectNode([
                PropertyNode('foo', ScalarNode('baz'))
            ])
        ]))
    ])
    res = root.exec()

    print(json.dumps(json.loads(res), indent=4, sort_keys=True, ensure_ascii=False).encode('utf8').decode())
    print()
    print(res)
