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


class ObjectNode(GroupNode):
    def __init__(self, properties):
        super().__init__('{', '}', properties)


class ArrayNode(GroupNode):
    def __init__(self, children):
        super().__init__('[', ']', children)
