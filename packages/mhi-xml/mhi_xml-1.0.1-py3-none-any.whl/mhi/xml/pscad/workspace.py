from __future__ import annotations

import logging

from collections.abc import Iterator
from enum import Enum
from lxml import etree as ET
from pathlib import Path
from typing import cast, Optional, Protocol

from mhi.xml.node import *
import mhi.xml.pscad
import mhi.xml.file


#===============================================================================

__all__ = ['WorkspaceFile']


#===============================================================================

LOG = logging.getLogger(__name__)


#===============================================================================

workspace_lookup = TagLookup.base.new_child()


#===============================================================================

class FileProtocol(Protocol):

    @property
    def _file(self) -> mhi.xml.file.File: ...


class WorkspaceMixin(FileProtocol):

    @property
    def workspace(self) -> WorkspaceFile:
        return cast(WorkspaceFile, self._file)


#===============================================================================

@workspace_lookup.register('projects')
class ProjectsNode(XmlNode):
    """
    Workspace `<projects/>` container
    """

    def _project(self, name):
        return self.find(f"project[@name={name!r}]")

    def __contains__(self, key):
        if isinstance(key, str):
            return self._project(key) is not None
        return super().__contains__(key)

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._project(key)
        return super().__getitem__(key)

    def names(self):
        return [project.name for project in self.xpath('project')]


#===============================================================================

@workspace_lookup.register('project')
class ProjectNode(NamedNode, WorkspaceMixin):
    """
    A `<project name='project_name' type='type' filepath='...' />` node.
    """

    class Type(Enum):
        LIBRARY = 'library'
        PROJECT = 'project'

    TYPE_BY_EXT = {
        '.pslx': Type.LIBRARY,
        '.pscx': Type.PROJECT,
        }

    def __repr__(self):
        return f"{self.type.title()}<{self.name!r}, {self.filepath!r}>"

    @staticmethod
    def validate_name(name: str):
        if not name.isidentifier():
            raise ValueError("Illegal Project name")

    @staticmethod
    def validate_type(cls, kind: str):
        ProjectNode.Type(kind)

    @property
    def type(self) -> str:
        """
        Type of the project

        Either `'library'` or `'project'`
        """

        return self.get('type', ProjectNode.Type.PROJECT.value)

    @property
    def library(self) -> bool:
        """
        Returns `True` if the project represents a PSCAD Library.
        """

        return self.type == ProjectNode.Type.LIBRARY.value

    @property
    def project(self) -> bool:
        """
        Returns `True` if the project represents a PSCAD Project Case.
        """

        return self.type == ProjectNode.Type.PROJECT.value

    @property
    def filepath(self) -> str:
        """
        Return the project's filepath attribute string
        """

        return self.get('filepath', '')

    @property
    def path(self) -> Path:
        """
        Return the filepath, resolved relative to the workspace's path
        """

        return self.workspace._folder / self.filepath


    def open(self) -> mhi.xml.pscad.ProjectFile:
        """
        Open the project's XML file
        """

        path = self.path
        LOG.info("Opening %s", path)

        return mhi.xml.pscad.ProjectFile(path, self.workspace)


#===============================================================================

@workspace_lookup.register('simulations')
class SimulationsNode(XmlNode):
    """
    Workspace "simulation set" container
    """

    def __getitem__(self, key):

        if isinstance(key, str):
            xpath = f"simulation[@name={key!r}]"
            return self.find(xpath)
        return super().__getitem__(key)


#===============================================================================

