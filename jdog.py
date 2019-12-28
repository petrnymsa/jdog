import json
import re

# todo import faker
# todo sphinx  https://readthedocs.org/

TOKEN_CITY = "city"


class Placeholder:
    def __init__(self, full_name, name, arguments):
        print(f'input argument: {full_name}')
        self.full_name = full_name
        print(f'assigned {self.full_name}')
        self.name = name
        self.arguments = arguments

    def exec(self):
        pass

    def __str__(self):
        print(self.full_name)
        return f"{self.full_name} {self.name} {self.arguments}"

class PlaceholderParser:
    def __init__(self):
        self.token_pattern = re.compile("^{{.*}}$")
        self.city = re.compile("^{{(city)}}$")

    def parse(self, input_value):
        res = re.match(self.token_pattern, input_value)

        if res is None:
            raise ValueError(f"Given {input_value} is not valid token")
        print(input_value)
        res = self.try_pattern(self.city, input_value)
        if res is not None:
            return Placeholder(input_value, TOKEN_CITY, None)

        if res is None:
            raise ValueError(f"Given {input_value} is not valid token")

    def try_pattern(self, pattern, input_value):
        return re.match(pattern, input_value)


class Node:
    def exec(self):
        pass


class GroupNode(Node):

    def __init__(self, begin_token, end_token, nodes):
        self.begin_token = begin_token
        self.end_token = end_token
        self.nodes = nodes

    def exec(self):
        s = ','.join(n.exec() for n in self.nodes)
        return f'{self.begin_token}{s}{self.end_token}'


class ArrayNode(GroupNode):
    def __init__(self, children):
        super().__init__('[', ']', children)


class ObjectNode(GroupNode):
    def __init__(self, properties):
        super().__init__('{', '}', properties)


class ScalarNode(Node):
    def __init__(self, value):
        self.value = value

    def exec(self):
        return f'"{self.value}"'


class RandomScalarNode(Node):
    def __init__(self, placeholder):
        self.placeholder = placeholder

    def exec(self):
        print("Using placeholder to generate scalar value")
        return 'random placeholder used'


class PropertyNode(Node):
    def __init__(self, name, child):
        self.name = name
        self.child = child

    def exec(self):
        return f'"{self.name}":{self.child.exec()}'




if __name__ == '__main__':
    inp = """{"p": "a" }"""
    # parser = TokenParser()
    # token = parser.parse(inp)
    # print(token)

    root = ObjectNode([
        PropertyNode('A', ScalarNode('a')),
        PropertyNode('B', ScalarNode('b')),
        PropertyNode('NestedObject', ObjectNode([
            PropertyNode('age', ScalarNode(18)),
            PropertyNode('name', ScalarNode('petr'))
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

    print(json.dumps(json.loads(res), indent=4, sort_keys=True))
    print()
    print(res)
    print()