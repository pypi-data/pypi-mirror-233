"""Methods related with file management/processing."""
import re
from io import StringIO, TextIOBase
from pathlib import Path

from yaml import safe_load

from balba.models import EXT_BOARD, EXT_MARKDOWN, EXT_PROJECT, EXT_SCHEMATIC, ProjectFiles

FRONT_MATTER_REGEX = re.compile(r"^-{3,}$")


def find_project_files(path: Path) -> list[ProjectFiles]:
    """Return a list of all Kicad projects found under a certain directory.

    :param path: Path where the search will start from
    :return: List of projects found
    """
    project_files = path.glob(f"**/*{EXT_PROJECT}")

    return [
        ProjectFiles(
            project=Path(project),
            board=Path(project).with_suffix(EXT_BOARD),
            readme=(Path(project).parent / "README").with_suffix(EXT_MARKDOWN),
            schematic=Path(project).with_suffix(EXT_SCHEMATIC),
        )
        for project in project_files
    ]


def read_frontmatter(stream: TextIOBase()) -> dict:
    """
    Extract a YAML front matter from a text stream. Valid streams must start with at least three dashes (---)
    followed by a newline, this marks the start of the front-matter.
    They must end with the same dash pattern, no other text should be on said line (only dashes).
    Keys with multiline data are not supported.
    The stream's position is left at the end of the front matter.

    :param TextIOBase() stream: IO stream where data will be read from.
    :return: A dictionary which represents the extracted front matter.
    """
    front_matter = StringIO()
    line = stream.readline()
    if not FRONT_MATTER_REGEX.match(line):
        raise ValueError("invalid front matter detected. make sure it starts with '---'")

    while (line := stream.readline()) and not FRONT_MATTER_REGEX.match(line):
        front_matter.write(line)

    front_matter.seek(0)
    return safe_load(front_matter)
