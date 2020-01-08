from click.testing import CliRunner
from jdog.cli import run


def test_no_scheme():
    runner = CliRunner()
    res = runner.invoke(run)

    assert res.exit_code != 1
    assert 'Missing argument "SCHEME"' in res.stdout


def test_scheme():
    scheme = '{"value":"foo"}'
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('scheme.json', 'w') as f:
            f.write(scheme)

        result = runner.invoke(run, ['scheme.json'])
        assert result.exit_code == 0
        assert result.output == f'{scheme}\n'


def test_scheme_pretty():
    scheme = '{"value":"foo"}'
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('scheme.json', 'w') as f:
            f.write(scheme)

        result = runner.invoke(run, ['scheme.json', '-p'])
        assert result.exit_code == 0
        assert result.output == """{\n    "value": "foo"\n}\n"""


def test_scheme_invalid():
    scheme ='{"val:}'
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('scheme.json', 'w') as f:
            f.write(scheme)

        result = runner.invoke(run, ['scheme.json'])
        assert result.exit_code != 0
        assert 'Provided SCHEME does not have valid JSON format' in result.stdout


def test_scheme_invalid_placeholder():
    scheme ='{"value":"{{foo}}"}'
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('scheme.json', 'w') as f:
            f.write(scheme)

        result = runner.invoke(run, ['scheme.json', '-s'])
        assert result.exit_code == 0
        assert result.output == f'{scheme}\n'
