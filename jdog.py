import json
import random
import re
from faker import Faker

from jdog.parser import SchemeParser


# todo sphinx  https://readthedocs.org/
from jdog.placeholder.placeholder import FuncPlaceholder


def validate(text):
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    faker = Faker('cs-CZ')

    parser = SchemeParser('cs-CZ')

    parser.add_matcher('zip', lambda t: re.match('^{{postcode}}$', t), lambda t: FuncPlaceholder(t, faker.postcode))

    #raw = """{"first_name":"{{first_name}}","last_name":"{{last_name}}", "city":"{{city}}","age":"{{age}}","address":"{{option({{number(0,3)}},{{empty}})}}"}"""
    # raw = """{"text":"{{option({{city}},{{first_name}},{{number(0,10)}})}}"}"""
   #raw = """{"{{range(people,4)}}":{"name": "{{first_name}}"}}"""
    raw = """{
	"{{range(people,3)}}": {
		"name": "{{name}}",
		"rank": "{{number(1,100)}}",
		"age": "{{option({{empty}},{{age}})}}",
		"city": "{{option(praha,brno)}}"
	}
}"""
    root = parser.parse(raw)
    res = root.exec()

    if validate(res):
        print('valid json')
    else:
        print('not valid json')
    # print(json.dumps(json.loads(res), indent=4, sort_keys=True, ensure_ascii=False).encode('utf8').decode())
    print()
    print(res)

    for x in range(3):
        res = root.exec()
        print(res)
