from __future__ import annotations
from ast import literal_eval
from dataclasses import dataclass
from lxml import etree as ET
from pathlib import Path
from typing import cast, Iterator, Optional, Protocol, Union

from mhi.xml.node import *
import mhi.xml.pscad
import mhi.xml.file


#===============================================================================

__all__ = ['ProjectFile', 'XY', 'UP', 'DOWN', 'LEFT', 'RIGHT',
           'Component', 'Definition']


#===============================================================================

project_tag_lookup = TagLookup.base.new_child()

classid_map = {}

def classid(class_id: str):
    def wrapper(cls):
        if class_id in classid_map:
            raise KeyError(f"Duplicate classid {class_id!r}")
        classid_map[class_id] = cls
        return cls
    return wrapper


#===============================================================================

class FileProtocol(Protocol):
    @property
    def _file(self) -> mhi.xml.file.File: ...

class ProjectMixin(FileProtocol):
    @property
    def project(self) -> ProjectFile:
        return cast(ProjectFile, self._file)


#===============================================================================

@dataclass(frozen=True)
class XY:
    """
    Two dimensional position or size, used to specify `Component` locations
    on a `Schematic` canvas.
    """

    x: int
    y: int

    def __add__(self, other: XY):
        return XY(self.x + other.x, self.y + other.y)

    def __sub__(self, other: XY):
        return XY(self.x - other.x, self.y - other.y)

    def __mul__(self, scale: int):
        return XY(self.x * scale, self.y * scale)

UP = XY(0, -18)
DOWN = XY(0, 18)
LEFT = XY(-18, 0)
RIGHT = XY(18, 0)


#===============================================================================
# Definitions
#===============================================================================

@project_tag_lookup.register('definitions')
class Definitions(XmlNode):
    """
    Project `<definitions/>` container
    """

    def __getitem__(self, key):
        if isinstance(key, str):
            xpath = f"Definition[@name={key!r}]"
            return self.find(xpath)
        return super().__getitem__(key)


#===============================================================================

@project_tag_lookup.register('Definition')
class Definition(NamedNode, ProjectMixin):
    """
    Definition node
    """

    @property
    def form(self):
        return self.find('form')

    @property
    def schematic(self):
        return self.find('schematic')

    def __repr__(self) -> str:
        return f"Definition<{self.name}>"


#===============================================================================
# Forms
#===============================================================================

@project_tag_lookup.register('form')
class Form(NamedNode):
    """
    Definition `<form/>` node

    Contains 1 or more categories, each which contain 1 or more parameters.
    """

    def __repr__(self) -> str:

        return f"Form<{self.name}>"

    @property
    def w(self) -> int:

        return int(self.get('w', '320'))

    @property
    def h(self) -> int:

        return int(self.get('h', '400'))

    @property
    def splitter(self) -> int:

        return int(self.get('splitter', '50'))

    @property
    def commentlines(self) -> int:

        return int(self.get('commentlines', '4'))

    def __getitem__(self, key):

        if isinstance(key, str):
            xpath = f"category[@name={key!r}]"
            return self.find(xpath)

        return super().__getitem__(key)

    @property
    def parameters(self):
        """
        View of the form parameters as a flat list without categories
        """

        return self.Parameters(self)

    class Parameters:

        def __init__(self, node: Form):

            self._node = node

        def __iter__(self):

            for param in self._node.iterfind('category/parameter'):
                yield param

        def __len__(self):

            return sum(1 for _ in self)

        def __getitem__(self, key):

            if isinstance(key, str):
                xpath = f"category/parameter[@name={key!r}]"
                return self._node.find(xpath)
            elif isinstance(key, int):
                return list(iter(self))[key]


#===============================================================================

@project_tag_lookup.register('category')
class Category(NamedNode):
    """
    A form `<category/>` node

    Contains 1 or more parameters.
    """

    def __getitem__(self, key):
        if isinstance(key, str):
            xpath = f"parameter[@name={key!r}]"
            return self.find(xpath)
        return super().__getitem__(key)

    @property
    def cond(self):

        cond = self.find('cond')
        return cond.text if cond is not None else ''

    def __repr__(self) -> str:

        return f"Category<{self.name}>"


