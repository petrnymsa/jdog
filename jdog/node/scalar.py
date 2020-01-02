from jdog.node.base import Node


class ScalarNode(Node):
    def __init__(self, value):
        self.value = value

    def exec(self):
        return f'"{self.value}"'

