from jdog.parser import SchemeParser


class Jdog:
    def __init__(self, lang='en-US'):
        self.parser = SchemeParser(lang)
        self.scheme = None
        self.root = None

    def parse_scheme(self, scheme):
        self.scheme = scheme
        self.root = self.parser.parse(scheme)

    def generate(self):
        return self.root.exec()