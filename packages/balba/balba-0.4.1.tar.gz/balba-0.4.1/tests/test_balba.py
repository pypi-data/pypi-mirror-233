# pylint: disable=missing-module-docstring,missing-function-docstring,redefined-outer-name

from unittest.mock import patch

from click.testing import CliRunner
from pytest import fixture

from balba.cli import balba


@fixture
def runner() -> CliRunner:
    return CliRunner()


def test_no_kicad_cli(runner, tmpdir):
    with patch("balba.driver.run", side_effect=FileNotFoundError) as mock:
        output = runner.invoke(balba, ["--source", tmpdir.strpath])
        assert mock.call_count == 1

    assert output.exit_code == 127


def test_no_config_file(runner, tmpdir):
    with patch("balba.driver.run", return_Value="7.0.1") as mock:
        output = runner.invoke(balba, ["--source", tmpdir.strpath])
        assert mock.call_count == 1

    assert output.exit_code == 126