#===============================================================================

@project_tag_lookup.register('parameter')
class Parameter(NamedNode):
    """
    A parameter definition node.

    Gives the parameter a symbol name, description, type, units, default value,
    validation attributes (minimum and/or maximum limits, regex),
    and help attributes.
    """

    def _text(self, tag):

        node = self.find(tag)
        return node.text if node is not None else ''

    @property
    def description(self) -> str:

        return self.get('desc', '')

    @property
    def group(self) -> str:

        return self.get('group', '')

    @property
    def type(self) -> str:

        return self.get('type', 'Text')

    @property
    def min(self) -> Optional[Union[int, float]]:

        value = self.get('min')
        return literal_eval(value or 'None')

    @property
    def max(self) -> Optional[Union[int, float]]:

        value = self.get('max')
        return literal_eval(value or 'None')

    @property
    def unit(self) -> str:

        return self.get('unit', '')

    @property
    def empty_allowed(self) -> bool:

        return self.get('allowemptystr', 'true') == 'true'

    @property
    def animate(self) -> bool:

        return self.get('animate', 'false') == 'true'

    @property
    def help_mode(self) -> str:

        return self.get('helpmode', 'Append')

    @property
    def default(self) -> str:

        return self._text('value')

    @property
    def help(self) -> str:

        return self._text('help')

    @property
    def cond(self) -> str:

        return self._text('cond')

    @property
    def regex(self) -> str:

        return self._text('regex')

    @property
    def error_msg(self) -> str:

        return self._text('error_msg')

    @property
    def choices(self) -> list[str]:

        if self.type != 'Choice':
            raise KeyError(f"Parameter {self.name} is not type='Choice'")
        choices = [choice.text or '' for choice in self.iterfind('choice')]
        return choices

    def __repr__(self) -> str:

        return f"{self.type}<{self.name}={self.default!r}>"


#===============================================================================
# Graphics
#===============================================================================

@project_tag_lookup.register('graphics')
class Graphics(XmlNode):
    """
    A `<graphics/>` container node
    """


#===============================================================================
# Schematic Canvases
#===============================================================================

