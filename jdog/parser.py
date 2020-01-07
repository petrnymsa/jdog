import re
import json
import random

from faker import Faker

from jdog.node import PropertyNode, ScalarNode, PlaceholderNode, ObjectNode, ArrayNode, RangeNode
from jdog.placeholder.name import NamePlaceholder, NamePlaceholderOption

# todo name - gender parameter
from jdog.placeholder.option import OptionPlaceholder
from jdog.placeholder.placeholder import FuncPlaceholder, FuncStrPlaceholder
from jdog.placeholder.range import RangePlaceholder


class SchemeParser:
    NAME = 'name'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    CITY = 'city'
    STREET_ADDRESS = 'street_address'
    AGE = 'age'
    NUMBER = 'number'
    LOREM = 'lorem'
    OPTION = 'option'
    EMPTY = 'empty'
    RANGE = 'range'
    BOOL = 'bool'

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
            SchemeParser.OPTION: re.compile(r'^{{option\((.*)\)}}$'),
            SchemeParser.EMPTY: re.compile(r'^{{empty}}$'),
            SchemeParser.RANGE: re.compile(r'^{{range\((.*)\)}}$'),
            SchemeParser.BOOL: re.compile(r'^{{bool}}$')
        }
        self.matchers = {
            SchemeParser.NAME: lambda token: self.compiled_matchers[SchemeParser.NAME].match(token),
            SchemeParser.FIRST_NAME: lambda token: self.compiled_matchers[SchemeParser.FIRST_NAME].match(token),
            SchemeParser.LAST_NAME: lambda token: self.compiled_matchers[SchemeParser.LAST_NAME].match(token),
            SchemeParser.CITY: lambda token: self.compiled_matchers[SchemeParser.CITY].match(token),
            SchemeParser.STREET_ADDRESS: lambda token: self.compiled_matchers[SchemeParser.STREET_ADDRESS].match(token),
            SchemeParser.AGE: lambda token: self.compiled_matchers[SchemeParser.AGE].match(token),
            SchemeParser.NUMBER: lambda token: self.compiled_matchers[SchemeParser.NUMBER].match(token),
            SchemeParser.LOREM: lambda token: self.compiled_matchers[SchemeParser.LOREM].match(token),
            SchemeParser.OPTION: lambda token: self.compiled_matchers[SchemeParser.OPTION].match(token),
            SchemeParser.EMPTY: lambda token: self.compiled_matchers[SchemeParser.EMPTY].match(token),
            SchemeParser.RANGE: lambda token: self.compiled_matchers[SchemeParser.RANGE].match(token),
            SchemeParser.BOOL: lambda token: self.compiled_matchers[SchemeParser.BOOL].match(token),
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
                lambda token, args: FuncStrPlaceholder(token, lambda: self.faker.sentence(nb_words=int(args[0]))),
            SchemeParser.OPTION:
                lambda token, args: OptionPlaceholder(token, args),
            SchemeParser.EMPTY:
                lambda token, _: FuncStrPlaceholder(token, lambda: ''),
            SchemeParser.RANGE:
                lambda token, args: RangePlaceholder(token, args),
            SchemeParser.BOOL:
                lambda token, _: FuncStrPlaceholder(token, lambda: str(random.random() > 0.5).lower())
        }

    @staticmethod
    def _parse_arguments(p):
        args = []
        while len(p) > 0:
            m = p.partition(',')
            param = m[0]
            if param.startswith('{{'):  # token
                part = param
                parts = [part]
                # keep going until we got whole token
                while not part.endswith('}}') and len(p) > 0:
                    p = m[2]
                    m = p.partition(',')
                    part = m[0]
                    parts.append(part)

                param = ','.join(parts)
                p = m[2]
            else:  # just normal param
                p = m[2]

            args.append(param)

        return args

    @staticmethod
    def _is_token(arg):
        return re.match('^{{.*}}$', arg)

    def _match_token(self, token):
        for key in self.matchers:
            m = self.matchers[key](str(token))
            if m is not None:
                args = []
                if len(m.groups()) > 0:
                    parsed_args = self._parse_arguments(m.group(1))
                    # parse args to placeholders
                    for arg in parsed_args:
                        if self._is_token(arg):
                            args.append(self._sub_parse(arg))
                        else:
                            args.append(arg)

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
                    # special case for RangePlaceholder
                    if isinstance(placeholder, RangePlaceholder):
                        props.append(RangeNode(placeholder.prop, placeholder.low, self._sub_parse(sub[key]), placeholder.high if hasattr(placeholder, 'high') else None))
                    else:
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
