"""Collection of classes that represent Kicad entities."""
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

EXT_MARKDOWN = ".md"
EXT_BOARD = ".kicad_pcb"
EXT_PROJECT = ".kicad_pro"
EXT_SCHEMATIC = ".kicad_sch"


@dataclass
class ProjectFiles:
    """Main files that form part of a Kicad project."""

    board: Path
    readme: Path
    project: Path
    schematic: Path


class ProjectStatus(Enum):
    """Collection of available project status."""

    DEVELOPMENT = "development"
    RELEASED = "released"
    ON_REVISION = "on_revision"


@dataclass
class Project:
    """Represents a KiCad project."""

    title: str
    brief: str
    content: str
    files: ProjectFiles
    board_layers: list[str] = field(default_factory=lambda: ["F.Cu", "B.Cu", "F.Silkscreen", "Edge.Cuts"])

    @property
    def slug(self):
        """URL identifier for the project."""
        return self.files.project.stem


@dataclass(eq=True, frozen=True)
class Component:
    """A BOM component."""

    part: str
    value: str
    description: str


@dataclass
class Layer:
    """Kicad Layer as shown on the stackup section."""

    name: str
    type: str
    thickness: float


@dataclass
class Board:
    """A pcbnew board."""

    layers: list[Layer]
