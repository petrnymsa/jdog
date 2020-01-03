import re
import json
import random

from faker import Faker

from jdog.node import PropertyNode, ScalarNode, PlaceholderNode, ObjectNode, ArrayNode
from jdog.placeholder.name import NamePlaceholder, NamePlaceholderOption

# todo name - gender parameter
from jdog.placeholder.placeholder import FuncPlaceholder, FuncStrPlaceholder


class SchemeParser:
    NAME = 'name'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    CITY = 'city'
    STREET_ADDRESS = 'street_address'
    AGE = 'age'
    NUMBER = 'number'
    LOREM = 'lorem'

    def __init__(self, lang='en-US'):
        self.faker = Faker(lang)
        self.compiled_matchers = {
            SchemeParser.NAME: re.compile('^{{name}}$'),
            SchemeParser.FIRST_NAME: re.compile('^{{first_name}}$'),
            SchemeParser.LAST_NAME: re.compile('^{{last_name}}$'),
            SchemeParser.CITY: re.compile('^{{city}}$'),
            SchemeParser.STREET_ADDRESS: re.compile('^{{street_address}}$'),
            SchemeParser.AGE: re.compile('^{{age}}$'),
            SchemeParser.NUMBER: re.compile(r'^{{number\((.*)\)}}$'),
            SchemeParser.LOREM: re.compile(r'^{{lorem\((.*)\)}}$'),
        }
        self.matchers = {
            SchemeParser.NAME: lambda token: self.compiled_matchers[SchemeParser.NAME].match(token),
            SchemeParser.FIRST_NAME: lambda token: self.compiled_matchers[SchemeParser.FIRST_NAME].match(token),
            SchemeParser.LAST_NAME: lambda token: self.compiled_matchers[SchemeParser.LAST_NAME].match(token),
            SchemeParser.CITY: lambda token: self.compiled_matchers[SchemeParser.CITY].match(token),
            SchemeParser.STREET_ADDRESS: lambda token: self.compiled_matchers[SchemeParser.STREET_ADDRESS].match(token),
            SchemeParser.AGE: lambda token: self.compiled_matchers[SchemeParser.AGE].match(token),
            SchemeParser.NUMBER: lambda token: self.compiled_matchers[SchemeParser.NUMBER].match(token),
            SchemeParser.LOREM: lambda token: self.compiled_matchers[SchemeParser.LOREM].match(token)
        }
        self.placeholders = {
            SchemeParser.NAME:
                lambda token, _: NamePlaceholder(token, self.faker),
            SchemeParser.FIRST_NAME:
                lambda token, _: NamePlaceholder(token, self.faker, option=NamePlaceholderOption.FIRST_NAME),
            SchemeParser.LAST_NAME:
                lambda token, _: NamePlaceholder(token, self.faker, option=NamePlaceholderOption.LAST_NAME),
            SchemeParser.CITY:
                lambda token, _: FuncStrPlaceholder(token, self.faker.city),
            SchemeParser.STREET_ADDRESS:
                lambda token, _: FuncStrPlaceholder(token, self.faker.street_address),
            SchemeParser.AGE:
                lambda token, _: FuncPlaceholder(token, lambda: random.randint(1, 99)),
            SchemeParser.NUMBER:
                lambda token, args: FuncPlaceholder(token, lambda: random.randint(int(args[0]), int(args[1]) - 1)),
            SchemeParser.LOREM:
                lambda token, args: FuncStrPlaceholder(token, lambda: self.faker.sentence(nb_words=int(args[0])))
        }

    def _match_token(self, token):
        for key in self.matchers:
            m = self.matchers[key](token)
            if m is not None:
                args = []
                if len(m.groups()) > 0:
                    args = m.group(1).split(',')

                return self.placeholders[key](token, args)
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
