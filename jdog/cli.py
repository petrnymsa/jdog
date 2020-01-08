import click
import json
from . import Jdog
from jdog.parser import NoMatchingPlaceholder
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


def print_output(result, pretty, output):
    if pretty:
        pretty_output = json.dumps(json.loads(result), indent=4)
        if output:
            output.write(pretty_output)
        else:
            print(pretty_output)
    else:
        if output:
            output.write(result)
        else:
            click.echo(result)


# developer note: Although we cane use for -l parameter click.Choice,
# there is not way to truncate / or hide all options and its look ugly
# so I have decided to introduce special option --lang-help to show and do manual validation for -l option


@click.command('jdog')
@click.argument('scheme', type=click.File('r'))
@click.option('-p', '--pretty', is_flag=True, default=False, help='Output as pretty JSON.')
@click.option('-s', '--strict', is_flag=True, default=False, help='Raise error when no matching placeholder is found.')
@click.option('-l', '--lang', default='en_US', help='Language to use', callback=validate_lang)
@click.option('--lang-help', is_flag=True, default=False, help='Displays available language codes and exit.', callback=callback_lang_help)
@click.option('-o', '--output', type=click.File('w'), help='Output file where result is written.')
def run(scheme,strict, pretty, lang, lang_help, output):
    """Accepts SCHEME and generate new data to stdin or to specified OUTPUT"""
    try:
        jdog = Jdog(lang, strict)
        scheme_text = scheme.read()
        jdog.parse_scheme(scheme_text)
        result = jdog.generate()
        print_output(result, pretty, output)
    except json.JSONDecodeError as e:
        raise click.UsageError(f'Provided SCHEME does not have valid JSON format.\n\tJsonError: {e}')
    except NoMatchingPlaceholder as e:
        raise click.UsageError(e)
