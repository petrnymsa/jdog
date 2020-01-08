from jdog.parser import SchemeParser


class Jdog:
    """todo"""

    def __init__(self, lang='en-US', strict=False):
        self.parser = SchemeParser(lang, strict)
        self.scheme = None
        self.root = None

    def parse_scheme(self, scheme):
        # todo custom error if scheme is not valid
        """todo"""
        self.scheme = scheme
        self.root = self.parser.parse(scheme)

    def generate(self):
        """ Generate new data instance

        :return: Generated JSON
        :rtype: str
        """
        return self.root.exec()

    def add_matcher(self, key, f_matcher, f_placeholder):
        """ Add or redefine placeholder identified by KEY

                :param str key: Unique placeholder identification
                :param func f_matcher: Function to determine if given token is desired placeholder.
                    Function takes one str argument. Check this argument if matches.

                :param func f_placeholder: Function which should return :class:`Placeholder` object.
                    Function takes matched token and its arguments - if present.
        """
        self.parser.add_matcher(key, f_matcher, f_placeholder)

    def placeholder_keys(self):
        """ Returns all defined placeholder keys

            :returns: List of placeholder keys
            :rtype: list
        """
        return self.parser.placeholder_keys()