@project_tag_lookup.register('schematic')
class Schematic(XmlNode, ProjectMixin):
    """
    A `<schematic/>` container node for page modules
    """

    @staticmethod
    def _xpath(classid: str = None, defn: str = None,
               with_params: set[str] = None, params: dict[str, str] = None
               ) -> str:
        parts = []
        node = "*"
        if classid is not None:
            node += f"[@classid={classid!r}]" if classid else "[@classid]"
        if defn:
            node += f"[@defn={defn!r}]"
        parts.append(node)

        if params or with_params:
            parts.append('paramlist')
            if params:
                parts.extend(f"param[@name={name!r}][@value={value!r}]/.."
                             for name, value in params.items())
            if with_params:
                if params:
                    with_params = with_params - params.keys()
                parts.extend(f"param[@name={name!r}]/.."
                             for name in with_params)
            parts.append("..")

        xpath = "/".join(parts)

        return xpath

    def __repr__(self):
        classid = self.get('classid', 'Unknown!')
        return f'{classid}[{self.name!r}]'

    def __iter__(self):

        for node in super().__iter__():
            if node.tag == 'paramlist':
                continue
            yield node

    def __getitem__(self, key):

        xpath = ""
        if isinstance(key, int):
            xpath = f"*[@id='{key}']"
        else:
            raise KeyError(f"Invalid schematic component key={key!r}")

        return self.find(xpath)

    @property
    def name(self) -> str:
        parent = self.getparent()
        name = parent.get('name') if parent is not None else None
        assert name is not None
        return name

    @property
    def definition(self) -> Definition:
        return self.getparent()

    def components(self, name: str = None, /, *,
                   include_defns: set[str] = None,
                   exclude_defns: set[str] = None,
                   xpath: str = None,
                   classid: str = None,
                   defn: str = None,
                   with_params: set[str] = None,
                   **params) -> Iterator['Component']:

        if xpath is None:
            xpath = self._xpath(classid, defn, with_params, params)
        elif classid or defn or with_params or params:
            raise ValueError(
                f"xpath cannot be used with classid/defn/params\n"
                f"    xpath={xpath}\n"
                f"    classid={classid}\n"
                f"    defn={defn}\n"
                f"    with_params={with_params}\n"
                f"    params={params}")

        if name:
            name = name.casefold()

        for cmp in self.xpath(xpath):
            if cmp.tag in {'paramlist', 'grouping'}:
                continue
            cmp = cast(Component, cmp)
            if name is not None:
                cmp_name = cmp.name
                if cmp_name is None or cmp_name.casefold() != name:
                    continue
            if include_defns and cmp.defn not in include_defns:
                continue
            if exclude_defns and cmp.defn in exclude_defns:
                continue
            yield cmp

    def component(self, name: str = None, /, *,
                  include_defns: set[str] = None,
                  exclude_defns: set[str] = None,
                  raise_if_not_found: bool = False,
                  classid: str = None,
                  defn: str = None,
                  with_params: set[str] = None,
                  **params) -> Optional['Component']:

        xpath = self._xpath(classid, defn, with_params, params)
        comps = list(self.components(name, xpath=xpath,
                                     include_defns=include_defns,
                                     exclude_defns=exclude_defns))

        if len(comps) == 0:
            if raise_if_not_found:
                raise NameError(f"Component {xpath!r} not found")
            return None
        if len(comps) > 1:
            raise NameError(f"Multiple components {xpath!r} found ({len(comps)})")

        return comps[0]

    def page_modules(self) -> Iterator[UserCmp]:

        project = self.project
        project_namespace = project.namespace
        for user in self.components(xpath='User[@classid="UserCmp"]'):
            user = cast(UserCmp, user)
            namespace, name = user.defn.split(':', 1)
            if namespace == project_namespace:
                canvas = project.canvas(name)
                if canvas is not None:
                    yield user

    @property
    def parameters(self):

        return self.Parameters(self.find('paramlist'))

    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):
        """
        Schematic parameters
        """

        # All canvases
        show_grid: int
        size: int
        orient: int
        show_border: int

        # Additional user canvas parameters
        show_signal: int
        show_virtual: int
        show_sequence: int
        auto_sequence: int
        monitor_bus_voltage: int
        show_terminals: int
        virtual_filter: str
        animation_freq: int


#===============================================================================
# Components
#===============================================================================

