from __future__ import annotations

from collections import ChainMap
from lxml import etree as ET
from pathlib import Path
from typing import get_type_hints, ClassVar, Optional

import mhi.xml.file

__all__ = ['XmlNode', 'NamedNode', 'IdNode', 'NamedIdNode',
           'ParamNode', 'ParamListNode', 'ParametersBase',
           'TagLookup']


#===============================================================================

class TagLookup(ET.CustomElementClassLookup):
    """
    Tag-based XML Class Looking

    The class supports a chain of dictionary lookups, going from
    XML tag name to Python class for that tag.
    File specific lookup objects can delegate to other lookup objects
    for XML tags common to a variety of files.
    """

    base: ClassVar[TagLookup]
    _tag_map: ChainMap

    def __init__(self, tag_map: ChainMap):

        self._tag_map = tag_map

    def new_child(self) -> TagLookup:
        """
        Create a new Lookup object, using the current lookup object as
        a base.
        """

        return TagLookup(self._tag_map.new_child())

    def register(self, tag):
        """
        Decorator, used to register a tag-class pair to this lookup object

        Usage:
            @lookup_object.register("tagname")
            class SomeClass(ET.ElementBase):
                ...
        """

        def wrapper(cls):
            if tag in self._tag_map.maps[0]:
                raise KeyError(f"Duplicate tag {tag!r}")

            self._tag_map[tag] = cls
            return cls

        return wrapper

    def lookup(self, node_type, document, namespace, name):
        """
        Return a type to be used for the given XML element

        Parameters:
            node_type: one of 'element', 'comment', 'PI', 'entity'
            doc: document that the node is in
            namespace: namespace URI of the node (None for comments/PIs/entities)
            name: name of the element/entity (None for comments, target for PIs)
        """

        if node_type == 'element':
            return self._tag_map.get(name, XmlNode)

        # Fallback for non-element nodes
        return None

TagLookup.base = TagLookup(ChainMap())


#===============================================================================

class XmlNode(ET.ElementBase):
    """
    Custom nase for XML nodes
    """

    @property
    def _parser(self):
        """
        Return the parser used to parse the XML tree
        """

        return self.getroottree().parser

    @property
    def _file(self) -> mhi.xml.file.File:
        """
        Return the file object which holds the XML tree
        """

        return self._parser._file

    def set_modified(self):
        """
        Mark the file containing this node as modified.
        """

        self._file.set_modified()

    def append_text(self, text: str) -> None:
        """
        Append the given text string to the content inside this node.

        If the node contains other elements, the text is added
        to the last child's `tail`, instead of as this node's `text`.
        """

        if len(self) > 0:
            last_child = self[-1]
            if last_child.tail:
                last_child.tail += text
            last_child.tail = text
        else:
            if self.text:
                self.text += text
            else:
                self.text = text

    def append_indented(self, node: ET._Element,
                        spaces: int = -1, space_inc: int = 2) -> None:
        """
        Append a child node to the children of the current node, with
        white-space before and after the element to maintain proper
        indentation.

        Note: The child's content is not modified; it is assumed to already
        be properly indented.
        """

        if spaces < 0:
            if len(self) > 0:
                tail = self[-1].tail
            else:
                tail = self.tail
            spaces = len(tail.lstrip("\n")) if tail else 0

        indent = "\n" + " " * spaces
        indent_inc = " " * space_inc

        if len(self) > 0:
            last_child = self[-1]
            if last_child.tail is None:
                last_child.tail = indent
            last_child.tail += indent_inc
        else:
            if self.text is None:
                self.text = indent
            self.text += indent_inc

        node.tail = indent
        self.append(node)


#===============================================================================

class NamedNode(XmlNode):
    """
    An XML node with a read-only `name` attribute

    <tag name='something'>
    """

    @property
    def name(self) -> str:
        """
        The value of the `name` attribute
        """

        name = self.get('name')
        assert name is not None

        return name


#===============================================================================

class IdNode(XmlNode):
    """
    An XML node with a read-only `id` attribute

    <tag id='123456789'>
    """

    @property
    def id(self) -> int:
        """
        The value of the `id` attribute
        """

        return int(self.get('id', '0'))


#===============================================================================

class NamedIdNode(NamedNode, IdNode):
    """
    An XML node with read-only `name` and `id` attributes

    <tag name='something' id='123456789'>
    """


