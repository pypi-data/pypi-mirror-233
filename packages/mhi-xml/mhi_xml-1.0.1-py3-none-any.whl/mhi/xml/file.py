from __future__ import annotations

from lxml import etree as ET
from pathlib import Path
from random import randint
from typing import get_type_hints, Optional

__all__ = ['File', ]

class File:
    """
    Base-class for various XML files
    """

    class Parser(ET.XMLParser):
        """
        XML Parser subclass

        Each lxml node can get obtain a reference to the root XML node,
        but those references may actually be different Python objects
        despite referring to the same underlying XML node.
        However, each Python object representing the XML tree root
        will reference the same parser object ... since that is required
        to properly create new XML nodes in the tree.
        By subclassing the XML parser, we create a singular object,
        accessable from any XML node in the XML tree, which may be used
        to store additional data about the XML tree ... such as the
        mhi.xml.file.File that read it.
        """

        __slots__ = ('_file',)

        def __init__(self, file):
            self._file = file
            super().__init__()

    _path: Optional[Path]
    _doc: ET._ElementTree
    _root: ET._Element
    _modified: bool

    def __init__(self, lookup: ET.ElementClassLookup):

        self._parser = File.Parser(lookup)
        self._parser.set_element_class_lookup(lookup)
        self._parser._file = self

        self._modified = False

    def _parse(self, xml_str: str) -> ET._Element:
        return ET.fromstring(xml_str, self._parser)

    def _read(self, path: Path):

        self._doc = ET.parse(path, self._parser)
        self._root = self._doc.getroot()
        self._path = path
        self._modified = False

    def _load(self, xml_str: str):

        self._root = self._parse(xml_str)
        self._doc = self._root.getroottree()
        self._path = None
        self.set_modified()

    def set_modified(self):

        self._modified = True

    @property
    def modified(self) -> bool:

        return self._modified

    @property
    def path(self) -> Optional[Path]:

        return self._path

    def save(self):

        self.save_as(self._path)
        self._modified = False

    def save_as(self, path: Path):

        self._doc.write(path, encoding='utf-8')

    def id_exists(self, id_: int) -> bool:

        node = self._root.find(f".//*[@id={id!r}]")
        return node is not None

    def make_id(self) -> int:

        new_id = randint(100_000_000, 1_000_000_000)
        while self.id_exists(new_id):
            new_id = randint(100_000_000, 1_000_000_000)
        return new_id
