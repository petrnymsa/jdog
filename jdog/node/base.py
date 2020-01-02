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
        self.l = l
        self.h = h
        self.child = child

    def exec(self):
        children = []
        if self.h is None:
            for i in range(self.l):
                children.append(self.child)
        else:
            top = random.randint(self.l, self.h-1)
            for i in range(self.l, top):
                children.append(self.child)

        return f'"{self.name}": {ArrayNode(children).exec()}'
