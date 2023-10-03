"""CLI Frontend implementation."""
from pathlib import Path

import click
from click import command, option, version_option

from balba import __version__
from balba.balba import balba_run


@command()
@option(
    "-s",
    "--source",
    help="Source directory",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path.cwd(),
)
@option(
    "-o",
    "--output",
    type=click.Path(file_okay=False, path_type=Path),
    help="Output directory",
    default=Path.cwd() / "balba-build",
)
@option("--dev", default=False, is_flag=True)
@version_option(__version__)
def balba(*args, **kwargs):
    """Command line entrypoint."""
    raise SystemExit(balba_run(*args, **kwargs))


if __name__ == "__main__":
    balba()
