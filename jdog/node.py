import random


class Node:
    def exec(self):
        pass


class _GroupNode(Node):
    def __init__(self, begin_token, end_token, nodes):
        self.begin_token = begin_token
        self.end_token = end_token
        self.nodes = nodes

    def exec(self):
        s = ','.join(str(n.exec()) for n in self.nodes)
        return f'{self.begin_token}{s}{self.end_token}'


class ObjectNode(_GroupNode):
    def __init__(self, properties):
        super().__init__('{', '}', properties)


class ArrayNode(_GroupNode):
    def __init__(self, children):
        super().__init__('[', ']', children)


class FuncNode(Node):
    def __init__(self, f):
        self.f = f

    def exec(self):
        return self.f()


class RangeNode(Node):
    def __init__(self, name, l, child, h=None):
        self.name = name
        self.low = int(l)
        self.high = int(h) if h else None
        self.child = child

    def exec(self):
        children = []
        if self.high is None:
            for i in range(self.low):
                children.append(self.child)
        else:
            for i in range(random.randint(self.low, self.high - 1)):
                children.append(self.child)

        return f'"{self.name}": {ArrayNode(children).exec()}'


class PlaceholderNode(Node):
    def __init__(self, placeholder):
        self.placeholder = placeholder

    def exec(self):
        return self.placeholder.exec()


class PropertyNode(Node):
    def __init__(self, name, child):
        self.name = name
        self.child = child

    def exec(self):
        if self.child:
            return f'{self.name.exec()}:{self.child.exec()}'
        else:
            return f'{self.name.exec()}:""'


class ScalarNode(Node):
    def __init__(self, value):
        self.value = value

    def exec(self):
        if isinstance(self.value, str) and not self.value.isdigit():
            return f'"{self.value}"'
        else:
            return self.value
