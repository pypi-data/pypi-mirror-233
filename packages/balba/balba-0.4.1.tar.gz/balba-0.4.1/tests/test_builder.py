# pylint: disable=missing-module-docstring,missing-function-docstring
from pathlib import Path

from lxml.etree import HTMLParser, parse

from balba.builder import Builder
from balba.driver import Driver
from balba.models import EXT_SCHEMATIC, Component, Project, ProjectFiles


def test_builder_dev_mode(tmpdir):
    base_url = "https://my.random.url.test"
    builder = Builder(Path(tmpdir), Driver(False), {"base_url": base_url}, True)
    builder.build_index([])

    tree = parse(str(Path(tmpdir) / "index.html"), HTMLParser())
    legend = tree.xpath("//small[@id='copyright-legend']/a")[0]

    assert legend.attrib["href"] == "/"


def test_builder_no_dev_mode(tmpdir):
    base_url = "https://my.random.url.test/"
    builder = Builder(Path(tmpdir), Driver(False), {"base_url": base_url}, False)
    builder.build_index([])

    tree = parse(str(Path(tmpdir) / "index.html"), HTMLParser())
    legend = tree.xpath("//small[@id='copyright-legend']/a")[0]

    assert legend.attrib["href"] == base_url


def test_build_bom(tmpdir):
    builder = Builder(Path(tmpdir), Driver(False), {}, False)
    schematic = (Path(__file__).parent / "resources" / "usbled").with_suffix(EXT_SCHEMATIC)
    project = Project(
        title="Dummy",
        brief="Test",
        content="",
        files=ProjectFiles(board=Path(), readme=Path(), schematic=schematic, project=Path()),
    )

    components = builder.build_bom(project)
    assert components == {
        Component("USB_B_Mini", "USB_B_Mini", "USB Mini Type B connector"): ["J1"],
        Component("C", "1u", "Unpolarized capacitor"): ["C1", "C2"],
        Component("FerriteBead", "FerriteBead", "Ferrite bead"): ["FB1"],
        Component("C", "100n", "Unpolarized capacitor"): ["C3"],
        Component("R", "2.2k", "Resistor"): ["R1"],
        Component("LED", "LED", "Light emitting diode"): ["D1"],
    }
