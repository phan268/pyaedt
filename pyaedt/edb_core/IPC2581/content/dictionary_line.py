import xml.etree.cElementTree as ET

from pyaedt.edb_core.IPC2581.content.content import Content
from pyaedt.edb_core.IPC2581.content.entry_line import EntryLine


class DictionaryLine(Content):
    def __init__(self):
        self._dict_lines = {}

    @property
    def dict_lines(self):
        return self._dict_lines

    @dict_lines.setter
    def dict_lines(self, value):
        if isinstance(value, EntryLine):
            self._dict_lines = value

    def add_line(self, value):
        if isinstance(value, EntryLine):
            self._dict_colors.append(value)

    def write_xml(self, content=None):
        if content:
            dict_line = ET.SubElement(content, "DictionaryLineDesc")
            dict_line.set("units", self.design_units)
            for line in self._dict_lines.keys():
                self._dict_lines[line].write_xml()