class Component(IdNode, ProjectMixin):
    """
    A Component
    """

    def __repr__(self):

        classid = self.defn or self.get('classid')
        name = self.name
        return f'{classid}[{name}, #{self.id}]'

    @property
    def classid(self) -> str:

        classid = self.get('classid')
        assert classid is not None
        return classid

    @property
    def location(self) -> XY:

        return XY(int(self.get('x', '0')), int(self.get('y', '0')))

    @location.setter
    def location(self, xy: XY) -> None:

        self.set('x', str(xy.x))
        self.set('y', str(xy.y))

    @property
    def canvas(self) -> Schematic:

        return self.getparent()

    @property
    def size(self) -> XY:

        return XY(int(self.get('w', '0')), int(self.get('h', '0')))

    @size.setter
    def size(self, xy: XY) -> None:

        self.set('w', str(xy.x))
        self.set('h', str(xy.y))

    @property
    def defn(self) -> Optional[str]:

        return self.get('defn')

    @property
    def scope_and_defn(self) -> Tuple[str, str]:

        defn = self.defn
        if not defn:
            return '', ''
        if ':' in defn:
            return defn.split(':', 1)
        return '', defn

    @property
    def name(self) -> Optional[str]:

        paramlist = self.params
        return next((param.get('value')
                     for param in paramlist.iter('param')
                     if param.get('name', '').casefold() == 'name'), None)

    @property
    def params(self) -> ParamListNode:

        xpath = 'paramlist[@link="-1"][@name=""]'
        param_list = self.find(xpath)
        if param_list is None:
            param_lists = cast(list, self.xpath('paramlist'))
            if param_lists:
                param_list = param_lists[0]

        assert param_list is not None
        return cast(ParamListNode, param_list)

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.params.get_param(key)
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, str):
            self.params.set_param(key, value)
        else:
            super().__setitem__(key, value)

    def enable(self, state=True) -> None:
        """
        Enable this component

        Note:
            This does not affect whether the component is on a disabled layer.
        """

        disabled = 'false' if state else 'true'
        self.set('disable', disabled)

    def disable(self) -> None:
        """
        Disable this component
        """

        self.enable(False)

    @property
    def enabled(self) -> bool:
        """
        Is this component enabled.

        Note:
            This does not check if the component is on a disabled layer.
        """

        disabled = self.get('disable', 'false')
        return disabled.casefold() == 'false'


    @property
    def layer(self) -> Optional[Layer]:
        """
        The `Layer` the component is on, if any
        """

        layer = self.find(f'/project/Layers/Layer/ref[@id="{self.id}"/..')
        if layer is not None:
            return cast(Layer, layer)
        return None

    @layer.setter
    def layer(self, layer: Optional[Union[Layer, str]]) -> None:

        old_layer = self.layer
        if isinstance(layer, str):
            new_layer = self.project.layers[layer]
        else:
            new_layer = layer

        if old_layer is not None:
            if old_layer != new_layer:
                ref = old_layer.find(f'ref[@link="{self.id}"]')
                old_layer.remove(ref)

        if new_layer is not None:
            ref = new_layer.makeelement('ref', link=str(self.id))
            new_layer.append_indented(ref, 4)


#===============================================================================

@project_tag_lookup.register('User')
#@classid('UserCmp')
class UserCmp(Component):

    @property
    def defn(self) -> str:

        defn = self.get('defn')
        assert defn is not None
        return defn

    @defn.setter
    def defn(self, new_defn) -> None:

        return self.set('defn', new_defn)

    @property
    def subcanvas(self) -> Optional[Schematic]:

        project = self.project
        namespace, name = self.defn.split(':', 1)
        if project.namespace == namespace:
            return project.canvas(name)
        return None

    def is_module(self):

        return self.subcanvas is not None


#===============================================================================

@project_tag_lookup.register('Wire')
#@classid('WireOrthogonal')
class Wire(Component):
    pass


#===============================================================================

@classid('TLine')
class TLine(Wire):

    def __repr__(self) -> str:
        return f"TLine[{self.name}]"

    @property
    def user(self) -> UserCmp:

        user = self.find('User')
        assert user is not None

        return cast(UserCmp, user)

    @property
    def params(self) -> ParamListNode:

        return self.user.params

    @property
    def subcanvas(self) -> Optional[Schematic]:

        namespace, name = self.user.defn.split(':', 1)

        project = self.project
        if namespace == project.namespace:
            return project.canvas(name)
        return None


#===============================================================================

@project_tag_lookup.register('Sticky')
#@classid('Sticky')
class Sticky(Component):
    pass


#===============================================================================

@project_tag_lookup.register('Instrument')
#@classid('PolyMeter')
class Instrument(Component):
    pass


#===============================================================================

@project_tag_lookup.register('Frame')
#@classid('GraphFrame')
class Frame(Component):
    pass


#===============================================================================
# Layers
#===============================================================================

@project_tag_lookup.register('Layers')
class Layers(XmlNode):

    def __getitem__(self, key):

        if isinstance(key, str):
            if key == "":
                return None

            layer = self.find(f"Layer[@name={key!r}]")
            if layer is None:
                raise KeyError(f"Layer not found: {key!r}")

            return cast(Layer, layer)

        return super().__getitem__(key)

    def names(self):
        return [layer.name for layer in self]


#===============================================================================

