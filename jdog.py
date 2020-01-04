import json
import os
import random
import re
from faker import Faker
import click

from jdog.jdog import Jdog


# todo sphinx  https://readthedocs.org/
from jdog.placeholder.placeholder import FuncPlaceholder


def validate(text):
    try:
        json.loads(text)
        return True
    except ValueError:
        return False

def validate_scheme(ctx, param, value):
    if os.path.exists(value):
        return value

    raise click.BadArgumentUsage(f'Provided scheme path {value} does not exists')


@click.command('jdog')
@click.argument('scheme', callback=validate_scheme)
@click.option('-p', '--pretty', is_flag=True, default=False, help='Output pretty JSON')
def run(scheme, pretty):
    jdog = Jdog()
    with open(scheme, "r") as f:
        scheme_text = f.read()

    jdog.parse_scheme(scheme_text)
    result = jdog.generate()
    if pretty:
        print(json.dumps(json.loads(result), indent=4))
    else:
        click.echo(result)

if __name__ == '__main__':
    run()
    #raw = """{"first_name":"{{first_name}}","last_name":"{{last_name}}", "city":"{{city}}","age":"{{age}}","address":"{{option({{number(0,3)}},{{empty}})}}"}"""
    # raw = """{"text":"{{option({{city}},{{first_name}},{{number(0,10)}})}}"}"""
   #raw = """{"{{range(people,4)}}":{"name": "{{first_name}}"}}"""
    #     scheme = """{
    # 	"{{range(people,3)}}": {
    # 		"name": "{{name}}",
    # 		"rank": "{{number(1,100)}}",
    # 		"age": "{{option({{empty}},{{age}})}}",
    # 		"city": "{{option(praha,brno)}}"
    # 	}
    # }"""