#===============================================================================

@TagLookup.base.register('param')
class ParamNode(NamedNode):
    """
    A param node, contained in a `paramlist` node container.

    A param have both a name and a value.  Usually, the value is stored
    as a `value` attribute, but may be stored as child nodes for complex
    values (such as tables).

    <paramlist>
      <param name="p1" value="10"/>
      <param name="p2" value="true"/>
      ...
    </paramlist>
    """

    @property
    def value(self) -> str:
        """
        The value of the param node, returned as a string
        """

        value = self.get('value')
        if value is None:
            raise NotImplementedError("Non-attribute values not yet supported")

        return value

    @value.setter
    def value(self, value):

        if isinstance(value, bool):
            value = str(value).lower()
        self.set('value', str(value))

    def __bool__(self) -> bool:

        value = self.value.casefold()
        if value == 'false': return False
        if value == 'true': return True
        raise ValueError(f"Expected 'true' or 'false', not {value!r}")

    def __int__(self) -> int:

        return int(self.value)

    def __float__(self) -> float:

        return float(self.value)

    def __str__(self) -> str:

        return self.value


#===============================================================================

@TagLookup.base.register('paramlist')
class ParamListNode(NamedNode):
    """
    A container of `<param/>` nodes.
    """

    def _find_param(self, name):

        return self.find(f"param[@name={name!r}]")

    def _param(self, name: str):

        param = self._find_param(name)
        if param is None:
            raise KeyError(f"No such param: {name!r}")
        return param

    def get_param(self, name: str) -> str:

        return self._param(name).value

    def set_param(self, name: str, value) -> None:

        self._param(name).value = value

    def __getitem__(self, key):

        if isinstance(key, str):
            return self._param(key)
        return super().__getitem__(key)

    def __setitem__(self, key, value):

        if isinstance(key, str):
            self._param(key).value = value
        else:
            super().__setitem__(key, value)

    def __contains__(self, key: str) -> bool:
        return self._find_param(key) is not None

    def has_keys(self, *keys: str) -> bool:
        """
        Test if the `<paramlist/>` contains all of the given keys
        """

        return all(self._find_param(key) is not None for key in keys)

    def missing_keys(self, *keys: str) -> str:
        """
        Returns a comma-separated string of which keys of the given keys
        are not present in the `<paramlist/>`.

        Returns an empty string if all keys are found.
        """

        return ", ".join(key for key in keys if self._find_param(key) is None)

    def as_dict(self) -> dict[str, str]:
        """
        Returns all of the `<paramlist/>` parameters as a dictionary.

        No attempt is made to convert values to other types.
        """

        return {param.get('name', ''): param.get('value', '') for param in self}

    def __repr__(self):
        params = ", ".join(f"{param.name}={param.value!r}"
                           for param in self)
        return f"ParamList[{params}]"


#===============================================================================

class ParametersBase:
    """
    A typed-enhanced proxy of a `<paramlist/>`.

    The type for a param's value is determine using the type-hint
    for that member name.

    Example:
        class MyParameters(ParametersBase):
            enabled: bool
            time_step: float
            num_runs: int
    """

    def __init__(self, param_list: Optional[ET._Element], unknown: type = None):
        assert isinstance(param_list, ParamListNode)

        object.__setattr__(self, '_param_list', param_list)
        object.__setattr__(self, '_unknown_type', param_list)

    def _type(self, name):

        types = get_type_hints(self)
        param_type = types.get(name, self._unknown_type)
        if param_type is None:
            raise ValueError(f"No type given for parameter {name!r}")
        return param_type

    def __getattr__(self, name):

        param = self._param_list._find_param(name)
        if param is not None:
            param_type = self._type(name)
            return param_type(param)

        return super().__getattr__(name)

    def __setattr__(self, name, value):

        param = self._param_list._find_param(name)
        if param is None:
            raise AttributeError(f"No such parameter: {name!r}")

        param_type = self._type(name)
        if not isinstance(value, param_type):
            raise TypeError(f"Expected {param_type} for {name}")
        param.value = value

    def __repr__(self):

        if self._param_list is not None:
            params = {param.name: self._type(param.name)(param)
                      for param in self._param_list}
        else:
            params = {}

        return repr(params)