@project_tag_lookup.register('Layer')
class Layer(NamedNode):

    @property
    def parameters(self) -> Parameters:

        return self.Parameters(self.find('paramlist'))

    @property
    def state(self) -> str:

        return self.get('state', 'Enabled')

    @state.setter
    def state(self, state: str) -> None:

        self.set('state', state)

    @property
    def disabled(self) -> bool:

        return self.state.casefold() == 'disabled'

    @property
    def enabled(self) -> bool:

        return self.state.casefold() == 'enabled'

    @property
    def ids(self) -> set[int]:
        return {int(ref.get('link', '0'))
                for ref in self.iterfind('ref')}

    def __eq__(self, other):
        if isinstance(other, Layer):
            return self.id == other.id
        return False

    def __ne__(self, other):
        if isinstance(other, Layer):
            return self.id != other.id
        return True

    class Parameters(ParametersBase):

        disabled_color: str
        disabled_opacity: int
        highlight_color: str
        highlight_opacity: int


#===============================================================================
# Project File
#===============================================================================

project_lookup = ET.AttributeBasedElementClassLookup(
    'classid', classid_map, project_tag_lookup)


#===============================================================================

class ProjectFile(mhi.xml.file.File):
    """
    A PSCAD Project (Library or Case)
    """

    _workspace: mhi.xml.pscad.WorkspaceFile
    _path: Path
    _doc: ET._ElementTree
    _root: ET._Element

    _canvases_in_use: Optional[list[Schematic]] = None

    def __init__(self, path: Union[Path, str],
                 workspace: mhi.xml.pscad.WorkspaceFile = None):

        super().__init__(project_lookup)

        self._read(Path(path))

        if workspace is None:
            workspace = mhi.xml.pscad.WorkspaceFile(self._path.parent)
            workspace.add_project(self)
        self._workspace = workspace

    def __repr__(self) -> str:

        return f"Project[{self.namespace}]"


    @property
    def path(self) -> Path:

        return self._path

    @property
    def namespace(self) -> str:

        namespace = self._root.get('name')
        assert namespace is not None

        return namespace

    @property
    def workspace(self) -> mhi.xml.pscad.WorkspaceFile:

        return self._workspace

    @property
    def root(self) -> XmlNode:

        return self._root

    @property
    def version(self) -> str:

        return self._root.get('version', '5.0.0')

    def parameters(self, name: str = "Settings") -> Parameters:

        xpath = f"paramlist[@name={name!r}]"
        return self.Parameters(self._root.find(xpath))

    class Parameters(ParametersBase):

        time_duration: float
        time_step: float
        sample_step: float
        chatter_threshold: float
        branch_threshold: float
        Mruns: int
        sparsity_threshold: int

    @property
    def layers(self) -> Layers:

        layers = self._root.find('Layers')
        if layers is None:
            layers = self._parse("<Layers/>")
            self._root.append(layers)

        return cast(Layers, layers)

    _SCHEMATICS = ET.XPath('definitions/Definition/schematic[@classid=$classid]')

    def _schematics(self, classid: str) -> list[Schematic]:
        schematics = self._SCHEMATICS(self._root, classid=classid)
        return cast(list[Schematic], schematics)

    def user_canvases(self) -> list[Schematic]:

        return self._schematics('UserCanvas')

    def canvas(self, name: str) -> Schematic:

        xpath = f'definitions/Definition[@name={name!r}]/schematic'
        return cast(Schematic, self._root.find(xpath))

    _USERCMP = ET.XPath('User[@classid="UserCmp"]')

    def canvases_in_use(self) -> list[Schematic]:

        if self._canvases_in_use is not None:
            return self._canvases_in_use

        canvases = {canvas.name: canvas for canvas in self.user_canvases()}
        active = []
        found = {'Main'}

        prefix = f'{self.namespace}:'

        while found:
            name = found.pop()
            canvas = canvases.pop(name)
            active.append(canvas)

            user_components = cast(list[UserCmp], self._USERCMP(canvas))
            for user in user_components:
                defn = user.defn
                if defn.startswith(prefix):
                    name = defn.split(':', 1)[1]
                    if name in canvases:
                        found.add(name)

        self._canvases_in_use = active
        return self._canvases_in_use
