from jdog.parser import SchemeParser


class Jdog:
    """todo"""

    def __init__(self, lang='en-US'):
        self.parser = SchemeParser(lang)
        self.scheme = None
        self.root = None

    def parse_scheme(self, scheme):
        """todo"""
        self.scheme = scheme
        self.root = self.parser.parse(scheme)

    def generate(self):
        """todo"""
        return self.root.exec()

    #todo add_matcher