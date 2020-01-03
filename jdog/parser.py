import re
import json

from faker import Faker

from jdog.node import PropertyNode, ScalarNode, PlaceholderNode, ObjectNode, ArrayNode
from jdog.placeholder.name import NamePlaceholder, NamePlaceholderOption

# todo name - gender parameter


class SchemeParser:
    NAME = 'name'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'

    def __init__(self, lang='en-US'):
        self.compiled_matchers = {
            SchemeParser.NAME: re.compile('^{{name}}$'),
            SchemeParser.FIRST_NAME: re.compile('^{{first_name}}$'),
            SchemeParser.LAST_NAME: re.compile('^{{last_name}}$')
        }
        self.matchers = {
            SchemeParser.NAME: lambda token: self.compiled_matchers[SchemeParser.NAME].match(token),
            SchemeParser.FIRST_NAME: lambda token: self.compiled_matchers[SchemeParser.FIRST_NAME].match(token),
            SchemeParser.LAST_NAME: lambda token: self.compiled_matchers[SchemeParser.LAST_NAME].match(token)
        }
        self.placeholders = {
            SchemeParser.NAME: self._name,
            SchemeParser.FIRST_NAME:
                lambda token: NamePlaceholder(token, self.faker, option=NamePlaceholderOption.FIRST_NAME)
                if self._try_match(SchemeParser.FIRST_NAME, token)
                else None,
            SchemeParser.LAST_NAME:
                lambda token: NamePlaceholder(token, self.faker, option=NamePlaceholderOption.LAST_NAME)
                if self._try_match(SchemeParser.LAST_NAME, token)
                else None
        }
        self.faker = Faker(lang)

    def _try_match(self, key, token):
        return self.matchers[key](token) is not None

    def _name(self, token):
        if self.matchers[SchemeParser.NAME](token) is None:
            return None

        return NamePlaceholder(token, self.faker)

    def _match_token(self, token):
        for key in self.placeholders:
            m = self.placeholders[key](str(token))
            if m is not None:
                return m
        return None

    def add_matcher(self, key, f_matcher, f_placeholder):
        self.matchers[key] = f_matcher
        self.placeholders[key] = f_placeholder

    def defined_keys(self):
        return self.matchers.keys()

    def _sub_parse(self, sub):
        if isinstance(sub, list):
            array = []
            for x in sub:
                array.append(self._sub_parse(x))
            return ArrayNode(array)
        elif isinstance(sub, dict):
            props = []
            for key in sub:
                # Key could be token
                placeholder = self._match_token(key)
                if placeholder is None:
                    props.append(PropertyNode(ScalarNode(key), self._sub_parse(sub[key])))
                else:
                    placeholder = self._match_token(key)
                    props.append(PropertyNode(PlaceholderNode(placeholder), self._sub_parse(sub[key])))
            return ObjectNode(props)
        else:
            placeholder = self._match_token(sub)
            if placeholder is None:
                return ScalarNode(sub)
            else:
                return PlaceholderNode(placeholder)

    def parse(self, scheme):
        js = json.loads(scheme)
        root = self._sub_parse(js)
        return root
