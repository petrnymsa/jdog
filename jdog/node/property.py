from jdog.node.base import Node


class PropertyNode(Node):
    def __init__(self, name, child):
        self.name = name
        self.child = child

    def exec(self):
        return f'{self.name.exec()}:{self.child.exec()}'
