from jdog.node.base import Node


class ScalarNode(Node):
    def __init__(self, value):
        self.value = value

    def exec(self):
        if isinstance(self.value, str):
            return f'"{self.value}"'
        else:
            return self.value

