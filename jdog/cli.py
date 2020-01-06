import click
import json
import os
from . import Jdog


def validate_scheme(_, __, value):
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