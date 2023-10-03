# pylint: disable=missing-module-docstring,missing-function-docstring

from pathlib import Path
from textwrap import dedent

from pytest import raises

from balba.explorer import EXT_BOARD, EXT_MARKDOWN, EXT_PROJECT, EXT_SCHEMATIC, find_project_files, read_frontmatter


def test_find_project_files(tmpdir):
    test_projects = ["blinker", "buck", "boost"]
    for project in test_projects:
        folder = Path(tmpdir) / project
        folder.mkdir()

        (folder / f"{folder.name}{EXT_BOARD}").touch()
        (folder / f"{folder.name}{EXT_PROJECT}").touch()
        (folder / f"{folder.name}{EXT_SCHEMATIC}").touch()

    found_projects = find_project_files(Path(tmpdir))
    assert len(found_projects) == 3
    for project in found_projects:
        project_name = project.project.parent.name

        assert Path(tmpdir / project_name / f"{project_name}{EXT_BOARD}") == project.board
        assert Path(tmpdir / project_name / f"{project_name}{EXT_PROJECT}") == project.project
        assert Path(tmpdir / project_name / f"README{EXT_MARKDOWN}") == project.readme
        assert Path(tmpdir / project_name / f"{project_name}{EXT_SCHEMATIC}") == project.schematic


def test_read_frontmatter(tmpdir):
    test_file = Path(tmpdir) / "hello.md"

    brief = "This brief must be a one liner because as of now multiline data is not allowed in this Minecraft server"
    test_data = dedent(
        f"""
    ---
    title: Handsome unit test
    brief: {brief}
    status: dying
    version: 5.0.6
    ---
    # Random stuff not read
    """
    ).strip()

    with test_file.open("w", encoding="utf-8") as test_fd:
        test_fd.write(test_data)

    front_matter = read_frontmatter(test_file.open("r", encoding="utf-8"))
    assert {
        "title": "Handsome unit test",
        "brief": brief,
        "status": "dying",
        "version": "5.0.6",
    } == front_matter


def test_read_frontmatter_invalid(tmpdir):
    test_file = Path(tmpdir) / "bye.md"
    with test_file.open("w", encoding="utf-8") as test_fd:
        test_fd.write(
            dedent(
                """INVALID START
          ---
          title: I am sorry
          brief: please don't fail
          ---
        """
            ).strip()
        )

    with raises(ValueError):
        read_frontmatter(test_file.open("r", encoding="utf-8"))
