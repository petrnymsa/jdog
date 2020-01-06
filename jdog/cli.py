import click
import json
from . import Jdog
from faker.config import AVAILABLE_LOCALES


def callback_lang_help(ctx, prop, value):
    if not value:
        return
    click.echo('Use one of the following language code: ')
    click.echo(AVAILABLE_LOCALES)
    ctx.exit()



def validate_lang(ctx, prop, value):
    if value not in AVAILABLE_LOCALES:
        raise click.BadParameter('Language code is invalid. See --lang-help for accepted values')

    return value

# developer note: Although we cane use for -l parameter click.Choice,
# there is not way to truncate / or hide all options and its look ugly
# so I have decided to introduce special option --lang-help to show and do manual validation for -l option


@click.command('jdog')
@click.argument('scheme', type=click.Path(exists=True))
@click.option('-p', '--pretty', is_flag=True, default=False, help='Output pretty JSON')
@click.option('-l', '--lang', default='en-US', help='Language to use', callback=validate_lang)
@click.option('--lang-help', is_flag=True, default=False, help='Displays available language codes and exit.', callback=callback_lang_help)
def run(scheme, pretty, lang, lang_help):
    """Accepts SCHEME and generate new data to stdin or to specified OUTPUT"""

    jdog = Jdog(lang)

    with open(scheme, "r") as f:
        scheme_text = f.read()

    jdog.parse_scheme(scheme_text)
    result = jdog.generate()

    if pretty:
        print(json.dumps(json.loads(result), indent=4))
    else:
        click.echo(result)
