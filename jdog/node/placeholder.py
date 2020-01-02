from jdog.node.base import Node


class PlaceholderNode(Node):
    def __init__(self, placeholder):
        self.placeholder = placeholder

    def exec(self):
        return f'"{self.placeholder.exec()}"'