@workspace_lookup.register('simulation')
class SimulationNode(NamedNode):
    """
    A simulation set node.
    """

    def __repr__(self):
        return f"Simulation<{self.name!r}>"

    @property
    def tasks(self):
        return Tasks(self)

    def parameters(self, name='Default'):
        xpath = f'paramlist[@name={name!r}]'
        return self.Parameters(self.find(xpath))

    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        The simulation set's parameters
        """

        enabled: bool
        before_run: str
        before_block: bool
        after_run: str
        after_block: bool


#===============================================================================

class Tasks:
    """
    A simulation's tasks container proxy.
    """

    def __init__(self, simset: SimulationNode):
        self._simset = simset

    def __iter__(self):
        for task in self._simset.xpath('task'):
            yield task

    def __len__(self):
        return sum(1 for _ in self)

    def __getitem__(self, key):
        xpath = ""
        if isinstance(key, int):
            idx = key if key >= 0 else len(self) + key
            xpath = f"task[{idx+1}]"
        elif isinstance(key, str) and key:
            xpath = f"task[@namespace={key!r}]"
        else:
            raise KeyError(f"Invalid task key: {key!r}")

        return self._simset.find(xpath)


#===============================================================================

@workspace_lookup.register('task')
class SimulationTaskNode(XmlNode):
    """
    A Simulation Set's Task node.
    """

    def __repr__(self):
        return f"SimulationTask<{self.namespace!r}>"

    @property
    def namespace(self):
        return self.get('namespace')

    def parameters(self, name='Options'):
        xpath = f'paramlist[@name={name!r}]'
        return self.Parameters(self.find(xpath))

    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        Parameters of a simulation set's task.
        """

        simulationset: str
        namespace: str
        name: str
        ammunition: int
        volley: int
        affinity_type: int
        affinity: int
        rank_snap: bool
        substitutions: str
        clean: bool


#===============================================================================

class WorkspaceFile(mhi.xml.file.File):
    """
    A PSCAD Workspace XML File
    """

    _EMPTY = """\
<workspace name="default" version="5.0.2" crc="0">
  <paramlist name="options">
  </paramlist>
  <projects/>
  <simulations/>
</workspace>"""


    def __init__(self, path: Path = None):

        super().__init__(workspace_lookup)

        ws_path = Path(path) if path is not None else Path(".")
        if ws_path.is_dir():
            self._folder = ws_path
            self._load(self._EMPTY)
        elif ws_path.is_file():
            self._read(ws_path)
            self._folder = ws_path.parent
        else:
            raise FileNotFoundError(f"Invalid workspace path {path!r}")

    @property
    def name(self) -> str:
        """
        Name of the workspace
        """

        return self._root.get('name', '')

    @property
    def version(self) -> str:
        """
        PSCAD version used to create the workspace
        """

        return self._root.get('version', '')

    def __repr__(self):

        name = self._path or self._folder / "<unnamed>.pswx"
        return f"Workspace[{name}]"

    @property
    def projects(self) -> ProjectsNode:
        """
        The workspace's projects container.
        """

        node = self._root.find('projects')
        assert isinstance(node, ProjectsNode)
        return node

    def add_project(self, project: mhi.xml.pscad.ProjectFile) -> None:
        """
        Add a project to the workspace
        """

        path = project.path
        name = project.namespace
        prj_type = ProjectNode.TYPE_BY_EXT[path.suffix.lower()]

        if name in self.projects:
            raise KeyError(f"Project {name!r} already exists in workspace")

        if path.is_absolute():
            path = path.relative_to(self._folder)
        filepath = str(path)

        prj_node = self._root.makeelement('project', name=name,
                                          type=prj_type.value,
                                          filepath=filepath)

        self.projects.append_indented(prj_node)
        self.set_modified()

    def all_exist(self) -> bool:
        """
        Verify that all projects in the workspace exist.
        """

        for prj in self.projects.xpath('project'):
            prj = cast(ProjectNode, prj)
            path = self._folder / prj.filepath
            all_exist = True
            if not path.is_file():
                LOG.error("Project %r not found: %s", prj.name, path)
                all_exist = True

        return all_exist


    @property
    def simulations(self) -> Optional[SimulationsNode]:
        """
        The workspace's simulation sets.
        """

        node = self._root.find('simulations')
        assert isinstance(node, SimulationsNode)
        return node
